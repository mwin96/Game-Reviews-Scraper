from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests
import heapq
import re

url = 'https://noisypixel.net/review/' 
url2 = 'https://store.steampowered.com/explore/new/' 
url3 = 'https://www.destructoid.com/products-index.phtml?filt=reviews&date_s=desc&category='

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

urlSet = grabLinks(url3)
greatReviews = []
ownedConsoles = {'PC','PS4','Switch','Mobile','iOS'}

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
                    tmpReviews['Score:'] = revws.text
                    upTo = revws.text.index('/')        #We want to store the float value of the score for sorting purposes
                    tmpReviews['floatScore:'] = float(revws.text[:upTo])
                else:
                    tmpReviews[revws.text] = revws.next_sibling
            splitTags = a.replace('/','').split('-')
            tmpReviews['Consoles I own:'] =''
            for console in ownedConsoles:
                # cons = console.replace('/','') #Sometimes a / can be attached to the tag
                # print(cons)
                if console in splitTags:
                    if tmpReviews['Consoles I own:'] != '':   #If something already exists, add a comma and space
                        tmpReviews['Consoles I own:'] += ', ' + console
                    else:
                        tmpReviews['Consoles I own:'] += console
            # print(test)
            greatReviews.append(tmpReviews)

def grabSteamReviews():
    '''Pulls back game reviews from Steam new releases page.'''

    count = 0 
    for a in urlSet:
        if 'app' in a: #'app' is the notation steam uses to link to an application  

            tmpReviews = {} #Store info for each review in dictionary 
            
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
            
                tmpReviews['Link:'] = a
                tmpReviews['Title:'] = appName
                tmpReviews['Developer:'] = appDev.strip()
                # print('x', appDev.strip())
                tmpReviews['Release Date:'] = releasedDate
                if not scoreToNum.get(appScore):    #Situation where not enough user reviews to generate a score
                    tmpReviews['Score:'] = 'None available yet'
                    tmpReviews['floatScore:'] = 0
                else:
                    tmpReviews['Score:'] = appScore
                    tmpReviews['floatScore:'] = scoreToNum.get(appScore)
                tmpReviews['Consoles I own:'] = 'PC' #Hardcoding pc since this is Steam

                # print(appName)

                # print(appName)
                # print(releasedDate)
                # print(appScore)

                greatReviews.append(tmpReviews)
                
def grabDestructoidReviews():
    '''Pulls back reviews from Destructoid'''
    for a in urlSet:
        if isinstance(a,str) and 'stories/review' in a:
            fullURL = 'https://www.destructoid.com/' + a        

            reviewUrl = requests.get(fullURL)
            reviewData = reviewUrl.text
            reviewSoup = BeautifulSoup(reviewData,'html.parser')

            developer = reviewSoup.find(text=re.compile('Developer:'))
            publisher = reviewSoup.find(text=re.compile('Publisher:'))
            released = reviewSoup.find(text=re.compile('Released:'))
            if released:
                releaseDate = released.split(' ')[1:4] #Destructoid groups dates and consoles, I need to split them up
                cleanUp = released.replace('(','').replace(')','')
                print(cleanUp)
                # for items in released:
                #     if 
                # if releaseDate: 
                #     print(releaseDate)
                # print(developer,publisher,released)
        # for revws in reviewSoup.find_all('strong'): #Important info on this site happens to be identified with <strong> tags
        #     print(revws)
            # print(test)
            # tmpReviews = {} #Store info for each review in dictionary 
            # print('w')
            # # reviewUrl = requests.get(a)
            # reviewData = reviewUrl.text
            # reviewSoup = BeautifulSoup(reviewData,'html.parser')
            # print(test)
            # tmpReviews['Review Link:'] = a

            # for revws in reviewSoup.find_all('strong'): #Important info on this site happens to be identified with <strong> tags
            


# grabSteamReviews()
# grabNoisyPixelReviews()
grabDestructoidReviews()



def printReviews(dic):
    '''Prints out games and scores. '''

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
