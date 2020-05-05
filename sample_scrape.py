#Sample Program for Web Scraping
### THIS IS VERY MUCH A PROTOTYPE ###
#Kieffer Higgins 2019

##########################################
#WHAT THIS PROGRAM DOES
    #This program searches the web for various search terms,
    #then pulls pages relating to those terms and cleans the page data,
    #Saving the data to an individual / per page text file and then,
    #writing the URL and the title of the text document to a citations document
##########################################

##########################################
#Argument Values and Calling the program:
####
    # use is: "py sample_scrape.py search_terms.txt 4" - where 4 is how many results to pull per search
    ### ARGV[1] = Search Terms file ## It is impportant not to leave blank lines in the search terms file!!
    ### ARGV[2] = Number of Google Results to Pull for Each Term
    ######## In planning
    ### ARGV[3] = Could choose output directory?
    ### ARGV[4] = Choose name of citation file
###########################################

###########################################
#When Using the Program Keep in mind:

### Make sure that each text file is opened with notepad ++

###########################################
##Things I might still wanna do:
## still need to find a way to save the address as first part of the document
## Do argv checking and help
##Perhaps sentences of less than a certain length should be omitted? Hard to clean for random stuff
############################################

#############################################
#IMPORTS
############################################
#Lets import some things we will likely need:
##############################################
#unused as of right  now
#import numpy as np
#import pandas as pd

#used to clean the data
import re
import unicodedata
import inflect

#Used to make this program more robust and convenient
from sys import argv
#Used to open URLS
from urllib.request import urlopen
#Used to Parse HTML
from bs4 import BeautifulSoup
#Google is used to search
#This helps to know what error we are having if we are unable to import google
try:
    #Used to get links from a google search for each search term
    from googlesearch import search
except ImportError:
    print("Was unable to import Google :( ")
#String is used to manipulate strings
import string
#import requests
###############################################


###############################################################
#Methods:
###############################################################

###############
## Cleaning:
###############
#This functions goal is to return a new paragraph where each sentence is on its own line
def format_sentence(paragraph) :
    #We filter out by splitting at each period
    sentenceSplit = filter(None, paragraph.split("."))
    #We create a new paragrah to write to
    newParagraph = ''
    #For each object in our filter...
    for s in sentenceSplit :
        #We add to the new paragraph and replace the period that we split at
        #as well as adding a newline char, so that each sentence is on its own line
         newParagraph += (s.strip() ) + '\n' #at one point I was adding the periods back in but we don't need that


    #we then return our paragraph for use later on
    return newParagraph
#This method uses regular expressions to clean our paragraphs of HTML Tags
def cleanhtml(raw_html):
    #Creates an RE of anything surrounded by HTML tags
  cleanr = re.compile('<.*?>')
  #Replaces every instance of those with nothing (cleaning them out)
  cleantext = re.sub(cleanr, '', raw_html)
  #Returns text free of HTML Garbage
  return cleantext
def cleanCitation(text):
    cleanr = re.compile('[.*?]')
    cleanerText = re.sub(cleanr,'',text)
    return cleanerText


# I don't like this...
def removePunctuation(text):
    text = re.sub(r'[^\w\s]','',text)
    return text

#We may not need to use this function yet

# def removeNotASCII(words):
#     new = []
#     for word in words:
#         new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8','ignore')
#         new.append(new_word)
#     return new
#

#It would be better to do this REGEX due to string spacing, etc.
# def make_lowercase(words):
#     new = []
#     for word in words:
#          new_word = word.lower()
#          new.append(new_word)
#     return new

# #We don't need to use this function yet either
# #I'm not sold on the efficiency of this function
# def replace_numbers(words):
#     x = inflect.engine()
#     new = []
#     for word in words:
#         if word.isdigit():
#             new_word = x.number_to_words(word)
#             new.append(new_word)
#         else:
#             new.append(new_word)
#     return new

#####################
#Searching and Page Acquisition
#####################
#This is my search method it returns a list of links matching a keyword
def googs(query):
    #Created a list for our search results
    searchResults =[]
    #For each item that Google has returned for our query, we add it to the list, with a brief pause not to overload googles servers
        #and we are trying to get a certain "num" of results per search
    numToSearch = int(argv[2])

    for k in search(query, tld="com",num=numToSearch,stop= 20, pause = 7):
        searchResults.append(k)
    return searchResults
#Now we need to accept a link and use BeautifulSoup to extract HTML
def getHTML(url):
    try:
        #We try to open a specific HTML
        html = urlopen(url)
        #And pass it into a BeautifulSoup constructor
        soup = BeautifulSoup(html, 'html.parser')
        #soup = soup.encode("utf-8") ##Sometimes Strangely Useful, Usually Left Turned Off.
        #We then return the Soup for later use
        return soup
    except :
        #If we can't open the page we say so in the CMD line and we Return None
        print("A page couldn't be opened: " + str(url))
        return None
#Now we get text from Soup!
def pageText(pageSoup):
    #We create an empty string
    text = ''
    try:
        ################# WE NEED TO CAPUTRE OTHER TAGS HERE TOO. Try <a href> ?
        #For each tag in our BeautifulSoup we find all the paragraphs
        for tag in pageSoup.findAll('p'):

            # for child in tag.children:
            #     if child ==
            #     print(child)
            # #We then convert each paragraph to a string (adding a new line for each one and add it to the text)
            text = text + (str(tag) + '\n')
        return text
    except:
        print("NoneType Error Potentially Page Was Blank or 404 Error")
        return None
#List of search terms is opened from a file
def getSearchTerms():
    #We get our list of search terms as a file specified in CMD line
    searchTerms = argv[1]
    #We open the file and read each search term returning them to a list
    with open(searchTerms, "r") as file: #gotta be in the same directory as this file
        terms = file.read().split('\n')
    return terms
######################################################################
#Main Program
######################################################################
#To initiate the program we get our searchTerms from file
terms = getSearchTerms()
#For each term...
for term in terms:
    #We return a list of websites from a Google Search
    results = googs(term)
    #This is a counter for each article for a specific search term
    i = 0
    #For each result Google returned...
    for result in results:
        #If we cannot open the page for the result:
        if getHTML(result) == None:
            #Go back to the next result and ignore the rest of the loop
            continue
        #If we can open it...
        else:
            #If the page is blank or corrupted we don't want to crash this program so we ignore rest of loop
            if pageText(getHTML(result)) == None:
                continue
            #We extract the main text from the page
            text = pageText(getHTML(result))
            try:
                #We clean it of HTML tags
                text = cleanhtml(text)
            except:
                continue
            #We clean the text of citation like [] characters commonly found in Wikipedia articles
            text = cleanCitation(text)

            text = format_sentence(text)

            text = removePunctuation(text)


            #We encode the text in a format that we can write a file with
            text = text.encode("utf-8")
            #We open a file based on the search term and the result
            with open('dump (%s) (%d).txt' % (term,i), 'wb') as file:
                #and we write our text to the file
                file.write(text)
                #Then increasing our counter for next time
                i += 1
            #Let's save the link for this file
            with open ("Citations.txt", 'a') as file2:
                file2.write('(%s) (%d)' % (term,i) + ' ')
                file2.write(result + "\n")
print("All done!")



















#### DEPRECEATED STUFF:

##Let's try using THIS
##pageSoup = getHTML('https://en.wikipedia.org/wiki/Environmental_science')
#print(pageSoup.get_text())


#tables = page.find_all('table')
#for table in tables:
#    print(table.prettify())



################ Stuff  I tried using in the page text function
    #text = pageSoup.get_text()
    ########text = pageSoup.find('p')
    #for strong_tag in pageSoup.find_all('strong'):
    #    print (strong_tag.text, strong_tag.next_sibling)
    #for strong_tag in pageSoup.find_all('p'):
    #    print (strong_tag.text, strong_tag.next_sibling)
    #print (pageSoup.text)
    #text = pageSoup.find(text=True)
    #print(text)
    #VALID_TAGS = ['div', 'p']


    ################# Was trying to remove punctuation
    #table = str.maketrans('', '', string.punctuation)
    #words = text.split()
    #punctFree = [k.translate(table) for k in words]
    #noPunctString = ''.join(punctFree)

    #noPunctString = text.strip(string.punctuation) doesn't do enough....
    #words = text.split()
    #return ' '.join(word.strip(string.punctuation) for word in words)
