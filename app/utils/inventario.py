# ==============================
# VERIFICAR STOCK SUFICIENTE
# ==============================
def verificar_stock_suficiente(conexion, id_producto, cantidad_solicitada):
    cur = conexion.cursor()

    cur.execute("""
        SELECT r.id_insumo, i.nombre, i.stock_actual, r.cantidad
        FROM recetas r
        INNER JOIN insumos i ON r.id_insumo = i.id_insumo
        WHERE r.id_producto = %s
    """, (id_producto,))
    receta = cur.fetchall()

    for id_insumo, nombre_insumo, stock_actual, cantidad_receta in receta:
        stock_requerido = float(cantidad_receta) * float(cantidad_solicitada)

        if float(stock_actual) < stock_requerido:
            cur.close()
            return False, (
                f"No hay suficiente stock para '{nombre_insumo}'. "
                f"Disponible: {stock_actual}, requerido: {stock_requerido}"
            )

    cur.close()
    return True, None


# ==============================
# VERIFICAR CARRITO COMPLETO
# ==============================
def verificar_stock_carrito(conexion, carrito):
    for item in carrito:
        if item.get('tipo') == 'combo':
            # Verificar stock para cada producto del combo
            ok, mensaje = verificar_stock_combo(conexion, item['id_combo'], item['cantidad'])
            if not ok:
                return False, f"Combo '{item['nombre']}': {mensaje}"
        elif item.get('tipo') == 'personalizado':
            # Verificar stock para base e ingredientes
            ok, mensaje = verificar_stock_personalizado(conexion, item['id_base'], item.get('ingredientes', []), item['cantidad'])
            if not ok:
                return False, f"Personalizado '{item['nombre']}': {mensaje}"
        else:
            # Producto normal
            ok, mensaje = verificar_stock_suficiente(
                conexion=conexion,
                id_producto=item['id_producto'],
                cantidad_solicitada=item['cantidad']
            )
            if not ok:
                return False, f"Producto '{item['nombre']}': {mensaje}"

    return True, None


# ==============================
# VERIFICAR STOCK DE COMBO
# ==============================
def verificar_stock_combo(conexion, id_combo, cantidad_solicitada):
    cur = conexion.cursor()

    cur.execute("""
        SELECT cd.id_producto, p.nombre, cd.cantidad
        FROM combo_detalle cd
        INNER JOIN productos p ON cd.id_producto = p.id_producto
        WHERE cd.id_combo = %s
    """, (id_combo,))
    productos_combo = cur.fetchall()
    cur.close()

    for id_producto, nombre_producto, cantidad_por_combo in productos_combo:
        cantidad_total = float(cantidad_por_combo) * float(cantidad_solicitada)
        ok, mensaje = verificar_stock_suficiente(conexion, id_producto, cantidad_total)
        if not ok:
            return False, f"Producto '{nombre_producto}': {mensaje}"

    return True, None


# ==============================
# VERIFICAR STOCK DE PERSONALIZADO
# ==============================
def verificar_stock_personalizado(conexion, id_base, ingredientes_ids, cantidad_solicitada):
    # Verificar stock del insumo base (carne)
    cur = conexion.cursor()
    cur.execute("""
        SELECT nombre, stock_actual
        FROM insumos
        WHERE id_insumo = %s
    """, (int(id_base),))
    insumo_base = cur.fetchone()
    
    if insumo_base:
        nombre_base, stock_actual = insumo_base
        if float(stock_actual) < float(cantidad_solicitada):
            cur.close()
            return False, f"Insumo '{nombre_base}': stock insuficiente"

    # Verificar stock de insumos adicionales
    for ing_id in ingredientes_ids:
        cur.execute("""
            SELECT nombre, stock_actual
            FROM insumos
            WHERE id_insumo = %s
        """, (int(ing_id),))
        insumo = cur.fetchone()
        if insumo:
            nombre_insumo, stock_actual = insumo
            if float(stock_actual) < float(cantidad_solicitada):
                cur.close()
                return False, f"Insumo '{nombre_insumo}': stock insuficiente"
    cur.close()

    return True, None


# ==============================
# DESCONTAR INVENTARIO
# ==============================
def descontar_inventario_por_producto(conexion, id_producto, cantidad_vendida, referencia):
    cur = conexion.cursor()

    cur.execute("""
        SELECT id_insumo, cantidad
        FROM recetas
        WHERE id_producto = %s
    """, (id_producto,))
    receta = cur.fetchall()

    for id_insumo, cantidad_receta in receta:
        cantidad_total_descontar = float(cantidad_receta) * float(cantidad_vendida)

        cur.execute("""
            UPDATE insumos
            SET stock_actual = stock_actual - %s
            WHERE id_insumo = %s
        """, (cantidad_total_descontar, id_insumo))

        cur.execute("""
            INSERT INTO movimientos_inventario (
                id_insumo,
                tipo_movimiento,
                cantidad,
                referencia,
                observacion,
                fecha_movimiento
            )
        """, (id_insumo, cantidad_total_descontar, referencia))

    cur.close()


# ==============================
# DESCONTAR INVENTARIO DE COMBO
# ==============================
def descontar_inventario_combo(conexion, id_combo, cantidad_vendida, referencia):
    cur = conexion.cursor()

    cur.execute("""
        SELECT cd.id_producto, cd.cantidad
        FROM combo_detalle cd
        WHERE cd.id_combo = %s
    """, (id_combo,))
    productos_combo = cur.fetchall()
    cur.close()

    for id_producto, cantidad_por_combo in productos_combo:
        cantidad_total = float(cantidad_por_combo) * float(cantidad_vendida)
        descontar_inventario_por_producto(conexion, id_producto, cantidad_total, referencia)


# ==============================
# DESCONTAR INVENTARIO DE PERSONALIZADO
# ==============================
def descontar_inventario_personalizado(conexion, id_base, ingredientes_ids, cantidad_vendida, referencia, papas_id=None, bebida_id=None):
    cur = conexion.cursor()
    
    # Descontar insumo base (carne)
    cur.execute("""
        UPDATE insumos
        SET stock_actual = stock_actual - %s
        WHERE id_insumo = %s
    """, (cantidad_vendida, int(id_base)))

    cur.execute("""
        INSERT INTO movimientos_inventario (
            id_insumo,
            tipo_movimiento,
            cantidad,
            referencia,
            observacion,
            fecha_movimiento
        )
        VALUES (%s, 'salida_venta', %s, %s, 'Descuento carne personalizado', NOW())
    """, (int(id_base), cantidad_vendida, referencia))

    # Descontar ingredientes adicionales
    for ing_id in ingredientes_ids:
        # ing_id es el id_insumo directamente
        id_insumo = int(ing_id)
        # Descontar 1 unidad por ingrediente por cantidad vendida
        cur.execute("""
            UPDATE insumos
            SET stock_actual = stock_actual - %s
            WHERE id_insumo = %s
        """, (cantidad_vendida, id_insumo))

        cur.execute("""
            INSERT INTO movimientos_inventario (
                id_insumo,
                tipo_movimiento,
                cantidad,
                referencia,
                observacion,
                fecha_movimiento
            )
            VALUES (%s, 'salida_venta', %s, %s, 'Descuento ingrediente personalizado', NOW())
        """, (id_insumo, cantidad_vendida, referencia))
    
    # Descontar papas si se seleccionaron
    if papas_id and papas_id != 'no':
        try:
            descontar_inventario_por_producto(conexion, int(papas_id), cantidad_vendida, referencia)
        except:
            pass  # Si no hay receta para papas, continuar sin error
    
    # Descontar bebida si se seleccionó
    if bebida_id and bebida_id != 'no':
        try:
            descontar_inventario_por_producto(conexion, int(bebida_id), cantidad_vendida, referencia)
        except:
            pass  # Si no hay receta para bebida, continuar sin error
    
    cur.close()