from etl.config import get_source_engine, get_target_engine
from etl.load import load_table
from etl.orchestrator import orchestrate_extraction, TABLE_NAME_MAPPING
from etl.utils import ensure_dim_fecha

TABLES_TO_MIGRATE = [
    'Sales.Customers',
    'Application.Countries',
    'Application.StateProvinces',
    'Application.Cities',
    'Purchasing.Suppliers',
    'Warehouse.StockItems',
    'Warehouse.StockGroups',
    'Warehouse.StockItemStockGroups',
    'Application.PaymentMethods',
    'Application.TransactionTypes',
    'Warehouse.StockItemHoldings',
    'Warehouse.StockItemTransactions',
    'Sales.Orders',
    'Sales.Invoices',
    'Purchasing.PurchaseOrderLines',
    'Purchasing.PurchaseOrders',
]

def run_etl():
    source_engine = get_source_engine()
    target_engine = get_target_engine()

    ensure_dim_fecha(target_engine)

    for table in TABLES_TO_MIGRATE:
        df = orchestrate_extraction(table, source_engine)
        dest_table = TABLE_NAME_MAPPING.get(table, table)
        load_table(df, dest_table, target_engine)

if __name__ == "__main__":
    run_etl()