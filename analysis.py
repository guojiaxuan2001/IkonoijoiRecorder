from following import keywords

def filter_by_keywords(tweets):
    result = []
    for tweet in tweets:
        text = tweet["text"]
        if any(kw in text for kw in keywords):
            result.append(tweet)
    return result