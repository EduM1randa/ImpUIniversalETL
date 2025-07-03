# ETL SQL Server a SQL Server

Este proyecto implementa un proceso ETL usando Python para migrar múltiples tablas desde una base de datos SQL Server origen a otra destino.

## Estructura

- `extract.py`: extrae datos de las tablas en la base origen.
- `transform.py`: permite transformar los datos si es necesario.
- `load.py`: carga los datos en la base destino.
- `config.py`: gestiona las conexiones a las bases de datos usando variables de entorno.

## Uso

1. Crea un entorno virtual: `python -m venv venv`
2. Actívalo: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
3. Instala dependencias: `pip install -r requirements.txt`
4. Configura `.env` con tus credenciales
5. Ejecuta el ETL: `python main.py`
