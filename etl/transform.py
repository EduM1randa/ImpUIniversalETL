import pandas as pd

def transform_fact_movimiento_inventario(df):
    int_columns = [
        'id_movimiento_inventario',
        'id_producto',
        'id_tipo_transaccion',
        'id_cliente',
        'id_factura',
        'id_proveedor',
        'id_orden_compra',
        'cantidad',
        'fecha_ocurrencia'
    ]
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    return df

def transform_dim_pedido_venta(df):
    int_columns = [
        'id_pedido',
        'id_cliente',
        'id_persona_ventas',
        'id_persona_recolección',
        'id_persona_contacto',
        'id_pedido_pendiente',
        'fecha_pedido',
        'fecha_entrega_esperada',
        'fecha_completado_recolección',
        'fecha_última_modificación',
        'modificado_por'
    ]
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    return df

def transform_fact_ventas(df):
    int_columns = [
        'id_metodo_pago',
        'id_tipo_transaccion',
        'id_producto',
        'id_cliente',
        'id_factura',
        'id_pedido',
        'fecha_pedido',
        'fecha_factura',
        'fecha_transaccion',
        'fecha_entrega',
        'cantidad'
    ]
    float_columns = [
        'precio_unitario',
        'tasa_impuesto',
        'total_sin_impuesto',
        'monto_impuesto',
        'monto_total_con_impuesto',
        'deuda'
    ]
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    for col in float_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def transform_fact_compras(df):
    int_columns = [
        'id_pedido_compra',
        'id_metodo_pago',
        'id_producto',
        'id_proveedor',
        'id_tipo_transaccion',
        'fecha_pedido',
        'fecha_transaccion',
        'fecha_entrega',
        'fecha_entrega_esperada'
    ]
    float_columns = [
        'precio_unitario_esperado',
        'total_sin_impuesto',
        'monto_impuesto',
        'monto_total_con_impuesto',
        'deuda'
    ]
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    for col in float_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df