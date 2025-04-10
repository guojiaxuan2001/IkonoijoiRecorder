import requests
from bs4 import BeautifulSoup
from following import nitterBase
from following import accounts


def fetch_latest_tweets(account):
    url = f"{nitterBase}/{account}"
    respouse = requests.get(url)
    soup = BeautifulSoup(respouse.text, 'html.parser')
    tweets = []

    for item in soup.select('.timeline-item'):
        text = item.select_one('.tweet-content').get_text(strip = True)
        time = item.select_one('span.tweet-date a')['title']

        tweets.append({''})

        return tweets
