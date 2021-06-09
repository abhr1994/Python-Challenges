#!/usr/bin/python
import sys
import os
import subprocess
import glob
import re
from threading import Timer

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#
def time_out(cmd):
    kill = lambda process: process.kill()
    ping = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    my_timer = Timer(5, kill, [ping])
 
    try:
        my_timer.start()
        stdout, stderr = ping.communicate()
    finally:
        my_timer.cancel()
        return stdout
#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#
def vm_list():
    result = time_out(['xl','list'])
    temp = result.split('\n')
    temp = filter(None,temp)
    temp = [i for i in temp if not ('Domain-0' in i or 'Name' in i)]
    if len(temp) > 0:
        l = []
        
        if not os.path.exists('/OVS/Repositories/*/VirtualMachines/*/vm.cfg'):
            print "/OVS/Repositories/*/VirtualMachines/*/vm.cfg is not being listed!!! Exiting!!"
            sys.exit()
        for filename in glob.glob("/OVS/Repositories/*/VirtualMachines/*/vm.cfg"):
            l.append(filename)
        final_list = []
        for i in temp:
            for j in l:
                if i.split()[0] in j:
                    f = open(j).readlines()
                    lis = list(f)
                    for element in lis:
                        if 'simple_name' in element and not(element.startswith('#')):
                            resu = element.split('=')[1].strip()
                            portf = os.popen('xenstore-read /local/domain/'+i.split()[1]+'/console/vnc-port 2>/dev/null')
                            port = portf.read().strip()
                            temporary = [re.sub("\'","",resu),i.split()[1],i.split()[4],port,j]
                            final_list.append(temporary)
                    break
        for element in final_list:
            print element[0],element[1],element[2],element[3],element[4]
    else:
        print "No VMs running!!"
    return temp
#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#

def vm_destroy():
    run_id = vm_list()
    if len(run_id) > 0:
        vmname = raw_input("\nInput the VM name: ")
        for ids in run_id:
            f = os.popen('grep -i simple /OVS/Repositories/*/VirtualMachines/'+ids.split()[0]+'/vm.cfg')
            ab = f.read()
            name = re.sub("'","",ab.split('=')[1].strip())
            if name == vmname:
                print "INFO: ",vmname,"Found Running!!!\n"
                print ids
                opt = raw_input("Do you still want to destroy the VM (y/n): ")
                if opt.lower() == 'y':
                    des = os.popen('xm destroy '+ids.split()[0])
                    print des.read()
                    print "VM has been destroyed \n"
                elif opt.lower() == 'n':
                    print "VM Not destroyed"
                else:
                    print "Wrong choice"
                break
        else:
            print "VM is not running..!!!"
    
    

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#

def create_vm():
    run_id = vm_list()
    vmname = raw_input("\nInput the VM name: ")
    for ids in run_id:
        f = os.popen('grep -i simple /OVS/Repositories/*/VirtualMachines/'+ids.split()[0]+'/vm.cfg')
        ab = f.read()
        name = re.sub("'","",ab.split('=')[1].strip())
        if name == vmname:
            print "INFO: ",vmname,"Found Running!!!\n"
            print ids
            print "If u still want to create VM, Destroy the VM and then try to create"
            sys.exit()
    f = os.popen('grep -i '+vmname+' /OVS/Repositories/*/VirtualMachines/*/vm.cfg |grep -i simple |wc -l 2>/dev/null')
    cfg_count = int(f.read().strip())
    f = os.popen('grep -i '+vmname+' /OVS/Repositories/*/VirtualMachines/*/vm.cfg |grep -i simple 2>/dev/null')
    cfg = f.read().strip()
    if cfg_count > 1:
        print "WARNING: There are more than one vm.cfg files were found... NOT Creating VM, Check manually....!!!\n"
        f = os.popen('grep -i '+vmname+' /OVS/Repositories/*/VirtualMachines/*/vm.cfg |grep -i simple 2>/dev/null')
        print f.read()
        sys.exit()
    else:
        cfg_file = cfg.split(':')[0]
        if cfg_file == "":
            print "WARNING: Couldn't find the config file..!!!"
        else:
            f = os.popen('xm create '+cfg_file)
            print vmname," has been created"

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#

def firstfunction():
    try:
        opt = sys.argv[1]
        if opt == '-h':
            print "-c\t--create    Create VM on DOM0\n"
            print "-d\t--destroy   Destroy VM on DOM0\n"
            print "-l\t--list      List VMs on DOM0\n"
            print "-h\t--help      Displays help\n"
        elif opt == '-c':
            create_vm()
        elif opt == '-d':
            vm_destroy()
        elif opt == '-l':
            ids = vm_list()
        else:
            print "WRONG ARGUMENTS PASSED, try -h for help"
    except IndexError:
        print "WARNING: ARGUMENTS ARE MISSING, try -h for help"
        sys.exit()

def mainfunction():
    try:
        f=open("/etc/ovs-release")
        ver = f.read()
        if '3.' in ver.strip():
            print ver.strip()
            f = open('/etc/mtab').readlines()
            for i in f:
                if '/OVS/Repositories/' in i:
                    break
            else:
                print "WARNING: /OVS/Repositories were not found mounted....!!!!!"
                sys.exit()
            firstfunction()
        elif '2.' in ver.strip():
            pass
        else:
            pass
    except IOError:
        print "WARNING: It may not be a DOM0 or /etc/ovs-release file doesn't exists...!!!"

mainfunction()
