from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app import mysql
from app.routes.auth import login_required, roles_required

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/dashboard')
@login_required
@roles_required('administrador')
def dashboard_admin():
    cur = mysql.connection.cursor()

    # Total ventas
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(total), 0)
        FROM ventas
        WHERE estado = 'pagada'
    """)
    ventas_resumen = cur.fetchone()

    total_ventas = ventas_resumen[0]
    monto_ventas = float(ventas_resumen[1])


    # Total compras
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(total), 0)
        FROM compras
        WHERE estado = 'registrada'
    """)
    compras_resumen = cur.fetchone()

    total_compras = compras_resumen[0]
    monto_compras = float(compras_resumen[1])

    # Total empleados
    cur.execute("""
        SELECT COUNT(*)
        FROM empleados
        WHERE estado = 'activo'
    """)
    total_empleados = cur.fetchone()[0]

    # Total proveedores
    cur.execute("""
        SELECT COUNT(*)
        FROM proveedores
        WHERE estado = 'activo'
    """)
    total_proveedores = cur.fetchone()[0]

    # Stock bajo
    cur.execute("""
        SELECT COUNT(*)
        FROM insumos
        WHERE estado = 'activo' AND stock_actual <= stock_minimo
    """)
    stock_bajo = cur.fetchone()[0]

    # Últimas ventas
    cur.execute("""
        SELECT v.id_venta, v.fecha_venta, v.total, p.numero_pedido
        FROM ventas v
        LEFT JOIN pedidos p ON v.id_pedido = p.id_pedido
        WHERE v.estado = 'pagada'
        ORDER BY v.fecha_venta DESC
        LIMIT 5
    """)
    ultimas_ventas = cur.fetchall()

    # Últimos pedidos
    cur.execute("""
        SELECT numero_pedido, nombre_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        ORDER BY fecha_pedido DESC
        LIMIT 5
    """)
    ultimos_pedidos = cur.fetchall()

    cur.close()

    return render_template(
        'admin/dashboard_admin.html',
        total_ventas=total_ventas,
        monto_ventas=monto_ventas,
        total_compras=total_compras,
        monto_compras=monto_compras,
        total_empleados=total_empleados,
        total_proveedores=total_proveedores,
        stock_bajo=stock_bajo,
        ultimas_ventas=ultimas_ventas,
        ultimos_pedidos=ultimos_pedidos
    )


@admin.route('/ventas')
@login_required
@roles_required('administrador', 'cajero')
def listar_ventas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT v.id_venta, v.fecha_venta, v.tipo_venta, v.metodo_pago,
               v.total, v.estado, p.numero_pedido
        FROM ventas v
        LEFT JOIN pedidos p ON v.id_pedido = p.id_pedido
        ORDER BY v.fecha_venta DESC
    """)
    ventas = cur.fetchall()
    cur.close()

    return render_template('admin/ventas.html', ventas=ventas)


@admin.route('/estado-pedidos')
@login_required
@roles_required('administrador', 'cajero')
def listar_estado_pedidos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, telefono_cliente_invitado,
               estado, fecha_pedido, total
        FROM pedidos
        ORDER BY fecha_pedido DESC
    """)
    pedidos = cur.fetchall()
    cur.close()

    return render_template('admin/estado_pedidos.html', pedidos=pedidos)


@admin.route('/inventario')
@login_required
@roles_required('administrador')
def listar_inventario():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.id_insumo, i.nombre, u.abreviatura, i.stock_actual,
               i.stock_minimo, i.costo_referencia, i.estado
        FROM insumos i
        INNER JOIN unidades_medida u ON i.id_unidad = u.id_unidad
        ORDER BY i.nombre ASC
    """)
    insumos = cur.fetchall()
    cur.close()

    return render_template('admin/inventario.html', insumos=insumos)


@admin.route('/proveedores')
@login_required
@roles_required('administrador')
def listar_proveedores():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_proveedor, nombre_empresa, contacto_nombre, telefono,
               correo, nit, estado
        FROM proveedores
        ORDER BY nombre_empresa ASC
    """)
    proveedores = cur.fetchall()
    cur.close()

    return render_template('admin/proveedores.html', proveedores=proveedores)


@admin.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_proveedor():
    if request.method == 'POST':
        nombre_empresa = request.form['nombre_empresa'].strip()
        contacto_nombre = request.form['contacto_nombre'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()
        nit = request.form['nit'].strip()

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO proveedores (
                nombre_empresa, contacto_nombre, telefono,
                correo, direccion, nit, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'activo')
        """, (nombre_empresa, contacto_nombre, telefono, correo, direccion, nit))
        mysql.connection.commit()
        cur.close()

        flash('Proveedor creado correctamente.')
        return redirect(url_for('admin.listar_proveedores'))

    return render_template('admin/proveedor_form.html', proveedor=None)


@admin.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_proveedor(id_proveedor):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre_empresa = request.form['nombre_empresa'].strip()
        contacto_nombre = request.form['contacto_nombre'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()
        nit = request.form['nit'].strip()
        estado = request.form['estado'].strip()

        cur.execute("""
            UPDATE proveedores
            SET nombre_empresa=%s, contacto_nombre=%s, telefono=%s,
                correo=%s, direccion=%s, nit=%s, estado=%s
            WHERE id_proveedor=%s
        """, (nombre_empresa, contacto_nombre, telefono, correo, direccion, nit, estado, id_proveedor))
        mysql.connection.commit()
        cur.close()

        flash('Proveedor actualizado correctamente.')
        return redirect(url_for('admin.listar_proveedores'))

    cur.execute("""
        SELECT id_proveedor, nombre_empresa, contacto_nombre, telefono,
               correo, direccion, nit, estado
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))
    proveedor = cur.fetchone()
    cur.close()

    return render_template('admin/proveedor_form.html', proveedor=proveedor)

@admin.route('/compras')
@login_required
@roles_required('administrador')
def listar_compras():
    """Lista todas las compras registradas"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.id_compra, c.numero_factura, p.nombre_empresa, 
               c.fecha_compra, c.subtotal, c.total, c.estado
        FROM compras c
        INNER JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        ORDER BY c.fecha_compra DESC
    """)
    compras = cur.fetchall()
    cur.close()

    return render_template('admin/compras.html', compras=compras)


@admin.route('/compras/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_compra():
    """Crear nueva compra de insumos"""
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        id_proveedor = int(request.form['id_proveedor'])
        fecha_compra = request.form['fecha_compra']
        numero_factura = request.form['numero_factura'].strip()
        
        # Obtener items de la compra
        items_json = request.form.get('items_json', '[]')
        import json
        try:
            items = json.loads(items_json)
        except:
            items = []

        if not items or len(items) == 0:
            flash('Debe agregar al menos un insumo.')
            cur.close()
            return redirect(url_for('admin.nueva_compra'))

        try:
            # Calcular total
            subtotal = sum(item['cantidad'] * item['costo_unitario'] for item in items)
            total = subtotal  # Sin impuestos por ahora
            
            # Obtener id_empleado de la sesión
            id_empleado = session.get('user_id', 1)

            # INSERTAR COMPRA
            cur.execute("""
                INSERT INTO compras (
                    id_proveedor, id_empleado, numero_factura, 
                    fecha_compra, subtotal, total, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'registrada')
            """, (id_proveedor, id_empleado, numero_factura, fecha_compra, subtotal, total))
            mysql.connection.commit()

            # Obtener ID de compra creada
            id_compra = cur.lastrowid

            # INSERTAR DETALLES DE COMPRA
            for item in items:
                id_insumo = int(item['id_insumo'])
                cantidad = float(item['cantidad'])
                costo_unitario = float(item['costo_unitario'])
                item_subtotal = cantidad * costo_unitario

                # Insertar detalle
                cur.execute("""
                    INSERT INTO compras_detalle (
                        id_compra, id_insumo, cantidad, costo_unitario, subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_compra, id_insumo, cantidad, costo_unitario, item_subtotal))

                # ACTUALIZAR STOCK del insumo
                cur.execute("""
                    UPDATE insumos
                    SET stock_actual = stock_actual + %s
                    WHERE id_insumo = %s
                """, (cantidad, id_insumo))

                # REGISTRAR MOVIMIENTO en auditoría
                cur.execute("""
                    INSERT INTO movimientos_inventario (
                        id_insumo, tipo_movimiento, cantidad, 
                        referencia, observacion, fecha_movimiento
                    )
                    VALUES (%s, 'entrada_compra', %s, %s, 'Entrada por compra', NOW())
                """, (id_insumo, cantidad, numero_factura))

            mysql.connection.commit()
            flash('Compra registrada correctamente.')
            return redirect(url_for('admin.listar_compras'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al registrar compra: {str(e)}')
        finally:
            cur.close()

    # GET: Cargar formulario
    cur = mysql.connection.cursor()
    
    # Obtener proveedores
    cur.execute("""
        SELECT id_proveedor, nombre_empresa 
        FROM proveedores 
        WHERE estado = 'activo'
        ORDER BY nombre_empresa ASC
    """)
    proveedores = cur.fetchall()

    # Obtener insumos
    cur.execute("""
        SELECT id_insumo, nombre, costo_referencia 
        FROM insumos 
        WHERE estado = 'activo'
        ORDER BY nombre ASC
    """)
    insumos = cur.fetchall()
    cur.close()

    from datetime import date
    today = date.today().isoformat()

    return render_template('admin/compra_form.html', 
                          proveedores=proveedores, 
                          insumos=insumos,
                          today=today)


@admin.route('/compras/editar/<int:id_compra>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_compra(id_compra):
    """Editar compra (solo si no está pagada)"""
    cur = mysql.connection.cursor()

    # Obtener compra
    cur.execute("""
        SELECT id_compra, id_proveedor, numero_factura, fecha_compra, total, estado
        FROM compras
        WHERE id_compra = %s
    """, (id_compra,))
    compra = cur.fetchone()

    if not compra:
        flash('Compra no encontrada.')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    # No permitir editar si está anulada
    if compra[5] == 'anulada':
        flash('No puedes editar una compra anulada.')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    if request.method == 'POST':
        id_proveedor = int(request.form['id_proveedor'])
        numero_factura = request.form['numero_factura'].strip()
        fecha_compra = request.form['fecha_compra']
        estado = request.form['estado'].strip()

        try:
            cur.execute("""
                UPDATE compras
                SET id_proveedor=%s, numero_factura=%s, 
                    fecha_compra=%s, estado=%s
                WHERE id_compra=%s
            """, (id_proveedor, numero_factura, fecha_compra, estado, id_compra))
            mysql.connection.commit()

            flash('Compra actualizada correctamente.')
            return redirect(url_for('admin.listar_compras'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar compra: {str(e)}')
        finally:
            cur.close()

    # GET: Cargar datos
    cur = mysql.connection.cursor()

    # Obtener proveedores
    cur.execute("""
        SELECT id_proveedor, nombre_empresa 
        FROM proveedores 
        WHERE estado = 'activo'
        ORDER BY nombre_empresa ASC
    """)
    proveedores = cur.fetchall()

    # Obtener detalles de compra
    cur.execute("""
        SELECT cd.id_insumo, i.nombre, cd.cantidad, cd.costo_unitario, cd.subtotal
        FROM compras_detalle cd
        INNER JOIN insumos i ON cd.id_insumo = i.id_insumo
        WHERE cd.id_compra = %s
    """, (id_compra,))
    detalles = cur.fetchall()

    # Obtener insumos
    cur.execute("""
        SELECT id_insumo, nombre, costo_referencia 
        FROM insumos 
        WHERE estado = 'activo'
        ORDER BY nombre ASC
    """)
    insumos = cur.fetchall()
    cur.close()

    return render_template('admin/compra_form.html', 
                          compra=compra, 
                          detalles=detalles,
                          proveedores=proveedores,
                          insumos=insumos)


@admin.route('/compras/eliminar/<int:id_compra>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_compra(id_compra):
    """Eliminar compra (solo si está en estado 'registrada')"""
    cur = mysql.connection.cursor()

    # Obtener compra
    cur.execute("""
        SELECT id_compra, estado
        FROM compras
        WHERE id_compra = %s
    """, (id_compra,))
    compra = cur.fetchone()

    if not compra:
        flash('Compra no encontrada.')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    if compra[1] != 'registrada':
        flash('Solo puedes eliminar compras en estado "registrada".')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    try:
        # Obtener detalles de compra para revertir stock
        cur.execute("""
            SELECT id_insumo, cantidad
            FROM compras_detalle
            WHERE id_compra = %s
        """, (id_compra,))
        detalles = cur.fetchall()

        # Revertir stock
        for id_insumo, cantidad in detalles:
            cur.execute("""
                UPDATE insumos
                SET stock_actual = stock_actual - %s
                WHERE id_insumo = %s
            """, (cantidad, id_insumo))

        # Eliminar detalles de compra
        cur.execute("DELETE FROM compras_detalle WHERE id_compra = %s", (id_compra,))

        # Eliminar compra
        cur.execute("DELETE FROM compras WHERE id_compra = %s", (id_compra,))
        
        mysql.connection.commit()
        flash('Compra eliminada correctamente (stock revertido).')

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar compra: {str(e)}')
    finally:
        cur.close()

    return redirect(url_for('admin.listar_compras'))


@admin.route('/empleados')
@login_required
@roles_required('administrador')

def listar_empleados():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_empleado, nombres, apellidos, dpi, telefono, direccion, puesto, salario, fecha_contratacion, estado
        FROM empleados
        ORDER BY nombres ASC
    """)
    empleados = cur.fetchall()
    cur.close()

    return render_template('admin/empleados.html', empleados=empleados)


@admin.route('/empleados/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_empleado():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        correo = request.form['correo'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        dpi = request.form['dpi'].strip() if request.form['dpi'].strip() else None
        telefono = request.form['telefono'].strip() if request.form['telefono'].strip() else None
        direccion = request.form['direccion'].strip() if request.form['direccion'].strip() else None
        puesto = int(request.form['puesto']) if request.form['puesto'].strip() else None
        salario = request.form['salario'] if request.form['salario'] else None
        fecha_contratacion = request.form['fecha_contratacion'] if request.form['fecha_contratacion'] else None

        try:
            # Hashear la contraseña
            password_hash = generate_password_hash(password)
            
            # Crear usuario primero
            cur.execute("""
                INSERT INTO usuarios (username, correo, password_hash, id_rol)
                VALUES (%s, %s, %s, %s)
            """, (username, correo, password_hash, puesto))
            mysql.connection.commit()
            
            # Obtener el id_usuario creado
            cur.execute("SELECT id_usuario FROM usuarios WHERE username = %s", (username,))
            usuario_resultado = cur.fetchone()
            id_usuario = usuario_resultado[0] if usuario_resultado else None
            
            if id_usuario:
                # Crear empleado con el id_usuario
                cur.execute("""
                    INSERT INTO empleados (
                        id_usuario, nombres, apellidos, dpi, telefono, direccion,
                        puesto, salario, fecha_contratacion, estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'activo')
                """, (id_usuario, nombres, apellidos, dpi, telefono, direccion, puesto, salario, fecha_contratacion))
                mysql.connection.commit()
            else:
                flash('Error: No se pudo crear el usuario')
                
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al crear empleado: {str(e)}')
        finally:
            cur.close()

        return redirect(url_for('admin.listar_empleados'))

    # Obtener lista de roles
    cur.execute("SELECT id_rol, nombre FROM roles ORDER BY nombre ASC")
    roles = cur.fetchall()
    cur.close()
    
    return render_template('admin/empleado_form.html', empleado=None, roles=roles)


@admin.route('/empleados/editar/<int:id_empleado>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_empleado(id_empleado):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        dpi = request.form['dpi'].strip() if request.form['dpi'].strip() else None
        telefono = request.form['telefono'].strip() if request.form['telefono'].strip() else None
        direccion = request.form['direccion'].strip() if request.form['direccion'].strip() else None
        puesto = request.form['puesto'].strip() if request.form['puesto'].strip() else None
        salario = request.form['salario'] if request.form['salario'] else None
        fecha_contratacion = request.form['fecha_contratacion'] if request.form['fecha_contratacion'] else None
        estado = request.form['estado'].strip()

        try:
            cur.execute("""
                UPDATE empleados
                SET nombres=%s, apellidos=%s, dpi=%s, telefono=%s,
                    direccion=%s, puesto=%s, salario=%s, fecha_contratacion=%s, estado=%s
                WHERE id_empleado=%s
            """, (nombres, apellidos, dpi, telefono, direccion, puesto, salario, fecha_contratacion, estado, id_empleado))
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar empleado: {str(e)}')
        finally:
            cur.close()

        return redirect(url_for('admin.listar_empleados'))

    cur.execute("""
        SELECT id_empleado, nombres, apellidos, dpi, telefono, direccion, puesto, salario, fecha_contratacion, estado
        FROM empleados
        WHERE id_empleado = %s
    """, (id_empleado,))
    empleado = cur.fetchone()
    
    # Obtener lista de roles
    cur.execute("SELECT id_rol, nombre FROM roles ORDER BY nombre ASC")
    roles = cur.fetchall()
    cur.close()

    return render_template('admin/empleado_form.html', empleado=empleado, roles=roles)