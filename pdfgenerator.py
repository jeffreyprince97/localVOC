import os

import fpdf
import numpy as np
import datetime
from decimal import Decimal

import time

import practicalities as pr

listProcedures = pr.getProcedureList()

def generatepdf(procedure,timestr):
    myp = os.getcwd()+os.sep
    p_template = myp + "templates" + os.sep
    directory = myp + 'Procedures'+ os.sep+ procedure + os.sep
    csvfile = directory + 'content.csv'


    # PDF layout variabler:
    w = 90
    h = 80
    wlogo = 25
    hlogo =wlogo/0.844374343
    wcameslogo = 60
    hcameslogo = wcameslogo/8.701612903
    margin_left = 20
    margin_right = 20
    margin_top = 15
    linespacing = 12


    # For-loop for at gemme aktiviteter og maxpoints i lister:
    activity_names = [] #Dataholder
    Types = [] #Type holder
    maxpoints = []
    li = 0
    with open(csvfile,'r') as f: #Open file
        for line in f.readlines():
            data = line.split(";")
            try:
                if li > 0:
                    activity_names.append(str(data[1]))
                    Types.append(str(data[0]))
                    maxpoints.append(str(data[3]))
            except ValueError:
                pass

            li += 1

    # For-loop for resultater:
    results = [] #Dataholder

    with open(myp + "results.txt",'r') as f: #Open file. With statement is temporary
        for i in f.readlines():
            data = i.split(";")
            try:
                results.append(str(data[0]))
            except ValueError:
                pass

    # Comments:

    comments = []
    #with open(myp + "comments.txt",'r') as f:
        #comments.append(f.readlines())
        #str1 = "".join(str(e) for e in comments)

    with open(myp + "comments.txt",'r') as f: #Open file. With statement is temporary
        for i in f.readlines():
            data = i.split(";")
            try:
                comments.append(str(data[0]))
            except ValueError:
                pass


    # PDF generator
    pdf=fpdf.FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.image(myp + 'voclogo.png', margin_left/2, 10, wlogo, hlogo)
    pdf.image(myp + 'CAMESLOGO.png', margin_left/2+wlogo+5, 10+hlogo-hcameslogo-2, wcameslogo, hcameslogo)

    # Date/time:
    pdf.set_font("Helvetica", 'B', size = 15)
    #pdf.text(x = 150, y = margin_top, txt = "Assessment tool")
    pdf.multi_cell(180, 10, "Assessment tool", 0,'R', False)
    #df.text(x = 130, y = margin_top+7, txt = "Tool - " + procedure)
    pdf.multi_cell(180, 10, "Tool - " + procedure, 0,'R', False)
    #pdf.multi_cell(190, 5, "txt", 0,'R', False)

    pdf.set_font("Helvetica", 'B', size = 12)
    currenttime = datetime.datetime.now()
    #pdf.text(x = 130, y = margin_top+14, txt=currenttime.strftime("%c"))
    pdf.multi_cell(180, 10, currenttime.strftime("%c"), 0,'R', False)

    # pdf.text(x = margin_left, y = hlogo+margin_top + 10, txt=currenttime.strftime("%c"))

    # Results print to pdf:
    pdf.set_font("Helvetica", 'B', size = 12)
    pdf.set_y(50)

    for i,result in enumerate(results):
        #print(Types[i],result,results[i])
        try:
            #print(i,result,Types)
            activity = activity_names[i]
            comment = comments[i]

            # hvis det er ja/nej skrives hhv. ja/nej i parentes efter point.
            if Types[i] == "YN":
                if result =="0":
                    yn = "No"
                else:
                    yn = "Yes"

                print(i," : ",activity,result,yn)

                #pdf.text(x = margin_left, y = 35 + linespacing*i+20,
                #txt = ("{}: {} ({} pts)".format(activity, yn,result)))
                pdf.set_font("Helvetica", 'B', size = 12)
                pdf.multi_cell(180, 8.5, ("{}: {} ({} pts)".format(activity, yn, result)), 1, "J", False)
                if not comment.strip():
                    pass
                else:
                    pdf.set_font("Helvetica",'I', size = 12)
                    pdf.multi_cell(180,12, comment,1,"J",False)



            elif Types[i] == "SCALE":

                #pdf.text(x = margin_left, y = 35 + linespacing*i+20,
                #txt = ("{}: {} pts".format(activity, result)))
                pdf.set_font("Helvetica", 'B', size = 12)
                pdf.multi_cell(180, 9.5, ("{}: {} pts".format(activity, result)), 1, "J", False)
                if not comment.strip():
                    pass
                else:
                    pdf.set_font("Helvetica",'I', size = 12)
                    pdf.multi_cell(180,9.5, comment,1,"J",False)



        except IndexError:
            print("End of List")


    # Comments print to pdf:
    #pdf.set_font("Helvetica",'I', size = 15)
    #pdf.multi_cell(180,12, "Comments: "+str1,0,"J",False


    # Total score calc:
    total = sum(Decimal(i) for i in results)
    maxscore = sum(Decimal(i) for i in maxpoints)

    # Total score print to pdf:
    pdf.set_font("Helvetica",'B', size = 15)

    #pdf.text(x = margin_left, y = 35 + linespacing*(iend+1)+20,
    #txt = ("Your global scale result is: " + str(total)))

    pdf.multi_cell(180, 12, "Total points: " + str(total) + " out of " + str(maxscore), 0, 'R', False)

    #

    # Opretter static mappe, hvis den ikke eksisterer:
    if not os.path.exists(myp + os.sep + "static"):
        os.mkdir(myp + os.sep + "static")

    timestr = pr.gettime()

    pdf.output(myp+"static"+os.sep+procedure+"-"+timestr+'.pdf','F') # Gemmer filen korrekt med dato og procedure-navn, men linket fører til den nyeste "summary.pdf".
    #pdf.output(myp+"static"+os.sep+'Summary.pdf','F') # F: gemmer filen
    #pdf.output(myp+"static"+os.sep+procedure+'.pdf','F') # F: gemmer filen
