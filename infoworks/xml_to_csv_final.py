import xml.etree.ElementTree as ET
import os,sys,csv,io
import signal,time
import logging
from pathos.multiprocessing import ProcessingPool as Pool
import argparse
from multiprocessing import Manager
parser = argparse.ArgumentParser()

parser.add_argument('-xmldirectory',required=True,dest='xmlpath',help="Provide the xml path")
parser.add_argument('-csvdirectory',required=True,dest='csvpath',help="Provide the csv path")
parser.add_argument('-table_header_file',required=True,dest='table_header_file',help="Provide the absolute path of header file")
parser.add_argument('-enabledatavalidation',action='store_true',help="Give this key if data validation is needed")
parser.add_argument('-enablelogging',action='store_true',help="Give this key if logging is needed")
parser.add_argument('-logfiledirectory',required=False,dest='logfilepath',help="provide the log file directory")
parser.add_argument('-batchsize',required=False,default=1000,dest='batchsize',help="Provide the batch size")

args = parser.parse_args()

class xmlconversionException(Exception):
    pass


global_validate = True


def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    global global_validate
    global_validate = False


def enableLogging(logfilepath=None):
    if logfilepath:
        logfiledirectory=logfilepath
    else:
        logfiledirectory='/opt/infoworks/temp'

    try:
        if not os.path.exists(logfiledirectory):
            os.makedirs(logfiledirectory)
    except:
        print("Unable to create log file directory")
        raise Exception("Failed while initializing the logger")

    logfileabspath=os.path.join(logfiledirectory,'xmltocsvconversionscript.log')
    logging.basicConfig(filename=logfileabspath,filemode='a',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
    return logging

def logaMessage(message,level,logging):
    if args.enablelogging:
        if level == 'info':
            logging.info(message)
        else:
            logging.error(message)

def inputValidation(xmldirectory,headerfilepath,logging):
    if not os.path.exists(xmldirectory):
        logaMessage("xml directory doesn't exists!..exiting the script","error",logging)
        print("xml directory doesn't exists!..exiting the script")
        raise Exception("xml directory doesn't exists!")
    if not (os.path.exists(headerfilepath) and os.path.isfile(headerfilepath)):
        logaMessage("Wrong header file inputed!..exiting the script","error",logging)
        print("Wrong header file inputed!..exiting the script")
        raise Exception("Wrong header file inputed!")

def getData(member,xml_filename,logging):
    try:
        if len(member.getchildren()) < 1:
            member_data={}
            if member.items():
                for item in member.items():
                    member_data[item[0]]=item[1]
            else:
                if member.text:
                    temp_str = str(member.text.encode('ascii', 'replace')).replace("\n", "").replace("\t", "").replace("\r", "")
                    member_data[member.tag] = temp_str
                else:
                    member_data[member.tag]=None
            return member_data[member.tag]
        else:
            children_list=[]
            member_data={}
            for child in member.getchildren():
                children_list.append({child.tag:getData(child,xml_filename,logging)})
            #this is for attribute data
            if member.items():
                for item in member.items():
                    member_data[item[0]]=item[1]
            occurance={}
            for child_details in children_list:
                for childname in child_details:
                    if childname in occurance:
                        occurance[childname]=occurance[childname]+1
                    else:
                        occurance[childname]=1
            modified_children_list=[]
            for key in occurance:
                if occurance[key]>1:
                    temp=[]
                    for child_details in children_list:
                        for childname in child_details:
                            temp.append(child_details[childname])

                    modified_children_list.append({childname:temp})
                else:
                    for child_details in children_list:
                        for childname in child_details:
                            if key==childname:
                                modified_children_list.append({childname:child_details[childname]})

            for child_details in modified_children_list:
                for key in child_details.keys():
                    member_data[key]=child_details[key]
            return member_data
    except Exception as e:
        logaMessage(str(e),"error",logging)
        raise xmlconversionException("Error while processing file[stage=JSONconversion]: {}".format(xml_filename))

def convertToJSON(xml_filename,logging):
    try:
        converted_data_each_file=[]
        tree=ET.parse(xml_filename)
        root=tree.getroot()
        for child in root:
            each_record=getData(child,xml_filename,logging)
            converted_data_each_file.append({root.tag:{child.tag:each_record}})
        return ({xml_filename:converted_data_each_file})
    except xmlconversionException as e:
        error_file_list.append((e,xml_filename))
    except Exception as e:
        logaMessage(str(e),"error",logging)
        error_file_list.append(("Error while processing file[stage=JSONconversion]: {}".format(xml_filename),xml_filename))

def getCollection(data,match):
    if match in data.keys():
        return data[match]
    else:
        for key in data.keys():
            if type(data[key]) is dict:
                value = getCollection(data[key],match)
                if value:
                    return value
        return None

def createCSVDirectory(filepath,table):
    try:
        if os.path.exists(os.path.join(filepath,table)):
            return (os.path.join(filepath,table))
        else:
            os.makedirs(os.path.join(filepath,table))
            return (os.path.join(filepath,table))
    except:
        raise Exception("Failed to create directory")

def putTableDataToCSVFile(tableheaderfile,convertedjsonofeachfile,csvfilepath,logging):
    try:
        f_open=open(tableheaderfile,'r').readlines()
        tables_header_info={}
        for tabledetails in f_open:
            table_name=tabledetails.split(":")[0].strip()
            column_name=tabledetails.split(":")[-1].strip().split(",")
            tables_header_info[table_name]=column_name
        for key in convertedjsonofeachfile:
            filename=key
            break

        convertedcsvdata={}
        for table in tables_header_info:
            convertedcsvdata[table]=[]

        for eachrowdata in convertedjsonofeachfile[filename]:
            for table in tables_header_info:
                if table == 'partymasteramn':
                    parties_data=getCollection(eachrowdata,table)
                    columndataineachiteration=[]
                    for column in tables_header_info[table]:
                        if column in parties_data.keys():
                            columndataineachiteration.append(parties_data[column])
                        else:
                            columndataineachiteration.append(None)
                    convertedcsvdata[table].append(columndataineachiteration)
                else:
                    parties_data=getCollection(eachrowdata,'partymasteramn')
                    table_data=getCollection(eachrowdata,table)
                    if type(table_data) is list:
                        for i in range(len(table_data)):
                            columndataineachiteration=[]
                            for column in tables_header_info['partymasteramn']:
                                if column in parties_data.keys():
                                    columndataineachiteration.append(parties_data[column])
                                else:
                                    columndataineachiteration.append(None)
                            for column in tables_header_info[table]:
                                if column in table_data[i].keys():
                                    columndataineachiteration.append(table_data[i][column])
                                else:
                                    columndataineachiteration.append(None)
                            convertedcsvdata[table].append(columndataineachiteration)
                    else:
                        columndataineachiteration=[]
                        for column in tables_header_info['partymasteramn']:
                            if column in parties_data.keys():
                                columndataineachiteration.append(parties_data[column])
                            else:
                                columndataineachiteration.append(None)
                        for column in tables_header_info[table]:
                            if column in table_data.keys():
                                columndataineachiteration.append(table_data[column])
                            else:
                                columndataineachiteration.append(None)
                        convertedcsvdata[table].append(columndataineachiteration)
        for table in tables_header_info:
            if table=='partymasteramn':
                csvfiledirectory=createCSVDirectory(csvfilepath,table)
                columnlist=tables_header_info[table]
                table_data=convertedcsvdata[table]
                csvfilename=filename.split('/')[-1].strip('.xml')+".csv"
                abs_csvfilename=os.path.join(csvfiledirectory,csvfilename)
                with open(abs_csvfilename, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile,delimiter="~")
                    csvwriter.writerow(columnlist)
                    csvwriter.writerows(table_data)
            else:
                csvfiledirectory=createCSVDirectory(csvfilepath,table)
                columnlist=tables_header_info['partymasteramn']+tables_header_info[table]
                table_data=convertedcsvdata[table]
                csvfilename=filename.split('/')[-1].strip('.xml')+".csv"
                abs_csvfilename=os.path.join(csvfiledirectory,csvfilename)
                with open(abs_csvfilename, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile,delimiter="~")
                    csvwriter.writerow(columnlist)
                    csvwriter.writerows(table_data)
    except Exception as e:
        logaMessage(str(e),"error",logging)
        error_file_list.append(("Error while processing file[stage=write to CSV]: {}".format(filename),filename))

def convertDataToCSV(args_tuple):
    try:
        xml_filename,tableheaderfile,csvfilepath,logging=args_tuple
        logaMessage("Processing file: " + xml_filename, "info", logging)
        convertedjsonofeachfile=convertToJSON(xml_filename,logging)
        if convertedjsonofeachfile:
            putTableDataToCSVFile(tableheaderfile,convertedjsonofeachfile,csvfilepath,logging)
            processed_xml.append(xml_filename)
            logaMessage("Processed file " + xml_filename, "info", logging)
    except Exception as e:
        logaMessage(str(e),"error",logging)

def getLineCount(filename,pattern=None):
    f_open_temp=io.open(filename,'r',encoding="utf-8").readlines()
    f_open=[]
    for line in f_open_temp:
        f_open.append(line.encode('utf8', 'replace'))
    count=0
    if pattern:
        for line in f_open:
            if line and pattern in str(line):
                count=count+1
        return count
    else:
        for line in f_open:
            if line:
                count=count+1
        return count

def validateData(args_tuple):
    try:
        filename,csvpath,csvsubdirectorylist,logging=args_tuple
        table_count_info={}
        abs_xml_file_path=filename
        for table in csvsubdirectorylist:
            table_count_info[table]={}
            csv_directory=csvpath+"/"+table
            abs_csv_file_path=os.path.join(csv_directory,filename.split('/')[-1].strip('.xml')+".csv")
            pattern="</"+table+">"
            countfromxml=getLineCount(abs_xml_file_path,pattern)
            countfromcsv=getLineCount(abs_csv_file_path)
            table_count_info[table]['xmlcount']=countfromxml
            table_count_info[table]['csvcount']=countfromcsv-1
        logaMessage("count metrics for file "+filename.split('/')[-1].strip('.xml')+".csv"+" is : "+str(table_count_info),"info",logging)
    except Exception as e:
        logaMessage(str(e),"error",logging)
        raise Exception("Failed during data validation of file: {}".format(filename))

if __name__=="__main__":
    signal.signal(signal.SIGUSR2, receiveSignal)
    logging=enableLogging(args.logfilepath)
    manager=Manager()
    processed_xml=manager.list()
    error_file_list=manager.list()
    inputValidation(args.xmlpath,args.table_header_file,logging)
    f_open=open(args.table_header_file,'r').readlines()
    sub_directories=[]
    for tabledetails in f_open:
        sub_directories.append(tabledetails.split(":")[0].strip())
    try:
        for sub_directory in sub_directories:
            abs_path=createCSVDirectory(args.csvpath,sub_directory)
    except Exception as e:
        logaMessage("Error while creating directory {}".format(sub_directory), "error", logging)
        raise Exception("Error while creating directory {}".format(sub_directory))

    xml_file_list = []
    for file in [os.path.join(path, name) for path, subdirs, files in os.walk(args.xmlpath) for name in files]:
        if file.endswith(".xml"):
            xml_file_list.append(file)

    args_tuples = []
    for xmlfile in xml_file_list:
        args_tuples.append((xmlfile,args.table_header_file,args.csvpath,logging))
    with Pool(5) as pool:
        pool.map(convertDataToCSV,args_tuples)
        pool.close()
        pool.join()
        pool.clear()

    #Send a notification that data conversion is done. Now the validation phase starts
    os.system(
        """curl -X POST -H 'Authorization: Bearer xoxb-4963982146-514692973266-g9tNQt4K6iuhSpXueBdVQnGA' -H 'Content-type: application/json' --data '{"channel":"UCFKCUW10","text":"XML to CSV Conversion successfull. Data validation starts now"}' https://slack.com/api/chat.postMessage""")
    #Make the process halt or wait for signal
    while global_validate:
        print("Please copy all the CSV files to the SFTP server....")
        time.sleep(10)

    if global_validate == False:
        if args.enabledatavalidation:
            csvsubdirectorylist = []
            f_open = open(args.table_header_file, 'r').readlines()
            for table_info in f_open:
                csvsubdirectorylist.append(table_info.split(":")[0].strip())

            validate_args_tuples=[]
            for xmlfile in processed_xml:
                validate_args_tuples.append((xmlfile,args.csvpath,csvsubdirectorylist,logging))

            with Pool(5) as pool1:
                pool1.map(validateData,validate_args_tuples)
                pool1.close()
                pool1.join()
                pool1.clear()

        if error_file_list:
            logaMessage("Failed to process below files","error",logging)
            for errormessage in error_file_list:
                logaMessage(errormessage[0],"error",logging)
                print(errormessage[0])
                raise Exception("Processing failed for some xml files...see the log file for more details")

    os.system(
        """curl -X POST -H 'Authorization: Bearer xoxb-4963982146-514692973266-g9tNQt4K6iuhSpXueBdVQnGA' -H 'Content-type: application/json' --data '{"channel":"UCFKCUW10","text":"XML to CSV Conversion and Data validation are done"}' https://slack.com/api/chat.postMessage""")