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
google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
logger.info(f"环境变量内容：用户名='{twitter_username}'")
logger.info(f"Google认证文件路径: {google_creds}")

def main():
    # 获取所有账号的推文
    all_tweets = fetch_tweets_for_accounts(account)
    
    logger.info(f"总共获取到 {len(all_tweets)} 条推文")
    
    logger.info("\n获取到的所有推文内容：")
    for tweet in all_tweets:
        logger.info(f"\n账号: {tweet['account']}")
        logger.info(f"时间: {tweet['time']}")
        logger.info(f"内容: {tweet['text']}")
        logger.info("包含的关键词：")
        for keyword in keywords:
            if keyword in tweet['text']:
                logger.info(f"- {keyword}")
        logger.info("-" * 50)
    
    # 筛选匹配关键词的推文
    matching_tweets = []
    for tweet in all_tweets:
        matched_keywords = [k for k in keywords if k in tweet['text']]
        if matched_keywords:
            matching_tweets.append(tweet)
            logger.info(f"\n找到匹配关键词的推文：")
            logger.info(f"账号: {tweet['account']}")
            logger.info(f"关键词: {matched_keywords}")
            logger.info(f"内容: {tweet['text'][:100]}...")
    
    if matching_tweets:
        logger.info(f"\n准备导出 {len(matching_tweets)} 条匹配的推文")
        if save_to_csv(matching_tweets):
            logger.info(f"成功导出 {len(matching_tweets)} 条推文")
        else:
            logger.error("导出推文失败")
    else:
        logger.info("\n未找到匹配的推文")

if __name__ == "__main__":
    main()