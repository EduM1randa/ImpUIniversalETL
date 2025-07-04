from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from main import run_etl

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

@app.on_event("startup")
def schedule_etl():
    run_etl()
    scheduler.add_job(run_etl, CronTrigger(hour=0, minute=0), id="daily_etl", replace_existing=True)
