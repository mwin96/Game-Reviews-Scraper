from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests
import heapq

url = 'https://noisypixel.net/review/' 
url2 = 'https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&os=win&filter=popularnew'

def grabLinks(currUrl):
    r = requests.get(currUrl)
    data = r.text
    soup = BeautifulSoup(data,'html.parser')
    urlList = []
    for link in soup.find_all('a'):
        urlList.append(link.get('href')) #Grab links in the review page
    linkSet = set(urlList) #Set to remove any duplicates
    return linkSet

urlSet = grabLinks(url2)
greatReviews = []
ownedConsoles = {'pc','ps4','switch','mobile','ios'}

def grabNoisyPixelReviews():
    for a in urlSet:
        if '-review-' in a and (console in a for console in ownedConsoles) and not a.endswith('#respond'): #I want reviews in consoles I own
            
            tmpReviews = {} #Store info for each review in dictionary 

            reviewUrl = requests.get(a)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')

            tmpReviews['Review Link:'] = a

            for revws in reviewSoup.find_all('strong'): #Important info on this site happens to be identified with <strong> tags
                
                if '/10' in revws.text:
                    tmpReviews['Score:'] = revws.text
                    upTo = revws.text.index('/')        #We want to store the float value of the score for sorting purposes
                    tmpReviews['floatScore:'] = float(revws.text[:upTo])
                else:
                    tmpReviews[revws.text] = revws.next_sibling
            splitTags = a.replace('/','').split('-')
            tmpReviews['For consoles I own:'] =''
            for console in ownedConsoles:
                # cons = console.replace('/','') #Sometimes a / can be attached to the tag
                # print(cons)
                if console in splitTags:
                    if tmpReviews['For consoles I own:'] != '':   #If something already exists, add a comma and space
                        tmpReviews['For consoles I own:'] += ', ' + console
                    else:
                        tmpReviews['For consoles I own:'] += console
            # print(test)
            greatReviews.append(tmpReviews)

def grabSteamReviews():
    count = 0 
    for a in urlSet:
        if 'app' in a: #I want reviews in consoles I own   
            # tmpReviews = {} #Store info for each review in dictionary 
            
            reviewUrl = requests.get(a)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')
            tmpDate = reviewSoup.find_all('div',class_ = 'date')
            if len(tmpDate) > 0:
                reviewDate = datetime.strptime(tmpDate[0].text,'%b %d, %Y') #Date time calculations
                oneWeek = datetime.today() - timedelta(days=7)
            else:
                continue

            if reviewDate > oneWeek:
                reviewDate = reviewDate.date().strftime('%B %d, %Y')
                appName = reviewSoup.find_all('div',class_ = 'apphub_AppName')
                appScore = reviewSoup.find_all('span',class_ = 'game_review_summary positive')
                for name,score in zip(appName,appScore):
                    print(name.text,':',score.text)
                    print('Reviewed on:',reviewDate)
                

grabSteamReviews()
# grabNoisyPixelReviews()


def printReviews(dic): #Print out games and scores 
    for review in dic:
        currScore = review['Score:']
        noPrint = {'floatScore:','Publisher:', 'Reviewed On:'} #Valid tags, but not really things that matter to me 
        for values in review:
            if values not in noPrint:
                print(values,review[values])
        print('\n')

if len(greatReviews) > 0:
    sortedReviews = sorted(greatReviews, key = lambda k: k['floatScore:']) #Sort by float value
    printReviews(sortedReviews)
