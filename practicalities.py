import os
import time

#Path to library
myp = os.path.dirname(os.path.abspath(__file__)) + os.sep


def getProcedureList():
    mylist = []
    for root, dirs, files in os.walk(myp + "Procedures", topdown=False):
        for d in dirs:
            print(d)
            mylist.append(d)
    return mylist

def setprocedure(procedure):
    if procedure != 'favicon.ico':
        with open(myp +os.sep + "presentproc.cames","w") as f:
            f.write(procedure)

def getprocedure():
    with open(myp +os.sep + "presentproc.cames","r") as f:
        procedure = f.readlines()[0]
    return procedure



def settime(timestr):
    with open(myp +os.sep + "presenttime.cames","w") as f:
        f.write(timestr)

def gettime():
    with open(myp +os.sep + "presenttime.cames","r") as f:
        timestr = f.readlines()[0]
    return timestr