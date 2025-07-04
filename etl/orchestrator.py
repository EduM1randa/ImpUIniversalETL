from etl.constants import CUSTOM_EXTRACTION_FUNCTIONS

def orchestrate_extraction(table_name: str, engine):
    if table_name in CUSTOM_EXTRACTION_FUNCTIONS:
        return CUSTOM_EXTRACTION_FUNCTIONS[table_name](table_name, engine)
    else:
        raise ValueError(f"No custom extraction function defined for table: {table_name}")
