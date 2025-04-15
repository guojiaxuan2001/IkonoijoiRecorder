import requests
from bs4 import BeautifulSoup
from following import nitterBase, account
import time
from datetime import datetime

def fetch_latest_tweets(account, max_retries=3):
    url = f"{nitterBase}/{account}"
    tweets = []
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for item in soup.select('.timeline-item'):
                try:
                    text = item.select_one('.tweet-content').get_text(strip=True)
                    time_element = item.select_one('span.tweet-date a')
                    tweet_time = time_element['title'] if time_element else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    tweets.append({
                        'account': account,
                        'time': tweet_time,
                        'text': text
                    })
                except Exception as e:
                    print(f"Error parsing tweet: {e}")
                    continue
            
            return tweets
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                print(f"Failed to fetch tweets for {account} after {max_retries} attempts")
                return []
