import os
import tempfile
from sqlalchemy import text

def load_table(df, table_name: str, engine):
    if not engine.dialect.has_table(engine.connect(), table_name):
        df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)

    # Normalizar columnas tipo BIT a 0/1
    for col in ['es_reposición_pendiente', 'esta_finalizado']:
        if col in df.columns:
            df[col] = df[col].astype(float).fillna(0).astype(int)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', newline='', encoding='utf-8') as tmp_file:
        tmp_path = tmp_file.name
        df.to_csv(tmp_file, sep='|', index=False, header=False)

    try:
        print(f"Usando BULK INSERT desde archivo temporal: {tmp_path}")

        with engine.begin() as conn:
            conn.execute(text(f"""
                BULK INSERT {table_name}
                FROM '{tmp_path}'
                WITH (
                    FIELDTERMINATOR = '|',
                    ROWTERMINATOR = '\\n',
                    FIRSTROW = 1,
                    TABLOCK
                )
            """))

        print(f"✔️ Datos cargados exitosamente en {table_name}.")
    finally:
        os.remove(tmp_path)