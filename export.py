import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def test_google_sheet():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    logger.info(f"[TEST] Credentials path: {cred_path}")
    if not cred_path or not os.path.exists(cred_path):
        logger.error("[TEST] Google credentials file not found!")
        return False
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
        client = gspread.authorize(creds)
        logger.info(f"[TEST] client_email: {creds.service_account_email}")
        # 创建测试表格
        sh = client.create('TestSheet')
        sh.share(creds.service_account_email, perm_type='user', role='writer')
        worksheet = sh.get_worksheet(0)
        worksheet.append_row(['测试', '写入', '成功', datetime.now().isoformat()])
        logger.info("[TEST] 成功写入TestSheet!")
        return True
    except Exception as e:
        logger.error(f"[TEST] Google Sheet写入失败: {e}")
        return False

def save_to_csv(tweets):
    try:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        logger.info(f"Credentials path: {cred_path}")
        
        if not cred_path:
            logger.error("Google credentials path not found in environment variables")
            return False
            
        if not os.path.exists(cred_path):
            logger.error(f"Credentials file does not exist at: {cred_path}")
            return False

        logger.info("Attempting to authorize with Google Sheets...")
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
            client = gspread.authorize(creds)
            logger.info("Successfully authorized with Google Sheets")
        except Exception as e:
            logger.error(f"Failed to authorize with Google Sheets: {e}")
            return False

        logger.info("Attempting to open spreadsheet 'Ikonoijoi'...")
        try:
            # 打开主表格
            spreadsheet = client.open("Ikonoijoi")
            logger.info("Successfully opened spreadsheet")
            
            # 按账号分组推文
            tweets_by_account = {}
            for tweet in tweets:
                account = tweet['account']
                if account not in tweets_by_account:
                    tweets_by_account[account] = []
                tweets_by_account[account].append(tweet)
            
            # 为每个账号处理工作表
            for account, account_tweets in tweets_by_account.items():
                try:
                    # 尝试获取已存在的工作表
                    try:
                        worksheet = spreadsheet.worksheet(account)
                        logger.info(f"Found existing worksheet for {account}")
                    except gspread.exceptions.WorksheetNotFound:
                        # 如果工作表不存在，创建新的
                        worksheet = spreadsheet.add_worksheet(title=account, rows=100, cols=4)
                        logger.info(f"Created new worksheet for {account}")
                        # 添加表头
                        worksheet.append_row(["时间", "内容", "批次时间"])
                    
                    # 准备数据行
                    rows = []
                    for tweet in account_tweets:
                        rows.append([
                            tweet['time'],
                            tweet['text'],
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ])
                    
                    if rows:
                        logger.info(f"Preparing to append {len(rows)} rows to worksheet {account}")
                        worksheet.append_rows(rows)
                        logger.info(f"Successfully exported {len(rows)} tweets to worksheet {account}")
                    
                except Exception as e:
                    logger.error(f"Error processing worksheet for {account}: {e}")
                    continue
            
            return True
            
        except gspread.exceptions.SpreadsheetNotFound:
            logger.error("Spreadsheet 'Ikonoijoi' not found. Please create it first.")
            return False
        except Exception as e:
            logger.error(f"Error accessing spreadsheet: {e}")
            return False
            
    except Exception as e:
        logger.error(f"Error exporting to Google Sheets: {str(e)}")
        return False

if __name__ == "__main__":
    test_google_sheet()
