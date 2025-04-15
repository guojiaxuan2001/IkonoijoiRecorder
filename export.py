import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging
from datetime import datetime

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
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            logger.error("Google credentials path not found in environment variables")
            return False

        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
        client = gspread.authorize(creds)

        sheet = client.open("Ikonoijoi").sheet1
        
        # 获取当前时间作为批次标识
        batch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 准备数据行
        rows = []
        for tweet in tweets:
            rows.append([
                tweet['account'],
                tweet['time'],
                tweet['text'],
                batch_time  # 添加批次时间
            ])
        
        if rows:
            sheet.append_rows(rows)
            logger.info(f"Successfully exported {len(rows)} tweets to Google Sheets")
            return True
        else:
            logger.info("No tweets to export")
            return True
            
    except Exception as e:
        logger.error(f"Error exporting to Google Sheets: {e}")
        return False
