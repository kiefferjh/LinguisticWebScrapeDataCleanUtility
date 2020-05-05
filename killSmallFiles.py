#This script is used to clean up files that are less than a certain size
#Kieffer Higgins

#This script might delete itself
import os

directory = os.listdir(os.getcwd())
for file in directory:
    fileinfo = os.stat(file)
    if fileinfo.st_size < 3000: #3kb
        os.remove(file)
