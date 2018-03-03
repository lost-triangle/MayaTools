import os
#Variables must be configured to the proper Path
projectName = "default"
path = os.environ['USERPROFILE'] + "\Documents\maya\projects" + "\\" + projectName + "\\" + "autosave"
#Camera selected
camera = "persp"

filename = "batchRender.bat"
fileoutput = path + "\\" + filename
file = open(fileoutput, "w")
file.write("@ECHO OFF")
file.write("TITLE Rendering AutoSaves")

outputpathCmd ="-rd " + path + "\img "

filelist = os.listdir(path)
filelist.remove(filename)

for item in filelist:
    outputimgNameCmd = "-im " + os.path.splitext(item)[0] + " "
    file.write("Render -r mr -of tga -cam " + camera + " " + outputimgNameCmd + outputpathCmd + path +"\\" + item)
    file.write("\n")

file.write("ECHO Batchrendering Completed \n")
file.write("ECHO Press Any Key to Finish... \n")
file.write("PAUSE")
file.write("DEL " + fileoutput)
file.close()

os.startfile(fileoutput)