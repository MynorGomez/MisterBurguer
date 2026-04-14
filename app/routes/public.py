from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from app import mysql
from app.utils.inventario import (
    verificar_stock_carrito,
    descontar_inventario_por_producto,
    descontar_inventario_combo,
    descontar_inventario_personalizado
)
from datetime import datetime
from app.utils.correo import enviar_confirmacion_pedido, enviar_factura_pedido

public = Blueprint('public', __name__)

@public.route('/')
def menu_publico():
    cur = mysql.connection.cursor()

    # Productos individuales (para combos y personalización)
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.imagen, c.nombre
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.estado = 'activo' AND p.disponible = 'si'
        ORDER BY c.nombre, p.nombre
    """)
    productos = cur.fetchall()

    # Combos predefinidos
    cur.execute("""
        SELECT id_combo, nombre, descripcion, precio, imagen
        FROM combos
        WHERE disponible = 'si'
        ORDER BY nombre
    """)
    combos = cur.fetchall()

    # Insumos para personalización
    cur.execute("""
        SELECT id_insumo, nombre, costo_referencia
        FROM insumos
        WHERE estado = 'activo'
        ORDER BY nombre
    """)
    insumos = cur.fetchall()

    # Bebidas de la categoría (id_categoria = 2)
    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        WHERE id_categoria = 2 AND estado = 'activo' AND disponible = 'si'
        ORDER BY nombre
    """)
    bebidas = cur.fetchall()

    # Papas/Acompañamientos de la categoría (id_categoria = 3)
    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        WHERE id_categoria = 3 AND estado = 'activo' AND disponible = 'si'
        ORDER BY nombre
    """)
    papas = cur.fetchall()

    # Filtrar tipos de carne para la selección (insumos que contengan "carne", "pollo", "res", etc.)
    carnes = [i for i in insumos if any(palabra in i[1].lower() for palabra in ['carne', 'pollo', 'res', 'cerdo', 'pavo', 'hamburguesa'])]

    # Hamburguesas originales (mantener por compatibilidad si se necesitan)
    hamburguesas = [p for p in productos if p[5].strip().lower() == 'hamburguesas' and 'combo' not in p[1].strip().lower()]

    cur.close()

    if 'carrito' not in session:
        session['carrito'] = []

    cantidad_carrito = sum(item['cantidad'] for item in session.get('carrito', []))

    return render_template(
        'menu_publico.html',
        productos=productos,
        combos=combos,
        insumos=insumos,
        carnes=carnes,
        hamburguesas=hamburguesas,
        bebidas=bebidas,
        papas=papas,
        cantidad_carrito=cantidad_carrito
    )


@public.route('/agregar_combo/<int:id_combo>', methods=['POST'])
def agregar_combo(id_combo):
    cantidad = int(request.form.get('cantidad', 1))

    if cantidad <= 0:
        flash('La cantidad debe ser mayor a 0.')
        return redirect(url_for('public.menu_publico'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nombre, precio
        FROM combos
        WHERE id_combo = %s AND disponible = 'si'
    """, (id_combo,))
    combo = cur.fetchone()

    if not combo:
        flash('Combo no disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    nombre_combo, precio_combo = combo

    carrito = session.get('carrito', [])

    # Agregar el combo como un item único
    encontrado = False
    for item in carrito:
        if item.get('tipo') == 'combo' and item['id_combo'] == id_combo:
            item['cantidad'] += cantidad
            item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            encontrado = True
            break

    if not encontrado:
        carrito.append({
            'tipo': 'combo',
            'id_combo': id_combo,
            'nombre': nombre_combo,
            'precio': float(precio_combo),
            'cantidad': cantidad,
            'subtotal': round(float(precio_combo) * cantidad, 2)
        })

    session['carrito'] = carrito
    session.modified = True
    cur.close()
    return redirect(url_for('public.menu_publico'))


@public.route('/personalizar_hamburguesa', methods=['POST'])
def personalizar_hamburguesa():
    # Obtener carne por defecto (primera carne disponible)
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_insumo FROM insumos WHERE nombre LIKE '%carne%' AND estado = 'activo' LIMIT 1")
    carne_default = cur.fetchone()
    if not carne_default:
        flash('No hay carne disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))
    base_id = carne_default[0]

    pan = request.form.get('pan', 'normal')
    queso = request.form.get('queso', 'no')
    ingredientes_ids = request.form.getlist('ingredientes')
    papas = request.form.get('papas', 'no')
    bebida = request.form.get('bebida', 'no')
    cantidad = int(request.form.get('cantidad', 1))

    if cantidad <= 0:
        flash('Cantidad inválida.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    cur = mysql.connection.cursor()

    # Obtener carne base
    cur.execute("SELECT nombre, costo_referencia FROM insumos WHERE id_insumo = %s", (base_id,))
    base = cur.fetchone()
    if not base:
        flash('Carne no disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    nombre_base, _ = base

    # Obtener precio de la hamburguesa clásica
    cur.execute("""
        SELECT precio FROM productos 
        WHERE nombre LIKE '%lásica%' AND estado = 'activo' 
        LIMIT 1
    """)
    precio_result = cur.fetchone()
    if precio_result:
        precio_total = float(precio_result[0])
    else:
        # Si no existe hamburguesa clásica, usar el precio del insumo como fallback
        precio_total = float(base[1])

    # Obtener nombres de insumos adicionales para el detalle
    insumos_nombres = []
    for ing_id in ingredientes_ids:
        cur.execute("SELECT nombre FROM insumos WHERE id_insumo = %s", (int(ing_id),))
        ing = cur.fetchone()
        if ing:
            insumos_nombres.append(ing[0])

    cur.close()

    # Construir nombre personalizado
    nombre_personalizado = f"Hamburguesa Personalizada"
    detalles = []

    if pan != 'normal':
        if pan == 'integral':
            detalles.append("Pan Integral")
        elif pan == 'sesamo':
            detalles.append("Pan con Sésamo")

    detalles.append(nombre_base)

    if queso != 'no':
        cur_tmp = mysql.connection.cursor()
        cur_tmp.execute("SELECT nombre FROM insumos WHERE id_insumo = %s", (int(queso),))
        queso_nombre = cur_tmp.fetchone()
        if queso_nombre:
            detalles.append(queso_nombre[0])
        cur_tmp.close()

    if insumos_nombres:
        detalles.extend(insumos_nombres)

    # Agregar papas al detalle
    if papas != 'no':
        cur_papas = mysql.connection.cursor()
        cur_papas.execute("SELECT nombre FROM productos WHERE id_producto = %s", (int(papas),))
        papas_row = cur_papas.fetchone()
        if papas_row:
            detalles.append(papas_row[0])
        cur_papas.close()

    # Agregar bebida al detalle
    if bebida != 'no':
        cur_bebida = mysql.connection.cursor()
        cur_bebida.execute("SELECT nombre FROM productos WHERE id_producto = %s", (int(bebida),))
        bebida_row = cur_bebida.fetchone()
        if bebida_row:
            detalles.append(bebida_row[0])
        cur_bebida.close()

    nombre_personalizado += f": {', '.join(detalles)}"

    # Combinar todos los ingredientes para el carrito
    todos_ingredientes = []
    if queso != 'no':
        todos_ingredientes.append(queso)
    todos_ingredientes.extend(ingredientes_ids)

    carrito = session.get('carrito', [])

    # Agregar como item único
    carrito.append({
        'tipo': 'personalizado',
        'id_base': base_id,
        'pan': pan,
        'queso': queso,
        'ingredientes': todos_ingredientes,
        'papas': papas,
        'bebida': bebida,
        'nombre': nombre_personalizado,
        'precio': float(precio_total),
        'cantidad': cantidad,
        'subtotal': round(float(precio_total) * cantidad, 2)
    })

    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.menu_publico'))


@public.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = round(sum(item['subtotal'] for item in carrito), 2)
    return render_template('carrito.html', carrito=carrito, total=total)





@public.route('/sumar_item/<int:id_producto>')
def sumar_item(id_producto):
    carrito = session.get('carrito', [])

    for item in carrito:
        if item['id_producto'] == id_producto:
            item['cantidad'] += 1
            item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break

    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))


@public.route('/restar_item/<int:id_producto>')
def restar_item(id_producto):
    carrito = session.get('carrito', [])

    for item in carrito:
        if item['id_producto'] == id_producto:
            item['cantidad'] -= 1

            if item['cantidad'] <= 0:
                carrito.remove(item)
            else:
                item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break

    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))


@public.route('/eliminar_item/<int:id_producto>')
def eliminar_item(id_producto):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id_producto'] != id_producto]
    session['carrito'] = carrito
    session.modified = True
    flash('Producto eliminado del carrito.')
    return redirect(url_for('public.ver_carrito'))


@public.route('/vaciar_carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    flash('Carrito vaciado.')
    return redirect(url_for('public.ver_carrito'))


# Rutas para combos en carrito
@public.route('/sumar_combo/<int:id_combo>')
def sumar_combo(id_combo):
    carrito = session.get('carrito', [])
    for item in carrito:
        if item.get('tipo') == 'combo' and item['id_combo'] == id_combo:
            item['cantidad'] += 1
            item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))

@public.route('/restar_combo/<int:id_combo>')
def restar_combo(id_combo):
    carrito = session.get('carrito', [])
    for item in carrito:
        if item.get('tipo') == 'combo' and item['id_combo'] == id_combo:
            item['cantidad'] -= 1
            if item['cantidad'] <= 0:
                carrito.remove(item)
            else:
                item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))

@public.route('/eliminar_combo/<int:id_combo>')
def eliminar_combo(id_combo):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if not (item.get('tipo') == 'combo' and item['id_combo'] == id_combo)]
    session['carrito'] = carrito
    session.modified = True
    flash('Combo eliminado del carrito.')
    return redirect(url_for('public.ver_carrito'))


# Rutas para personalizados en carrito
@public.route('/sumar_personalizado/<int:id_base>')
def sumar_personalizado(id_base):
    pan = request.args.get('pan', 'normal')
    queso = request.args.get('queso', 'no')
    ingredientes = request.args.get('ingredientes', '').split(',')
    carrito = session.get('carrito', [])
    for item in carrito:
        if (item.get('tipo') == 'personalizado' and
            item['id_base'] == id_base and
            item.get('pan', 'normal') == pan and
            item.get('queso', 'no') == queso and
            set(item.get('ingredientes', [])) == set(ingredientes)):
            item['cantidad'] += 1
            item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))

@public.route('/restar_personalizado/<int:id_base>')
def restar_personalizado(id_base):
    pan = request.args.get('pan', 'normal')
    queso = request.args.get('queso', 'no')
    ingredientes = request.args.get('ingredientes', '').split(',')
    carrito = session.get('carrito', [])
    for item in carrito:
        if (item.get('tipo') == 'personalizado' and
            item['id_base'] == id_base and
            item.get('pan', 'normal') == pan and
            item.get('queso', 'no') == queso and
            set(item.get('ingredientes', [])) == set(ingredientes)):
            item['cantidad'] -= 1
            if item['cantidad'] <= 0:
                carrito.remove(item)
            else:
                item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('public.ver_carrito'))

@public.route('/eliminar_personalizado/<int:id_base>')
def eliminar_personalizado(id_base):
    pan = request.args.get('pan', 'normal')
    queso = request.args.get('queso', 'no')
    ingredientes = request.args.get('ingredientes', '').split(',')
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if not (
        item.get('tipo') == 'personalizado' and
        item['id_base'] == id_base and
        item.get('pan', 'normal') == pan and
        item.get('queso', 'no') == queso and
        set(item.get('ingredientes', [])) == set(ingredientes)
    )]
    session['carrito'] = carrito
    session.modified = True
    flash('Hamburguesa personalizada eliminada del carrito.')
    return redirect(url_for('public.ver_carrito'))


@public.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    carrito = session.get('carrito', [])

    if not carrito:
        return jsonify({'error': 'Tu carrito está vacío.'}), 400

    nombre_cliente = request.form.get('nombre_cliente', '').strip()
    correo_cliente = request.form.get('correo_cliente', '').strip()

    if not nombre_cliente:
        return jsonify({'error': 'Debes ingresar tu nombre.'}), 400
    
    if not correo_cliente:
        return jsonify({'error': 'Debes ingresar tu correo.'}), 400

    # Verificar stock antes de confirmar
    stock_ok, mensaje_stock = verificar_stock_carrito(mysql.connection, carrito)
    if not stock_ok:
        return jsonify({'error': mensaje_stock}), 400

    subtotal = round(sum(item['subtotal'] for item in carrito), 2)
    total = subtotal

    numero_pedido = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    cur = mysql.connection.cursor()

    try:
        # 1. Crear pedido
        cur.execute("""
            INSERT INTO pedidos (
                id_cliente,
                nombre_cliente_invitado,
                correo_cliente_invitado,
                numero_pedido,
                tipo_pedido,
                estado,
                fecha_pedido,
                subtotal,
                total
            )
            VALUES (NULL, %s, %s, %s, 'web', 'confirmado', NOW(), %s, %s)
        """, (nombre_cliente, correo_cliente, numero_pedido, subtotal, total))

        id_pedido = cur.lastrowid

        # 2. Detalle del pedido
        for item in carrito:
            # Determinar id_producto basado en el tipo de item
            if item.get('tipo') == 'combo':
                id_prod = item['id_combo']  # Usar id_combo como id_producto
                observaciones = None
            elif item.get('tipo') == 'personalizado':
                id_prod = item['id_base']  # Usar id_base como id_producto
                # Construir observaciones con detalles de personalización
                detalles_pers = []
                if item.get('pan') and item['pan'] != 'normal':
                    detalles_pers.append(f"Pan: {item['pan'].upper()}")
                if item.get('queso') and item['queso'] != 'no':
                    cur_queso = mysql.connection.cursor()
                    cur_queso.execute("SELECT nombre FROM insumos WHERE id_insumo = %s", (int(item['queso']),))
                    queso_row = cur_queso.fetchone()
                    if queso_row:
                        detalles_pers.append(f"Queso: {queso_row[0]}")
                    cur_queso.close()
                
                if item.get('ingredientes'):
                    ingredientes_names = []
                    cur_ing = mysql.connection.cursor()
                    for ing_id in item['ingredientes']:
                        cur_ing.execute("SELECT nombre FROM insumos WHERE id_insumo = %s", (int(ing_id),))
                        ing_row = cur_ing.fetchone()
                        if ing_row:
                            ingredientes_names.append(ing_row[0])
                    cur_ing.close()
                    if ingredientes_names:
                        detalles_pers.append(f"Ingredientes: {', '.join(ingredientes_names)}")
                
                if item.get('papas') and item['papas'] != 'no':
                    cur_papas = mysql.connection.cursor()
                    cur_papas.execute("SELECT nombre FROM productos WHERE id_producto = %s", (int(item['papas']),))
                    papas_row = cur_papas.fetchone()
                    if papas_row:
                        detalles_pers.append(f"Papas: {papas_row[0]}")
                    cur_papas.close()
                
                if item.get('bebida') and item['bebida'] != 'no':
                    cur_bebida = mysql.connection.cursor()
                    cur_bebida.execute("SELECT nombre FROM productos WHERE id_producto = %s", (int(item['bebida']),))
                    bebida_row = cur_bebida.fetchone()
                    if bebida_row:
                        detalles_pers.append(f"Bebida: {bebida_row[0]}")
                    cur_bebida.close()
                
                observaciones = " | ".join(detalles_pers) if detalles_pers else "Personalizado"
            else:
                id_prod = item['id_producto']
                observaciones = None

            cur.execute("""
                INSERT INTO pedido_detalle (
                    id_pedido,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal,
                    observaciones
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_pedido,
                id_prod,
                item['cantidad'],
                item['precio'],
                item['subtotal'],
                observaciones
            ))

        # 3. Crear venta automática
        id_empleado_sistema = 1

        cur.execute("""
            INSERT INTO ventas (
                id_pedido,
                id_cliente,
                id_empleado,
                fecha_venta,
                tipo_venta,
                metodo_pago,
                subtotal,
                total,
                estado
            )
            VALUES (%s, NULL, %s, NOW(), 'pedido_web', 'efectivo', %s, %s, 'pagada')
        """, (id_pedido, id_empleado_sistema, subtotal, total))

        id_venta = cur.lastrowid

        # 4. Detalle de venta
        for item in carrito:
            # Determinar id_producto basado en el tipo de item
            if item.get('tipo') == 'combo':
                id_prod = item['id_combo']  # Usar id_combo como id_producto
            elif item.get('tipo') == 'personalizado':
                id_prod = item['id_base']  # Usar id_base como id_producto
            else:
                id_prod = item['id_producto']

            cur.execute("""
                INSERT INTO venta_detalle (
                    id_venta,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                id_venta,
                id_prod,
                item['cantidad'],
                item['precio'],
                item['subtotal']
            ))

        # 5. Descuento de inventario
        for item in carrito:
            if item.get('tipo') == 'combo':
                descontar_inventario_combo(
                    conexion=mysql.connection,
                    id_combo=item['id_combo'],
                    cantidad_vendida=item['cantidad'],
                    referencia=numero_pedido
                )
            elif item.get('tipo') == 'personalizado':
                descontar_inventario_personalizado(
                    conexion=mysql.connection,
                    id_base=item['id_base'],
                    ingredientes_ids=item.get('ingredientes', []),
                    cantidad_vendida=item['cantidad'],
                    referencia=numero_pedido,
                    papas_id=item.get('papas'),
                    bebida_id=item.get('bebida')
                )
            else:
                # Producto normal
                descontar_inventario_por_producto(
                    conexion=mysql.connection,
                    id_producto=item['id_producto'],
                    cantidad_vendida=item['cantidad'],
                    referencia=numero_pedido
                )

        mysql.connection.commit()

        session['carrito'] = []
        session.modified = True

        # Enviar correo de confirmación al cliente
        detalles_correo = []
        for item in carrito:
            detalles_correo.append({
                'nombre': item['nombre'],
                'cantidad': item['cantidad'],
                'precio': item['precio'],
                'subtotal': item['subtotal']
            })
        
        # Enviar correo (de forma asíncrona en producción)
        try:
            # Construir URL de seguimiento del pedido
            url_seguimiento = request.url_root.rstrip('/') + url_for('public.estado_pedido', numero_pedido=numero_pedido)
            
            enviar_confirmacion_pedido(
                nombre_cliente=nombre_cliente,
                correo_cliente=correo_cliente,
                numero_pedido=numero_pedido,
                total=total,
                detalles=detalles_correo,
                url_seguimiento=url_seguimiento
            )
        except Exception as e:
            print(f"Error al enviar correo: {str(e)}")

        # Devolver JSON en lugar de redirigir
        return jsonify({
            'numero_pedido': numero_pedido,
            'estado': 'confirmado',
            'total': total,
            'nombre': nombre_cliente,
            'correo': correo_cliente,
            'items': carrito
        })

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': f'Error al confirmar pedido: {str(e)}'}), 500
    finally:
        cur.close()


@public.route('/pedido/<numero_pedido>')
def estado_pedido(numero_pedido):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado,
               correo_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE numero_pedido = %s
    """, (numero_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        cur.close()
        flash('Pedido no encontrado.')
        return redirect(url_for('public.menu_publico'))

    cur.execute("""
        SELECT pd.cantidad, p.nombre, pd.precio_unitario, pd.subtotal
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (pedido[0],))
    detalles = cur.fetchall()
    cur.close()

    return render_template('estado_pedido_cliente.html', pedido=pedido, detalles=detalles)


# API REST para auto-actualización de pedidos
@public.route('/api/pedidos_cocina', methods=['GET'])
def api_pedidos_cocina():
    """API para obtener pedidos activos en formato JSON"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE estado IN ('confirmado', 'en_preparacion', 'listo')
        ORDER BY fecha_pedido ASC
    """)
    pedidos = cur.fetchall()
    cur.close()

    # Convertir a formato JSON
    pedidos_json = []
    for p in pedidos:
        pedidos_json.append({
            'id': p[0],
            'numero': p[1],
            'cliente': p[2],
            'estado': p[3],
            'fecha': str(p[4]),
            'total': float(p[5])
        })

    return jsonify(pedidos_json)


# Ruta para obtener estado actualizado de un pedido específico
@public.route('/api/pedido/<numero_pedido>', methods=['GET'])
def api_estado_pedido(numero_pedido):
    """API para obtener estado actualizado de un pedido"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado,
               correo_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE numero_pedido = %s
    """, (numero_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        cur.close()
        return jsonify({'error': 'Pedido no encontrado'}), 404

    cur.execute("""
        SELECT pd.cantidad, p.nombre, pd.precio_unitario, pd.subtotal
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (pedido[0],))
    detalles = cur.fetchall()
    cur.close()

    return jsonify({
        'id': pedido[0],
        'numero': pedido[1],
        'cliente': pedido[2],
        'correo': pedido[3],
        'estado': pedido[4],
        'fecha': str(pedido[5]),
        'total': float(pedido[6]),
        'detalles': [
            {
                'cantidad': d[0],
                'nombre': d[1],
                'precio': float(d[2]),
                'subtotal': float(d[3])
            } for d in detalles
        ]
    })


# Ruta para generar factura en PDF o HTML
@public.route('/factura/<numero_pedido>')
def factura_pedido(numero_pedido):
    """Genera y muestra la factura del pedido"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado,
               correo_cliente_invitado, estado, fecha_pedido, total, subtotal
        FROM pedidos
        WHERE numero_pedido = %s
    """, (numero_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        cur.close()
        flash('Pedido no encontrado.')
        return redirect(url_for('public.menu_publico'))

    cur.execute("""
        SELECT pd.cantidad, p.nombre, pd.precio_unitario, pd.subtotal, pd.observaciones
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (pedido[0],))
    detalles = cur.fetchall()
    cur.close()

    return render_template('factura.html', pedido=pedido, detalles=detalles)