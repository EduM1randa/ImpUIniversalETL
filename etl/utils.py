from sqlalchemy import text

def ensure_dim_fecha(engine):
    with engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(text("""
        IF OBJECT_ID('dbo.DimFecha', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.DimFecha (
                id_fecha           INT           NOT NULL PRIMARY KEY,
                fecha              DATE          NOT NULL,
                dia                TINYINT       NOT NULL,
                mes                TINYINT       NOT NULL,
                año                INT           NOT NULL,
                trimestre          TINYINT       NOT NULL,
                semestre           TINYINT       NOT NULL,
                nombre_dia_semana  VARCHAR(10)   NOT NULL,
                es_fin_de_semana   BIT           NOT NULL,
                nombre_mes         VARCHAR(10)   NOT NULL,
                nombre_trimestre   VARCHAR(3)    NOT NULL,
                año_fiscal         INT           NOT NULL
            );
        END
        """))

        result = conn.execute(text("SELECT COUNT(*) FROM dbo.DimFecha"))
        count = result.scalar()

        if count == 0:
            print("Poblando DimFecha…")
            conn.execute(text("""
            DECLARE @FechaInicio DATE = '2010-01-01', @FechaFin DATE = '2030-12-31';
            ;WITH Calendario AS (
                SELECT @FechaInicio AS Fecha
                UNION ALL
                SELECT DATEADD(DAY, 1, Fecha)
                  FROM Calendario
                 WHERE Fecha < @FechaFin
            )
            INSERT INTO dbo.DimFecha
                (id_fecha,fecha,dia,mes,año,trimestre,semestre,
                 nombre_dia_semana,es_fin_de_semana,nombre_mes,
                 nombre_trimestre,año_fiscal)
            SELECT
                CONVERT(INT, FORMAT(Fecha, 'yyyyMMdd')) AS id_fecha,
                Fecha,
                DAY(Fecha),
                MONTH(Fecha),
                YEAR(Fecha),
                DATEPART(QUARTER, Fecha),
                CASE WHEN MONTH(Fecha) BETWEEN 1 AND 6 THEN 1 ELSE 2 END,
                DATENAME(WEEKDAY, Fecha),
                CASE WHEN DATENAME(WEEKDAY, Fecha) IN ('sábado','domingo') THEN 1 ELSE 0 END,
                DATENAME(MONTH, Fecha),
                'T' + CAST(DATEPART(QUARTER, Fecha) AS VARCHAR(1)),
                CASE WHEN MONTH(Fecha) >= 7 THEN YEAR(Fecha) + 1 ELSE YEAR(Fecha) END
            FROM Calendario
            OPTION (MAXRECURSION 0);
            """))
            print("DimFecha creada y poblada.")
        else:
            print("DimFecha ya existe y tiene datos.")
