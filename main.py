from etl.config import get_source_engine, get_target_engine
from etl.constants import TABLE_NAME_MAPPING, TABLES_TO_MIGRATE
from etl.load import load_table
from etl.orchestrator import orchestrate_extraction
from etl.utils import ensure_dim_fecha

def run_etl():
    source_engine = get_source_engine()
    target_engine = get_target_engine()

    ensure_dim_fecha(target_engine)

    for table in TABLES_TO_MIGRATE:
        df = orchestrate_extraction(table, source_engine)
        dest_table = TABLE_NAME_MAPPING.get(table, table)
        load_table(df, dest_table, target_engine)

# Para ejecutar el ETL a mano sin fastapi 
if __name__ == "__main__":
    run_etl()