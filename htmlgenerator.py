
#Python Libraries
import os
import sys


#Own libraries
import practicalities as pr

listProcedures = pr.getProcedureList()

print(list)



# https://bjssjournals.onlinelibrary.wiley.com/doi/abs/10.1046/j.1365-2168.1997.02502.x

# Alternative for creating html
# https://stackoverflow.com/questions/54446345/flask-loop-through-post-requests-with-input-data
def generatehtml(procedure):
    myp = os.getcwd()+os.sep
    p_template = myp + "templates" + os.sep
    directory = myp + os.sep + 'Procedures' + os.sep + procedure + os.sep # tænker at hente variablen ind fra main (post)
    csvfile = directory + 'content.csv'
    desctext = directory + 'desctext.txt'
    ratermanualtext = directory + 'ratermanual.txt'
    metadata = directory + 'metadata.txt'

    print("path: "+myp)




    html = "<head><link rel='stylesheet' href='static/VOCCSS.css'></head>"
    html += "<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' />"
    html += "<meta http-equiv='X-UA-Compatible' content='IE=Edge, chrome=1'>"
    html += "<meta http-equiv='Cache-control' content='no-store'> <title> "+procedure+"</title>"

    html += "<div class='title'> <h1> Assessment tool </h1> <h2> "+procedure+" </h2> </div> \n"


    html += "<a href='/' class=home> <button id=home> Home </button> </a>"

    html += "<div class='content'> <div class='desctext1'> <p class='desctext1'>"

    with open(desctext,'r') as f:
        for i,l in enumerate(f.readlines()):
            html += l

    html += "<div class=btnsright>"
    html += "<button id='myBtn'>Rater manual</button> <div id='myModal' class='modal'> <div class='modal-content'> <span class='close'>&times;</span> <b>Rater manual</b> </br>"

    with open(ratermanualtext,'r') as f:
        for i,l in enumerate(f.readlines()):
             html += l
    html += "</div></div>"

    html += "<div class='metadata'> <p class='metadata'>"
    with open(metadata,'r') as f:
        for i,l in enumerate(f.readlines()):
             html += l
    html +=  "<div class='anchortoggle'><input type='button' value='Toggle anchors' id='btnToggle'/></div>"
    html += "</p></div></div></div>"

    html += "<form action='' method='post'>"





    with open(csvfile,'r') as f:
        for i,l in enumerate(f.readlines()):
            if i > 0: #Skips header
                scale = l.split(";")
                mytype = scale[0]
                object = scale[1]
                vmin = scale[2]
                vmax = scale[3]
                descs = []
                for k,c in enumerate(scale):

                    if k+5 == len(scale):
                        # print(k,k+5,len(scale))
                        break

                    elif k % 2 == 0: #USING REMAINDER TO CATCH EVERY SECOND K.
                        descs.append(scale[4 + k] + ": " + scale[5 + k])
                        # print(descs[-1],k)

                # print("LENGTH DESCS LIST ", len(descs))

                html += "<div class=toolbox> <div class=tools><div class=tool1 id=object" +str(i) + ">"

                # print(object)
                html += "<p> " + "<b>" + object + ":" + "</b>" + "</p>"


                if mytype == "YN":
                    html += "</br> </div>"
                    html += "<div class ='YN'><div class = 'option'><input type = 'radio' class='optionclick' id = 'obj" + str(i)+ "val" + str(int(vmax))
                    html += "' name=obj" +str(i) + " value=" + str(int(vmax)) + " required>"
                    html += "<label for='obj"+ str(i)+ "val" + str(int(vmax)) + "' style='vertical-align: super;'>"   #
                    html += " Yes </label> </div>"

                    html += "<div class = 'option'><input type = 'radio' class='optionclick' id = 'obj" + str(i)+ "val" + str(int(vmin))
                    html += "' name=obj" +str(i) + " value=" + str(int(vmin)) + " required>"
                    html += "<label for='obj"+ str(i)+ "val" + str(int(vmin)) + "' style='vertical-align: super;'>"   #
                    html += " No</label> </div> </div><div class='tool3'>"


                elif mytype == "SCALE":
                    html += "</div><div class=tool2>"
                    for val in range(int(vmin),int(vmax)+1):
                        # print(val)
                        html += "<div class='option'><input type = 'radio' class='optionclick' id = 'obj" + str(i)+ "val" + str(val)
                        html += "' name=obj" +str(i) + " value=" + str(val) + " required>"
                        html += "<label for='obj"+ str(i)+ "val" + str(val) + "' style='vertical-align: super;'>"   #
                        html += str(val) + "</label> </div>"
                    html += "</div> <div class='tool3'>"
                    # beskrivende tekst
                    for j in range(0,len(descs)):
                        html += "</br> <p> " + descs[j]
                html += "</div></div><div class='comments"+str(i)+"'style='display: flex;align-items: center;'><label for='comments"+str(i)+"'>Comments: </label> <input type='text' id='comments"+str(i)+"' name='comments"+str(i)+"' value=''></div>"


                        #ADD SUBMIT BUTTON
                        #RECEIVE DATA IN PYTHON&FLASK
                html += "</div></div>" + " </p>"

    # html += "<label for='comments'>Comments:</label><br> <input type='text' id='comments' name='comments' value=''><br><br>"
    html += "<input type='submit' value='Save to PDF'>"
    html += "</form>"

    # https://jsbin.com/gijozazihu/1/edit?html,output

    # anchor toggle

    html += "<script src='//code.jquery.com/jquery-1.11.1.min.js'></script> <meta charset='utf-8'><script>\n"
    html += "  $(function() {\n"
    html += "    $('#btnToggle').click(function() {\n"
    html += "       $('.tool3').toggle();\n"
    html += "   });\n"
    html += "});\n\n"


    # Rater manual

    html +="var modal = document.getElementById('myModal');\n"
    html += "var btn = document.getElementById('myBtn');\n"
    html += "var span = document.getElementsByClassName('close')[0];\n"
    html += "btn.onclick = function() {\n"
    html += "    modal.style.display = 'block'; }\n"
    html += "span.onclick = function() {\n"
    html +="     modal.style.display = 'none'; }\n"
    html += "window.onclick = function(event) {\n"
    html += "   if (event.target == modal) {\n"
    html +="        modal.style.display = 'none'; } }\n\n"

    # comments toggle

    html+="$(function () {\n"
    html+="n = document.querySelectorAll('[class^=tool1]').length;\n"
    html+="for (let i = 1; i < n+1; i++) {\n"
    html+="    $('#object'+i).click(function () {\n"
    html+="        $('.comments'+i).toggle();\n"
    html+="    });\n"
    html+="}\n"
    html+="});\n"

    html+="</script>"


    with open(p_template +procedure +".html", 'w') as fhtml:
        fhtml.write(html)
    print("html generated succesfully")




