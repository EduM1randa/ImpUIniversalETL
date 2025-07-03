from etl.extract import (
    extract_dim_cliente,
    extract_dim_pais,
    extract_dim_provincias,
    extract_dim_ciudades,
    extract_dim_proveedor,
    extract_dim_producto,
    extract_dim_categoria_producto,
    extract_dim_categorias_productos,
    extract_dim_metodo_pago,
    extract_dim_tipo_transaccion,
    extract_fact_inventario,
    extract_fact_movimiento_inventario,
    extract_dim_pedido_venta,
    extract_fact_ventas,
    extract_fact_compras,
    extract_dim_pedido_compra,
    # ...agrega aquí otras funciones si las creas
)


CUSTOM_EXTRACTION_FUNCTIONS = {
    # Dimensiones
    'Sales.Customers': extract_dim_cliente,
    'Application.Countries': extract_dim_pais,
    'Application.StateProvinces': extract_dim_provincias,
    'Application.Cities': extract_dim_ciudades,
    'Purchasing.Suppliers': extract_dim_proveedor,
    'Warehouse.StockItems': extract_dim_producto,
    'Warehouse.StockGroups': extract_dim_categoria_producto,
    'Warehouse.StockItemStockGroups': extract_dim_categorias_productos,
    'Application.PaymentMethods': extract_dim_metodo_pago,
    'Application.TransactionTypes': extract_dim_tipo_transaccion,
    'Warehouse.StockItemHoldings': extract_fact_inventario,
    'Warehouse.StockItemTransactions': extract_fact_movimiento_inventario,
    'Sales.Orders': extract_dim_pedido_venta,
    'Sales.Invoices': extract_fact_ventas, 
    'Purchasing.PurchaseOrderLines': extract_fact_compras, 
    'Purchasing.PurchaseOrders': extract_dim_pedido_compra,
}

def orchestrate_extraction(table_name: str, engine):
    if table_name in CUSTOM_EXTRACTION_FUNCTIONS:
        return CUSTOM_EXTRACTION_FUNCTIONS[table_name](table_name, engine)
    else:
        raise ValueError(f"No custom extraction function defined for table: {table_name}")

TABLE_NAME_MAPPING = {
    'Sales.Customers': 'DimCliente',
    'Application.Countries': 'DimPais',
    'Application.StateProvinces': 'DimProvincias',
    'Application.Cities': 'DimCiudades',
    'Purchasing.Suppliers': 'DimProveedor',
    'Warehouse.StockItems': 'DimProducto',
    'Warehouse.StockGroups': 'DimCategoriaProducto',
    'Warehouse.StockItemStockGroups': 'DimCategoriasProductos',
    'Application.PaymentMethods': 'DimMetodoPago',
    'Application.TransactionTypes': 'DimTipoTransaccion',
    'Warehouse.StockItemHoldings': 'FactInventario',
    'Warehouse.StockItemTransactions': 'FactMovimientoInventario',
    'Sales.Orders': 'DimPedidoVenta',
    'Sales.Invoices': 'FactVentas',
    'Purchasing.PurchaseOrderLines': 'FactCompras',
    'Purchasing.PurchaseOrders': 'DimPedidoCompra',
}