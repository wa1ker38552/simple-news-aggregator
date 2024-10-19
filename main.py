from scrape import scrape_news
from flask import render_template
from threading import Thread
from flask import Flask
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

def relative_time(timestamp):
    timestamp = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    difference = relativedelta(now, timestamp)

    if difference.years > 0:
        return f"{difference.years} year(s) ago"
    elif difference.months > 0:
        return f"{difference.months} month(s) ago"
    elif difference.days > 0:
        return f"{difference.days} day(s) ago"
    elif difference.hours > 0:
        return f"{difference.hours} hour(s) ago"
    elif difference.minutes > 0:
        return f"{difference.minutes} minute(s) ago"
    else:
        return "just now"

def update_news():
    global news, last_updated
    news = scrape_news()
    news = sorted(news, key=lambda x: x['relevancy'], reverse=True)
    last_updated = time.time()

news = scrape_news()
news = sorted(news, key=lambda x: x['relevancy'], reverse=True)
last_updated = time.time()
app = Flask(__name__)


@app.route('/')
def app_index():
    if time.time()-last_updated > 3600:
        Thread(target=update_news).start()
    return render_template('index.html', news=news, last_updated=relative_time(last_updated))

app.run(host='0.0.0.0', port=6969, debug=True)