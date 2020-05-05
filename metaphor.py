#War Metaphor Script
# Make it more efficient later!
#Imports
import os
import re
from sys import argv
#Let... argv[1] = BBC Climate Change List, argv[2] = War List, argv[3] = Intersection List
#functions for later use:
#Saves a set that was made from a line of an article to file specified in argv[3]
def saveToIntersectionFile(lineSet):
    lineString = ''.join(lineSet)
    with open(argv[3], 'a') as file:
        file.write(lineString)
        #new line?
def getBBCList():
    with open(argv[1], 'r') as file:
        bbcList = file.read().split("\n")
        return bbcList
def getWarList():
    with open(argv[2], 'r') as file:
        warList = file.read().split("\n")
        return warList






### If we have to replace the words then we have also found what we need
####but no because we are using set operators later.

#Let us get our BBC List and War List
bbcList = getBBCList()
warList = getWarList()

#Get all the files in genre folder (this script will be run in each folder)
files = [file for file in os.listdir() if file.endswith(".txt")]
#For each file
for file in files:
    #Try to do the following
    try:
        #Open the file
        with open(file, 'r', encoding = 'utf8') as openedFile:
            #If there's a word in the file that is also in the BBC list and it contains a space...
            if (word in file for word in bbcList) and " " in word:
                #Replace that space with an underscore
                file.replace(" ", "_")
    #If we can't do any of the above just move on and don't crash the program
    except:
        #but make a note of it
        print("Failed to open a file or replace something")
        continue

#seems like a waste of time to search for words we aren't touching


#Search all words from BBC Climate Change List in each genre

    #If a compound word is found it must be replaced with an underscore variant

# So for each file, we re.sub what we want

#Then the word must be changed to its compound variant in the BBC list
#someting to note about sets is a lack of repetition

#Make BBC list and War List into sets
bbcSet = set(bbcList)
warSet = set(warList)
#For each sentence in each genre

    for line in file:
        #Make the sentence a list
        lineList = line.split()
        #then make sentence a set
        lineSet = set(lineList)
        #Check if intersection between bbc list and this set
        #check if intersection between war list and this set
        #If intersections are had with both return that sentence and save to file
        if (lineSet.intersection(bbcSet) and lineSet.intersection(warSet)):
            saveToIntersectionFile(lineSet)
