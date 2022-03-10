
#Python Libraries
import os
import sys


import time

#Own libraries
import practicalities as pr

listProcedures = pr.getProcedureList()


def generateresult(procedure,timesstr):
    myp = os.getcwd()+os.sep
    p_template = myp + "templates" + os.sep
    directory = myp + os.sep + 'Procedures' + os.sep + procedure + os.sep
    metadata = directory + 'metadata.txt'

    procedure = pr.getprocedure()


    html = "<head><link rel='stylesheet' href='static/VOCCSS.css'></head>"
    html += "<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' />"
    html += "<meta http-equiv='X-UA-Compatible' content='IE=Edge, chrome=1'>"
    html += "<meta http-equiv='Cache-control' content='no-store'> <title> "+procedure+' result'"</title>"

    timestr = pr.gettime()

    html +="<body> <div class='title'> <h1> Assessment tool result for "+ procedure+" </h1> <h2> Download below </h2> </div>"
    html +="<div class='divdownload'> Download here: <a href='static/"+procedure+"-"+timestr+".pdf'>"
    html +="<button id='downloadbtn'> Link </button></a> </div></body></html>"


    html += "<div class='metadataresult'> <p class='metadata'>"
    with open(metadata,'r') as f:
        for i,l in enumerate(f.readlines()):
             html += l
    html += "</p></div></div></div>"

    html += "<a href='/' class=home> <button id=home> Home </button> </a>"


    with open(p_template +"result"+procedure+timestr+".html", 'w') as fhtml:
        fhtml.write(html)





















