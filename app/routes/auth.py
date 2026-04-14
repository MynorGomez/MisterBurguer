from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import mysql
from functools import wraps
from app import mysql
auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles_permitidos):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'rol' not in session:
                flash('Acceso no autorizado.')
                return redirect(url_for('auth.login'))

            if session['rol'] not in roles_permitidos:
                flash('No tienes permiso para acceder a esta sección.')
                return redirect(url_for('auth.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        cur = mysql.connection.cursor()
        cur.execute("""
    SELECT 
        u.id_usuario, 
        u.username, 
        u.password_hash, 
        r.nombre AS rol,
        e.nombres,
        e.apellidos
    FROM usuarios u
    INNER JOIN roles r ON u.id_rol = r.id_rol
    LEFT JOIN empleados e ON u.id_usuario = e.id_usuario
    WHERE u.username = %s AND u.estado = 'activo'
""", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            id_usuario, username_db, password_hash, rol, nombres, apellidos = user
            if check_password_hash(password_hash, password):
                nombre_completo = ""

                if nombres and apellidos:
                    nombre_completo = f"{nombres} {apellidos}"
                else:
                    nombre_completo = username_db  # fallback

                session['user_id'] = id_usuario
                session['username'] = username_db
                session['rol'] = rol
                session['nombre'] = nombre_completo
                session['user_id'] = id_usuario
                session['username'] = username_db
                session['rol'] = rol

                flash('Bienvenido al sistema.')
                return redirect(url_for('auth.dashboard'))
            else:
                flash('Contraseña incorrecta.')
        else:
            flash('Usuario no encontrado.')

    return render_template('login.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    from datetime import datetime
    cur = mysql.connection.cursor()
    
    # Obtener ventas del mes actual
    mes_actual = datetime.now().strftime('%Y-%m')
    cur.execute("""
        SELECT DATE(fecha_venta) as fecha, SUM(total) as total
        FROM ventas
        WHERE DATE_FORMAT(fecha_venta, '%%Y-%%m') = %s
        GROUP BY DATE(fecha_venta)
        ORDER BY fecha ASC
    """, (mes_actual,))
    ventas_mes = cur.fetchall()
    
    # Obtener compras del mes actual
    cur.execute("""
        SELECT DATE(fecha_compra) as fecha, SUM(total) as total
        FROM compras
        WHERE DATE_FORMAT(fecha_compra, '%%Y-%%m') = %s
        GROUP BY DATE(fecha_compra)
        ORDER BY fecha ASC
    """, (mes_actual,))
    compras_mes = cur.fetchall()
    
    # Total ventas del mes
    cur.execute("SELECT SUM(total) FROM ventas WHERE DATE_FORMAT(fecha_venta, '%%Y-%%m') = %s", (mes_actual,))
    total_ventas_mes = cur.fetchone()[0] or 0
    
    # Total compras del mes
    cur.execute("SELECT SUM(total) FROM compras WHERE DATE_FORMAT(fecha_compra, '%%Y-%%m') = %s", (mes_actual,))
    total_compras_mes = cur.fetchone()[0] or 0
    
    # Cantidad de pedidos del mes
    cur.execute("SELECT COUNT(*) FROM pedidos WHERE DATE_FORMAT(fecha_pedido, '%%Y-%%m') = %s", (mes_actual,))
    cantidad_pedidos = cur.fetchone()[0] or 0
    
    # Ventas por estado
    cur.execute("""
        SELECT estado, COUNT(*) as cantidad
        FROM pedidos
        WHERE DATE_FORMAT(fecha_pedido, '%%Y-%%m') = %s
        GROUP BY estado
    """, (mes_actual,))
    pedidos_por_estado = cur.fetchall()
    
    cur.close()
    
    # Preparar datos para gráficos
    fechas_ventas = [v[0].strftime('%d/%m') if v[0] else '' for v in ventas_mes]
    totales_ventas = [float(v[1]) if v[1] else 0 for v in ventas_mes]
    
    fechas_compras = [c[0].strftime('%d/%m') if c[0] else '' for c in compras_mes]
    totales_compras = [float(c[1]) if c[1] else 0 for c in compras_mes]
    
    estados = [p[0] for p in pedidos_por_estado]
    cantidades_estados = [p[1] for p in pedidos_por_estado]
    
    return render_template('dashboard.html', 
                          total_ventas_mes=float(total_ventas_mes),
                          total_compras_mes=float(total_compras_mes),
                          cantidad_pedidos=cantidad_pedidos,
                          fechas_ventas=fechas_ventas,
                          totales_ventas=totales_ventas,
                          fechas_compras=fechas_compras,
                          totales_compras=totales_compras,
                          estados=estados,
                          cantidades_estados=cantidades_estados)

@auth.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('auth.login'))