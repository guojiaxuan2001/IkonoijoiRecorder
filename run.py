import schedule
import time
from main import main
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        logger.info("开始执行推文抓取任务...")
        main()
        logger.info("任务执行完成")
    except Exception as e:
        logger.error(f"任务执行出错: {e}")

def run_scheduler():
    schedule.every(6).hours.do(job)
    logger.info("定时任务已启动，每6小时执行一次")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("首次执行任务...")
    job()  # 立即执行一次
    run_scheduler()  # 启动定时任务 