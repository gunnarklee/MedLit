import os
import time
import sys
import string

'''The following will cause the iPython notebook to stop printing within
the document!!  You will still see it in the terminal.  Was the easiest
way to get rid of all the utf-8 encoding errors so I kept it.'''
reload(sys)
sys.setdefaultencoding('utf-8')


'''First step is to walk through our directory to find all the filenames'''
#So we can measure duration
start = time.time()

#What we append to
fileSet = set()

#Just walks through all the files in PMC_Files and appends filenames to fileSet
for dir_, _, files in os.walk("./PMC_Files"):
    for fileName in files:
        relDir = os.path.relpath(dir_, "./")
        relFile = os.path.join(relDir, fileName)
        fileSet.add(relFile)

stop = time.time()
duration = stop - start

print "We have %s total records" %(len(fileSet))
print "This process took %s seconds" %(duration)

from xml.dom import minidom as md
import csv



def removePunctuation(s):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)

def parseXML(data):
    '''Takes XML input and extracts several relevant fields. Note that right now
    this uses a lot of IO, as we write to the csv file for every article.
    Optimization possible.'''
    xmldoc = md.parse(data)

    #Establish basic XML tree structure.  I find this easier to use than ElementTree
    #This allows us to drill down to individual trees later
    jmeta = xmldoc.getElementsByTagName("journal-meta")[0]
    ameta = xmldoc.getElementsByTagName("article-meta")[0]

    #Get journal title
    jtitle = jmeta.getElementsByTagName("journal-title")[0].firstChild.data
    
    #Get Pubmed ID ("pmid"), article title, contributors
    '''Getting the pubmed ID is a little cumbersome. Its not always in the same
    location under article-id so we cant just pull from a direct node. While there
    is a unique type for each ID, I wasnt able to figure out how to select it.
    Pubmed IDs appear to be the only ones that are 8 characters long, so I just
    iterated through IDs instead.  This may cause problems if another ID type
    also has 8 characters and appears before "pmid" - though I didnt see any.'''
    a_id = ameta.getElementsByTagName("article-id")
    for ids in a_id:
        id_val = ids.firstChild.data
        if len(id_val) == 8:
            pubmedID = id_val
            break
    
    #Get Article Title
    '''Theres a problem here - if the journal used italics or bold and its tagged that
    way then it creates a whole separate element, breaking up the normal title flow.
    I tried multiple ways of fixing it but couldnt find any that worked.  As of now
    we simply exclude these from the dataset.  Its a minority of documents for sure, but
    still something I would like to have fixed.  This probably means were biasing
    against certain journals.'''
    atitle = ameta.getElementsByTagName("article-title")[0].firstChild.data
    
    #get the PMC Release year - change to 0 for nihms-submitted and 1 for ppub
    '''Note: given the issue with Pubmed IDs, this may also provide years from other tags.
    I havent researched it to find out.'''
    pubdate = ameta.getElementsByTagName("pub-date")[0]
    year = pubdate.getElementsByTagName("year")[0].firstChild.data
    
    #get contributors
    c_group = ameta.getElementsByTagName("contrib-group")[0]
    contributor = c_group.getElementsByTagName("contrib")
    
    #Open the output file
    outputFile = open("output2.csv",'a')
    wr = csv.writer(outputFile)
    
    #Cycle through to get all contributors
    for person in contributor:
        
        #If element contains names, use those
        try:
            lastname = person.getElementsByTagName("surname")[0].firstChild.data
            firstname = person.getElementsByTagName("given-names")[0].firstChild.data
        
        #Businesses use 'collab' instead of names
        except IndexError:   
            firstname = person.getElementsByTagName("collab")[0].firstChild.data
            lastname=""

        fullname = firstname+" "+lastname              
        
        fullname = removePunctuation(fullname)
        atitle = removePunctuation(atitle)
        pubmedID = removePunctuation(pubmedID)
        jtitle = removePunctuation(jtitle)
        
        #Output
        csvline = [fullname,atitle,pubmedID,jtitle,year]
        wr.writerow(csvline)
    
    #Close output file when for loop completes
    outputFile.close()

'''Takes a LONG time'''
'''HEADS UP - I have an empty "except" argument so we can get through
the entire list in one attempt without stalling every few hours for a
one-off error.  This means that once you start this there is no stopping 
it unless you hard stop the iPython Notebook server (Control-C twice in terminal).
Trying to "Stop Kernel" from within iPython will simply raise the
Unknown Error condition and the script will continue on its merry way.'''

start = time.time()

successes = 0
failures = 0

for n in fileSet:
    
    #Using 'try' helps with debugging issues
    try:
        print n
        parseXML(n)
        successes += 1
    
    #The following catch errors, the most prevalent of which are AttributeErrors
    except IndexError:
        print "IndexError in", n
        failures += 1
    except AttributeError:
        print "AttributeError in", n
        failures += 1
    except:
        print "Unknown Error in", n
        failures += 1
    
    try:
        os.remove("./"+n)
    except:
        print "Failed to remove", n
        
    #Just helps monitor what's happening
    if successes%5000 == 0:
        tempstop = time.time()
        tempduration = (tempstop - start)/60
        print "%s successes, %s failures :: %s minutes" %(successes,failures,tempduration)

stop = time.time()
duration = stop - start

print "Processing completed in %s seconds"  %(duration)
print "output.csv file was generated in the same directory as this python script."
print ""
print "%s successes. %s failures." %(successes, failures)



