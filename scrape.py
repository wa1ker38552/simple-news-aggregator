from bs4 import BeautifulSoup
from ai import add_category
import requests

def scrape_news():
    total_links = []

    # cnn
    print('scraping cnn')
    r = requests.get('https://lite.cnn.com/')
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    links = [{
        'url': 'https://lite.cnn.com'+l.get('href'), 
        'title': l.get_text().strip(), 
        'source': 'cnn'
    } for l in links if l.get('href').strip() != '' and l.get_text().strip() not in ['Cookie Settings', 'Go to the full CNN experience', 'Privacy Policy', 'Ad Choices', 'Terms of Use', 'CNN']]
    total_links.extend(links)

    # npr
    print('scraping npr')
    r = requests.get('https://text.npr.org/')
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'topic-title'})
    links = [{
        'url': 'https://text.npr.org'+l.get('href').strip(),
        'title': l.get_text().strip(),
        'source': 'npr'
    } for l in links]
    total_links.extend(links)

    # daily mail
    print('scraping daily mail')
    r = requests.get('https://www.dailymail.co.uk/textbased/channel-561/index.html')
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    links = [{
        'url': 'https://www.dailymail.co.uk'+l.get('href').strip() if l.get('href') else None,
        'title': l.get_text().strip(),
        'source': 'dailymail'
    } for l in links if (l.get('href') and l.get('href').strip() != '') and l.get_text().strip() not in ['Terms', 'Privacy policy & cookies', 'read', 'Back to Main Site', 'Home', 'Showbiz', 'TV', 'Politics', 'Femail', 'Royals', 'Sports', 'Health', 'Science', 'Money', 'U.K.', 'Video', 'Travel', 'Puzzles', 'Shopping', 'Breaking News', 'US Elections 2024', 'Donald Trump', 'Kamala Harris', 'Joe Biden', 'NFL', 'Diddy', 'Taylor Swift', 'Games', 'For You', 'Poll Tracker']]
    total_links.extend(links)

    # cbc
    print('scraping cbc')
    r = requests.get('https://www.cbc.ca/lite/news', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'contentlist_title__GRPR1'})
    links = [{
        'url': 'https://www.cbc.ca'+l.get('href'),
        'title': l.get_text().strip(),
        'source': 'cbc'
    } for l in links]
    total_links.extend(links)

    # new york times
    print('scraping nyt')
    r = requests.get('https://nytimes.com/timeswire', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'css-8hzhxf'})
    links = [{
        'url': 'https://www.nytimes.com'+l.get('href'),
        'title': l.get_text().strip(),
        'source': 'ny times'
    } for l in links]
    total_links.extend(links)

    # csm
    print('scraping csm')
    r = requests.get('https://www.csmonitor.com/layout/set/text/textedition', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'ezc-csm-story-link'})
    links = [{
        'url': 'https://www.csmonitor.com'+l.get('href'),
        'title': l.get_text().strip(),
        'source': 'csm'
    } for l in links]
    total_links.extend(links)

    # neuters
    print('scraping neuters')
    r = requests.get('https://neuters.de/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    links = [{
        'url': 'https://neuters.de'+l.get('href'),
        'title': l.get_text().strip(),
        'source': 'neuters'
    } for l in links if l.get('href') and l.get_text().strip() not in ['Home', 'Search', 'About', '<', '>']]
    total_links.extend(links)

    # post online
    print('scraping post online')
    r = requests.get('https://lite.poandpo.com/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('div', attrs={'class': 'contentgore'})
    links = content.find_all('a')
    links = [{
        'url': l.get('href'),
        'title': l.get_text().strip(),
        'source': 'post online'
    } for l in links]
    total_links.extend(links)


    categories = ['politics', 'world', 'health', 'science', 'technology', 'other', 'sports', 'finance']
    titles = [l['title'] for l in total_links]

    ri = {}
    i = 0
    while i < len(titles):
        d = add_category(titles[i:i+50], categories)
        d_data = [a.split(' ;; ') for a in d]
        for nc in d_data:
            if len(nc) >= 3:
                ri[nc[0]] = [nc[1], int(nc[2])]
        print('Batching AI', i, len(titles))
        i += 50

    for ln in total_links:
        if ln['title'] in ri:
            ln['category'] = ri[ln['title']][0]
            ln['relevancy'] = ri[ln['title']][1]
        else:
            ln['relevancy'] = 1

    return total_links