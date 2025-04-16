from dotenv import load_dotenv
import os
import logging
from following import account, keywords
from fetcher import fetch_tweets_for_accounts
from export import save_to_csv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 验证环境变量
twitter_username = os.getenv('TWITTER_USERNAME')
twitter_password = os.getenv('TWITTER_PASSWORD')
logger.info(f"环境变量内容：用户名='{twitter_username}'")  # 不要打印密码

def main():
    # 获取所有账号的推文
    all_tweets = fetch_tweets_for_accounts(account)
    
    # 筛选匹配关键词的推文
    matching_tweets = []
    for tweet in all_tweets:
        if any(keyword in tweet['text'] for keyword in keywords):
            matching_tweets.append(tweet)
    
    if matching_tweets:
        if save_to_csv(matching_tweets):
            logger.info(f"成功导出 {len(matching_tweets)} 条推文")
        else:
            logger.error("导出推文失败")
    else:
        logger.info("未找到匹配的推文")

if __name__ == "__main__":
    main()