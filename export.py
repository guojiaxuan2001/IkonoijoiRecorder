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
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
        client = gspread.authorize(creds)
        logger.info("Successfully authorized with Google Sheets")

        logger.info("Attempting to open spreadsheet 'Ikonoijoi'...")
        try:
            sheet = client.open("Ikonoijoi").sheet1
            logger.info("Successfully opened spreadsheet")
        except gspread.exceptions.SpreadsheetNotFound:
            logger.error("Spreadsheet 'Ikonoijoi' not found. Please create it first.")
            return False
        
        # 获取当前时间作为批次标识
        batch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 准备数据行
        rows = []
        for tweet in tweets:
            rows.append([
                tweet['account'],
                tweet['time'],
                tweet['text'],
                batch_time
            ])
        
        if rows:
            logger.info(f"Preparing to append {len(rows)} rows to spreadsheet")
            sheet.append_rows(rows)
            logger.info(f"Successfully exported {len(rows)} tweets to Google Sheets")
            return True
        else:
            logger.info("No tweets to export")
            return True
            
    except Exception as e:
        logger.error(f"Error exporting to Google Sheets: {str(e)}")
        return False
