from flask import Blueprint, render_template, redirect, url_for, flash
from app import mysql
from app.routes.auth import login_required, roles_required

cocina = Blueprint('cocina', __name__)

@cocina.route('/cocina/pedidos')
@login_required
@roles_required('cocina', 'administrador')
def lista_pedidos_cocina():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE estado IN ('confirmado', 'en_preparacion', 'listo')
        ORDER BY fecha_pedido ASC
    """)
    pedidos = cur.fetchall()
    cur.close()

    return render_template('cocina_pedidos.html', pedidos=pedidos)


@cocina.route('/cocina/pedido/<int:id_pedido>')
@login_required
@roles_required('cocina', 'administrador')
def detalle_pedido_cocina(id_pedido):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE id_pedido = %s
    """, (id_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        cur.close()
        flash('Pedido no encontrado.')
        return redirect(url_for('cocina.lista_pedidos_cocina'))

    cur.execute("""
        SELECT p.nombre, pd.cantidad, pd.observaciones
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (id_pedido,))
    detalles = cur.fetchall()

    cur.close()
    return render_template('cocina_detalle.html', pedido=pedido, detalles=detalles)


@cocina.route('/cocina/cambiar_estado/<int:id_pedido>/<string:nuevo_estado>')
@login_required
@roles_required('cocina', 'administrador')
def cambiar_estado_pedido(id_pedido, nuevo_estado):
    estados_validos = ['en_preparacion', 'listo', 'entregado']

    if nuevo_estado not in estados_validos:
        flash('Estado no válido.')
        return redirect(url_for('cocina.lista_pedidos_cocina'))

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE pedidos
        SET estado = %s
        WHERE id_pedido = %s
    """, (nuevo_estado, id_pedido))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cocina.lista_pedidos_cocina'))