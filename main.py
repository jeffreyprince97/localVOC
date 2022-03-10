import os
import time
from flask import Flask, flash, jsonify, render_template, request,redirect, send_file, url_for
import webbrowser



import subprocess

import htmlgenerator as mgh
import practicalities as pr
import pdfgenerator as gpdf
import resultgen as rgen

#Path to script
myp = os.getcwd()+os.sep
static = myp+'static/'
procs = myp+'Procedures/'

app = Flask(__name__)


arraydirs = []

@app.route('/update', methods=['GET','POST'])
def update():


    # for categories in os.listdir(procs):
    #     for procedures in os.listdir(procs+categories):
    #         mgh.generatehtml(categories,procedures)

    for root, dirs, files in os.walk(myp + "Procedures", topdown=True): #
        for d in dirs: # names in procedures
            mgh.generatehtml(d)

    return render_template('update.html')


@app.route('/', methods=['GET','POST'])
def dropdown():
    arraydirs = []
    for root, dirs, files in os.walk(myp + "Procedures", topdown=True): #
        for d in dirs: # names in procedures
            with open(root + os.sep + d + os.sep+"fullname.cames", "r") as tf: # open fullname file in each folder
                fullname = tf.readlines()[0] # save as variable in array
            arraydirs.append((d,fullname))
            arraydirs.sort() # ville ikke blive alfabetisk ellers.

    return render_template('start.html',dirs=arraydirs)





@app.route('/<name>', methods=['GET','POST'])

def handledata(name):
    pr.setprocedure(name)


    if name == "favicon.ico":

        return ('', 204) #No content
    else:
        if request.method == 'POST':
            print("POST")
            objs = []
            procedure = pr.getprocedure()
            #categories = arraydirs[0]
            #procedure = name
            directory = myp + os.sep + 'Procedures' + os.sep + procedure + os.sep
            csvfile = directory + 'content.csv'
            print(directory)
            count = len(open(csvfile,'r').readlines(  ))
            for i in range(count-1):
                objs.append(request.form.get('obj'+str(i+1)))

            with open(myp+"results.txt", "w") as f:
                for oo in objs:
                    f.write("%s;\n" % (oo)) # måske indsætte en if isinstance(oo, int)

            comments = []

            count = len(open(csvfile,'r').readlines(  ))
            for i in range(count-1):
                comments.append(request.form.get('comments'+str(i+1)))

            with open(myp+"comments.txt", "w") as f:
                for cc in comments:
                    f.write("%s;\n" % (cc))


            return redirect('result') # Redirect to result pages for pdf download

        elif request.method == 'GET':
            pr.setprocedure(name)
            print("get")

        return render_template(name+'.html')




@app.route('/result', methods=['GET','POST'])

def resultpresent():

    if request.method == 'POST':
        print("POST")

    elif request.method == 'GET':
        print("GET. Makes PDF")
        procedure = pr.getprocedure()
        print(procedure)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        pr.settime(timestr)
        rgen.generateresult(procedure,timestr)
        gpdf.generatepdf(procedure,timestr)

    return render_template('result'+procedure+timestr+'.html')

if __name__ == "__main__":
    app.run(debug=False)