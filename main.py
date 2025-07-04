from etl.config import get_source_engine, get_target_engine
from etl.constants import TABLE_NAME_MAPPING, TABLES_TO_MIGRATE
from etl.load import load_table
from etl.orchestrator import orchestrate_extraction
from etl.utils import ensure_dim_fecha

import requests

def run_etl():
    PING_URL = "https://hc-ping.com/fb544b72-4241-4661-a4de-4e768363a1a9"

    try:
        # Avisar que la tarea inició
        requests.get(f"{PING_URL}/start")

        source_engine = get_source_engine()
        target_engine = get_target_engine()

        ensure_dim_fecha(target_engine)

        for table in TABLES_TO_MIGRATE:
            df = orchestrate_extraction(table, source_engine)
            dest_table = TABLE_NAME_MAPPING.get(table, table)
            load_table(df, dest_table, target_engine)

        # Avisar que la tarea terminó OK
        requests.get(PING_URL)

    except Exception as e:
        print(f"Error durante ETL: {e}")
        try:
            # Avisar que la tarea falló
            requests.get(f"{PING_URL}/fail")
        except Exception as ping_fail_exc:
            print(f"No se pudo notificar el fallo a Healthchecks: {ping_fail_exc}")



# Para ejecutar el ETL a mano sin fastapi 
if __name__ == "__main__":
    run_etl()