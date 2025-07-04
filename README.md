# ETL SQL Server a SQL Server

Este proyecto implementa un proceso ETL usando Python para migrar múltiples tablas desde una base de datos SQL Server origen a otra destino.

## Integrantes:

- Eduardo Miranda
- José Carrillo
- Walter Arancibia
- Gabriel Zuleta
- Giacomo Baldessari

## Estructura

```
ImpUniversal/
├── etl/
│   ├── config.py           # Configuración de conexiones a bases de datos
│   ├── constants.py        # Listas y mapeos de tablas a migrar
│   ├── extract.py          # Funciones de extracción de datos
│   ├── load.py             # Funciones de carga de datos (incluye BULK INSERT)
│   ├── orchestrator.py     # Orquestación completa del proceso ETL
│   ├── utils.py            # Utilidades (DimFecha, helpers, etc.)
│   └── main.py             # Script principal para ejecutar el ETL completo
├── etl_api.py              # API FastAPI para disparar y programar el ETL
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no subir a git)
├── .gitignore              # Archivos y carpetas ignorados por git
└── README.md               # Este archivo
```

## Uso

1. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   ```
2. **Actívalo** \
   Linux/Mac:
   ```
   source venv/bin/activate
   ```
   Windows:
   ```
   venv\Scripts\activate
   ```
3. **Instala dependencias**
   ```
   pip install -r requirements.txt
   ```
4. **Configura `.env` con tus credenciales de las bases de datos.**

5. **Ejecuta el ETL**

   ```
   python main.py
   ```

   o desde api

   ```
   uvicorn etl_api:app --reload\
   ```
