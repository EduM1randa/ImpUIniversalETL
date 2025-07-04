from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

def run_etl_job():
    from main import run_etl
    run_etl()

@app.on_event("startup")
def schedule_etl():
    run_etl_job()
    scheduler.add_job(run_etl_job, CronTrigger(hour=0, minute=0), id="daily_etl", replace_existing=True)
