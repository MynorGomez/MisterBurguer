# 🎯 MISTERBURGER - DOCUMENTACIÓN MASTER COMPLETA

**Versión: 1.0 - Fecha: 2026-04-01**

## 📚 ÍNDICE GENERAL

1. [Configuración y Setup](#configuración-y-setup)
2. [Módulo PUBLIC - Cliente](#módulo-público---cliente)
3. [Módulo AUTH - Autenticación](#módulo-auth---autenticación)
4. [Módulo ADMIN - Administrador](#módulo-admin---administrador)
5. [Módulo COCINA - Panel de Cocina](#módulo-cocina---panel-de-cocina)
6. [Sistema de Inventario](#sistema-de-inventario-completo)
7. [Base de Datos](#esquema-de-base-de-datos)
8. [Roles y Permisos](#roles-y-permisos)
9. [Manejo de Errores](#manejo-de-errores)

---

## 🔧 Configuración y Setup

### Archivo: `app/config.py`

```python
class Config:
    SECRET_KEY = 'tu_clave_super_segura_2025'          # Clave para cifrar sesiones
    MYSQL_HOST = 'localhost'                             # Host de BD
    MYSQL_USER = 'root'                                  # Usuario BD
    MYSQL_PASSWORD = 'Minato15@'                         # Contraseña BD
    MYSQL_DB = 'restaurante'                             # Nombre de BD
```

**¿Qué hace?**
- Define dónde está la BD
- Define credenciales de acceso
- Define clave secreta para Flask

**Cómo cambiar:**
1. Edita `MYSQL_HOST` si tu BD no es localhost
2. Edita `MYSQL_USER` y `MYSQL_PASSWORD`
3. Edita `MYSQL_DB` al nombre de tu BD

---

### Archivo: `app/__init__.py` - Inicializador

```python
from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()  # Instancia global de conexión a BD

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # 1. Cargar configuración
    app.config.from_object('app.config.Config')  # Lee de config.py
    
    # 2. Inicializar BD
    mysql.init_app(app)  # Conecta Flask con MySQL
    
    # 3. Registrar Blueprints (módulos de rutas)
    from app.routes.auth import auth         # Login/Logout
    from app.routes.public import public     # Menú público ⭐
    from app.routes.cocina import cocina     # Panel cocina
    from app.routes.admin import admin       # Panel admin
    
    app.register_blueprint(auth)
    app.register_blueprint(public)
    app.register_blueprint(cocina)
    app.register_blueprint(admin)
    
    return app
```

**¿Qué hace?**
1. Crea la aplicación Flask
2. **Conecta con MySQL** (IMPORTANTE)
3. Carga todas las rutas

---

## 🛣️ Todas las Rutas Completas

### 📍 RUTA 1: GET `/` - CARGAR MENÚ PRINCIPAL

```python
@public.route('/')
def menu_publico():
    """
    Punto de entrada de la aplicación.
    Carga el menú con todos los productos.
    """
    cur = mysql.connection.cursor()
    
    # QUERY 1: Obtener todos los productos
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, 
               p.precio, p.imagen, c.nombre
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.estado = 'activo' AND p.disponible = 'si'
        ORDER BY c.nombre, p.nombre
    """)
    productos = cur.fetchall()
    # Resultado: [(1, 'Hamburguesa Clásica', '...', 45.00, 'img.jpg', 'Hamburguesas'), ...]

    # QUERY 2: Obtener combos predefinidos
    cur.execute("""
        SELECT id_combo, nombre, descripcion, precio, imagen
        FROM combos
        WHERE disponible = 'si'
        ORDER BY nombre
    """)
    combos = cur.fetchall()
    # Resultado: [(1, 'Combo Completo', '...', 60.00, 'img.jpg'), ...]

    # QUERY 3: Obtener insumos (ingredientes)
    cur.execute("""
        SELECT id_insumo, nombre, costo_referencia
        FROM insumos
        WHERE estado = 'activo'
        ORDER BY nombre
    """)
    insumos = cur.fetchall()
    # Resultado: [(1, 'Carne Roja', 20.00), (2, 'Queso Cheddar', 5.00), ...]

    # QUERY 4: Obtener bebidas (categoría 2)
    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        WHERE id_categoria = 2 
          AND estado = 'activo' 
          AND disponible = 'si'
        ORDER BY nombre
    """)
    bebidas = cur.fetchall()
    # Resultado: [(4, 'Coca Cola', 10.00)]

    # QUERY 5: Obtener papas/acompañamientos (categoría 3)
    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        WHERE id_categoria = 3 
          AND estado = 'activo' 
          AND disponible = 'si'
        ORDER BY nombre
    """)
    papas = cur.fetchall()
    # Resultado: [(5, 'Papas Fritas', 15.00)]

    # FILTRO 1: Obtener tipos de carne
    carnes = [i for i in insumos 
              if any(palabra in i[1].lower() 
              for palabra in ['carne', 'pollo', 'res', 'cerdo', 'pavo', 'hamburguesa'])]
    # Resultado: Lista de insumos que contienen esas palabras

    # FILTRO 2: Obtener hamburguesas originales
    hamburguesas = [p for p in productos 
                    if p[5].strip().lower() == 'hamburguesas' 
                    and 'combo' not in p[1].strip().lower()]
    # Resultado: Solo productos de categoría "Hamburguesas"

    cur.close()

    # INICIALIZAR CARRITO EN SESIÓN
    if 'carrito' not in session:
        session['carrito'] = []

    # CONTAR ITEMS EN CARRITO
    cantidad_carrito = sum(item['cantidad'] 
                          for item in session.get('carrito', []))

    # RENDERIZAR TEMPLATE CON DATOS
    return render_template(
        'menu_publico.html',
        productos=productos,           # Todos los productos
        combos=combos,                 # Combos predefinidos
        insumos=insumos,               # Ingredientes disponibles
        carnes=carnes,                 # Tipos de carne
        hamburguesas=hamburguesas,     # Hamburguesas pre-hechas
        bebidas=bebidas,               # Bebidas desde BD
        papas=papas,                   # Papas desde BD
        cantidad_carrito=cantidad_carrito  # Total items en carrito
    )
```

**¿Qué retorna?**
- Template HTML con menú completo
- 8 variables diferentes para mostrar

**Base de Datos usada:**
- `productos` (tabla principal)
- `categorias` (para filtrar por tipo)
- `combos` (combos predefinidos)
- `insumos` (ingredientes)

---

### 📍 RUTA 2: POST `/agregar_combo/<id_combo>` - AGREGAR COMBO AL CARRITO

```python
@public.route('/agregar_combo/<int:id_combo>', methods=['POST'])
def agregar_combo(id_combo):
    """
    Agrega un combo predefinido al carrito.
    Si ya existe → aumenta cantidad
    Si no existe → lo agrega
    """
    # PASO 1: Obtener cantidad del formulario
    cantidad = int(request.form.get('cantidad', 1))
    # cantidad = 2 (ó 1 por defecto)

    # PASO 2: Validar cantidad > 0
    if cantidad <= 0:
        flash('La cantidad debe ser mayor a 0.')
        return redirect(url_for('public.menu_publico'))

    # PASO 3: Obtener datos del combo de la BD
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nombre, precio
        FROM combos
        WHERE id_combo = %s AND disponible = 'si'
    """, (id_combo,))
    combo = cur.fetchone()
    # combo = ('Combo Completo', 60.00)

    # PASO 4: Validar que el combo existe
    if not combo:
        flash('Combo no disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    nombre_combo, precio_combo = combo

    # PASO 5: Obtener carrito de sesión
    carrito = session.get('carrito', [])
    # carrito = [{'tipo': 'combo', 'id_combo': 1, ...}, ...]

    # PASO 6: Buscar si ya existe el combo
    encontrado = False
    for item in carrito:
        if item.get('tipo') == 'combo' and item['id_combo'] == id_combo:
            # YA EXISTE → Sumar cantidad
            item['cantidad'] += cantidad
            item['subtotal'] = round(item['cantidad'] * item['precio'], 2)
            encontrado = True
            break

    # PASO 7: Si no existe, agregarlo nuevo
    if not encontrado:
        carrito.append({
            'tipo': 'combo',
            'id_combo': id_combo,
            'nombre': nombre_combo,
            'precio': float(precio_combo),
            'cantidad': cantidad,
            'subtotal': round(float(precio_combo) * cantidad, 2)
        })

    # PASO 8: Guardar carrito en sesión
    session['carrito'] = carrito
    session.modified = True
    cur.close()
    
    # PASO 9: Redirigir al menú
    return redirect(url_for('public.menu_publico'))
```

**Estructura del item agregado:**
```python
{
    'tipo': 'combo',                    # Para identificar tipo
    'id_combo': 1,                      # ID del combo
    'nombre': 'Combo Completo',         # Descrición
    'precio': 60.00,                    # Precio unitario
    'cantidad': 2,                      # Cuántos pidió
    'subtotal': 120.00                  # precio × cantidad
}
```

**Flujo:**
1. Lee cantidad ✓
2. Obtiene datos de combo ✓
3. Busca si ya está en carrito ✓
4. Si sí → suma cantidad ✓
5. Si no → lo agrega nuevo ✓
6. Guarda carrito en sesión ✓

---

### 📍 RUTA 3: POST `/personalizar_hamburguesa` - LA RUTA MÁS IMPORTANTE

```python
@public.route('/personalizar_hamburguesa', methods=['POST'])
def personalizar_hamburguesa():
    """
    Crea una hamburguesa personalizada.
    Usuario elige: pan, queso, ingredientes, papas, bebida.
    Precio = PRECIO FIJO (sin extras)
    """
    
    # PASO 1: Obtener carne por defecto
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_insumo 
        FROM insumos 
        WHERE nombre LIKE '%carne%' 
          AND estado = 'activo' 
        LIMIT 1
    """)
    carne_default = cur.fetchone()
    # carne_default = (1,) ← ID de Carne Roja
    
    if not carne_default:
        flash('No hay carne disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))
    
    base_id = carne_default[0]  # base_id = 1

    # PASO 2: Obtener selecciones del usuario del formulario
    pan = request.form.get('pan', 'normal')                    # 'normal', 'integral', 'sesamo'
    queso = request.form.get('queso', 'no')                    # ID del queso o 'no'
    ingredientes_ids = request.form.getlist('ingredientes')    # [3, 4, 5] (IDs)
    papas = request.form.get('papas', 'no')                    # ID de papas o 'no'
    bebida = request.form.get('bebida', 'no')                  # ID de bebida o 'no'
    cantidad = int(request.form.get('cantidad', 1))            # 1, 2, 3, ...

    # PASO 3: Validar cantidad > 0
    if cantidad <= 0:
        flash('Cantidad inválida.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    # PASO 4: Obtener datos de carne base
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nombre, costo_referencia 
        FROM insumos 
        WHERE id_insumo = %s
    """, (base_id,))
    base = cur.fetchone()
    # base = ('Carne Roja', 20.00)

    if not base:
        flash('Carne no disponible.')
        cur.close()
        return redirect(url_for('public.menu_publico'))

    nombre_base, _ = base  # nombre_base = 'Carne Roja'

    # PASO 5: Obtener precio FIJO de "Hamburguesa Clásica"
    cur.execute("""
        SELECT precio 
        FROM productos 
        WHERE nombre LIKE '%lásica%' 
          AND estado = 'activo' 
        LIMIT 1
    """)
    precio_result = cur.fetchone()
    
    if precio_result:
        precio_total = float(precio_result[0])  # precio_total = 45.00 ← FIJO
    else:
        # Fallback si no existe
        precio_total = float(base[1])

    # PASO 6: Obtener nombres de ingredientes adicionales
    insumos_nombres = []
    for ing_id in ingredientes_ids:  # [3, 4, 5]
        cur.execute("""
            SELECT nombre 
            FROM insumos 
            WHERE id_insumo = %s
        """, (int(ing_id),))
        ing = cur.fetchone()
        if ing:
            insumos_nombres.append(ing[0])  # ['Pepinillos', 'Tomate', 'Cebolla']

    cur.close()

    # PASO 7: ARMAR DESCRIPCIÓN COMPLETA
    nombre_personalizado = "Hamburguesa Personalizada"
    detalles = []

    # Agregar pan si no es normal
    if pan != 'normal':
        if pan == 'integral':
            detalles.append("Pan Integral")
        elif pan == 'sesamo':
            detalles.append("Pan con Sésamo")

    # Agregar carne base (siempre)
    detalles.append(nombre_base)  # detalles = ['Carne Roja']

    # Agregar queso si se seleccionó
    if queso != 'no':
        cur_tmp = mysql.connection.cursor()
        cur_tmp.execute("""
            SELECT nombre 
            FROM insumos 
            WHERE id_insumo = %s
        """, (int(queso),))
        queso_nombre = cur_tmp.fetchone()
        if queso_nombre:
            detalles.append(queso_nombre[0])  # detalles = ['Carne Roja', 'Queso Cheddar']
        cur_tmp.close()

    # Agregar ingredientes
    if insumos_nombres:
        detalles.extend(insumos_nombres)
        # detalles = ['Carne Roja', 'Queso Cheddar', 'Pepinillos', 'Tomate', 'Cebolla']

    # Agregar papas si se seleccionaron
    if papas != 'no':
        cur_papas = mysql.connection.cursor()
        cur_papas.execute("""
            SELECT nombre 
            FROM productos 
            WHERE id_producto = %s
        """, (int(papas),))
        papas_row = cur_papas.fetchone()
        if papas_row:
            detalles.append(papas_row[0])  # 'Papas Fritas'
        cur_papas.close()

    # Agregar bebida si se seleccionó
    if bebida != 'no':
        cur_bebida = mysql.connection.cursor()
        cur_bebida.execute("""
            SELECT nombre 
            FROM productos 
            WHERE id_producto = %s
        """, (int(bebida),))
        bebida_row = cur_bebida.fetchone()
        if bebida_row:
            detalles.append(bebida_row[0])  # 'Coca Cola'
        cur_bebida.close()

    # PASO 8: CONSTRUIR NOMBRE FINAL
    nombre_personalizado += f": {', '.join(detalles)}"
    # nombre_personalizado = "Hamburguesa Personalizada: Carne Roja, Queso Cheddar, Pepinillos, Tomate, Cebolla, Papas Fritas, Coca Cola"

    # PASO 9: Preparar ingredientes para carrito
    todos_ingredientes = []
    if queso != 'no':
        todos_ingredientes.append(queso)
    todos_ingredientes.extend(ingredientes_ids)
    # todos_ingredientes = [2, 3, 4, 5] (IDs de insumos)

    # PASO 10: Obtener carrito
    carrito = session.get('carrito', [])

    # PASO 11: AGREGAR AL CARRITO
    carrito.append({
        'tipo': 'personalizado',                      # Tipo
        'id_base': base_id,                           # ID carne
        'pan': pan,                                   # Tipo de pan
        'queso': queso,                               # ID queso
        'ingredientes': todos_ingredientes,           # IDs ingredientes
        'papas': papas,                               # ID papas
        'bebida': bebida,                             # ID bebida
        'nombre': nombre_personalizado,               # Descripción completa
        'precio': float(precio_total),                # PRECIO FIJO (45.00)
        'cantidad': cantidad,                         # Cantidad
        'subtotal': round(float(precio_total) * cantidad, 2)  # Total
    })

    # PASO 12: Guardar carrito
    session['carrito'] = carrito
    session.modified = True
    
    # PASO 13: Redirigir
    return redirect(url_for('public.menu_publico'))
```

**Estructura del item personalizado:**
```python
{
    'tipo': 'personalizado',              # Para validar tipo
    'id_base': 1,                         # Carne que usa
    'pan': 'integral',                    # Tipo de pan
    'queso': 2,                           # ID del queso (2) o "no"
    'ingredientes': [3, 4, 5],            # IDs de ingredientes
    'papas': 5,                           # ID papas o "no"
    'bebida': 4,                          # ID bebida o "no"
    'nombre': 'Hamburguesa Personalizada: Pan Integral, Carne Roja, Queso Cheddar, Pepinillos, Tomate, Cebolla, Papas Fritas, Coca Cola',
    'precio': 45.00,                      # ← PRECIO FIJO, SIN EXTRAS
    'cantidad': 2,
    'subtotal': 90.00
}
```

**PUNTO CLAVE: Precio es FIJO desde Hamburguesa Clásica, sin importar ingredientes**

---

### 📍 RUTA 4: GET `/carrito` - VER CARRITO

```python
@public.route('/carrito')
def ver_carrito():
    """Muestra el carrito con todos los items"""
    carrito = session.get('carrito', [])
    total = round(sum(item['subtotal'] for item in carrito), 2)
    return render_template('carrito.html', carrito=carrito, total=total)
```

Parametros para template:
- `carrito`: Lista de items
- `total`: Suma de subtotales

---

### 📍 RUTAS 5-7: SUMAR/RESTAR/ELIMINAR ITEMS

```python
@public.route('/sumar_item/<int:id_producto>')
def sumar_item(id_producto):
    """Aumenta cantidad de un producto"""
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
    """Disminuye cantidad. Si llega a 0, lo elimina"""
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
    """Elimina un item completamente"""
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id_producto'] != id_producto]
    session['carrito'] = carrito
    session.modified = True
    flash('Producto eliminado del carrito.')
    return redirect(url_for('public.ver_carrito'))

# Similar para combos:
@public.route('/sumar_combo/<int:id_combo>')
@public.route('/restar_combo/<int:id_combo>')
@public.route('/eliminar_combo/<int:id_combo>')

# Similar para personalizados:
@public.route('/sumar_personalizado/<int:id_base>')
@public.route('/restar_personalizado/<int:id_base>')
@public.route('/eliminar_personalizado/<int:id_base>')
```

---

### 📍 RUTA 8: GET `/vaciar_carrito` - VACIAR TODO

```python
@public.route('/vaciar_carrito')
def vaciar_carrito():
    """Elimina todos los items del carrito"""
    session['carrito'] = []
    session.modified = True
    flash('Carrito vaciado.')
    return redirect(url_for('public.ver_carrito'))
```

---

### 📍 RUTA 9: POST `/confirmar_pedido` - LA RUTA CRÍTICA ⭐⭐⭐

```python
@public.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    """
    Procesa la venta:
    1. Verifica stock
    2. Crea pedido en BD
    3. Descuenta inventario
    4. Genera venta automática
    """
    
    # PASO 1: Obtener carrito
    carrito = session.get('carrito', [])
    if not carrito:
        return jsonify({'error': 'Tu carrito está vacío.'}), 400

    # PASO 2: Obtener datos del cliente
    nombre_cliente = request.form.get('nombre_cliente', '').strip()
    telefono_cliente = request.form.get('telefono_cliente', '').strip()

    if not nombre_cliente:
        return jsonify({'error': 'Debes ingresar tu nombre.'}), 400

    # PASO 3: ⭐ VERIFICAR STOCK (CRÍTICO)
    stock_ok, mensaje_stock = verificar_stock_carrito(mysql.connection, carrito)
    if not stock_ok:
        return jsonify({'error': mensaje_stock}), 400
    # Si falla aquí → RECHAZA TODO y no continúa

    # PASO 4: Calcular totales
    subtotal = round(sum(item['subtotal'] for item in carrito), 2)
    total = subtotal  # Sin impuestos por ahora

    # PASO 5: Generar número de pedido único
    numero_pedido = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Ejemplo: "PED-20260401143025"

    # PASO 6: Obtener cursor de BD
    cur = mysql.connection.cursor()

    try:
        # ========== INICIA TRANSACCIÓN ==========
        
        # PASO 7: CREAR REGISTRO DE PEDIDO
        cur.execute("""
            INSERT INTO pedidos (
                id_cliente,
                nombre_cliente_invitado,
                telefono_cliente_invitado,
                numero_pedido,
                tipo_pedido,
                estado,
                fecha_pedido,
                subtotal,
                total
            )
            VALUES (NULL, %s, %s, %s, 'web', 'confirmado', NOW(), %s, %s)
        """, (nombre_cliente, telefono_cliente, numero_pedido, subtotal, total))
        
        id_pedido = cur.lastrowid  # ID del pedido creado

        # PASO 8: CREAR DETALLES DEL PEDIDO
        for item in carrito:
            # Determinar qué ID usar (varía según tipo)
            if item.get('tipo') == 'combo':
                id_prod = item['id_combo']
            elif item.get('tipo') == 'personalizado':
                id_prod = item['id_base']
            else:
                id_prod = item['id_producto']

            # Insertar detalle
            cur.execute("""
                INSERT INTO pedido_detalle (
                    id_pedido,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                id_pedido,
                id_prod,
                item['cantidad'],
                item['precio'],
                item['subtotal']
            ))

        # PASO 9: CREAR VENTA AUTOMÁTICA
        id_empleado_sistema = 1  # Empleado "Sistema"
        
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

        # PASO 10: CREAR DETALLES DE VENTA
        for item in carrito:
            if item.get('tipo') == 'combo':
                id_prod = item['id_combo']
            elif item.get('tipo') == 'personalizado':
                id_prod = item['id_base']
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
            """, (id_venta, id_prod, item['cantidad'], item['precio'], item['subtotal']))

        # PASO 11: ⭐ DESCONTAR INVENTARIO
        for item in carrito:
            if item.get('tipo') == 'combo':
                # Descuenta receta del combo
                descontar_inventario_combo(
                    conexion=mysql.connection,
                    id_combo=item['id_combo'],
                    cantidad_vendida=item['cantidad'],
                    referencia=numero_pedido
                )
            elif item.get('tipo') == 'personalizado':
                # Descuenta ingredientes + papas + bebida
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
                # Descuenta receta del producto
                descontar_inventario_por_producto(
                    conexion=mysql.connection,
                    id_producto=item['id_producto'],
                    cantidad_vendida=item['cantidad'],
                    referencia=numero_pedido
                )

        # PASO 12: CONFIRMAR TRANSACCIÓN
        mysql.connection.commit()  # ✅ TODO PASÓ, GUARDAR CAMBIOS

        # PASO 13: LIMPIAR CARRITO
        session['carrito'] = []
        session.modified = True

        # PASO 14: RETORNAR RESPUESTA JSON
        return jsonify({
            'numero_pedido': numero_pedido,
            'estado': 'confirmado',
            'total': total,
            'items': carrito
        })

    except Exception as e:
        # SI HAY ERROR → REVERTIR TODO
        mysql.connection.rollback()
        return jsonify({'error': f'Error al confirmar pedido: {str(e)}'}), 500
    finally:
        cur.close()
```

**Flujo Crítico:**
```
1. Verificar stock ✅
   └─ Si falla → retorna error, NO continúa

2. Crear pedido ✅
3. Crear detalle pedido ✅
4. Crear venta ✅
5. Crear detalle venta ✅
6. Descontar inventario ✅

7. commit() ← ⭐ TODOS LOS CAMBIOS SE GUARDAN

Si algo falla (paso 7) → rollback() ← REVIERTA TODO
```

---

### 📍 RUTA 10: GET `/pedido/<numero_pedido>` - VER ESTADO

```python
@public.route('/pedido/<numero_pedido>')
def estado_pedido(numero_pedido):
    """Muestra el estado y detalles de un pedido confirmado"""
    cur = mysql.connection.cursor()
    
    # Obtener pedido
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado,
               telefono_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE numero_pedido = %s
    """, (numero_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        cur.close()
        flash('Pedido no encontrado.')
        return redirect(url_for('public.menu_publico'))

    # Obtener detalles del pedido
    cur.execute("""
        SELECT pd.cantidad, p.nombre, pd.precio_unitario, pd.subtotal
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (pedido[0],))
    detalles = cur.fetchall()
    cur.close()

    return render_template('estado_pedido.html', pedido=pedido, detalles=detalles)
```

---

## 🔐 Módulo AUTH - Autenticación

### Archivo: `app/routes/auth.py`

#### DECORADORES DE PROTECCIÓN

```python
def login_required(f):
    """Protege una ruta: solo permite usuarios logueados"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# USO: @login_required sobre cualquier ruta
@auth.route('/dashboard')
@login_required
def dashboard():
    # Ejecuta solo si hay user_id en sesión
```

```python
def roles_required(*roles_permitidos):
    """Protege una ruta: solo permite ciertos roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'rol' not in session:
                flash('Acceso no autorizado.')
                return redirect(url_for('auth.login'))

            if session['rol'] not in roles_permitidos:
                flash('No tienes permiso para acceder.')
                return redirect(url_for('auth.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# USO: @roles_required('administrador') sobre ruta admin
@admin.route('/dashboard')
@login_required
@roles_required('administrador')  # Solo admin puede acceder
def dashboard_admin():
    # ...
```

---

### 📍 RUTA 1: POST/GET `/login` - INICIO DE SESIÓN

```python
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Autenticación de usuario con contraseña hasheada.
    Valida credenciales contra BD y crea sesión.
    """
    if request.method == 'POST':
        # PASO 1: Obtener credenciales del formulario
        username = request.form['username'].strip()      # 'juan_perez'
        password = request.form['password'].strip()      # '123456'

        # PASO 2: Buscar usuario en BD
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                u.id_usuario,                    # 1
                u.username,                      # 'juan_perez'
                u.password_hash,                 # hash($2b$12...) 
                r.nombre AS rol,                 # 'administrador', 'cocina', 'cajero'
                e.nombres,                       # 'Juan'
                e.apellidos                      # 'Pérez'
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            LEFT JOIN empleados e ON u.id_usuario = e.id_usuario
            WHERE u.username = %s AND u.estado = 'activo'
        """, (username,))
        user = cur.fetchone()
        # user = (1, 'juan_perez', '$2b$12...', 'administrador', 'Juan', 'Pérez')

        # PASO 3: Validar que usuario existe
        if user:
            id_usuario, username_db, password_hash, rol, nombres, apellidos = user

            # PASO 4: ⭐ VERIFICAR CONTRASEÑA (compara hash)
            if check_password_hash(password_hash, password):
                # ✅ CONTRASEÑA CORRECTA

                # PASO 5: Construir nombre completo
                if nombres and apellidos:
                    nombre_completo = f"{nombres} {apellidos}"  # 'Juan Pérez'
                else:
                    nombre_completo = username_db

                # PASO 6: CREAR SESIÓN
                session['user_id'] = id_usuario           # 1
                session['username'] = username_db         # 'juan_perez'
                session['rol'] = rol                      # 'administrador'
                session['nombre'] = nombre_completo       # 'Juan Pérez'
                session.modified = True

                # PASO 7: REDIRIGIR
                flash('Bienvenido al sistema.')
                return redirect(url_for('auth.dashboard'))
            else:
                # ❌ CONTRASEÑA INCORRECTA
                flash('Contraseña incorrecta.')
        else:
            # ❌ USUARIO NO EXISTE
            flash('Usuario no encontrado.')

        cur.close()

    # GET: Mostrar formulario de login
    return render_template('login.html')
```

**¿Qué se guarda en sesión?**
```python
session = {
    'user_id': 1,                  # ID para consultas
    'username': 'juan_perez',      # Para mostrar en UI
    'rol': 'administrador',        # Para @roles_required
    'nombre': 'Juan Pérez',        # Para saludos
}
```

---

### 📍 RUTA 2: GET `/dashboard` - DASHBOARD GENERAL

```python
@auth.route('/dashboard')
@login_required
def dashboard():
    """
    Muestra dashboard con estadísticas del mes actual.
    Accesible a todos los usuarios logueados.
    """
    from datetime import datetime
    
    cur = mysql.connection.cursor()
    mes_actual = datetime.now().strftime('%Y-%m')  # '2026-04'

    # QUERY 1: Ventas del mes por día
    cur.execute("""
        SELECT DATE(fecha_venta) as fecha, SUM(total) as total
        FROM ventas
        WHERE DATE_FORMAT(fecha_venta, '%%Y-%%m') = %s
        GROUP BY DATE(fecha_venta)
        ORDER BY fecha ASC
    """, (mes_actual,))
    ventas_mes = cur.fetchall()
    # Resultado: [(2026-04-01, 500.00), (2026-04-02, 750.00), ...]

    # QUERY 2: Compras del mes por día
    cur.execute("""
        SELECT DATE(fecha_compra) as fecha, SUM(total) as total
        FROM compras
        WHERE DATE_FORMAT(fecha_compra, '%%Y-%%m') = %s
        GROUP BY DATE(fecha_compra)
        ORDER BY fecha ASC
    """, (mes_actual,))
    compras_mes = cur.fetchall()

    # QUERY 3: Total ventas mes
    cur.execute("""
        SELECT SUM(total) 
        FROM ventas 
        WHERE DATE_FORMAT(fecha_venta, '%%Y-%%m') = %s
    """, (mes_actual,))
    total_ventas_mes = cur.fetchone()[0] or 0

    # QUERY 4: Total compras mes
    cur.execute("""
        SELECT SUM(total) 
        FROM compras 
        WHERE DATE_FORMAT(fecha_compra, '%%Y-%%m') = %s
    """, (mes_actual,))
    total_compras_mes = cur.fetchone()[0] or 0

    # QUERY 5: Cantidad de pedidos mes
    cur.execute("""
        SELECT COUNT(*) 
        FROM pedidos 
        WHERE DATE_FORMAT(fecha_pedido, '%%Y-%%m') = %s
    """, (mes_actual,))
    cantidad_pedidos = cur.fetchone()[0] or 0

    # QUERY 6: Pedidos por estado
    cur.execute("""
        SELECT estado, COUNT(*) as cantidad
        FROM pedidos
        WHERE DATE_FORMAT(fecha_pedido, '%%Y-%%m') = %s
        GROUP BY estado
    """, (mes_actual,))
    pedidos_por_estado = cur.fetchall()
    # Resultado: [('confirmado', 15), ('en_preparacion', 5), ('listo', 3), ('entregado', 20)]

    cur.close()

    # PREPARAR DATOS PARA GRÁFICOS
    fechas_ventas = [v[0].strftime('%d/%m') for v in ventas_mes]
    totales_ventas = [float(v[1]) for v in ventas_mes]
    
    fechas_compras = [c[0].strftime('%d/%m') for c in compras_mes]
    totales_compras = [float(c[1]) for c in compras_mes]
    
    estados = [p[0] for p in pedidos_por_estado]
    cantidades = [p[1] for p in pedidos_por_estado]

    return render_template(
        'dashboard.html',
        total_ventas_mes=float(total_ventas_mes),
        total_compras_mes=float(total_compras_mes),
        cantidad_pedidos=cantidad_pedidos,
        fechas_ventas=fechas_ventas,
        totales_ventas=totales_ventas,
        fechas_compras=fechas_compras,
        totales_compras=totales_compras,
        estados=estados,
        cantidades_estados=cantidades
    )
```

---

### 📍 RUTA 3: GET `/logout` - CERRAR SESIÓN

```python
@auth.route('/logout')
def logout():
    """Limpia la sesión y redirige al login"""
    session.clear()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('auth.login'))
**Observación importante:** Cuando se elimina una compra, el stock se revierte automáticamente.

---

### 📍 RUTAS 11-14: COMPRAS (CRUD COMPLETO)

```python
# RUTA 11: Listar compras
@admin.route('/compras')
@login_required
@roles_required('administrador')
def listar_compras():
    """Lista todas las compras registradas"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.id_compra, c.numero_compra, p.nombre_empresa, 
               c.fecha_compra, c.total, c.estado
        FROM compras c
        INNER JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        ORDER BY c.fecha_compra DESC
    """)
    compras = cur.fetchall()
    cur.close()
    return render_template('admin/compras.html', compras=compras)

# RUTA 12: Crear compra (GET/POST)
@admin.route('/compras/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nueva_compra():
    """Registrar nueva compra de insumos con actualización de stock"""
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        # OBTENER DATOS
        id_proveedor = int(request.form['id_proveedor'])
        fecha_compra = request.form['fecha_compra']
        numero_compra = request.form['numero_compra'].strip()
        
        # PROCESAR ITEMS (JSON)
        items_json = request.form.get('items_json', '[]')
        import json
        try:
            items = json.loads(items_json)
        except:
            items = []

        if not items:
            flash('Debe agregar al menos un insumo.')
            cur.close()
            return redirect(url_for('admin.nueva_compra'))

        try:
            # CALCULAR TOTAL
            total = sum(i['cantidad'] * i['precio_unitario'] for i in items)

            # INSERTAR COMPRA
            cur.execute("""
                INSERT INTO compras (
                    id_proveedor, numero_compra, fecha_compra, total, estado
                )
                VALUES (%s, %s, %s, %s, 'registrada')
            """, (id_proveedor, numero_compra, fecha_compra, total))
            mysql.connection.commit()
            id_compra = cur.lastrowid

            # PROCESAR ITEMS
            for item in items:
                id_insumo = int(item['id_insumo'])
                cantidad = float(item['cantidad'])
                precio_unitario = float(item['precio_unitario'])

                # INSERTAR DETALLE
                cur.execute("""
                    INSERT INTO compra_detalle (
                        id_compra, id_insumo, cantidad, 
                        precio_unitario, subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_compra, id_insumo, cantidad, precio_unitario, 
                      cantidad * precio_unitario))

                # ⭐ ACTUALIZAR STOCK
                cur.execute("""
                    UPDATE insumos
                    SET stock_actual = stock_actual + %s
                    WHERE id_insumo = %s
                """, (cantidad, id_insumo))

                # ⭐ REGISTRAR MOVIMIENTO
                cur.execute("""
                    INSERT INTO movimientos_inventario (
                        id_insumo, tipo_movimiento, cantidad, 
                        referencia, observacion, fecha_movimiento
                    )
                    VALUES (%s, 'entrada_compra', %s, %s, 'Entrada por compra', NOW())
                """, (id_insumo, cantidad, numero_compra))

            mysql.connection.commit()
            flash('Compra registrada correctamente.')
            return redirect(url_for('admin.listar_compras'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
        finally:
            cur.close()

    # GET: Cargar formulario
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT id_proveedor, nombre_empresa 
        FROM proveedores 
        WHERE estado = 'activo'
        ORDER BY nombre_empresa ASC
    """)
    proveedores = cur.fetchall()

    cur.execute("""
        SELECT id_insumo, nombre, costo_referencia 
        FROM insumos 
        WHERE estado = 'activo'
        ORDER BY nombre ASC
    """)
    insumos = cur.fetchall()
    cur.close()

    return render_template('admin/compra_form.html', 
                          proveedores=proveedores, insumos=insumos)

# RUTA 13: Editar compra (GET/POST)
@admin.route('/compras/editar/<int:id_compra>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_compra(id_compra):
    """Editar compra (solo si está 'registrada')"""
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id_compra, id_proveedor, numero_compra, 
               fecha_compra, total, estado
        FROM compras
        WHERE id_compra = %s
    """, (id_compra,))
    compra = cur.fetchone()

    if not compra:
        flash('Compra no encontrada.')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    if compra[5] == 'pagada':
        flash('No puedes editar una compra pagada.')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    if request.method == 'POST':
        id_proveedor = int(request.form['id_proveedor'])
        numero_compra = request.form['numero_compra'].strip()
        fecha_compra = request.form['fecha_compra']
        estado = request.form['estado'].strip()

        try:
            cur.execute("""
                UPDATE compras
                SET id_proveedor=%s, numero_compra=%s, 
                    fecha_compra=%s, estado=%s
                WHERE id_compra=%s
            """, (id_proveedor, numero_compra, fecha_compra, estado, id_compra))
            mysql.connection.commit()
            flash('Compra actualizada correctamente.')
            return redirect(url_for('admin.listar_compras'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
        finally:
            cur.close()

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_proveedor, nombre_empresa 
        FROM proveedores 
        WHERE estado = 'activo'
        ORDER BY nombre_empresa ASC
    """)
    proveedores = cur.fetchall()

    cur.execute("""
        SELECT cd.id_insumo, i.nombre, cd.cantidad, 
               cd.precio_unitario, cd.subtotal
        FROM compra_detalle cd
        INNER JOIN insumos i ON cd.id_insumo = i.id_insumo
        WHERE cd.id_compra = %s
    """, (id_compra,))
    detalles = cur.fetchall()
    cur.close()

    return render_template('admin/compra_form.html', 
                          compra=compra, detalles=detalles,
                          proveedores=proveedores)

# RUTA 14: Eliminar compra (POST)
@admin.route('/compras/eliminar/<int:id_compra>', methods=['POST'])
@login_required
@roles_required('administrador')
def eliminar_compra(id_compra):
    """Eliminar compra y revertir stock automáticamente"""
    cur = mysql.connection.cursor()

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
        flash('Solo puedes eliminar compras "registrada".')
        cur.close()
        return redirect(url_for('admin.listar_compras'))

    try:
        # OBTENER DETALLES
        cur.execute("""
            SELECT id_insumo, cantidad
            FROM compra_detalle
            WHERE id_compra = %s
        """, (id_compra,))
        detalles = cur.fetchall()
        
        # REVERTIR STOCK
        for id_insumo, cantidad in detalles:
            cur.execute("""
                UPDATE insumos
                SET stock_actual = stock_actual - %s
                WHERE id_insumo = %s
            """, (cantidad, id_insumo))

        # ELIMINAR DETALLES
        cur.execute("DELETE FROM compra_detalle WHERE id_compra = %s", (id_compra,))

        # ELIMINAR COMPRA
        cur.execute("DELETE FROM compras WHERE id_compra = %s", (id_compra,))
        
        mysql.connection.commit()
        flash('Compra eliminada (stock revertido).')

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {str(e)}')
    finally:
        cur.close()

    return redirect(url_for('admin.listar_compras'))
```

---

### Archivo: `app/routes/admin.py`

#### Base de todas las rutas:
```python
@admin.route('/...')
@login_required                          # Debe estar logueado
@roles_required('administrador')         # Solo administrador
def función():
    # ...
```

---

### 📍 RUTA 1: GET `/admin/dashboard` - DASHBOARD ADMIN

```python
@admin.route('/dashboard')
@login_required
@roles_required('administrador')
def dashboard_admin():
    """
    Resumen ejecutivo del restaurante:
    - Total ventas
    - Total compras
    - Empleados activos
    - Proveedores activos
    - Stock bajo
    - Últimas transacciones
    """
    cur = mysql.connection.cursor()

    # STAT 1: Total ventas
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(total), 0)
        FROM ventas
        WHERE estado = 'pagada'
    """)
    total_ventas, monto_ventas = cur.fetchone()
    # (45, 15000.00)

    # STAT 2: Total compras
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(total), 0)
        FROM compras
        WHERE estado = 'registrada'
    """)
    total_compras, monto_compras = cur.fetchone()
    # (30, 8500.00)

    # STAT 3: Empleados activos
    cur.execute("SELECT COUNT(*) FROM empleados WHERE estado = 'activo'")
    total_empleados = cur.fetchone()[0]  # 12

    # STAT 4: Proveedores activos
    cur.execute("SELECT COUNT(*) FROM proveedores WHERE estado = 'activo'")
    total_proveedores = cur.fetchone()[0]  # 5

    # STAT 5: Stock bajo (< stock_minimo)
    cur.execute("""
        SELECT COUNT(*)
        FROM insumos
        WHERE estado = 'activo' AND stock_actual <= stock_minimo
    """)
    stock_bajo = cur.fetchone()[0]  # 3

    # STAT 6: Últimas 5 ventas
    cur.execute("""
        SELECT v.id_venta, v.fecha_venta, v.total, p.numero_pedido
        FROM ventas v
        LEFT JOIN pedidos p ON v.id_pedido = p.id_pedido
        WHERE v.estado = 'pagada'
        ORDER BY v.fecha_venta DESC
        LIMIT 5
    """)
    ultimas_ventas = cur.fetchall()

    # STAT 7: Últimos 5 pedidos
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
        total_ventas=total_ventas,              # 45
        monto_ventas=float(monto_ventas),       # 15000.00
        total_compras=total_compras,            # 30
        monto_compras=float(monto_compras),     # 8500.00
        total_empleados=total_empleados,        # 12
        total_proveedores=total_proveedores,    # 5
        stock_bajo=stock_bajo,                  # 3
        ultimas_ventas=ultimas_ventas,
        ultimos_pedidos=ultimos_pedidos
    )
```

---

### 📍 RUTA 2: GET `/admin/ventas` - LISTAR VENTAS

```python
@admin.route('/ventas')
@login_required
@roles_required('administrador', 'cajero')  # Admin Y Cajero
def listar_ventas():
    """Lista todas las ventas realizadas"""
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
```

---

### 📍 RUTA 3: GET `/admin/estado-pedidos` - ESTADO DE PEDIDOS

```python
@admin.route('/estado-pedidos')
@login_required
@roles_required('administrador', 'cajero')
def listar_estado_pedidos():
    """Ver todos los pedidos con su estado actual"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, 
               telefono_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        ORDER BY fecha_pedido DESC
    """)
    pedidos = cur.fetchall()
    cur.close()

    return render_template('admin/estado_pedidos.html', pedidos=pedidos)
```

---

### 📍 RUTA 4: GET `/admin/inventario` - INVENTARIO

```python
@admin.route('/inventario')
@login_required
@roles_required('administrador')
def listar_inventario():
    """Ver todos los insumos y su stock actual"""
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
```

---

### 📍 RUTAS 5-7: PROVEEDORES (CRUD)

```python
# RUTA 5: Listar proveedores
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

# RUTA 6: Crear proveedor
@admin.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_proveedor():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_empresa = request.form['nombre_empresa'].strip()
        contacto_nombre = request.form['contacto_nombre'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()
        nit = request.form['nit'].strip()

        # Insertar en BD
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

# RUTA 7: Editar proveedor
@admin.route('/proveedores/editar/<int:id_proveedor>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_proveedor(id_proveedor):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_empresa = request.form['nombre_empresa'].strip()
        contacto_nombre = request.form['contacto_nombre'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        direccion = request.form['direccion'].strip()
        nit = request.form['nit'].strip()
        estado = request.form['estado'].strip()

        # Actualizar en BD
        cur.execute("""
            UPDATE proveedores
            SET nombre_empresa=%s, contacto_nombre=%s, telefono=%s,
                correo=%s, direccion=%s, nit=%s, estado=%s
            WHERE id_proveedor=%s
        """, (nombre_empresa, contacto_nombre, telefono, correo, 
              direccion, nit, estado, id_proveedor))
        mysql.connection.commit()
        cur.close()

        flash('Proveedor actualizado correctamente.')
        return redirect(url_for('admin.listar_proveedores'))

    # GET: Cargar datos del proveedor
    cur.execute("""
        SELECT id_proveedor, nombre_empresa, contacto_nombre, telefono,
               correo, direccion, nit, estado
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))
    proveedor = cur.fetchone()
    cur.close()

    return render_template('admin/proveedor_form.html', proveedor=proveedor)
```

---

### 📍 RUTAS 8-10: EMPLEADOS (CRUD)

```python
# RUTA 8: Listar empleados
@admin.route('/empleados')
@login_required
@roles_required('administrador')
def listar_empleados():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_empleado, nombres, apellidos, dpi, telefono, 
               direccion, puesto, salario, fecha_contratacion, estado
        FROM empleados
        ORDER BY nombres ASC
    """)
    empleados = cur.fetchall()
    cur.close()
    return render_template('admin/empleados.html', empleados=empleados)

# RUTA 9: Crear empleado
@admin.route('/empleados/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def nuevo_empleado():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        correo = request.form['correo'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        dpi = request.form.get('dpi', '').strip() or None
        telefono = request.form.get('telefono', '').strip() or None
        direccion = request.form.get('direccion', '').strip() or None
        puesto = int(request.form['puesto']) if request.form['puesto'].strip() else None
        salario = float(request.form.get('salario', 0))
        fecha_contratacion = request.form.get('fecha_contratacion')

        try:
            # PASO 1: Hashear contraseña
            password_hash = generate_password_hash(password)

            # PASO 2: Crear usuario
            cur.execute("""
                INSERT INTO usuarios (
                    username, correo, password_hash, id_rol, estado
                )
                VALUES (%s, %s, %s, %s, 'activo')
            """, (username, correo, password_hash, puesto))
            mysql.connection.commit()

            # PASO 3: Obtener ID del usuario creado
            cur.execute("SELECT id_usuario FROM usuarios WHERE username = %s", (username,))
            usuario = cur.fetchone()
            id_usuario = usuario[0] if usuario else None

            # PASO 4: Crear empleado
            if id_usuario:
                cur.execute("""
                    INSERT INTO empleados (
                        id_usuario, nombres, apellidos, dpi, telefono, 
                        direccion, puesto, salario, fecha_contratacion, estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'activo')
                """, (id_usuario, nombres, apellidos, dpi, telefono, 
                      direccion, puesto, salario, fecha_contratacion))
                mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
        finally:
            cur.close()

        return redirect(url_for('admin.listar_empleados'))

    # GET: Cargar formulario
    cur.execute("SELECT id_rol, nombre FROM roles ORDER BY nombre ASC")
    roles = cur.fetchall()
    cur.close()

    return render_template('admin/empleado_form.html', empleado=None, roles=roles)

# RUTA 10: Editar empleado
@admin.route('/empleados/editar/<int:id_empleado>', methods=['GET', 'POST'])
@login_required
@roles_required('administrador')
def editar_empleado(id_empleado):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        dpi = request.form.get('dpi', '').strip() or None
        telefono = request.form.get('telefono', '').strip() or None
        direccion = request.form.get('direccion', '').strip() or None
        puesto = request.form.get('puesto', '').strip()
        salario = float(request.form.get('salario', 0))
        fecha_contratacion = request.form.get('fecha_contratacion')
        estado = request.form['estado'].strip()

        try:
            cur.execute("""
                UPDATE empleados
                SET nombres=%s, apellidos=%s, dpi=%s, telefono=%s,
                    direccion=%s, puesto=%s, salario=%s, 
                    fecha_contratacion=%s, estado=%s
                WHERE id_empleado=%s
            """, (nombres, apellidos, dpi, telefono, direccion, puesto,
                  salario, fecha_contratacion, estado, id_empleado))
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
        finally:
            cur.close()

        return redirect(url_for('admin.listar_empleados'))

    # GET: Cargar empleado
    cur.execute("""
        SELECT id_empleado, nombres, apellidos, dpi, telefono,
               direccion, puesto, salario, fecha_contratacion, estado
        FROM empleados
        WHERE id_empleado = %s
    """, (id_empleado,))
    empleado = cur.fetchone()

    # Cargar roles
    cur.execute("SELECT id_rol, nombre FROM roles ORDER BY nombre ASC")
    roles = cur.fetchall()
    cur.close()

    return render_template('admin/empleado_form.html', empleado=empleado, roles=roles)
```

---

## 👨‍🍳 Módulo COCINA - Panel de Cocina

### Archivo: `app/routes/cocina.py`

#### Base de todas las rutas:
```python
@cocina.route('/...')
@login_required                          # Debe estar logueado
@roles_required('cocina', 'administrador')  # Cocina O Admin
def función():
    # ...
```

---

### 📍 RUTA 1: GET `/cocina/pedidos` - LISTA DE PEDIDOS

```python
@cocina.route('/cocina/pedidos')
@login_required
@roles_required('cocina', 'administrador')
def lista_pedidos_cocina():
    """
    Muestra todos los pedidos que necesitan preparación.
    Estados: confirmado, en_preparacion, listo
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, 
               estado, fecha_pedido, total
        FROM pedidos
        WHERE estado IN ('confirmado', 'en_preparacion', 'listo')
        ORDER BY fecha_pedido ASC
    """)
    pedidos = cur.fetchall()
    # Resultado: [(1, 'PED-20260401143025', 'Juan', 'confirmado', ..., 90.00), ...]
    cur.close()

    return render_template('cocina_pedidos.html', pedidos=pedidos)
```

**Estados filtrados:**
- `confirmado`: Acaba de llegar
- `en_preparacion`: Se está preparando
- `listo`: Listo para entregar

---

### 📍 RUTA 2: GET `/cocina/pedido/<id>` - DETALLE DE PEDIDO

```python
@cocina.route('/cocina/pedido/<int:id_pedido>')
@login_required
@roles_required('cocina', 'administrador')
def detalle_pedido_cocina(id_pedido):
    """
    Muestra detalle completo de un pedido:
    - Cliente
    - Cada item con cantidad
    - Notas/observaciones
    """
    cur = mysql.connection.cursor()

    # QUERY 1: Obtener datos del pedido
    cur.execute("""
        SELECT id_pedido, numero_pedido, nombre_cliente_invitado, 
               telefono_cliente_invitado, estado, fecha_pedido, total
        FROM pedidos
        WHERE id_pedido = %s
    """, (id_pedido,))
    pedido = cur.fetchone()
    # pedido = (1, 'PED-20260401143025', 'Juan', '5554123456', 'confirmado', ..., 90.00)

    if not pedido:
        cur.close()
        flash('Pedido no encontrado.')
        return redirect(url_for('cocina.lista_pedidos_cocina'))

    # QUERY 2: Obtener detalles (items)
    cur.execute("""
        SELECT p.nombre, pd.cantidad, pd.observaciones
        FROM pedido_detalle pd
        INNER JOIN productos p ON pd.id_producto = p.id_producto
        WHERE pd.id_pedido = %s
    """, (id_pedido,))
    detalles = cur.fetchall()
    # detalles = [
    #   ('Hamburguesa Personalizada: Carne Roja, Queso...', 2, ''),
    #   ('Papas Fritas', 2, 'Extra sal'),
    #   ('Coca Cola', 2, '')
    # ]

    cur.close()

    return render_template('cocina_detalle.html', pedido=pedido, detalles=detalles)
```

---

### 📍 RUTA 3: GET `/cocina/cambiar_estado/<id>/<estado>` - CAMBIAR ESTADO

```python
@cocina.route('/cocina/cambiar_estado/<int:id_pedido>/<string:nuevo_estado>')
@login_required
@roles_required('cocina', 'administrador')
def cambiar_estado_pedido(id_pedido, nuevo_estado):
    """
    Avanza el estado de un pedido:
    confirmado → en_preparacion → listo → entregado
    """
    # VALIDAR que el estado es permitido
    estados_validos = ['en_preparacion', 'listo', 'entregado']

    if nuevo_estado not in estados_validos:
        flash('Estado no válido.')
        return redirect(url_for('cocina.lista_pedidos_cocina'))

    # ACTUALIZAR estado en BD
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE pedidos
        SET estado = %s
        WHERE id_pedido = %s
    """, (nuevo_estado, id_pedido))
    mysql.connection.commit()
    cur.close()

    # MENSAJES POR ESTADO
    mensajes = {
        'en_preparacion': 'Pedido en preparación...',
        'listo': 'Pedido listo para entregar.',
        'entregado': 'Pedido entregado al cliente.'
    }

    flash(mensajes.get(nuevo_estado, 'Estado actualizado.'))
    return redirect(url_for('cocina.lista_pedidos_cocina'))
```

**Flujo de estados:**
```
confirmado (llegó) 
    ↓
en_preparacion (estoy haciendo)
    ↓
listo (hecho, esperando cliente)
    ↓
entregado (cliente recibió)
```

---

## 🏥 Sistema de Inventario Completo

### FUNCIÓN 1: `verificar_stock_suficiente()`

```python
def verificar_stock_suficiente(conexion, id_producto, cantidad_solicitada):
    """
    Verifica si hay stock para un producto usando su RECETA.
    
    ¿Por qué receta? Porque un producto puede necesitar
    múltiples insumos. Ej: Papas necesitan: papa (kg), aceite, sal.
    """
    cur = conexion.cursor()

    # Obtener RECETA del producto
    cur.execute("""
        SELECT r.id_insumo, i.nombre, i.stock_actual, r.cantidad
        FROM recetas r
        INNER JOIN insumos i ON r.id_insumo = i.id_insumo
        WHERE r.id_producto = %s
    """, (id_producto,))
    receta = cur.fetchall()
    # receta = [(30, 'Papa', 100.0, 0.25), (31, 'Aceite', 50.0, 0.05)]
    
    # VERIFICAR CADA COMPONENTE DE LA RECETA
    for id_insumo, nombre_insumo, stock_actual, cantidad_receta in receta:
        # Stock necesario = cantidad_receta × cantidad_solicitada
        stock_requerido = float(cantidad_receta) * float(cantidad_solicitada)
        # Ejemplo: 0.25 kg × 2 = 0.5 kg de papa

        # ¿Hay suficiente?
        if float(stock_actual) < stock_requerido:
            cur.close()
            return False, (
                f"No hay suficiente stock para '{nombre_insumo}'. "
                f"Disponible: {stock_actual}, requerido: {stock_requerido}"
            )
            # Devuelve línea como:
            # "No hay suficiente stock para 'Papa'. Disponible: 100.0, requerido: 0.5"

    cur.close()
    return True, None  # ✅ Todo OK
```

**Ejemplo de cálculo:**
```
Producto: Papas Fritas (ID 5)
Cantidad solicitada: 2 unidades

Receta de Papas:
├─ Papa: 0.25 kg por unidad
│   Stock actual: 100 kg
│   Necesita: 0.25 × 2 = 0.5 kg
│   ¿0.5 <= 100? SÍ ✅

└─ Aceite: 0.05 L por unidad
    Stock actual: 50 L
    Necesita: 0.05 × 2 = 0.1 L
    ¿0.1 <= 50? SÍ ✅

Resultado: (True, None) → PUEDE CONTINUAR
```

---

### FUNCIÓN 2: `verificar_stock_carrito()`

```python
def verificar_stock_carrito(conexion, carrito):
    """
    Verifica TODOS los items del carrito.
    Si UNO falla → RECHAZA TODO.
    """
    for item in carrito:
        if item.get('tipo') == 'combo':
            # Verificar combo
            ok, mensaje = verificar_stock_combo(
                conexion, 
                item['id_combo'], 
                item['cantidad']
            )
            if not ok:
                return False, f"Combo '{item['nombre']}': {mensaje}"
                
        elif item.get('tipo') == 'personalizado':
            # Verificar personalizado
            ok, mensaje = verificar_stock_personalizado(
                conexion, 
                item['id_base'], 
                item.get('ingredientes', []), 
                item['cantidad']
            )
            if not ok:
                return False, f"Personalizado '{item['nombre']}': {mensaje}"
                
        else:
            # Verificar producto normal
            ok, mensaje = verificar_stock_suficiente(
                conexion=conexion,
                id_producto=item['id_producto'],
                cantidad_solicitada=item['cantidad']
            )
            if not ok:
                return False, f"Producto '{item['nombre']}': {mensaje}"

    return True, None  # ✅ TODOS PASARON
```

**Ejemplo:**
```
Carrito:
1. Combo (Combo Completo, qty=1)     → Verificar...
2. Personalizado (Hamburguesa, qty=2)→ Verificar...
3. Producto (Papas, qty=1)           → Verificar...

Si #1 OK, #2 OK, #3 OK → return (True, None)
Si #1 OK, #2 FALLA     → return (False, "mensaje error")
                           # NO VERIFICA #3
```

---

### FUNCIÓN 3: `verificar_stock_personalizado()`

```python
def verificar_stock_personalizado(conexion, id_base, ingredientes_ids, cantidad_solicitada):
    """
    Verifica si hay ingredientes para una hamburguesa personalizada.
    
    Verifica:
    1. Carne base
    2. Todos los ingredientes adicionales
    """
    cur = conexion.cursor()
    
    # VERIFICAR CARNE BASE
    cur.execute("""
        SELECT nombre, stock_actual
        FROM insumos
        WHERE id_insumo = %s
    """, (int(id_base),))
    insumo_base = cur.fetchone()
    # insumo_base = ('Carne Roja', 50)
    
    if insumo_base:
        nombre_base, stock_actual = insumo_base
        if float(stock_actual) < float(cantidad_solicitada):
            cur.close()
            return False, f"Insumo '{nombre_base}': stock insuficiente"
        # Ejemplo: "Carne Roja: stock insuficiente"

    # VERIFICAR CADA INGREDIENTE
    for ing_id in ingredientes_ids:  # [3, 4, 5]
        cur.execute("""
            SELECT nombre, stock_actual
            FROM insumos
            WHERE id_insumo = %s
        """, (int(ing_id),))
        insumo = cur.fetchone()
        # insumo = ('Pepinillos', 100)
        
        if insumo:
            nombre_insumo, stock_actual = insumo
            if float(stock_actual) < float(cantidad_solicitada):
                cur.close()
                return False, f"Insumo '{nombre_insumo}': stock insuficiente"

    cur.close()
    return True, None  # ✅ TODO BIEN
```

**Diferencia importante:**
Para personalizado NO usa receta (porque los ingredientes son individuales).
Simplemente verifica: ¿hay 1 unidad de cada ingrediente?

---

### FUNCIÓN 4: `descontar_inventario_por_producto()`

```python
def descontar_inventario_por_producto(conexion, id_producto, cantidad_vendida, referencia):
    """
    Descuenta del inventario usando la RECETA.
    Usa la misma lógica de cálculo que verificar_stock_suficiente.
    """
    cur = conexion.cursor()

    # Obtener receta
    cur.execute("""
        SELECT id_insumo, cantidad
        FROM recetas
        WHERE id_producto = %s
    """, (id_producto,))
    receta = cur.fetchall()
    # receta = [(30, 0.25), (31, 0.05)]

    # DESCONTAR CADA COMPONENTE
    for id_insumo, cantidad_receta in receta:
        # Calcular cuánto descontar
        cantidad_total_descontar = float(cantidad_receta) * float(cantidad_vendida)
        # Ejemplo: 0.25 × 2 = 0.5 kg

        # ACTUALIZAR STOCK
        cur.execute("""
            UPDATE insumos
            SET stock_actual = stock_actual - %s
            WHERE id_insumo = %s
        """, (cantidad_total_descontar, id_insumo))
        # SQ: UPDATE insumos SET stock = 100 - 0.5 WHERE id = 30
        # Resultado: 100 - 0.5 = 99.5 kg

        # REGISTRAR MOVIMIENTO (para auditoría)
        cur.execute("""
            INSERT INTO movimientos_inventario (
                id_insumo,
                tipo_movimiento,
                cantidad,
                referencia,
                observacion,
                fecha_movimiento
            )
            VALUES (%s, 'salida_venta', %s, %s, 'Venta pedido web', NOW())
        """, (id_insumo, cantidad_total_descontar, referencia))

    cur.close()
```

**Ejemplo de ejecución:**
```
Vendí 2 Papas Fritas (ID 5)

Receta de Papas:
├─ Papa (ID 30, qty 0.25 kg/unidad)
│   Actualizar: 100 - (0.25 × 2) = 100 - 0.5 = 99.5 kg
│   Registrar: papas, 0.5 kg, "PED-20260401143025"

└─ Aceite (ID 31, qty 0.05 L/unidad)
    Actualizar: 50 - (0.05 × 2) = 50 - 0.1 = 49.9 L
    Registrar: aceite, 0.1 L, "PED-20260401143025"

Resultado en BD:
┌─ insumos:
│  Papa stock: 99.5
│  Aceite stock: 49.9
│
└─ movimientos_inventario:
   [papa, salida_venta, 0.5, PED-20260401143025]
   [aceite, salida_venta, 0.1, PED-20260401143025]
```

---

### FUNCIÓN 5: `descontar_inventario_personalizado()` - LA MÁS COMPLEJA

```python
def descontar_inventario_personalizado(
    conexion, 
    id_base, 
    ingredientes_ids, 
    cantidad_vendida, 
    referencia, 
    papas_id=None, 
    bebida_id=None
):
    """
    Descuenta para una hamburguesa personalizada.
    Descuenta:
    1. Carne base (insumo)
    2. Cada ingrediente (insumos)
    3. Papas (si las pidió)
    4. Bebida (si la pidió)
    
    MUY IMPORTANTE: Papas y bebida usan RECETA
    """
    cur = conexion.cursor()
    
    # PASO 1: DESCONTAR CARNE BASE
    cur.execute("""
        UPDATE insumos
        SET stock_actual = stock_actual - %s
        WHERE id_insumo = %s
    """, (cantidad_vendida, int(id_base)))
    # UPDATE: Carne Roja stock = 50 - 2 = 48

    # Registrar movimiento
    cur.execute("""
        INSERT INTO movimientos_inventario 
        (id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
        VALUES (%s, 'salida_venta', %s, %s, 'Descuento carne personalizado', NOW())
    """, (int(id_base), cantidad_vendida, referencia))

    # PASO 2: DESCONTAR CADA INGREDIENTE
    for ing_id in ingredientes_ids:
        # ing_id = 3 (Pepinillos)
        id_insumo = int(ing_id)
        
        cur.execute("""
            UPDATE insumos
            SET stock_actual = stock_actual - %s
            WHERE id_insumo = %s
        """, (cantidad_vendida, id_insumo))
        # UPDATE: Pepinillos stock = 100 - 2 = 98

        cur.execute("""
            INSERT INTO movimientos_inventario 
            (id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
            VALUES (%s, 'salida_venta', %s, %s, 'Descuento ingrediente personalizado', NOW())
        """, (id_insumo, cantidad_vendida, referencia))

    # PASO 3: DESCONTAR PAPAS (si se seleccionaron)
    if papas_id and papas_id != 'no':
        # papas_id = 5 (Papas Fritas)
        try:
            # Usa receta (porque papas puede tener componentes)
            descontar_inventario_por_producto(
                conexion, 
                int(papas_id), 
                cantidad_vendida, 
                referencia
            )
            # Descuenta usando receta de Papas Fritas
        except:
            pass  # Si hay error, continúa sin fallar

    # PASO 4: DESCONTAR BEBIDA (si se seleccionó)
    if bebida_id and bebida_id != 'no':
        # bebida_id = 4 (Coca Cola)
        try:
            # Usa receta (porque bebida puede tener componentes)
            descontar_inventario_por_producto(
                conexion, 
                int(bebida_id), 
                cantidad_vendida, 
                referencia
            )
        except:
            pass

    cur.close()
```

**Resumen de descuentos en 1 hamburguesa:**
```
┌─ Insumos (directos):
│  ├─ Carne Roja: 50 - 1 = 49
│  ├─ Pepinillos: 100 - 1 = 99
│  ├─ Tomate: 80 - 1 = 79
│  └─ Cebolla: 60 - 1 = 59
│
├─ Papas Fritas (usa receta):
│  ├─ Papa: 100 - 0.25 = 99.75 kg
│  └─ Aceite: 50 - 0.05 = 49.95 L
│
└─ Coca Cola (usa receta):
   └─ Botella: 100 - 1 = 99
```

---

## 📊 Base de Datos - Esquema Completo

### Tabla: `productos`
```sql
id_producto | nombre                | id_categoria | precio | estado  | disponible
1           | Hamburguesa Clásica   | 1           | 45.00  | activo  | si
2           | Combo Completo        | 1           | 60.00  | activo  | si
4           | Coca Cola             | 2           | 10.00  | activo  | si
5           | Papas Fritas          | 3           | 15.00  | activo  | si
```

### Tabla: `insumos`
```sql
id_insumo | nombre          | costo_referencia | stock_actual | estado
1         | Carne Roja      | 20.00           | 50          | activo
2         | Queso Cheddar   | 5.00            | 30          | activo
3         | Pepinillos      | 1.00            | 100         | activo
4         | Tomate          | 2.00            | 80          | activo
30        | Papa            | 15.00           | 100.0       | activo
31        | Aceite          | 30.00           | 50.0        | activo
```

### Tabla: `recetas` (composición de productos)
```sql
id_producto | id_insumo | cantidad
5 (Papas)   | 30 (Papa) | 0.25
5 (Papas)   | 31 (Aceite) | 0.05
4 (Coca)    | 32 (Botella) | 1
```

### Tabla: `pedidos`
```sql
id_pedido | numero_pedido      | nombre_cliente | estado | total
1         | PED-20260401143025 | Juan           | confirmado | 90.00
```

### Tabla: `movimientos_inventario` (auditoría)
```sql
id_insumo | tipo_movimiento | cantidad | referencia         | fecha
1         | salida_venta    | 2        | PED-20260401143025 | 2026-04-01 14:30
3         | salida_venta    | 2        | PED-20260401143025 | 2026-04-01 14:30
```

---

## 💾 Gestor de Sesiones y Carrito

### Cómo funciona sesión en Flask:

```python
# Obtener carrito (o crear uno vacío)
carrito = session.get('carrito', [])

# Modificar carrito
carrito.append(nuevo_item)

# Guardar en sesión
session['carrito'] = carrito
session.modified = True  # Marca para guardar
```

**Estructura del archivo de sesión:**
```
{ 
  "carrito": [
    {
      "tipo": "combo",
      "id_combo": 1,
      "nombre": "Combo Completo",
      "precio": 60.00,
      "cantidad": 1,
      "subtotal": 60.00
    },
    {
      "tipo": "personalizado",
      "id_base": 1,
      "pan": "integral",
      "queso": 2,
      "ingredientes": [3, 4],
      "papas": 5,
      "bebida": 4,
      "nombre": "Hamburguesa Personalizada: ...",
      "precio": 45.00,
      "cantidad": 2,
      "subtotal": 90.00
    }
  ]
}
```

**Duración:**
- Se guarda en navegador como cookie/archivo
- Expira después de un tiempo (configurable)
- Se limpia al vaciar carrito o confirmar

---

## 🚨 Manejo de Errores

### Errores Controlados:

```python
# 1. Carrito vacío
if not carrito:
    return jsonify({'error': 'Tu carrito está vacío.'}), 400

# 2. Nombre no ingresado
if not nombre_cliente:
    return jsonify({'error': 'Debes ingresar tu nombre.'}), 400

# 3. Stock insuficiente
if not stock_ok:
    return jsonify({'error': mensaje_stock}), 400

# 4. Error de BD
try:
    # Operaciones BD
    mysql.connection.commit()
except Exception as e:
    mysql.connection.rollback()
    return jsonify({'error': f'Error: {str(e)}'}), 500
```

### Respuestas JSON:
```json
/* Success */
{
    "numero_pedido": "PED-20260401143025",
    "estado": "confirmado",
    "total": 90.00,
    "items": [...]
}

/* Error */
{
    "error": "No hay suficiente stock de Carne Roja"
}
```

---

## ✅ Testing y Validación

### Test 1: Verificar Stock
```python
# Simulación:
carrito = [
    {
        'tipo': 'personalizado',
        'id_base': 1,            # Carne
        'ingredientes': [3, 4],   # Pepinillos, Tomate
        'papas': 5,              # Papas Fritas
        'bebida': 4,             # Coca Cola
        'cantidad': 10          # ← MANY!
    }
]

# Verificar stock
ok, msg = verificar_stock_carrito(conexion, carrito)

# Si qty 10 es > stock disponible
# Result: (False, "Pepinillos: stock insuficiente")
# Pedido RECHAZADO
```

### Test 2: Flujo Completo
```python
# 1. Usuario accede a /
# → Carga menú con bebidas y papas

# 2. Usuario personaliza y agrega al carrito
# → Item se agrega a sesión

# 3. Usuario confirma
# → Verificar stock OK
# → Crear pedido
# → Descontar inventario
# → Devolver confirmación

# 4. Usuario accede a /pedido/PED-20260401143025
# → Ve detalles del pedido
```

---

## 📋 Checklist de Funcionalidades

- [x] Cargar menú con productos dinámicos
- [x] Obtener bebidas de BD (categoría 2)
- [x] Obtener papas de BD (categoría 3)
- [x] Agregar combo al carrito
- [x] Crear personalización
- [x] Precio fijo sin extras
- [x] Manejar carrito en sesión
- [x] Sumar/restar items
- [x] Vaciar carrito
- [x] Verificar stock ANTES de confirmar
- [x] Crear pedido en BD
- [x] Generar venta automática
- [x] Descontar inventario
- [x] Registrar movimientos (auditoría)
- [x] Ver estado de pedidos
- [x] Manejo de transacciones
- [x] Rollback en errores

---

## �️ Roles y Permisos

### Sistema de Roles

```python
# Tabla: roles
id_rol | nombre
1      | administrador     # Control total
2      | cocina            # Solo panel de cocina
3      | cajero            # Ventas y pedidos
4      | cliente           # Solo menú público (sin rol en BD)
```

### Matriz de Acceso

| Ruta | Admin | Cocina | Cajero | Cliente |
|------|-------|--------|--------|---------|
| `/` | ✅ | ✅ | ✅ | ✅ |
| `/login` | ✅ | ✅ | ✅ | ❌ |
| `/dashboard` | ✅ | ✅ | ✅ | ❌ |
| `/admin/*` | ✅ | ❌ | ❌ | ❌ |
| `/cocina/*` | ✅ | ✅ | ❌ | ❌ |
| `/carrito` | ✅ | ✅ | ✅ | ✅ |
| `/personalizar_hamburguesa` | ✅ | ✅ | ✅ | ✅ |
| `/confirmar_pedido` | ✅ | ✅ | ✅ | ✅ |

### Decoradores de Protección

```python
# SOLO LOGUEADOS
@login_required
def función():
    # Acceso: Todos los roles logueados

# SOLO ADMIN
@roles_required('administrador')
def función():
    # Acceso: Solo administrador

# ADMIN O COCINA
@roles_required('administrador', 'cocina')
def función():
    # Acceso: Administrador O Cocina

# ADMIN O CAJERO
@roles_required('administrador', 'cajero')
def función():
    # Acceso: Administrador O Cajero
```

---

## 📊 Flujo Completo de Roles

### 👥 Rol: CLIENTE (sin autenticación)

```
1. Accede a http://localhost:5000
2. Ve menú de productos
3. Personaliza hamburguesa
4. Agrega al carrito
5. Confirma pedido (sin login)
6. Recibe número de pedido
7. Accede a /pedido/PED-xxx para ver estado
```

### 📋 Rol: CAJERO

```
1. Login → /login
2. Ve /dashboard con estadísticas
3. Accede a /admin/ventas (ver ventas)
4. Accede a /admin/estado-pedidos (ver pedidos)
5. NO puede:
   - Editar empleados
   - Ver inventario
   - Acceder a /cocina/*
```

### 👨‍🍳 Rol: COCINA

```
1. Login → /login
2. Ve /dashboard (gráficos)
3. Accede a /cocina/pedidos
4. Ve detalles: /cocina/pedido/<id>
5. Cambia estado: /cocina/cambiar_estado/<id>/<estado>
6. NO puede:
   - Ver inventario
   - Ver empleados
   - Ver ventas/compras
   - Acceder a /admin/*
```

### 👨‍💼 Rol: ADMINISTRADOR

```
1. Login → /login
2. Ve /admin/dashboard (todos los datos)
3. Accede a:
   - /admin/ventas
   - /admin/inventario
   - /admin/empleados (CRUD)
   - /admin/proveedores (CRUD)
   - /admin/estado-pedidos
4. Accede a /cocina/* (puede ver cocina)
5. PERMISOS TOTALES
```

---

## 🚨 Manejo de Errores

### Errores de Autenticación

```python
# Error 1: Usuario no logueado
if 'user_id' not in session:
    flash('Debes iniciar sesión primero.')
    return redirect(url_for('auth.login'))

# Respuesta: Redirige a login

# Error 2: Rol insuficiente
if session['rol'] not in roles_permitidos:
    flash('No tienes permiso para acceder.')
    return redirect(url_for('auth.dashboard'))

# Respuesta: Redirige a dashboard
```

### Errores de Negocio

```python
# Error 1: Carrito vacío
if not carrito:
    return jsonify({'error': 'Tu carrito está vacío.'}), 400

# Error 2: Stock insuficiente
stock_ok, mensaje = verificar_stock_carrito(conexion, carrito)
if not stock_ok:
    return jsonify({'error': mensaje}), 400

# Error 3: Nombre cliente requerido
if not nombre_cliente:
    return jsonify({'error': 'Debes ingresar tu nombre.'}), 400

# Error 4: BD error
try:
    mysql.connection.commit()
except Exception as e:
    mysql.connection.rollback()
    return jsonify({'error': f'Error: {str(e)}'}), 500
```

### Respuestas JSON

```json
/* Success - Pedido confirmado */
{
    "numero_pedido": "PED-20260401143025",
    "estado": "confirmado",
    "total": 90.00,
    "items": [...]
}

/* Error - Stock insuficiente */
{
    "error": "Carne Roja: stock insuficiente"
}

/* Error - BD */
{
    "error": "Error al confirmar pedido: Connection lost"
}
```

---

## ✅ Testing y Validación

### Test 1: Flujo de Login

```python
# 1. POST /login con credenciales correctas
username="juan_perez", password="123456"
→ ✅ Redirecciona a /dashboard

# 2. POST /login con contraseña incorrecta
username="juan_perez", password="wrongpass"
→ ❌ Flash: "Contraseña incorrecta"

# 3. POST /login con usuario no existente
username="noexiste", password="anypass"
→ ❌ Flash: "Usuario no encontrado"

# 4. GET /admin/dashboard sin login
→ ❌ Flash: "Debes iniciar sesión primero"
→ Redirecciona a /login

# 5. GET /admin/dashboard después de logout
→ ❌ Misma respuesta que #4
```

### Test 2: Validación de Roles

```python
# Usuario COCINA intenta acceder a /admin/empleados
@roles_required('administrador')  # ← Solo admin
→ ❌ Flash: "No tienes permiso"
→ Redirecciona a /dashboard

# Usuario CAJERO intenta acceder a /cocina/pedidos
@roles_required('cocina', 'administrador')  # ← No incluye cajero
→ ❌ Flash: "No tienes permiso"

# Usuario ADMIN accede a /cocina/pedidos
@roles_required('cocina', 'administrador')  # ← Admin sí está incluido
→ ✅ Acceso permitido
```

### Test 3: Pedido Completo

```python
# Test: Cliente personaliza y confirma

1. GET / 
   → ✅ Carga menú con bebidas (BD)
   
2. POST /personalizar_hamburguesa
   → ✅ Agrega a sesión['carrito']
   
3. GET /carrito
   → ✅ Muestra items con total
   
4. POST /confirmar_pedido
   → Verifica stock: OK ✅
   → Crea pedido: ID 1
   → Crea venta: ID 1
   → Descuenta inventario: OK ✅
   → Commit: OK ✅
   → Response: {"numero_pedido": "PED-xxx"}
   
5. GET /pedido/PED-xxx
   → ✅ Muestra detalles del pedido
   
Estado en BD:
- pedidos: estado = 'confirmado'
- ventas: estado = 'pagada'
- insumos: stock_actual reducido
- movimientos_inventario: nuevos registros
```

---

## 🔐 Seguridad Implementada

### 1. Contraseñas

```python
# Registro: Hashear antes de guardar
password_hash = generate_password_hash('123456')
# Resultado: $2b$12$K1DvxQD2P5D2lZqPf8c1N.ZKZq1PfV6Q1Q1Q1Q1Q1Q1Q1Q1Q1

# Login: Comparar hash
if check_password_hash(password_hash, input_password):
    # Contraseña correcta
```

### 2. Sesiones

```python
# Crear sesión después de login
session['user_id'] = usuario_id
session['rol'] = rol
session.modified = True

# Destruir sesión en logout
session.clear()
```

### 3. Validación de Roles

```python
# Antes de ejecutar cualquier operación sensible
@roles_required('administrador')
# Valida que session['rol'] == 'administrador'
```

### 4. Validación de Entrada

```python
# Limpiar whitespace
username = request.form['username'].strip()

# Validar cantidad > 0
if cantidad <= 0:
    return error

# Validar email válido (mejor práctica)
# (no implementado pero recomendado)
```

### 5. Transacciones BD

```python
try:
    # Operaciones
    mysql.connection.commit()  # Solo si TODO OK
except:
    mysql.connection.rollback()  # Revierta TODO
```

---

## 📋 Checklist Completo

### Funcionalidades PUBLIC

- [x] Cargar menú dinámico
- [x] Obtener bebidas de BD
- [x] Obtener papas de BD
- [x] Agregar combo
- [x] Personalizar hamburguesa
- [x] Precio fijo sin extras
- [x] Carrito en sesión
- [x] Sumar/restar items
- [x] Vaciar carrito
- [x] Verificar stock ANTES de vender
- [x] Crear pedido
- [x] Crear venta automática
- [x] Descontar inventario
- [x] Ver estado de pedidos

### Funcionalidades AUTH

- [x] Login con hash
- [x] Crear sesión
- [x] Dashboard general
- [x] Logout
- [x] @login_required
- [x] @roles_required

### Funcionalidades ADMIN

- [x] Dashboard con estadísticas
- [x] Listar ventas
- [x] Ver estado pedidos
- [x] Listar inventario
- [x] Proveedores CRUD (crear, editar, listar)
- [x] Empleados CRUD (crear, editar, listar)
- [x] Compras CRUD (crear, editar, eliminar, listar) ⭐ NUEVO
- [x] Crear usuario con rol
- [x] Hash de contraseña
- [x] Actualizar stock automáticamente en compras
- [x] Auditoría de compras en movimientos_inventario

### Funcionalidades COCINA

- [x] Lista de pedidos
- [x] Detalle de pedido
- [x] Cambiar estado (confirmado → en_preparacion → listo → entregado)

---

## 🚀 Resumen de Módulos

| Módulo | Rutas | Protección | Uso |
|--------|-------|-----------|-----|
| PUBLIC | 9 rutas | Ninguna | Clientes (sin login) |
| AUTH | 3 rutas | login_required | Todos los roles |
| ADMIN | 14 rutas | @roles_required('admin') | Solo Administrador |
| COCINA | 3 rutas | @roles_required('cocina') | Personal de cocina |

### Desglose de Rutas ADMIN (14 en total)

| # | Ruta | Método | Descripción |
|----|------|--------|-------------|
| 1 | `/admin/dashboard` | GET | Dashboard estadísticas |
| 2 | `/admin/ventas` | GET | Listar ventas |
| 3 | `/admin/estado-pedidos` | GET | Estado de pedidos |
| 4 | `/admin/inventario` | GET | Listar insumos |
| 5 | `/admin/proveedores` | GET | Listar proveedores |
| 6 | `/admin/proveedores/nuevo` | GET/POST | Crear proveedor |
| 7 | `/admin/proveedores/editar/<id>` | GET/POST | Editar proveedor |
| 8 | `/admin/empleados` | GET | Listar empleados |
| 9 | `/admin/empleados/nuevo` | GET/POST | Crear empleado |
| 10 | `/admin/empleados/editar/<id>` | GET/POST | Editar empleado |
| 11 | `/admin/compras` | GET | Listar compras |
| 12 | `/admin/compras/nueva` | GET/POST | Crear compra ⭐ |
| 13 | `/admin/compras/editar/<id>` | GET/POST | Editar compra |
| 14 | `/admin/compras/eliminar/<id>` | POST | Eliminar compra |

---

**Documento creado: 2026-04-01**
**Versión: 2.0 ADMIN COMPLETO**
**Estado: COMPLETADO ✅**


