import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
import random

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def random_sleep(min_seconds=1, max_seconds=3):
    base_sleep = random.uniform(min_seconds, max_seconds)
    extra_sleep = random.uniform(0, 1) if random.random() < 0.3 else 0
    time.sleep(base_sleep + extra_sleep)

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument(f'--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login_twitter(driver, max_retries=3):
    for attempt in range(max_retries):
        try:
            logger.info(f"正在尝试登录Twitter... (第 {attempt + 1} 次尝试)")
            driver.get("https://twitter.com/i/flow/login")
            random_sleep(8, 12)  
            
            # 获取环境变量中的Twitter凭证
            twitter_username = os.getenv('TWITTER_USERNAME')
            twitter_password = os.getenv('TWITTER_PASSWORD')
            
            if not twitter_username or not twitter_password:
                logger.error("未在环境变量中找到Twitter凭证")
                return False
                
            logger.info(f"正在使用账号 {twitter_username} 登录...")
            wait = WebDriverWait(driver, 45)  
            
            try:
                username_input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
                )
                random_sleep(3, 5)
                username_input.clear()
                username_input.send_keys(twitter_username)
                random_sleep(2, 3)
                username_input.send_keys(Keys.RETURN)
                
                # 等待密码输入框
                logger.info("正在等待密码输入框...")
                password_input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
                )
                random_sleep(3, 5)
                password_input.clear()
                password_input.send_keys(twitter_password)
                random_sleep(2, 3)
                password_input.send_keys(Keys.RETURN)
                
                # 等待登录完成
                logger.info("正在等待登录完成...")
                random_sleep(10, 15)  

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]')))
                    logger.info("登录成功！")
                    return True
                except TimeoutException:
                    if attempt < max_retries - 1:
                        logger.warning("登录验证失败，准备重试...")
                        continue
                    else:
                        logger.error("登录验证失败 - 无法找到主栏")
                        return False
                    
            except TimeoutException as e:
                if attempt < max_retries - 1:
                    logger.warning(f"等待元素超时，准备重试: {e}")
                    continue
                else:
                    logger.error(f"等待元素超时: {e}")
                    return False
            except NoSuchElementException as e:
                if attempt < max_retries - 1:
                    logger.warning(f"未找到元素，准备重试: {e}")
                    continue
                else:
                    logger.error(f"未找到元素: {e}")
                    return False
                
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"登录过程中出错，准备重试: {e}")
                continue
            else:
                logger.error(f"登录Twitter失败: {e}")
                return False
                
    return False

def fetch_tweets_for_accounts(accounts):
    driver = None
    all_tweets = []
    
    try:
        driver = create_driver()
        
        # 只登录一次
        if not login_twitter(driver):
            logger.error("登录失败，无法获取推文")
            return []
            
        for account in accounts:
            try:
                tweets = fetch_tweets_for_account(driver, account)
                all_tweets.extend(tweets)
            except Exception as e:
                logger.error(f"获取账号 {account} 的推文时出错: {e}")
                continue
                
        return all_tweets
        
    except Exception as e:
        logger.error(f"获取推文过程中出错: {e}")
        return []
        
    finally:
        if driver:
            driver.quit()

def fetch_tweets_for_account(driver, account):
    url = f"https://twitter.com/{account}"
    logger.info(f"正在获取账号 {account} 的推文...")
    try:
        driver.get(url)
        random_sleep(8, 12)
        wait = WebDriverWait(driver, 30)
        timeline = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]')))
        processed_tweet_texts = set()
        processed_tweets = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        max_scrolls = 5
        scroll_count = 0
        while scroll_count < max_scrolls:
            scroll_count += 1
            logger.info(f"第 {scroll_count}/{max_scrolls} 次滚动")
            tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            logger.info(f"当前页面找到 {len(tweet_elements)} 条推文")
            for tweet in tweet_elements:
                try:
                    text = tweet.text.strip()
                    if not text or text in processed_tweet_texts:
                        continue
                    processed_tweet_texts.add(text)
                    logger.info(f"抓到推文: {text.replace(chr(10), ' ')[:100]}...")
                    try:
                        time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                        tweet_time = time_element.get_attribute('datetime')
                    except NoSuchElementException:
                        tweet_time = datetime.now().isoformat()
                    processed_tweets.append({
                        'account': account,
                        'time': tweet_time,
                        'text': text
                    })
                except Exception as e:
                    logger.warning(f"处理推文时出错: {e}")
                    continue
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep(3, 5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logger.info("没有新内容加载，提前结束滚动")
                break
            last_height = new_height
        logger.info(f"成功获取到 {len(processed_tweets)} 条推文 (来自 {account})")
        return processed_tweets
    except Exception as e:
        logger.error(f"获取推文时出错: {e}")
        return []
