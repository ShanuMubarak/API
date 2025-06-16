from apscheduler.schedulers.background import BackgroundScheduler
from app.logger import get_logger

logger = get_logger()
scheduler = BackgroundScheduler()

def update_data():
    logger.info("Running scheduled job...")
    # Your logic here

# Add the job
scheduler.add_job(update_data, 'interval', seconds=60)

# ✅ Define these so main.py can import them
def start():
    logger.info("Starting scheduler...")
    scheduler.start()

def shutdown():
    logger.info("Shutting down scheduler...")
    scheduler.shutdown()
