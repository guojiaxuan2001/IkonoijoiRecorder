from following import keywords

def filter_by_keywords(tweets):
    result = []
    for tweet in tweets:
        text = tweet["text"].lower()  # 转换为小写以进行大小写不敏感匹配
        if any(kw.lower() in text for kw in keywords):
            result.append(tweet)
    return result