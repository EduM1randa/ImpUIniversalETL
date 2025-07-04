-- 1. Tablas de hechos y relaciones (más dependientes)
IF OBJECT_ID('dbo.FactCompras', 'U') IS NOT NULL DROP TABLE dbo.FactCompras;
IF OBJECT_ID('dbo.FactVentas', 'U') IS NOT NULL DROP TABLE dbo.FactVentas;
IF OBJECT_ID('dbo.FactMovimientoInventario', 'U') IS NOT NULL DROP TABLE dbo.FactMovimientoInventario;
IF OBJECT_ID('dbo.FactInventario', 'U') IS NOT NULL DROP TABLE dbo.FactInventario;
IF OBJECT_ID('dbo.DimCategoriasProductos', 'U') IS NOT NULL DROP TABLE dbo.DimCategoriasProductos;

-- 2. Dimensiones hijas
IF OBJECT_ID('dbo.DimPedidoCompra', 'U') IS NOT NULL DROP TABLE dbo.DimPedidoCompra;
IF OBJECT_ID('dbo.DimPedidoVenta', 'U') IS NOT NULL DROP TABLE dbo.DimPedidoVenta;
IF OBJECT_ID('dbo.DimCliente', 'U') IS NOT NULL DROP TABLE dbo.DimCliente;
IF OBJECT_ID('dbo.DimProducto', 'U') IS NOT NULL DROP TABLE dbo.DimProducto;
IF OBJECT_ID('dbo.DimProveedor', 'U') IS NOT NULL DROP TABLE dbo.DimProveedor;

-- 3. Dimensiones padres
IF OBJECT_ID('dbo.DimCategoriaProducto', 'U') IS NOT NULL DROP TABLE dbo.DimCategoriaProducto;
IF OBJECT_ID('dbo.DimMetodoPago', 'U') IS NOT NULL DROP TABLE dbo.DimMetodoPago;
IF OBJECT_ID('dbo.DimTipoTransaccion', 'U') IS NOT NULL DROP TABLE dbo.DimTipoTransaccion;
IF OBJECT_ID('dbo.DimCiudades', 'U') IS NOT NULL DROP TABLE dbo.DimCiudades;
IF OBJECT_ID('dbo.DimProvincias', 'U') IS NOT NULL DROP TABLE dbo.DimProvincias;
IF OBJECT_ID('dbo.DimPais', 'U') IS NOT NULL DROP TABLE dbo.DimPais;

-- 1. Dimensiones padres
CREATE TABLE dbo.DimPais (
    id_pais INT PRIMARY KEY,
    nombre_pais NVARCHAR(100),
    nombre_formal NVARCHAR(100),
    codigo_iso_a3 NVARCHAR(10),
    codigo_iso_numerico INT,
    continente NVARCHAR(50),
    region NVARCHAR(50),
    subregion NVARCHAR(50),
    ultima_poblacion_registrada FLOAT NULL
);

CREATE TABLE dbo.DimProvincias (
    id_provincia INT PRIMARY KEY,
    codigo_provincia NVARCHAR(10),
    nombre_provincia NVARCHAR(100),
    id_pais INT FOREIGN KEY REFERENCES dbo.DimPais(id_pais),
    territorio_ventas NVARCHAR(50),
    ultima_poblacion_registrada FLOAT NULL
);

CREATE TABLE dbo.DimCiudades (
    id_ciudad INT PRIMARY KEY,
    nombre_ciudad NVARCHAR(100),
    id_provincia INT FOREIGN KEY REFERENCES dbo.DimProvincias(id_provincia),
    ultima_poblacion_registrada FLOAT NULL
);

CREATE TABLE dbo.DimCategoriaProducto (
    id_categoria INT PRIMARY KEY,
    nombre_categoria NVARCHAR(100)
);

CREATE TABLE dbo.DimMetodoPago (
    id_metodo_pago INT PRIMARY KEY,
    metodo NVARCHAR(100)
);

CREATE TABLE dbo.DimTipoTransaccion (
    id_tipo_transaccion INT PRIMARY KEY,
    tipo_transaccion NVARCHAR(100)
);

-- 2. Dimensiones hijas
CREATE TABLE dbo.DimProveedor (
    id_proveedor INT PRIMARY KEY,
    nombre_proveedor NVARCHAR(100),
    tipo_proveedor NVARCHAR(100),
    id_ciudad INT FOREIGN KEY REFERENCES dbo.DimCiudades(id_ciudad),
    id_provincia INT FOREIGN KEY REFERENCES dbo.DimProvincias(id_provincia),
    id_pais INT FOREIGN KEY REFERENCES dbo.DimPais(id_pais),
    direccion NVARCHAR(255),
    telefono NVARCHAR(50),
    email NVARCHAR(100)
);

CREATE TABLE dbo.DimProducto (
    id_producto INT PRIMARY KEY,
    nombre_producto NVARCHAR(100),
    id_proveedor INT FOREIGN KEY REFERENCES dbo.DimProveedor(id_proveedor),
    color NVARCHAR(50),
    talla NVARCHAR(50),
    dias_plazo_entrega INT,
    cantidad_por_empaque INT,
    tasa_impuesto FLOAT,
    precio_unitario MONEY,
    precio_venta_recomendado MONEY,
    peso_unitario FLOAT,
    comentarios_marketing NVARCHAR(MAX),
    campos_personalizados NVARCHAR(MAX),
    etiquetas NVARCHAR(MAX),
    detalles_busqueda NVARCHAR(MAX)
);

CREATE TABLE dbo.DimCliente (
    id_cliente INT PRIMARY KEY,
    nombre_cliente NVARCHAR(100),
    tipo_cliente NVARCHAR(100),
    segmento NVARCHAR(100),
    id_ciudad INT FOREIGN KEY REFERENCES dbo.DimCiudades(id_ciudad),
    id_provincia INT FOREIGN KEY REFERENCES dbo.DimProvincias(id_provincia),
    id_pais INT FOREIGN KEY REFERENCES dbo.DimPais(id_pais),
    direccion NVARCHAR(255),
    sub_direccion NVARCHAR(255),
    telefono NVARCHAR(50),
    email NVARCHAR(100),
    fecha_registro DATE,
    fecha_registro_key INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha)
);

CREATE TABLE dbo.DimPedidoVenta (
    id_pedido INT PRIMARY KEY,
    id_cliente INT NULL FOREIGN KEY REFERENCES dbo.DimCliente(id_cliente),
    id_persona_ventas INT,
    id_persona_recolección INT,
    id_persona_contacto INT,
    id_pedido_pendiente INT,
    fecha_pedido INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_entrega_esperada INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    numero_oc_cliente NVARCHAR(100),
    es_reposición_pendiente BIT,
    comentarios NVARCHAR(MAX),
    instrucciones_entrega NVARCHAR(MAX),
    comentarios_internos NVARCHAR(MAX),
    fecha_completado_recolección INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_última_modificación INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    modificado_por INT
);

CREATE TABLE dbo.DimPedidoCompra (
    id_pedido_compra INT PRIMARY KEY,
    id_proveedor INT FOREIGN KEY REFERENCES dbo.DimProveedor(id_proveedor),
    fecha_pedido INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    id_metodo_entrega INT,
    id_persona_contacto INT,
    fecha_entrega_esperada INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    esta_finalizado BIT,
    comentarios NVARCHAR(MAX),
    comentarios_internos NVARCHAR(MAX),
    modificado_por INT,
    fecha_última_modificación INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha)
);

-- 3. Tablas de hechos y relaciones
CREATE TABLE dbo.DimCategoriasProductos (
    id_categoria_producto INT PRIMARY KEY,
    id_producto INT FOREIGN KEY REFERENCES dbo.DimProducto(id_producto),
    id_categoria INT FOREIGN KEY REFERENCES dbo.DimCategoriaProducto(id_categoria)
);

CREATE TABLE dbo.FactInventario (
    id_producto INT FOREIGN KEY REFERENCES dbo.DimProducto(id_producto),
    cantidad_disponible INT,
    ubicacion NVARCHAR(100),
    cantidad_ultimo_inventario INT,
    costo_ultimo_inventario MONEY,
    nivel_reorden INT,
    nivel_objetivo_stock INT,
    fecha_modificacion INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha)
);

CREATE TABLE dbo.FactMovimientoInventario (
    id_movimiento_inventario INT PRIMARY KEY,
    id_producto INT FOREIGN KEY REFERENCES dbo.DimProducto(id_producto),
    id_tipo_transaccion INT FOREIGN KEY REFERENCES dbo.DimTipoTransaccion(id_tipo_transaccion),
    id_cliente INT NULL FOREIGN KEY REFERENCES dbo.DimCliente(id_cliente),
    id_factura INT,
    id_proveedor INT FOREIGN KEY REFERENCES dbo.DimProveedor(id_proveedor),
    id_orden_compra INT FOREIGN KEY REFERENCES dbo.DimPedidoCompra(id_pedido_compra),
    cantidad INT,
    fecha_ocurrencia INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha)
);

CREATE TABLE dbo.FactVentas (
    id_metodo_pago INT FOREIGN KEY REFERENCES dbo.DimMetodoPago(id_metodo_pago),
    id_tipo_transaccion INT FOREIGN KEY REFERENCES dbo.DimTipoTransaccion(id_tipo_transaccion),
    id_producto INT FOREIGN KEY REFERENCES dbo.DimProducto(id_producto),
    id_cliente INT NULL FOREIGN KEY REFERENCES dbo.DimCliente(id_cliente),
    id_factura INT,
    id_pedido INT FOREIGN KEY REFERENCES dbo.DimPedidoVenta(id_pedido),
    fecha_pedido INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_factura INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_transaccion INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_entrega INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    cantidad INT,
    precio_unitario MONEY,
    tasa_impuesto FLOAT,
    total_sin_impuesto MONEY,
    monto_impuesto MONEY,
    monto_total_con_impuesto MONEY,
    deuda MONEY
);

CREATE TABLE dbo.FactCompras (
    id_pedido_compra INT FOREIGN KEY REFERENCES dbo.DimPedidoCompra(id_pedido_compra),
    id_metodo_pago INT FOREIGN KEY REFERENCES dbo.DimMetodoPago(id_metodo_pago),
    id_producto INT FOREIGN KEY REFERENCES dbo.DimProducto(id_producto),
    id_proveedor INT FOREIGN KEY REFERENCES dbo.DimProveedor(id_proveedor),
    id_tipo_transaccion INT FOREIGN KEY REFERENCES dbo.DimTipoTransaccion(id_tipo_transaccion),
    fecha_pedido INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_transaccion INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_entrega INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    fecha_entrega_esperada INT FOREIGN KEY REFERENCES dbo.DimFecha(id_fecha),
    precio_unitario_esperado MONEY,
    total_sin_impuesto MONEY,
    monto_impuesto MONEY,
    monto_total_con_impuesto MONEY,
    deuda MONEY
);