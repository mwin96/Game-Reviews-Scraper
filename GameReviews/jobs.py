from schedule import Scheduler
import threading
import time
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests
from .models import Reviews

# from celery.schedules import crontab
# from celery.decorators import periodic_task
# from celery.task import periodic_task


def run_continuously(self, interval=86400):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    #86400 seconds in a day 
    #Interval is in seconds 
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def scraper():
    print('Starting scraper')
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

                tmpReviews['Link: '] = a

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
                    tmpReviews['Site: '] = 'Steam'
                    tmpReviews['Link: '] = a
                    tmpReviews['Title: '] = appName
                    tmpReviews['Developer: '] = appDev.strip()  
                    tmpReviews['Release Date: '] = releasedDate.date()
                    if not scoreToNum.get(appScore):    #Situation where not enough user reviews to generate a score
                        tmpReviews['Score: '] = 0
                        tmpReviews['floatScore: '] = 0
                        tmpReviews['SteamReview: '] = 'N/A'
                    else:
                        tmpReviews['Score: '] = scoreToNum.get(appScore)
                        tmpReviews['floatScore: '] = scoreToNum.get(appScore)
                        tmpReviews['SteamReview: '] = appScore
                    tmpReviews['Consoles I own: '] = 'PC' #Hardcoding pc since this is Steam
                    
                    duplicate = False
                    for i in greatReviews:
                        if i['Site: '] == tmpReviews['Site: '] and i['Title: '] == tmpReviews['Title: ']: #Prevents duplicates from same site
                            duplicate = True

                    if duplicate == False:
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
                                tmpReviews['Site: '] = 'Destructoid'
                                tmpReviews['Link: '] = fullURL
                                tmpReviews['Title: '] = gameName
                                tmpReviews['Developer: '] = developer
                                tmpReviews['Release Date: '] = releasedDate.date()
                                tmpReviews['Score: '] = score.text
                                tmpReviews['floatScore: '] = float(score.text)
                                tmpReviews['SteamReview: '] = ''

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
                                
    def save_function(gameReviews):
        print('Starting database insertion')
        Reviews.objects.all().delete() #Delete all current reviews since we are refreshing our data if we're calling this function

        new_count = 0
        sortedReviews = sorted(gameReviews, key = lambda k: k['floatScore: '], reverse=True) #Sort by float value
        
        for review in sortedReviews:
            try:
                Reviews.objects.create(
                    website = review['Site: '],
                    link = review['Link: '],
                    title = review['Title: '],
                    developer = review['Developer: '],
                    releaseDate = review['Release Date: '],
                    score = review['Score: '],
                    steamReview = review['SteamReview: '],
                    consoles = review['Consoles I own: ']
                    # consoles = review['floatScore: ']
                )
                new_count += 1
            except Exception as e:
                print('Failed at latest_article is none')
                print(e)
                break
        return print('Finished')

    anotherTmpSTRING = ''
    for urls in urlDict:
        urlSet = grabLinks(urlDict[urls])
        if urls == 'noisypixel':
            greatReviews = []
            # grabNoisyPixelReviews()
            # if len(greatReviews) > 0:
            #     anotherTmpSTRING += '-----Noisy Pixel Reviews-----\n'
            #     anotherTmpSTRING += printReviews(greatReviews)
            #     anotherTmpSTRING += '\n'
        if urls == 'destructoid':
            grabDestructoidReviews()
        
        if urls == 'steam':
            grabSteamReviews()
            # pass
    print('Finished scraping')
    return save_function(greatReviews)


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(scraper)
    scheduler.run_continuously()