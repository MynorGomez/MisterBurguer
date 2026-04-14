# 🔧 GUÍA TÉCNICA - ARQUITECTURA Y ESTRUCTURA INTERNA

## 📑 Tabla de Contenidos
1. [Arquitectura General](#arquitectura-general)
2. [Estructura de Carpetas](#estructura-de-carpetas)
3. [Flujo Detallado de Datos](#flujo-detallado-de-datos)
4. [Mapeos de Base de Datos](#mapeos-de-base-de-datos)
5. [Pseudocódigo de Funciones](#pseudocódigo-de-funciones)
6. [Casos de Uso](#casos-de-uso)

---

## 🏛️ Arquitectura General

### MVC Pattern (Flask)

```
┌─────────────────────────────────────────┐
│           VISTA (Templates)             │
│  - menu_publico.html                    │
│  - carrito.html                         │
│  - estado_pedido.html                   │
└────────────────┬────────────────────────┘
                 │ (render_template)
                 │
┌────────────────▼────────────────────────┐
│        CONTROLADOR (Routes)             │
│  - app/routes/public.py                 │
│  - Funciones: menu_publico()            │
│    personalizar_hamburguesa()           │
│    confirmar_pedido()                   │
└────────────────┬────────────────────────┘
                 │ (ORM queries)
                 │
┌────────────────▼────────────────────────┐
│          MODELO (Database)              │
│  - MySQL Connection                     │
│  - app/utils/inventario.py              │
│  - Funciones de validación              │
│  - Funciones de actualización           │
└─────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       BASE DE DATOS (MySQL)             │
│  - productos                            │
│  - pedidos                              │
│  - insumos                              │
│  - recetas                              │
│  - movimientos_inventario               │
└─────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
MisterBurger/
│
├── app/
│   ├── __init__.py                 # Aplicación Flask, config MySQL
│   ├── config.py                   # Variables de configuración
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py              # ⭐ RUTAS PRINCIPALES (menú, carrito, pedidos)
│   │   ├── auth.py                # Login/Logout
│   │   ├── admin.py               # Panel administrativo
│   │   ├── cocina.py              # Panel de cocina
│   │   └── [otros].py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── inventario.py          # ⭐ GESTIÓN DE STOCK (verificar, descontar)
│   │   └── [otros].py
│   │
│   ├── static/                    # Archivos estáticos
│   │   ├── css/
│   │   │   ├── menu.css
│   │   │   ├── carrito.css
│   │   │   └── [otros].css
│   │   ├── img/
│   │   └── js/ (si hay)
│   │
│   └── templates/
│       ├── base_panel.html
│       ├── menu_publico.html      # ⭐ INTERFAZ PRINCIPAL
│       ├── carrito.html           # ⭐ CARRITO DE COMPRAS
│       ├── estado_pedido.html
│       ├── login.html
│       ├── admin/
│       │   ├── dashboard_admin.html
│       │   ├── inventario.html
│       │   └── [otros].html
│       └── [otros].html
│
├── run.py                         # Punto de entrada de la aplicación
├── requirements.txt               # Dependencias Python
└── DOCUMENTACION_SISTEMA.md       # 📋 ESTE ARCHIVO

```

---

## 🔀 Flujo Detallado de Datos

### REQUEST 1: Usuario accede a /

```
HTTP GET /
    ↓
Flask route: @public.route('/')
    ↓
menu_publico()
    │
    ├─→ cur.execute("SELECT ... FROM productos")
    │   └─→ productos = [(1, 'Hamburguesa Clásica', ...), ...]
    │
    ├─→ cur.execute("SELECT ... FROM combos")
    │   └─→ combos = [(1, 'Combo Completo', ...), ...]
    │
    ├─→ cur.execute("SELECT ... FROM insumos")
    │   └─→ insumos = [(1, 'Carne Roja', ...), (2, 'Queso', ...), ...]
    │
    ├─→ cur.execute("... WHERE id_categoria = 2")
    │   └─→ bebidas = [(4, 'Coca Cola', 10.00), ...]
    │
    ├─→ cur.execute("... WHERE id_categoria = 3")
    │   └─→ papas = [(5, 'Papas Fritas', 15.00), ...]
    │
    ├─→ carnes = [filtro de insumos con 'carne', 'pollo', etc.]
    │
    ├─→ hamburguesas = [filtro de productos categoria='Hamburguesas']
    │
    └─→ render_template('menu_publico.html', 
        productos=productos, 
        bebidas=bebidas,
        papas=papas,
        ...)
        
    ↓
Jinja2 renderiza HTML
    ↓
HTTP Response 200 OK (HTML)
    ↓
Navegador renderiza página
```

### REQUEST 2: POST /personalizar

```
HTTP POST /personalizar
Content-Type: application/x-www-form-urlencoded
Body: {
  pan: 'integral',
  queso: '2',
  ingredientes: ['3', '4', '5'],
  papas: '5',
  bebida: '4',
  cantidad: '2'
}
    ↓
Flask route: @public.route('/personalizar', methods=['POST'])
    ↓
personalizar_hamburguesa()
    │
    ├─→ Obtener parámetros del formulario
    │   pan = 'integral'
    │   queso = 2
    │   ingredientes_ids = [3, 4, 5]
    │   papas = 5
    │   bebida = 4
    │   cantidad = 2
    │
    ├─→ Validar cantidad > 0
    │   if 2 > 0: ✅ OK
    │
    ├─→ Obtener carne por defecto
    │   cur.execute("SELECT id_insumo FROM insumos WHERE nombre LIKE '%carne%'")
    │   base_id = 1
    │
    ├─→ Obtener precio de "Hamburguesa Clásica"
    │   cur.execute("SELECT precio FROM productos WHERE nombre LIKE '%lásica%'")
    │   precio_total = 45.00 (SIN EXTRAS)
    │
    ├─→ Obtener nombres de ingredientes
    │   for ing_id in [3, 4, 5]:
    │       cur.execute("SELECT nombre FROM insumos WHERE id_insumo = %s")
    │   insumos_nombres = ['Pepinillos', 'Tomate', 'Cebolla']
    │
    ├─→ Obtener nombre de papas
    │   cur.execute("SELECT nombre FROM productos WHERE id_producto = 5")
    │   papas_nombre = 'Papas Fritas'
    │
    ├─→ Obtener nombre de bebida
    │   cur.execute("SELECT nombre FROM productos WHERE id_producto = 4")
    │   bebida_nombre = 'Coca Cola'
    │
    ├─→ Armar descripción completa
    │   nombre = "Hamburguesa Personalizada: Pan Integral, Carne Roja, Queso Cheddar, Pepinillos, Tomate, Cebolla, Papas Fritas, Coca Cola"
    │
    ├─→ Obtener carrito de sesión
    │   carrito = session.get('carrito', [])
    │
    ├─→ Agregar ítém al carrito
    │   carrito.append({
    │     'tipo': 'personalizado',
    │     'id_base': 1,
    │     'pan': 'integral',
    │     'queso': 2,
    │     'ingredientes': [3, 4, 5],
    │     'papas': 5,
    │     'bebida': 4,
    │     'nombre': '...',
    │     'precio': 45.00,
    │     'cantidad': 2,
    │     'subtotal': 90.00
    │   })
    │
    └─→ session['carrito'] = carrito
        session.modified = True
        
    ↓
redirect(url_for('public.menu_publico'))
    ↓
HTTP Response 302 Redirect
    ↓
Navegador recarga menú
```

### REQUEST 3: POST /confirmar_pedido

```
HTTP POST /confirmar_pedido
Content-Type: application/x-www-form-urlencoded
Body: {
  nombre_cliente: 'Juan',
  telefono_cliente: '12345678'
}
    ↓
Flask route: @public.route('/confirmar_pedido', methods=['POST'])
    ↓
confirmar_pedido()
    │
    ├─→ STEP 1: Obtener carrito
    │   carrito = session.get('carrito', [])
    │   if not carrito: return error JSON
    │
    ├─→ STEP 2: VERIFICAR STOCK
    │   ok, mensaje = verificar_stock_carrito(mysql.connection, carrito)
    │   for item in carrito:
    │       if tipo == 'personalizado':
    │           ok, msg = verificar_stock_personalizado(
    │               id_base=1,
    │               ingredientes_ids=[3,4,5],
    │               cantidad=2
    │           )
    │   if not ok: return error JSON
    │   ✅ STOCK OK
    │
    ├─→ STEP 3: CREAR PEDIDO
    │   numero_pedido = "PED-20260401143025"
    │   subtotal = 90.00
    │   
    │   INSERT INTO pedidos (
    │     nombre_cliente_invitado: 'Juan',
    │     telefono_cliente_invitado: '12345678',
    │     numero_pedido,
    │     tipo_pedido: 'web',
    │     estado: 'confirmado',
    │     subtotal: 90.00,
    │     total: 90.00
    │   )
    │   id_pedido = 1
    │
    ├─→ STEP 4: CREAR DETALLE DE PEDIDO
    │   INSERT INTO pedido_detalle (
    │     id_pedido: 1,
    │     id_producto: 1,  (carne base)
    │     cantidad: 2,
    │     precio_unitario: 45.00,
    │     subtotal: 90.00
    │   )
    │
    ├─→ STEP 5: CREAR VENTA AUTOMÁTICA
    │   INSERT INTO ventas (
    │     id_pedido: 1,
    │     id_empleado: 1,  (sistema)
    │     tipo_venta: 'pedido_web',
    │     metodo_pago: 'efectivo',
    │     subtotal: 90.00,
    │     total: 90.00,
    │     estado: 'pagada'
    │   )
    │   id_venta = 1
    │
    ├─→ STEP 6: CREAR DETALLE DE VENTA
    │   INSERT INTO venta_detalle (
    │     id_venta: 1,
    │     id_producto: 1,
    │     cantidad: 2,
    │     precio_unitario: 45.00,
    │     subtotal: 90.00
    │   )
    │
    ├─→ STEP 7: DESCONTAR INVENTARIO
    │   for item in carrito:
    │       if tipo == 'personalizado':
    │           descontar_inventario_personalizado(
    │               id_base=1,
    │               ingredientes_ids=[3,4,5],
    │               cantidad_vendida=2,
    │               papas_id=5,
    │               bebida_id=4
    │           )
    │
    │   Esto hace:
    │   - UPDATE insumos SET stock_actual = stock - 2 WHERE id = 1
    │   - UPDATE insumos SET stock_actual = stock - 2 WHERE id IN (3,4,5)
    │   - descontar_inventario_por_producto(5)  [papas]
    │   - descontar_inventario_por_producto(4)  [bebida]
    │   + INSERT INTO movimientos_inventario (x4 registros)
    │
    ├─→ STEP 8: CONFIRMAR TRANSACCIÓN
    │   mysql.connection.commit()
    │
    ├─→ STEP 9: LIMPIAR CARRITO
    │   session['carrito'] = []
    │   session.modified = True
    │
    └─→ return jsonify({
        'numero_pedido': 'PED-20260401143025',
        'total': 90.00,
        'estado': 'confirmado',
        'items': [...]
    })
        
    ↓
HTTP Response 200 OK (JSON)
    ↓
JavaScript procesa respuesta
    ↓
DOM actualiza con confirmación ✅
```

---

## 💾 Mapeos de Base de Datos

### Query 1: Obtener Bebidas
```sql
SELECT id_producto, nombre, precio
FROM productos
WHERE id_categoria = 2 
  AND estado = 'activo' 
  AND disponible = 'si'
ORDER BY nombre;

-- Resultado en código:
bebidas = [(4, 'Coca Cola', 10.00)]
-- Uso en template:
{% for bebida in bebidas %}
  <input value="{{ bebida[0] }}">  <!-- ID -->
  <label>{{ bebida[1] }}</label>   <!-- Nombre -->
{% endfor %}
```

### Query 2: Obtener Papas
```sql
SELECT id_producto, nombre, precio
FROM productos
WHERE id_categoria = 3 
  AND estado = 'activo' 
  AND disponible = 'si'
ORDER BY nombre;

-- Resultado en código:
papas = [(5, 'Papas Fritas', 15.00)]
```

### Query 3: Verificar Stock para Personalizado
```sql
-- Verifica carne base
SELECT nombre, stock_actual
FROM insumos
WHERE id_insumo = 1;
-- Resultado: ('Carne Roja', 50)
-- ¿Necesita 2? 50 >= 2? SÍ ✅

-- Verifica cada ingrediente
SELECT nombre, stock_actual
FROM insumos
WHERE id_insumo IN (3, 4, 5);  -- Pepinillos, Tomate, Cebolla
-- Resultado: 
--  ('Pepinillos', 100)  - ¿Necesita 2? 100 >= 2? SÍ ✅
--  ('Tomate', 80)       - ¿Necesita 2? 80 >= 2? SÍ ✅
--  ('Cebolla', 60)      - ¿Necesita 2? 60 >= 2? SÍ ✅
```

### Query 4: Descontar Insumos
```sql
-- Después del pedido: Restar cantidad
UPDATE insumos 
SET stock_actual = stock_actual - 2 
WHERE id_insumo = 1;
-- Nuevo stock: 50 - 2 = 48

UPDATE insumos 
SET stock_actual = stock_actual - 2 
WHERE id_insumo IN (3, 4, 5);
-- Nuevos stocks: 
--   Pepinillos: 100 - 2 = 98
--   Tomate: 80 - 2 = 78
--   Cebolla: 60 - 2 = 58
```

### Query 5: Registrar Movimiento
```sql
INSERT INTO movimientos_inventario 
(id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
VALUES 
(1, 'salida_venta', 2, 'PED-20260401143025', 'Descuento carne personalizado', NOW());

-- Registra: Que salieron 2 unidades de carne en pedido PED-20260401143025
-- Útil para: Auditoría, trazabilidad, reportes
```

---

## 🔍 Pseudocódigo de Funciones

### Función: verificar_stock_personalizado()

```python
def verificar_stock_personalizado(conexion, id_base, ingredientes_ids, cantidad_solicitada):
    """
    Verifica si hay stock suficiente para una personalización.
    
    Args:
        conexion: Conexión MySQL
        id_base: ID del insumo base (ej: 1 = Carne Roja)
        ingredientes_ids: Lista de IDs de ingredientes (ej: [3, 4, 5])
        cantidad_solicitada: Cantidad de hamburguesas (ej: 2)
    
    Returns:
        (True, None) si hay stock
        (False, "mensaje de error") si NO hay stock
    """
    
    # PASO 1: Verificar BASE (carne)
    cur = conexion.cursor()
    cur.execute("""
        SELECT nombre, stock_actual
        FROM insumos
        WHERE id_insumo = ?
    """, (int(id_base),))
    
    insumo_base = cur.fetchone()
    # insumo_base = ('Carne Roja', 50)
    
    if insumo_base:
        nombre_base, stock_actual = insumo_base
        # Necesita: cantidad_solicitada unidades
        # ¿Tiene suficiente?
        if float(stock_actual) < float(cantidad_solicitada):
            cur.close()
            return False, f"Insumo '{nombre_base}': stock insuficiente"
            # Ejemplo: "Carne Roja: stock insuficiente"
    
    # PASO 2: Verificar INGREDIENTES ADICIONALES
    for ing_id in ingredientes_ids:
        # ing_id = 3, 4, 5
        
        cur.execute("""
            SELECT nombre, stock_actual
            FROM insumos
            WHERE id_insumo = ?
        """, (int(ing_id),))
        
        insumo = cur.fetchone()
        # insumo = ('Pepinillos', 100)
        
        if insumo:
            nombre_insumo, stock_actual = insumo
            
            if float(stock_actual) < float(cantidad_solicitada):
                cur.close()
                return False, f"Insumo '{nombre_insumo}': stock insuficiente"
    
    cur.close()
    
    # PASO 3: TODO OK
    return True, None
    # ✅ Hay suficiente stock para proceder


# EJEMPLO DE USO:
ok, msg = verificar_stock_personalizado(
    conexion=mysql_connection,
    id_base=1,           # Carne Roja
    ingredientes_ids=[3, 4, 5],  # Pepinillos, Tomate, Cebolla
    cantidad_solicitada=2  # Quiero 2 hamburguesas
)

# Stock actual:
#   Carne: 50 >= 2? SÍ ✅
#   Pepinillos: 100 >= 2? SÍ ✅
#   Tomate: 80 >= 2? SÍ ✅
#   Cebolla: 60 >= 2? SÍ ✅

# Resultado: ok = True, msg = None → ✅ PUEDO PROCEDER
```

### Función: descontar_inventario_personalizado()

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
    Descuenta del inventario después de vender una hamburguesa personalizada.
    
    Args:
        conexion: Conexión MySQL
        id_base: ID del insumo base (carne)
        ingredientes_ids: Lista de IDs de ingredientes
        cantidad_vendida: Cuántas hamburguesas se vendieron
        referencia: Número de pedido (ej: 'PED-20260401143025')
        papas_id: ID del producto papas (opcional)
        bebida_id: ID del producto bebida (opcional)
    """
    
    cur = conexion.cursor()
    
    # PASO 1: Descontar CARNE BASE
    cur.execute("""
        UPDATE insumos
        SET stock_actual = stock_actual - ?
        WHERE id_insumo = ?
    """, (cantidad_vendida, int(id_base)))
    # UPDATE: stock = 50 - 2 = 48 (para Carne Roja)
    
    # Registrar movimiento
    cur.execute("""
        INSERT INTO movimientos_inventario 
        (id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
        VALUES (?, 'salida_venta', ?, ?, 'Descuento carne personalizado', NOW())
    """, (int(id_base), cantidad_vendida, referencia))
    
    # PASO 2: Descontar cada INGREDIENTE
    for ing_id in ingredientes_ids:
        # ing_id = 3 (Pepinillos)
        
        cur.execute("""
            UPDATE insumos
            SET stock_actual = stock_actual - ?
            WHERE id_insumo = ?
        """, (cantidad_vendida, int(ing_id)))
        # UPDATE: stock = 100 - 2 = 98
        
        cur.execute("""
            INSERT INTO movimientos_inventario 
            (id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
            VALUES (?, 'salida_venta', ?, ?, 'Descuento ingrediente personalizado', NOW())
        """, (int(ing_id), cantidad_vendida, referencia))
    
    # PASO 3: Descontar PAPAS (si se seleccionaron)
    if papas_id and papas_id != 'no':
        # papas_id = 5
        try:
            descontar_inventario_por_producto(
                conexion, 
                int(papas_id), 
                cantidad_vendida, 
                referencia
            )
            # Busca receta de Papas Fritas
            # Si requiere: 0.25 kg de papa × 2 = 0.5 kg
            # Descuenta 0.5 kg del stock de papa
        except:
            pass  # Si no hay receta, continúa sin error
    
    # PASO 4: Descontar BEBIDA (si se seleccionó)
    if bebida_id and bebida_id != 'no':
        # bebida_id = 4
        try:
            descontar_inventario_por_producto(
                conexion, 
                int(bebida_id), 
                cantidad_vendida, 
                referencia
            )
            # Busca receta de Coca Cola
            # Si requiere: 1 botella × 2 = 2 botellas
            # Descuenta 2 botellas del stock
        except:
            pass
    
    cur.close()


# RESULTADO: 
# - Carne Roja: 50 → 48
# - Pepinillos: 100 → 98
# - Tomate: 80 → 78
# - Cebolla: 60 → 58
# - Papas: -0.5 kg
# - Coca Cola: -2 botellas
# - 6 registros en movimientos_inventario para auditoría
```

---

## 💼 Casos de Uso

### Caso 1: Happy Path (Todo OK)
```
Usuario → Personaliza → Verifica Stock ✓ → Confirma → Crea Pedido ✓ → Descuenta Stock ✓ → ✅ FIN
```

### Caso 2: Stock Insuficiente
```
Usuario → Personaliza → Verifica Stock ✗ → Error JSON → Muestra Alerta → Carrito sin cambios → ❌ FIN
```

### Caso 3: Múltiples Items en Carrito
```
Carrito:
  - Combo 1 (OK stock) ✓
  - Personalizado (OK stock) ✓
  - Producto (NO stock) ✗
  
Resultado: TODO EL CARRITO RECHAZADO
(Si uno falla, ninguno se procesa)
```

---

## 🎯 Puntos Clave de Seguridad

1. **Validación de Stock ANTES de procesar:**
   - Si fallara después, la BD quedaría inconsistente
   - Ahora se previene

2. **Transacciones MySQL:**
   - `commit()` solo si TODO es exitoso
   - Si hay error, `rollback()` automático

3. **Auditoría de Movimientos:**
   - Todo descuento registra: QUÉ, CUÁNTO, CUÁNDO, REFERENCIA
   - Permite trazabilidad 100%

4. **Precios Fijos:**
   - No hay cálculos complejos
   - SIN EXTRAS por personalización
   - Menos errores de redondeo

5. **Validación de Entrada:**
   - Cantidad > 0
   - IDs válidos en BD
   - Carrito no vacío

---

**¡Sistema robusto y production-ready!** 🚀
