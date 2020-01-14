import shutil
import os

fd = open("webApp.py","r")
try:
	if not os.path.isdir("safe"):
		os.mkdir("safe")
		os.system("chmod 0200 safe")
except:
	print("directory exists!!")
path = os.path.dirname(os.path.realpath(fd.name))
filename, file_extension = os.path.splitext(fd.name)

shutil.copy(path+"/"+fd.name,path+'/safe/')
os.system("sudo mv safe/"+fd.name+ " " + "safe/" +fd.name + str(self.safenumber)+file_extension)
self.safenumber += 1