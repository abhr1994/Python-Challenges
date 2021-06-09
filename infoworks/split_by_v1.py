import os,sys
import traceback

try:
    iw_home = os.environ['IW_HOME']
except KeyError as e:
    print('Please source $IW_HOME/bin/env.sh before running this script')
    sys.exit(-1)
import pandas as pd
import argparse
try:
    import pyodbc
except ImportError:
    os.system('python -m pip install pyodbc')
    import pyodbc
infoworks_python_dir = os.path.abspath(os.path.join(iw_home, 'apricot-meteor', 'infoworks_python'))
sys.path.insert(0, infoworks_python_dir)
parser = argparse.ArgumentParser('SQL Insert')
parser.add_argument('--server', required=True, help='Enter the JDBC Connection URL')
parser.add_argument('--user', required=True, help="Enter the username")
parser.add_argument('--secretkey', required=True, help="Enter the secret key")
parser.add_argument('--database', required=True, help="Enter the database")
parser.add_argument('--schema', required=True, help="Enter the schema name")
parser.add_argument('--table', help='Enter the table name')
parser.add_argument('--parallelconnections', required=True, help="Enter the number of available connections")

args = parser.parse_args()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    p = os.popen("bash " + infoworks_python_dir + "/infoworks/bin/infoworks_security.sh -decrypt -p " + args.secretkey)
    password = p.read().strip()
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + args.server.strip() + ';PORT=1433' + ';DATABASE=' + args.database.strip() + ';UID=' + args.user.strip() + ';PWD=' + password)
    cursor = conn.cursor()
except Exception as e:
    print("Unable to conenct to SQL server "+str(e))

def get_datecolumn_feasiblitity(df,format,row_count,connections):
    print(format)
    df["Date"] = pd.to_datetime(df["Col"]).dt.strftime(format)
    df["Date"] = pd.to_numeric(df["Date"])
    max_col = df['Date'].max()
    min_col = df['Date'].min()
    blocksize = int((min_col + max_col) / connections)

    # min of connections and col_count is what we should loop
    loop_col = min(int(df.shape[0]), connections)
    out = []
    min_t = min_col

    for i in range(loop_col):
        max_t = min_t + blocksize
        df_temp = df[(df['Date'] >= min_t) & (df['Date'] < max_t)]
        out.append(df_temp['Count'].sum())
        min_t = max_t
    df_temp = df[(df['Date'] >= max_t)]

    out.append(df_temp['Count'].sum())
    print(out)
    avg = row_count // loop_col
    # difference between max and wat u r processing is less than avg
    count_of_failed = 0
    for i in out:
        if ((i - avg) / avg) * 100 <= -30:
            count_of_failed += 1

    if count_of_failed > 0.5 * loop_col:
        percent = int(((loop_col - count_of_failed) / loop_col) * 100)
        return (False, max(0, percent),format)
    else:
        return (True, int(((loop_col - count_of_failed) / loop_col) * 100),format)

def check_ts_column_splitby_compatible(col,row_count,connections):
    try:
        cursor.execute("select {},count(*) as count from {}.{} group by {} order by {}".format(col, args.schema.strip(),
                                                                                        args.table.strip(), col, col))
        list_colcounts = []
        for key, value in cursor:
            if key is not None:
                list_colcounts.append([key, int(value)])

        df = pd.DataFrame(list_colcounts, columns=['Col', 'Count'])
        df = df.dropna()
        ret_values = []
        for format in ["%d","%m","%Y","%m%d","%Y%m","%Y%m%d"]:
            ret_values.append(get_datecolumn_feasiblitity(df,format,row_count,connections))

        return ret_values
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return (False,0)


def check_int_column_splitby_compatible(col,row_count,connections):
    try:
        cursor.execute("select count(distinct({})) from {}.{}".format(col,args.schema.strip(), args.table.strip()))
        col_count = cursor.fetchone()[0]
        #Check if distinct col count is equal to total row count of table
        avg_count = (col_count+row_count)/2
        diff_count = row_count-col_count
        if diff_count >= avg_count:
            cursor.execute("select {},count(*) as count from {}.{} group by {} order by {}".format(col,args.schema.strip(), args.table.strip(),col,col))
            list_colcounts = []
            for key, value in cursor:
                if key is not None:
                    list_colcounts.append([int(key), int(value)])

            df = pd.DataFrame(list_colcounts, columns=['Col', 'Count'])
            df = df.dropna()
            max_col = df['Col'].max()
            min_col = df['Col'].min()
            blocksize = int((min_col + max_col) / connections)

            #min of connections and col_count is what we should loop
            loop_col = min(int(df.shape[0]),connections)
            out = []
            min_t = min_col
            for i in range(loop_col):
                max_t = min_t + blocksize
                df_temp = df[(df['Col'] >= min_t) & (df['Col'] < max_t)]
                out.append(df_temp['Count'].sum())
                min_t = max_t
            df_temp = df[(df['Col'] >= max_t)]

            out.append(df_temp['Count'].sum())
            print(out)
            avg = row_count//loop_col
            # difference between max and wat u r processing is less than avg
            count_of_failed = 0
            for i in out:
                if ((i-avg)/avg)*100<= -30:
                    count_of_failed += 1

            if count_of_failed > 0.5 * loop_col:
                percent = int(((loop_col-count_of_failed)/loop_col)*100)
                return (False,max(0,percent))
            else:
                return (True,int(((loop_col-count_of_failed)/loop_col)*100))
        else:
            return (True,100)
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return (False,0)

try:
    cursor.execute(
        "SELECT COLUMN_NAME, DATA_TYPE  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG='{}' AND TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}' AND DATA_TYPE in ('bigint' , 'numeric' , 'smallint' , 'decimal' , 'int' , 'tinyint' , 'float' , 'date' , 'datetime2' , 'smalldatetime' , 'datetime' , 'time')".format(
            args.database.strip(), args.schema.strip(), args.table.strip()))

    integertype_available_splitbycols=[]
    timestamptype_available_splitbycols=[]
    for row in cursor:
        if row[-1].strip().lower() in ['date' , 'datetime2' , 'smalldatetime' , 'datetime' , 'time']:
            timestamptype_available_splitbycols.append(row[0])
        else:
            integertype_available_splitbycols.append(row[0])

    cursor.execute("EXEC sp_helpindex '{}.{}.{}'".format(args.database.strip(),args.schema.strip(), args.table.strip()))
    out = []
    for row in cursor:
        out = out + [j.strip() for j in row[-1].split(',')]
    set_indexing_columns = set(out)
    set_int_available_splitbycols = set(integertype_available_splitbycols)
    set_ts_available_splitbycols = set(timestamptype_available_splitbycols)
    final_int_splitcols = list(set_int_available_splitbycols.intersection(set_indexing_columns))
    final_ts_splitcols = list(set_ts_available_splitbycols.intersection(set_indexing_columns))
    print(bcolors.HEADER+"Available columns for splitby are: "+", ".join(final_int_splitcols+final_ts_splitcols)+bcolors.ENDC)

    cursor.execute("select count(*) from {}.{}".format(args.schema.strip(), args.table.strip()))
    table_row_count = cursor.fetchone()[0]

    result_columns=[]
    for item in final_int_splitcols:
        print(bcolors.OKBLUE+"Checking if the column {} is best-fit for splitby? ".format(item)+bcolors.ENDC)
        ret = check_int_column_splitby_compatible(item,table_row_count,int(args.parallelconnections.strip()))
        if ret[-1] == 0:
            print(bcolors.FAIL+"Column {} is {} % fit for splitby ".format(item,ret[-1])+bcolors.ENDC+"\n")
        elif ret[-1] > 0 and ret[-1] <=75 :
            print(bcolors.WARNING+"Column {} is {} % fit for splitby ".format(item,ret[-1])+bcolors.ENDC+"\n")
        else:
            print(bcolors.OKGREEN+"Column {} is {} % fit for splitby ".format(item,ret[-1])+bcolors.ENDC+"\n")
        if ret[0]:
            result_columns.append((item,ret[-1]))

    for item in final_ts_splitcols:
        print(bcolors.OKBLUE + "Checking if the column {} is best-fit for splitby? ".format(item) + bcolors.ENDC)
        return_values = check_ts_column_splitby_compatible(item, table_row_count, int(args.parallelconnections.strip()))
        for ret in return_values:
            if ret[1] == 0:
                print(bcolors.FAIL+"Column {} with format {} is {} % fit for splitby ".format(item,ret[-1],ret[1])+bcolors.ENDC+"\n")
            elif ret[1] > 0 and ret[1] <=75 :
                print(bcolors.WARNING+"Column {} with format {} is {} % fit for splitby ".format(item,ret[-1],ret[1])+bcolors.ENDC+"\n")
            else:
                print(bcolors.OKGREEN+"Column {} with format {} is {} % fit for splitby ".format(item,ret[-1],ret[1])+bcolors.ENDC+"\n")
            if ret[0]:
                result_columns.append((item+" : "+ret[-1],ret[1]))

    #Print the results in sorted fashion
    out_list_final = sorted(result_columns, key=lambda x: x[-1],reverse=True)
    #print(out_list_final)
    print(bcolors.BOLD+"Printing the column list which are best suitable for split-by left to right"+bcolors.ENDC)
    print(", ".join([i[0] for i in out_list_final]))

except Exception as e:
    print("Error occured "+str(e))
    traceback.print_exc()
