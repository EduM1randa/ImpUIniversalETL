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
)

from etl.transform import (
    transform_dim_pedido_venta, 
    transform_fact_movimiento_inventario, 
    transform_fact_ventas,
    transform_fact_compras,
)

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

CUSTOM_EXTRACTION_FUNCTIONS = {
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

CUSTOM_TRANSFORMATION_FUNCTIONS = {
    'Warehouse.StockItemTransactions': transform_fact_movimiento_inventario,
    'Sales.Orders': transform_dim_pedido_venta,
    'Sales.Invoices': transform_fact_ventas,
    'Purchasing.PurchaseOrderLines': transform_fact_compras,
}

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