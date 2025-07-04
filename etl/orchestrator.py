from etl.constants import CUSTOM_EXTRACTION_FUNCTIONS, CUSTOM_TRANSFORMATION_FUNCTIONS
from etl.transform import transform_fact_movimiento_inventario

def orchestrate_extraction(table_name: str, engine):
    if table_name in CUSTOM_EXTRACTION_FUNCTIONS:
        return CUSTOM_EXTRACTION_FUNCTIONS[table_name](table_name, engine)
    else:
        raise ValueError(f"No custom extraction function defined for table: {table_name}")

def orchestrate_transformation(df, table_name: str):
    func = CUSTOM_TRANSFORMATION_FUNCTIONS.get(table_name)
    if func:
        print(f"Transforming {table_name} con función personalizada")
        return func(df)
    return df