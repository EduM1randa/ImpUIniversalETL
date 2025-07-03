# etl_api.py
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
    # run_etl_job() # Ejecutar ETL al iniciar la aplicación
    scheduler.add_job(run_etl_job, CronTrigger(hour=0, minute=0), id="daily_etl", replace_existing=True)

@app.post("/run-etl")
def run_etl_endpoint():
    run_etl_job()
    return {"status": "ETL ejecutada manualmente"}

@app.post("/schedule-etl")
def schedule_custom_etl(cron: str):
    # Ejemplo: cron="0 3 * * *" para las 03:00 am
    scheduler.add_job(run_etl_job, CronTrigger.from_crontab(cron), id="custom_etl", replace_existing=True)
    return {"status": f"ETL programada con cron: {cron}"}