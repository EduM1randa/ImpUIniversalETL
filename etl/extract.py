import pandas as pd

def extract_dim_pais(table_name: str, engine):
    query = """
    SELECT
      Countries.CountryID AS id_pais,
      Countries.CountryName AS nombre_pais,
      Countries.FormalName AS nombre_formal,
      Countries.IsoAlpha3Code AS codigo_iso_a3,
      Countries.IsoNumericCode AS codigo_iso_numerico,
      Countries.Continent AS continente,
      Countries.Region AS region,
      Countries.Subregion AS subregion,
      Countries.LatestRecordedPopulation AS ultima_poblacion_registrada
    FROM Application.Countries AS Countries
    """
    print("Extracting data from Dim.Pais...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_provincias(table_name: str, engine):
    query = """
    SELECT
      Provinces.StateProvinceID AS id_provincia,
      Provinces.StateProvinceCode AS codigo_provincia,
      Provinces.StateProvinceName AS nombre_provincia,
      Provinces.CountryID AS id_pais_fk,
      Provinces.SalesTerritory AS territorio_ventas,
      Provinces.LatestRecordedPopulation AS ultima_poblacion_registrada
    FROM Application.StateProvinces AS Provinces
    """
    print("Extracting data from Dim.Provincias...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_ciudades(table_name: str, engine):
    query = """
    SELECT
      Cities.CityID AS id_ciudad,
      Cities.CityName AS nombre_ciudad,
      Cities.StateProvinceID AS id_provincia_fk,
      Cities.LatestRecordedPopulation AS ultima_poblacion_registrada
    FROM Application.Cities AS Cities
    """
    print("Extracting data from Dim.Ciudades...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_proveedor(table_name: str, engine):
    query = """
    SELECT
      ps.SupplierID AS id_proveedor,
      ps.SupplierName AS nombre_proveedor,
      psc.SupplierCategoryName AS tipo_proveedor,
      cit.CityID AS id_ciudad,
      prov.StateProvinceID AS id_provincia,
      co.CountryID AS id_pais,
      ps.DeliveryAddressLine2 AS direccion,
      ps.PhoneNumber AS telefono,
      firstContact.EmailAddress AS email
    FROM Purchasing.Suppliers AS ps
    LEFT JOIN Application.Cities AS cit ON ps.DeliveryCityID = cit.CityID
    LEFT JOIN Application.StateProvinces AS prov ON cit.StateProvinceID = prov.StateProvinceID
    LEFT JOIN Application.Countries AS co ON prov.CountryID = co.CountryID
    LEFT JOIN Purchasing.SupplierCategories AS psc ON ps.SupplierCategoryID = psc.SupplierCategoryID
    LEFT JOIN Application.People AS firstContact ON ps.PrimaryContactPersonID = firstContact.PersonID
    """
    print("Extracting data from Dim.Proveedor...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_producto(table_name: str, engine):
    query = """
    SELECT
      Products.StockItemID AS id_producto,
      Products.StockItemName AS nombre_producto,
      Products.SupplierID AS id_proveedor,
      Colors.ColorName AS color,
      Products.Size AS talla,
      Products.LeadTimeDays AS dias_plazo_entrega,
      Products.QuantityPerOuter AS cantidad_por_empaque,
      Products.TaxRate AS tasa_impuesto,
      Products.UnitPrice AS precio_unitario,
      Products.RecommendedRetailPrice AS precio_venta_recomendado,
      Products.TypicalWeightPerUnit AS peso_unitario,
      Products.MarketingComments AS comentarios_marketing,
      Products.CustomFields AS campos_personalizados,
      Products.Tags AS etiquetas,
      Products.SearchDetails AS detalles_busqueda
    FROM Warehouse.StockItems AS Products
    INNER JOIN Warehouse.Colors AS Colors ON Products.ColorID = Colors.ColorID
    """
    print("Extracting data from Dim.Producto...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_categoria_producto(table_name: str, engine):
    query = """
    SELECT
      Categories.StockGroupID AS id_categoria,
      Categories.StockGroupName AS nombre_categoria
    FROM Warehouse.StockGroups AS Categories
    """
    print("Extracting data from Dim.CategoriaProducto...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_categorias_productos(table_name: str, engine):
    query = """
    SELECT
      ProductCategories.StockItemStockGroupID AS id_categoria_producto,
      ProductCategories.StockItemID AS id_producto,
      ProductCategories.StockGroupID AS id_categoria
    FROM Warehouse.StockItemStockGroups AS ProductCategories
    """
    print("Extracting data from Dim.CategoriasProductos...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_metodo_pago(table_name: str, engine):
    query = """
    SELECT 
      PaymentMethodID AS id_metodo_pago,
      PaymentMethodName AS metodo
    FROM Application.PaymentMethods
    """
    print("Extracting data from Dim.MetodoPago...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_tipo_transaccion(table_name: str, engine):
    query = """
    SELECT 
      TransactionTypeID AS id_tipo_transaccion,
      TransactionTypeName AS tipo_transaccion
    FROM Application.TransactionTypes
    """
    print("Extracting data from Dim.TipoTransaccion...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_cliente(table_name: str, engine):
    query = """
    SELECT     
      customer.CustomerID AS id_cliente,
      customer.CustomerName AS nombre_cliente,
      cc.CustomerCategoryName AS tipo_cliente,
      bg.BuyingGroupName AS segmento,
      cit.CityID AS id_ciudad,
      prov.StateProvinceID AS id_provincia,
      co.CountryID AS id_pais,
      customer.DeliveryAddressLine2 AS direccion,
      customer.DeliveryAddressLine1 AS sub_direccion,
      customer.PhoneNumber AS telefono,
      firstContact.EmailAddress AS email,
      customer.AccountOpenedDate AS fecha_registro,
      df_reg.id_fecha AS fecha_registro_key
    FROM Sales.Customers AS customer
    LEFT JOIN Application.Cities AS cit ON customer.DeliveryCityID = cit.CityID
    LEFT JOIN Application.StateProvinces AS prov ON cit.StateProvinceID = prov.StateProvinceID
    LEFT JOIN Application.Countries AS co ON prov.CountryID = co.CountryID
    LEFT JOIN Sales.CustomerCategories AS cc ON customer.CustomerCategoryID = cc.CustomerCategoryID
    LEFT JOIN Sales.BuyingGroups AS bg ON customer.BuyingGroupID = bg.BuyingGroupID
    LEFT JOIN dbo.DimFecha AS df_reg ON CONVERT(INT, FORMAT(customer.AccountOpenedDate, 'yyyyMMdd')) = df_reg.id_fecha
    LEFT JOIN Application.People AS firstContact ON customer.PrimaryContactPersonID = firstContact.PersonID
    """
    print("Extracting data from Dim.Cliente...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_pedido_venta(table_name: str, engine):
    query = """
    SELECT
      OrderID AS id_pedido,
      CustomerID AS id_cliente,
      SalespersonPersonID AS id_persona_ventas,
      PickedByPersonID AS id_persona_recolección,
      ContactPersonID AS id_persona_contacto,
      BackorderOrderID AS id_pedido_pendiente,
      df_ped.id_fecha AS fecha_pedido,
      df_ent.id_fecha AS fecha_entrega_esperada,
      CustomerPurchaseOrderNumber AS numero_oc_cliente,
      IsUndersupplyBackordered AS es_reposición_pendiente,
      Comments AS comentarios,
      DeliveryInstructions AS instrucciones_entrega,
      InternalComments AS comentarios_internos,
      df_pick.id_fecha AS fecha_completado_recolección,
      df_mod.id_fecha AS fecha_última_modificación,
      LastEditedBy AS modificado_por
    FROM Sales.Orders
    LEFT JOIN dbo.DimFecha AS df_ped
      ON CONVERT(INT, FORMAT(OrderDate, 'yyyyMMdd')) = df_ped.id_fecha
    LEFT JOIN dbo.DimFecha AS df_ent
      ON CONVERT(INT, FORMAT(ExpectedDeliveryDate, 'yyyyMMdd')) = df_ent.id_fecha
    LEFT JOIN dbo.DimFecha AS df_pick
      ON CONVERT(INT, FORMAT(PickingCompletedWhen, 'yyyyMMdd')) = df_pick.id_fecha
    LEFT JOIN dbo.DimFecha AS df_mod
      ON CONVERT(INT, FORMAT(LastEditedWhen, 'yyyyMMdd')) = df_mod.id_fecha
    """
    print("Extracting data from Dim.PedidoVenta...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_dim_pedido_compra(table_name: str, engine):
    query = """
    SELECT
      PurchaseOrderID AS id_pedido_compra,
      SupplierID AS id_proveedor_fk,
      df_ped.id_fecha AS fecha_pedido,
      DeliveryMethodID AS id_metodo_entrega_fk,
      ContactPersonID AS id_persona_contacto_fk,
      df_ent.id_fecha AS fecha_entrega_esperada,
      IsOrderFinalized AS esta_finalizado,
      Comments AS comentarios,
      InternalComments AS comentarios_internos,
      LastEditedBy AS modificado_por,
      df_mod.id_fecha AS fecha_última_modificación
    FROM Purchasing.PurchaseOrders
    LEFT JOIN dbo.DimFecha AS df_ped ON CONVERT(INT, FORMAT(OrderDate, 'yyyyMMdd')) = df_ped.id_fecha
    LEFT JOIN dbo.DimFecha AS df_ent ON CONVERT(INT, FORMAT(ExpectedDeliveryDate, 'yyyyMMdd')) = df_ent.id_fecha
    LEFT JOIN dbo.DimFecha AS df_mod ON CONVERT(INT, FORMAT(LastEditedWhen, 'yyyyMMdd')) = df_mod.id_fecha
    """
    print("Extracting data from Dim.PedidoCompra...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_fact_inventario(table_name: str, engine):
    query = """
    SELECT
      Inventory.StockItemID AS id_producto,
      Inventory.QuantityOnHand AS cantidad_disponible,
      Inventory.BinLocation AS ubicacion,
      Inventory.LastStocktakeQuantity AS cantidad_ultimo_inventario,
      Inventory.LastCostPrice AS costo_ultimo_inventario,
      Inventory.ReorderLevel AS nivel_reorden,
      Inventory.TargetStockLevel AS nivel_objetivo_stock,
      df_mod.id_fecha AS fecha_modificacion
    FROM Warehouse.StockItemHoldings AS Inventory
    LEFT JOIN dbo.DimFecha AS df_mod
      ON CONVERT(INT, FORMAT(Inventory.LastEditedWhen, 'yyyyMMdd')) = df_mod.id_fecha
    """
    print("Extracting data from Fact.Inventario...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_fact_movimiento_inventario(table_name: str, engine):
    query = """
    SELECT
      pm.StockItemTransactionID AS id_movimiento_inventario,
      pm.StockItemID AS id_producto,
      pm.TransactionTypeID AS id_tipo_transaccion,
      pm.CustomerID AS id_cliente,
      pm.InvoiceID AS id_factura,
      pm.SupplierID AS id_proveedor,
      pm.PurchaseOrderID AS id_orden_compra,
      pm.Quantity AS cantidad,
      df_mov.id_fecha AS fecha_ocurrencia
    FROM Warehouse.StockItemTransactions AS pm
    LEFT JOIN dbo.DimFecha AS df_mov
      ON CONVERT(INT, FORMAT(pm.TransactionOccurredWhen, 'yyyyMMdd')) = df_mov.id_fecha
    """
    print("Extracting data from Fact.MovimientoInventario...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_fact_ventas(table_name: str, engine):
    query = """
    ;WITH TransPagos AS (
    -- Todas las transacciones de cliente con método de pago
    SELECT
        ct.CustomerTransactionID,
        ct.InvoiceID,
        ct.CustomerID            AS id_cliente,
        ct.PaymentMethodID       AS id_metodo_pago,
        ct.TransactionTypeID     AS id_tipo_transaccion,
        ct.TransactionDate       AS fecha_de_transaccion,
        ct.FinalizationDate      AS fecha_de_entrega,
        ct.AmountExcludingTax    AS total_sin_impuesto,
        ct.TaxAmount             AS monto_impuesto,
        ct.TransactionAmount     AS monto_total_con_impuesto,
        ct.OutstandingBalance    AS deuda
    FROM Sales.CustomerTransactions ct
    WHERE ct.PaymentMethodID IS NOT NULL
    )

    SELECT
    tp.id_metodo_pago,
    tp.id_tipo_transaccion,

    il.StockItemID            AS id_producto,

    COALESCE(tp.id_cliente, inv.CustomerID) AS id_cliente,

    inv.InvoiceID             AS id_factura,
    inv.OrderID               AS id_pedido,
    df_ped.id_fecha           AS fecha_pedido,
    df_fac.id_fecha           AS fecha_factura,

    df_trn.id_fecha           AS fecha_transaccion,
    df_fin.id_fecha           AS fecha_entrega,

    -- Cantidades y precios
    il.Quantity               AS cantidad,
    il.UnitPrice              AS precio_unitario,
    il.TaxRate                AS tasa_impuesto,

    -- Montos de TransPagos
    tp.total_sin_impuesto,
    tp.monto_impuesto,
    tp.monto_total_con_impuesto,
    tp.deuda

    FROM Sales.Invoices inv

    -- 1) Unión “invoice‐first” con pagos
    FULL OUTER JOIN TransPagos tp
        ON inv.InvoiceID = tp.InvoiceID

    -- 2) Líneas de factura
    LEFT JOIN Sales.InvoiceLines il
        ON inv.InvoiceID = il.InvoiceID

    -- 3) Pedido original
    LEFT JOIN Sales.Orders ord
        ON inv.OrderID = ord.OrderID

    -- 4) Joins a DimFecha usando CONVERT(INT, FORMAT(..., 'yyyyMMdd'))
    LEFT JOIN dbo.DimFecha df_ped
        ON CONVERT(INT, FORMAT(ord.OrderDate,          'yyyyMMdd')) = df_ped.id_fecha

    LEFT JOIN dbo.DimFecha df_fac
        ON CONVERT(INT, FORMAT(inv.InvoiceDate,        'yyyyMMdd')) = df_fac.id_fecha

    LEFT JOIN dbo.DimFecha df_trn
        ON CONVERT(INT, FORMAT(tp.fecha_de_transaccion,'yyyyMMdd')) = df_trn.id_fecha

    LEFT JOIN dbo.DimFecha df_fin
    ON CONVERT(INT, FORMAT(tp.fecha_de_entrega,     'yyyyMMdd')) = df_fin.id_fecha;
    """
    print("Extracting data from Fact.Ventas...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

def extract_fact_compras(table_name: str, engine):
    query = """
    SELECT 
      po.PurchaseOrderID AS id_pedido_compra,    
      st.PaymentMethodID AS id_metodo_pago,
      pol.StockItemID AS id_producto,
      st.SupplierID AS id_proveedor,
      st.TransactionTypeID AS id_tipo_transaccion,
      df_ord.id_fecha AS fecha_pedido,
      df_trn.id_fecha AS fecha_transaccion,
      df_fin.id_fecha AS fecha_entrega,
      df_exp.id_fecha AS fecha_entrega_esperada,
      pol.ExpectedUnitPricePerOuter AS precio_unitario_esperado,
      st.AmountExcludingTax AS total_sin_impuesto,
      st.TaxAmount AS monto_impuesto,
      st.TransactionAmount AS monto_total_con_impuesto,
      st.OutstandingBalance AS deuda
    FROM Purchasing.PurchaseOrderLines AS pol
    JOIN Purchasing.PurchaseOrders AS po ON pol.PurchaseOrderID = po.PurchaseOrderID
    LEFT JOIN Purchasing.SupplierTransactions AS st ON po.PurchaseOrderID = st.PurchaseOrderID
    LEFT JOIN dbo.DimFecha AS df_ord ON CONVERT(INT, FORMAT(po.OrderDate, 'yyyyMMdd')) = df_ord.id_fecha
    LEFT JOIN dbo.DimFecha AS df_trn ON CONVERT(INT, FORMAT(st.TransactionDate, 'yyyyMMdd')) = df_trn.id_fecha
    LEFT JOIN dbo.DimFecha AS df_fin ON CONVERT(INT, FORMAT(st.FinalizationDate, 'yyyyMMdd')) = df_fin.id_fecha
    LEFT JOIN dbo.DimFecha AS df_exp ON CONVERT(INT, FORMAT(po.ExpectedDeliveryDate, 'yyyyMMdd')) = df_exp.id_fecha
    """
    print("Extracting data from Fact.Compras...")
    df = pd.read_sql(query, engine)
    print(df.head())
    return df

