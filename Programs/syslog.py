#!/usr/bin/python
import os

def write_syslog():
    file_sys = open('/usr/local/git/em/etc/procs.linux','r')
    lines = file_sys.readlines()
    file_sys.close()
    file_sys = open('/usr/local/git/em/etc/procs.linux','w')
    for line in lines:
        if not 'syslog' in line:
            file_sys.write(line.strip())
            file_sys.write('\n')
    file_sys.write('rsyslogd\n')
    file_sys.close()

def write_xinetd():
    file_sys = open('/usr/local/git/em/etc/procs.linux','r')
    lines = file_sys.readlines()
    file_sys.close()
    file_sys = open('/usr/local/git/em/etc/procs.linux','w')
    for line in lines:
        if not 'xinetd' in line:
            file_sys.write(line.strip())
            file_sys.write('\n')
    file_sys.close()

    
f = os.popen('/usr/local/git/bin/perl /usr/local/git/em/host/procs -f /usr/local/git/em/etc/procs 2>/dev/null')
pblm = f.read().strip()
if 'syslogd' in pblm:
    print 'syslogd issue'
    f = os.listdir('/etc/init.d/')
    if 'syslog' not in f:
        if 'rsyslog' in f:
            f1 = os.popen('/etc/init.d/rsyslog start')
            write_syslog()
        else:
            print 'syslog and rsyslog, both the services are not installed'
    else:
        f1 = os.popen('/etc/init.d/syslog start')
    
elif 'xinetd' in pblm:
    print 'xinetd issue'
    f = os.listdir('/etc/init.d/')
    if 'xinetd' not in f:
        write_xinetd()
    else:
        f1 = os.popen('/etc/init.d/xinetd start')


