from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests
import re

url = 'https://noisypixel.net/review/' 
url2 = 'https://store.steampowered.com/explore/new/' 
url3 = 'https://www.destructoid.com/products-index.phtml?filt=reviews&date_s=desc&category='

urlDict = {
    'noisypixel': url,
    'steam':url2,
    'destructoid':url3
}

ownedConsoles = {'PC','PS4','Switch','Mobile','iOS'}


def grabLinks(currUrl):
    '''Returns a set of game review URL's.''' 

    r = requests.get(currUrl)
    data = r.text
    soup = BeautifulSoup(data,'html.parser')
    urlList = []
    for link in soup.find_all('a'):
        urlList.append(link.get('href')) #Grab links in the review page
    linkSet = set(urlList) #Set to remove any duplicates
    return linkSet


def grabNoisyPixelReviews():
    '''Pulls back recently released Noisy Pixel reviews.'''

    for a in urlSet:
        if '-review-' in a and (console in a for console in ownedConsoles) and not a.endswith('#respond'): #I want reviews in consoles I own
            
            tmpReviews = {} #Store info for each review in dictionary 

            reviewUrl = requests.get(a)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')

            tmpReviews['Review Link:'] = a

            for revws in reviewSoup.find_all('strong'): #Important info on this site happens to be identified with <strong> tags
           
                if '/10' in revws.text:
                    tmpReviews['Score: '] = revws.text
                    upTo = revws.text.index('/')        #We want to store the float value of the score for sorting purposes
                    tmpReviews['floatScore: '] = float(revws.text[:upTo])
                else:
                    tmpReviews[revws.text] = revws.next_sibling.lstrip()
            splitTags = a.replace('/','').split('-')
            tmpReviews['Consoles I own: '] =''
            for console in ownedConsoles:
                if console.lower() in splitTags:
                    if tmpReviews['Consoles I own: '] != '':   #If something already exists, add a comma and space
                        tmpReviews['Consoles I own: '] += ', ' + console
                    else:
                        tmpReviews['Consoles I own: '] += console

            tempSplit = tmpReviews['Release Date:'].split()
            releasedDate = datetime.strptime(''.join(tempSplit),'%B%d,%Y')
            oneWeek = datetime.today() - timedelta(days=7)                 
            if releasedDate > oneWeek:
                greatReviews.append(tmpReviews)

def grabSteamReviews():
    '''Pulls back game reviews from Steam new releases page.'''

    count = 0 
    for a in urlSet:
        if 'app' in a: #'app' is the notation steam uses to link to an application  

            reviewUrl = requests.get(a)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')
            tmpDate = reviewSoup.find('div',class_ = 'date')
            tmpScore = reviewSoup.find('span',class_ = 'game_review_summary')
            if tmpScore and tmpDate:  #If it can not find a scoer and released date, it's not a game review link
                releasedDate = datetime.strptime(tmpDate.text,'%b %d, %Y') #Date time calculations
                oneWeek = datetime.today() - timedelta(days=7)
            else:
                continue
            if releasedDate > oneWeek:
                appScore = tmpScore.text
                appName = reviewSoup.find('div',class_ = 'apphub_AppName').text
                appDev = reviewSoup.find('div',attrs= {'class':'summary column', 'id':'developers_list'}).text
                releasedDate = releasedDate.date().strftime('%B %d, %Y')

                scoreToNum = {           #Conversions, used for sorting steam reviews
                    'Overwhelmingly Positive': 10,
                    'Very Positive': 9,
                    'Mostly Positive': 8,
                    'Positive': 7,
                    'Mixed': 6,
                    'Negative': 5,
                    'Mostly Negative': 4,
                    'Very Negative': 3,
                    'OverWhelmingly Negative': 2
                }

                tmpReviews = {} #Store info for each review in dictionary 
                tmpReviews['Link: '] = a
                tmpReviews['Title: '] = appName
                tmpReviews['Developer: '] = appDev.strip()  
                tmpReviews['Release Date: '] = releasedDate
                if not scoreToNum.get(appScore):    #Situation where not enough user reviews to generate a score
                    tmpReviews['Score: '] = 'None available yet'
                    tmpReviews['floatScore: '] = 0
                else:
                    tmpReviews['Score: '] = appScore
                    tmpReviews['floatScore: '] = scoreToNum.get(appScore)
                tmpReviews['Consoles I own: '] = 'PC' #Hardcoding pc since this is Steam

                greatReviews.append(tmpReviews)
                
def grabDestructoidReviews():
    '''Pulls back reviews from Destructoid'''
   
    for a in urlSet:
        if isinstance(a,str) and 'stories/review' in a:
            fullURL = 'https://www.destructoid.com/' + a        

            reviewUrl = requests.get(fullURL)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')

            for revws in reviewSoup.find_all('p'): 
                if 'Released' in revws.text and 'Developer' in revws.text:
                    gameName = revws.text[:revws.text.index('(')]
                    reviewedOn = revws.text[revws.text.index('('):revws.text.index('Developer')]
                    developer = revws.text[revws.text.index('Developer')+11:revws.text.index('Publisher')]
                    released = revws.text[revws.text.index('Released')+10:revws.text.index('MSRP')]
                    score = reviewSoup.find('div', class_ = 'gscore')
                    if developer and released and score:
                        try:
                            releasedDate = datetime.strptime(released[:released.index('(')-1],'%B %d, %Y') #Date time calculations
                        except ValueError:
                            pass
                        try:
                            releasedDate = datetime.strptime(released,'%B %d, %Y')
                        except ValueError:
                            break

                        oneWeek = datetime.today() - timedelta(days=7)
                        if releasedDate > oneWeek:   
                            tmpReviews = {} #Store info for each review in dictionary 
                            tmpReviews['Link: '] = fullURL
                            tmpReviews['Title: '] = gameName
                            tmpReviews['Developer: '] = developer
                            tmpReviews['Release Date: '] = releasedDate.date().strftime('%B %d, %Y')
                            tmpReviews['Score: '] = score.text
                            tmpReviews['floatScore: '] = float(score.text)

                            tmpReviews['Consoles I own: '] = ''
                            consoleList = reviewedOn.replace('(','').replace(')','').replace('[reviewed]','').replace(',','').split(' ')
                            lowerCaseConsole = set()
                            for x in consoleList:
                                lowerCaseConsole.add(x.lower())   #lowercase console names for uniformity 

                            for console in ownedConsoles:
                                if console.lower() in lowerCaseConsole:
                                    if tmpReviews['Consoles I own: '] != '':   #If something already exists, add a comma and space
                                        tmpReviews['Consoles I own: '] += ', ' + console
                                    else:
                                        tmpReviews['Consoles I own: '] += console

                            greatReviews.append(tmpReviews)

def printReviews(dic):
    '''Prints out games and scores. '''

    sortedReviews = sorted(dic, key = lambda k: k['floatScore: '], reverse=True) #Sort by float value
    for review in sortedReviews:
        currScore = review['Score: ']
        noPrint = {'floatScore: ','Publisher: ', 'Reviewed On: '} #Valid tags, but not really things that matter to me 
        for values in review:
            if values not in noPrint:
                print(values,review[values])
        print('\n')

for urls in urlDict:
    urlSet = grabLinks(urlDict[urls])
    if urls == 'noisypixel':
        greatReviews = []
        grabNoisyPixelReviews()
        if len(greatReviews) > 0:
            print('-----Noisy Pixel Reviews-----\n')
            printReviews(greatReviews)
    if urls == 'destructoid':
        greatReviews = []
        grabDestructoidReviews()
        if len(greatReviews) > 0:
            print('-----Destructoid Reviews-----\n')
            printReviews(greatReviews)
    if urls == 'steam':
        greatReviews = []
        grabSteamReviews()
        if len(greatReviews) > 0:
            print('-----Steam Reviews-----\n')
            printReviews(greatReviews)
