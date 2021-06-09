#!/usr/bin/python
import sys
import os
try:
    opt = sys.argv[1]
    if opt == '-h':
        print "-c\t--create    Create VM on DOM0\n"
        print "-d\t--destroy   Destroy VM on DOM0\n"
        print "-l\t--list      List VMs on DOM0\n"
        print "-h\t--help      Displays help\n"
    elif opt == '-c':
        pass
    elif opt == '-d':
        pass
    elif opt == '-l':
        pass
    else:
        print "WRONG ARGUMENTS PASSED, try -h for help"
except IndexError:
    print "WARNING: ARGUMENTS ARE MISSING, try -h for help"
    sys.exit()

def list_vm():


import subprocess
 
from threading import Timer
 
kill = lambda process: process.kill()
cmd = ['ping', 'www.google.com']
ping = subprocess.Popen(
    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
my_timer = Timer(5, kill, [ping])
 
try:
    my_timer.start()
    stdout, stderr = ping.communicate()
finally:
    my_timer.cancel()
    
