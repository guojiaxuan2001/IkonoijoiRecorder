from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_driver():
    """创建一个配置好的Chrome WebDriver实例"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_twitter(driver):
    """登录Twitter"""
    try:
        logger.info("Attempting to log in to Twitter...")
        driver.get("https://twitter.com/i/flow/login")
        
        # 获取环境变量中的Twitter凭证
        twitter_username = os.getenv('TWITTER_USERNAME')
        twitter_password = os.getenv('TWITTER_PASSWORD')
        
        if not twitter_username or not twitter_password:
            logger.error("Twitter credentials not found in environment variables")
            return False
        
        # 等待用户名输入框
        wait = WebDriverWait(driver, 20)
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_input.send_keys(twitter_username)
        username_input.send_keys(Keys.RETURN)
        
        # 等待密码输入框
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(twitter_password)
        password_input.send_keys(Keys.RETURN)
        
        # 等待登录完成
        time.sleep(5)
        logger.info("Successfully logged in to Twitter")
        return True
        
    except Exception as e:
        logger.error(f"Failed to log in to Twitter: {e}")
        return False

def fetch_latest_tweets(account, max_retries=3):
    tweets = []
    url = f"https://twitter.com/{account}"
    logger.info(f"Attempting to fetch tweets from {url}")
    
    driver = None
    try:
        driver = create_driver()
        
        # 登录Twitter
        if not login_twitter(driver):
            return []
            
        # 访问目标账号
        driver.get(url)
        
        # 等待推文加载
        wait = WebDriverWait(driver, 20)
        timeline = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]')))
        
        # 滚动几次以加载更多推文
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # 获取所有推文
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
        logger.info(f"Found {len(tweet_elements)} tweets")
        
        for tweet in tweet_elements:
            try:
                # 获取推文文本
                text_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                text = text_element.text
                
                # 获取时间戳
                time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                tweet_time = time_element.get_attribute('datetime')
                
                tweets.append({
                    'account': account,
                    'time': tweet_time,
                    'text': text
                })
                logger.info(f"Found tweet: {text[:50]}...")
                
            except NoSuchElementException as e:
                logger.warning(f"Failed to parse tweet element: {e}")
                continue
                
        logger.info(f"Successfully fetched {len(tweets)} tweets for {account}")
        return tweets
        
    except Exception as e:
        logger.error(f"Error fetching tweets: {e}")
        return []
        
    finally:
        if driver:
            driver.quit()
