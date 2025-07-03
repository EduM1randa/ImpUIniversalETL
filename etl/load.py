import pandas as pd
from sqlalchemy import event
from sqlalchemy.engine import Engine

def load_table(df, table_name: str, engine):
    print(f"Loading data into {table_name}...")

    @event.listens_for(Engine, "before_cursor_execute")
    def _enable_fast_executemany(conn, cursor, statement,
                                 parameters, context, executemany):
        try:
            cursor.fast_executemany = True
        except:
            pass

    n_cols = len(df.columns)
    max_rows = 2000 // n_cols
    if max_rows < 1:
        raise ValueError(f"Demasiadas columnas ({n_cols}); reduce columnas o usa BULK INSERT.")
    chunksize = min(1000, max_rows) 

    print(f"Usando chunksize={chunksize} para evitar el límite de 2100 parámetros.")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False,
        method='multi',
        chunksize=chunksize
    )

    print(f"Data loaded into {table_name} successfully.")
