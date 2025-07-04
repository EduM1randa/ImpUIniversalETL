import pandas as pd
import numpy as np
from sqlalchemy import inspect, text
from etl.load import load_table

def generate_date_dimension_df(start_date='2010-01-01', end_date='2030-12-31'):
    # Manejo de nombres en español
    spanish_days = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    spanish_months = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    # Crear rango de fechas
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Calcular componentes de fecha
    days = dates.day.astype('int8')
    months = dates.month.astype('int8')
    years = dates.year
    quarters = dates.quarter.astype('int8')
    
    # Calcular semestres (1: enero-junio, 2: julio-diciembre)
    semesters = np.where(months <= 6, 1, 2).astype('int8')
    
    # Días de la semana (0=lunes, 6=domingo)
    day_of_week = dates.dayofweek
    
    # Crear DataFrame
    df = pd.DataFrame({
        'id_fecha': dates.strftime('%Y%m%d').astype(int),
        'fecha': dates,
        'dia': days,
        'mes': months,
        'año': years,
        'trimestre': quarters,
        'semestre': semesters,
        'nombre_dia_semana': np.array(spanish_days)[day_of_week],
        'es_fin_de_semana': np.where(day_of_week >= 5, 1, 0).astype('int8'),
        'nombre_mes': np.array(spanish_months)[months - 1],
        'nombre_trimestre': 'T' + quarters.astype(str),
        'año_fiscal': np.where(months >= 7, years + 1, years)
    })
    
    # Convertir fecha a tipo date (sin hora)
    df['fecha'] = df['fecha'].dt.date
    
    return df

def ensure_dim_fecha(engine):
    table_name = 'DimFecha'
    inspector = inspect(engine)

    if table_name not in inspector.get_table_names():
        print(f"La tabla {table_name} no existe. Creando tabla y generando datos...")

        create_sql = """
        CREATE TABLE DimFecha (
            id_fecha           INT           NOT NULL PRIMARY KEY,
            fecha               DATE         NOT NULL,
            dia                 TINYINT      NOT NULL,
            mes                 TINYINT      NOT NULL,
            año                 INT          NOT NULL,
            trimestre           TINYINT      NOT NULL,
            semestre            TINYINT      NOT NULL,
            nombre_dia_semana   VARCHAR(10)  NOT NULL,
            es_fin_de_semana    BIT          NOT NULL,
            nombre_mes          VARCHAR(10)  NOT NULL,
            nombre_trimestre    VARCHAR(3)   NOT NULL,
            año_fiscal          INT          NOT NULL
        );
        """
        with engine.begin() as conn:
            conn.execute(text(create_sql))

        date_df = generate_date_dimension_df()

        load_table(date_df, table_name, engine)
        print("Tabla DimFecha creada y poblada exitosamente.")
    else:
        print(f"La tabla {table_name} ya existe. No se realizaron cambios.")