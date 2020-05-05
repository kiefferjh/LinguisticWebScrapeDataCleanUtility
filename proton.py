import re
import csv

def writeToFile(mightyList):
    with open('finale.csv', 'w', encoding = 'utf8') as csv_file: #Open a new file to write to
        writer = csv.writer(csv_file) #Establish csv_file as the fie to be written to


        x = 0
        while x < 72:

            list2 = [item[x] for item in mightyList]
            writer.writerow([list2[0], list2[1], list2[2], list2[3], list2[4]]) #The list key and then the value
            print("Row " + str(x) + "Printed")
            x=x+1

def getLink(line):
    lineList = line.split()
    #search for chunk with http
    for word in lineList:
        if "http" in word:
            #print(word)
            return word
        else:
            None
def getIntersection(line):
    #print(line)
    #print(line.split())
    #search for chunk with http
    if line != '':
        s = line
        m = s[s.find("[")+1:s.find("]")]
        if m == '':
            None
        elif m == '[SPACE REPLACED]':
            None
        else:
            #print(m)
            return m
def getGenre(line):
    if line != '':
        if "//NEWS//" in line:
            return "News"
        elif "//JOURNAL//" in line:
            return "Journal"
        elif "//MAGAZINE//" in line:
            return "Magazine"
        elif "//WEB//" in line:
            return "Web"
        else:
            return None

def getText(line):
    if "Intersection:" in line:
        None
    else:
        return line



    #     s = line
    #     #print(s)
    #     m = s[s.find("//")+1:s.find("//")]
    #     print(m)
    #     if m == '':
    #         None
    #     else:
    #         #print(m)
    #         return m

with open('grundle.txt', 'r') as file:
    grundleLines = file.read().split('\n')
    print(len(grundleLines))
httpList = []
intersectionList = []
genreList = []
textList = []
numList = []
#print(lines)
k = 1
for line in grundleLines:

    if getLink(line):
        http = getLink(line)
        httpList.append(http)
    if getIntersection(line):
        intersect = getIntersection(line)
        intersect = intersect.split()
        #print(intersect)
        if len(intersect) < 3:
            intersect = ' / '.join(intersect)
            intersectionList.append(intersect)
    if getGenre(line):
        genre = getGenre(line)
        genreList.append(genre)

        numList.append(k)
        k = k+1

with open('Metaphors_Environment.txt', 'r') as file2:
    boop2 = file2.read().split('\n')
    for line in boop2:
        if getText(line):
            text = getText(line)
            textList.append(text)
mightyList = []

mightyList.append(numList)
mightyList.append(intersectionList)
mightyList.append(httpList)
mightyList.append(genreList)
mightyList.append(textList)


print(len(intersectionList))
print(len(genreList))
print(len(httpList))
print(len(textList))
print(numList)
writeToFile(mightyList)
#with open('https.txt', 'w') as file:
