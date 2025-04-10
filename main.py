from fetcher import fetch_latest_tweets
from analyzer import filter_by_keywords
from exporter import save_to_csv
from following import account

all_matched = []
for acc in account:
    tweets = fetch_latest_tweets(acc)
    matched = filter_by_keywords(tweets)
    all_matched.extend(matched)

if all_matched:
    save_to_csv(all_matched)
    print(f"{len(all_matched)} matched tweets saved.")
else:
    print("No matching tweets found.")