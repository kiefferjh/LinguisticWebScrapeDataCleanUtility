#Citation Changing Script

with open("Citations.txt", 'r') as file:
    readFile = file.read()
readList = readFile.split("\n")

newList = []
for citation in readList:
    newCitation = "//WEB// "
    newCitation += citation
    newList.append(newCitation)

with open("NewCitations.txt", "w") as file:
        for cite in newList:
            file.write(cite + "\n")
