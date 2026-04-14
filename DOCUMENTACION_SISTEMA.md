# 📋 DOCUMENTACIÓN COMPLETA - SISTEMA DE PERSONALIZACIÓN DE HAMBURGUESAS

## 📌 Índice
1. [Visión General](#visión-general)
2. [Flujo de la Aplicación](#flujo-de-la-aplicación)
3. [Módulos Principales](#módulos-principales)
4. [Base de Datos](#base-de-datos)
5. [Funciones Clave](#funciones-clave)
6. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 🎯 Visión General

**MisterBurger** es un sistema web que permite a los clientes:
- Ver un menú de hamburguesas, combos y productos
- **Personalizar hamburguesas** eligiendo:
  - Tipo de pan (normal, integral, sésamo)
  - Tipo de queso (opcional)
  - Ingredientes adicionales (vegetales, salsas)
  - Tamaño de papas (pequeñas, medianas, grandes)
  - Tipo de bebida
- Agregar productos al carrito
- Confirmar pedidos y generar venta automática

**Características especiales:**
✅ Sin costo extra por personalización  
✅ Precio fijo basado en "Hamburguesa Clásica"  
✅ Gestión automática de inventario  
✅ Validación de stock antes de confirmar  

---

## 🔄 Flujo de la Aplicación

```
┌─────────────────────────────────────┐
│  1. Usuario accede a /menu_publico  │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Se cargan datos de BD:│
    │ - Productos          │
    │ - Bebidas (cat 2)    │
    │ - Papas (cat 3)      │
    │ - Insumos (carnes)   │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ Usuario elige opción:    │
    │ A) Combo predefinido     │
    │ B) Personalizar          │
    │ C) Producto individual   │
    └──────┬────────┬────┬─────┘
           │        │    │
     ┌─────▼──┐ ┌──▼──┐ ▼─────────┐
     │ Combo  │ │Pers.│ Producto  │
     │ Fijo   │ │     │ Individual│
     └─────┬──┘ └──┬──┘ └──────┬──┘
           │       │           │
           └───────┴─────┬─────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  Agregar al carrito    │
            │  (sesión Flask)        │
            └────┬───────────────────┘
                 │
                 ▼
        ┌───────────────────────┐
        │ Usuario ve carrito    │
        │ y confirma pedido     │
        └────┬──────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ VERIFICAR STOCK    │
    │ ¿Hay suficiente?   │
    └────┬─────┬────────┘
         │YES  │NO
         ▼     ▼
      [OK]  [Rechazo]
         │
         ▼
    ┌────────────────────┐
    │ CREAR PEDIDO en BD │
    │ CREAR VENTA        │
    │ DESCONTAR STOCK    │
    └────┬───────────────┘
         │
         ▼
    ✅ PEDIDO CONFIRMADO
```

---

## 🏗️ Módulos Principales

### 1️⃣ **app/routes/public.py** - RUTEO Y LÓGICA PRINCIPAL

#### Función: `menu_publico()` - CARGA EL MENÚ
```python
@public.route('/')
def menu_publico():
```
**¿Qué hace?**
- Usuario accede a la página principal
- Obtiene de la BD: productos, combos, insumos, bebidas, papas
- Calcula cantidad de items en carrito
- Renderiza template con todos los datos

**Datos que carga:**

| Variable | Origen | Descripción |
|----------|--------|------------|
| `productos` | Tabla productos | Todos los productos activos |
| `bebidas` | productos WHERE id_categoria=2 | Bebidas disponibles |
| `papas` | productos WHERE id_categoria=3 | Acompañamientos (papas) |
| `insumos` | Tabla insumos | Ingredientes (pan, queso, vegetales, etc.) |
| `carnes` | Filtro de insumos | Tipos de carne (carne roja, pollo, etc.) |

---

#### Función: `personalizar_hamburguesa()` - CREAR PERSONALIZACIÓN
```python
@public.route('/personalizar', methods=['POST'])
def personalizar_hamburguesa():
```

**¿Qué hace?**
1. **Obtiene selecciones del usuario:**
   - `pan` → tipo de pan (normal, integral, sésamo)
   - `queso` → ID del queso seleccionado
   - `ingredientes_ids` → lista de IDs de ingredientes adicionales
   - `papas` → ID del producto papas (o "no")
   - `bebida` → ID de bebida (o "no")
   - `cantidad` → cantidad de hamburguesas

2. **Valida datos:**
   - Cantidad > 0
   - Carne disponible
   - Cantidad válida

3. **Obtiene precio fijo:**
   - Busca "Hamburguesa Clásica" en BD
   - Usa ese precio (SIN EXTRA por personalización)

4. **Arma descripción:**
   ```
   Hamburguesa Personalizada: Pan Integral, Carne Roja, Queso Cheddar, Pepinillos, Mayonesa, Papas Fritas, Coca Cola
   ```

5. **Agrega al carrito con estructura:**
   ```python
   {
       'tipo': 'personalizado',
       'id_base': 1,              # ID de la carne
       'pan': 'integral',         # Tipo de pan
       'queso': 2,                # ID del queso
       'ingredientes': [3, 4, 5], # IDs de ingredientes
       'papas': 5,                # ID del producto papas
       'bebida': 4,               # ID del producto bebida
       'nombre': 'Hamburguesa Personalizada: ...',
       'precio': 45.00,           # Precio de Hamburguesa Clásica
       'cantidad': 2,
       'subtotal': 90.00
   }
   ```

**Ejemplo real:**
```
Usuario selecciona:
- Pan: Integral
- Queso: Cheddar (ID: 2)
- Ingredientes: Pepinillos, Tomate, Mayonesa (IDs: 3, 4, 5)
- Papas: Papas Pequeñas (ID: 5)
- Bebida: Coca Cola (ID: 4)
- Cantidad: 1

Resultado:
✅ Se agrega al carrito
✅ Precio: Q45.00 (Precio de Hamburguesa Clásica, SIN EXTRA)
✅ Nombre: Hamburguesa Personalizada: Pan Integral, Carne Roja, Cheddar, Pepinillos, Tomate, Mayonesa, Papas Fritas, Coca Cola
```

---

#### Función: `confirmar_pedido()` - PROCESAR VENTA
```python
@public.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
```

**¿Qué hace?**
1. **Verifica stock del carrito completo**
   - Llama a `verificar_stock_carrito()`
   - Si falla: devuelve error en JSON

2. **Si hay stock OK:**
   - Crea registro en tabla `pedidos`
   - Crea detalles en `pedido_detalle`
   - Crea venta automática en `ventas`
   - Crea detalles de venta en `venta_detalle`
   - **Descuenta inventario**
   - Limpia carrito de sesión

3. **Devuelve respuesta JSON:**
   ```json
   {
       "numero_pedido": "PED-20260401143025",
       "total": 90.00,
       "estado": "confirmado",
       "items": [...]
   }
   ```

---

### 2️⃣ **app/utils/inventario.py** - GESTIÓN DE STOCK

#### Función: `verificar_stock_personalizado()` - VALIDAR DISPONIBILIDAD

```python
def verificar_stock_personalizado(conexion, id_base, ingredientes_ids, cantidad_solicitada):
```

**¿Qué hace?**
- Valida que hay suficiente stock de:
  - Carne base (id_base)
  - Todos los ingredientes adicionales (ingredientes_ids)
- Retorna `(True, None)` si hay stock
- Retorna `(False, "mensaje de error")` si NO hay stock

**Ejemplo:**
```
Usuario quiere: 1 Hamburguesa Personalizada

Verifica:
✓ Carne roja: necesita 1, tiene 15 → OK
✓ Queso: necesita 1, tiene 8 → OK
✓ Pepinillos: necesita 1, tiene 12 → OK
✓ Tomate: necesita 1, tiene 20 → OK

Resultado: ✅ APROBADO - Puede hacer el pedido
```

---

#### Función: `descontar_inventario_personalizado()` - REDUCIR STOCK

```python
def descontar_inventario_personalizado(conexion, id_base, ingredientes_ids, cantidad_vendida, referencia, papas_id=None, bebida_id=None):
```

**¿Qué hace?**
1. **Descuenta carne base:**
   ```sql
   UPDATE insumos SET stock_actual = stock_actual - 1 WHERE id_insumo = id_base
   ```

2. **Descuenta cada ingrediente:**
   ```sql
   UPDATE insumos SET stock_actual = stock_actual - 1 WHERE id_insumo = ingredient_id
   ```

3. **Descuenta papas (si se seleccionaron):**
   - Llama `descontar_inventario_por_producto(papas_id)`
   - Busca receta de papas en tabla `recetas`
   - Usa la receta para calcular cuánto descontar

4. **Descuenta bebida (si se seleccionó):**
   - Llama `descontar_inventario_por_producto(bebida_id)`
   - Busca receta de bebida
   - Usa la receta para descontar

5. **Registra movimiento en `movimientos_inventario`:**
   ```sql
   INSERT INTO movimientos_inventario 
   (id_insumo, tipo_movimiento, cantidad, referencia, observacion, fecha_movimiento)
   VALUES (1, 'salida_venta', 1, 'PED-20260401143025', 'Descuento carne personalizado', NOW())
   ```

**Ejemplo completo:**
```
Pedido: 1 Hamburguesa Personalizada + Papas Pequeñas + Coca Cola

DESCUENTOS REALIZADOS:
1. Carne Roja (id_insumo=1):     -1 unidad
2. Queso Cheddar (id_insumo=2):  -1 unidad
3. Pepinillos (id_insumo=3):     -1 unidad
4. Tomate (id_insumo=4):         -1 unidad
5. Papas Fritas (id_producto=5): -usa receta (ej: -0.25 kg)
6. Coca Cola (id_producto=4):    -usa receta (ej: -1 botella)

Resultado:
✅ Stock actualizado en tabla insumos
✅ Movimientos registrados para auditoría
```

---

#### Función: `verificar_stock_carrito()` - VALIDAR CARRITO COMPLETO

```python
def verificar_stock_carrito(conexion, carrito):
```

**¿Qué hace?**
- Itera cada item del carrito
- Según el tipo (combo, personalizado, producto):
  - Llama función de verificación correspondiente
- Si alguno falla: retorna error inmediatamente
- Si todo OK: retorna éxito

**Tipos de items:**
```python
if item.get('tipo') == 'combo':
    # Verificar combo (usa verificar_stock_combo)
elif item.get('tipo') == 'personalizado':
    # Verificar personalizado (usa verificar_stock_personalizado)
else:
    # Verificar producto normal (usa verificar_stock_suficiente)
```

---

### 3️⃣ **app/templates/menu_publico.html** - INTERFAZ DE USUARIO

**Estructura de la página:**

```
┌─────────────────────────────────────────────┐
│  HEADER: MisterBurger (Logo, Carrito Count) │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ SECCIÓN 1: COMBOS PREDEFINIDOS               │
│ - Combo 1 (Imagen, Nombre, Precio)          │
│ - Combo 2                                   │
│ - Combo 3                                   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ SECCIÓN 2: PERSONALIZAR HAMBURGUESA (7 PASOS)│
│                                             │
│ Progress Bar: ■□□□□□□ (Paso 1/7)           │
│                                             │
│ Paso 1: ¿Qué Pan?                          │
│  ○ Pan Normal (Incluido)                   │
│  ○ Pan Integral (Incluido)                 │
│  ○ Pan con Sésamo (Incluido)               │
│                                             │
│ [Anterior] [Siguiente]                      │
└─────────────────────────────────────────────┘

│ Paso 2: ¿Qué Queso?                        │
│  ○ Sin Queso (Incluido)                    │
│  ○ Queso Cheddar (Incluido)                │
│  ○ Queso Mozzarella (Incluido)             │
│                                             │
│ Paso 3: ¿Ingredientes?                     │
│  ☐ Pepinillos (Incluido)                   │
│  ☐ Tomate (Incluido)                       │
│  ☐ Cebolla (Incluido)                      │
│  ☐ Lechuga (Incluido)                      │
│                                             │
│ Paso 4: ¿Salsas?                           │
│  ☐ Mayonesa (Incluido)                     │
│  ☐ Mostaza (Incluido)                      │
│  ☐ Salsa Picante (Incluido)                │
│                                             │
│ Paso 5: ¿Papas?                            │
│  ○ Sin Papas (Incluido) [SELECCIONADO]    │
│  ○ Papas Fritas (Incluido)                 │
│                                             │
│ Paso 6: ¿Bebida?                           │
│  ○ Sin Bebida (Incluido) [SELECCIONADO]   │
│  ○ Coca Cola (Incluido)                    │
│                                             │
│ Paso 7: RESUMEN                             │
│  🍞 Pan Normal                              │
│  🥩 Carne Roja                              │
│  🧀 Queso Cheddar                           │
│  🥬 Pepinillos, Tomate                      │
│  🍟 Papas Fritas                            │
│  🥤 Coca Cola                               │
│                                             │
│  Total: Q45.00                              │
│  Cantidad: [1]                              │
│  [Realizar Pedido]                          │
├─────────────────────────────────────────────┤
│ SECCIÓN 3: PRODUCTOS INDIVIDUALES           │
│ - Papas (Imagen, Nombre, Precio, Cantidad) │
│ - Bebidas                                   │
│ - Combos alternativos                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ MODAL: CARRITO DE COMPRAS                    │
│ Items agregados, Total, Confirmar, Datos    │
└─────────────────────────────────────────────┘
```

**JavaScript:**
- `pasoSiguiente()` - Avanza en pasos de personalización
- `pasoAnterior()` - Retrocede en pasos
- `validarPaso(numero)` - Valida que cumpla requisitos del paso
- `actualizarResumen()` - Actualiza descripción y precio
- Manejo de modales
- AJAX para agregar al carrito sin recargar

---

## 💾 Base de Datos

### Tablas relevantes:

#### 1. **productos**
```sql
id_producto | nombre          | id_categoria | precio | estado  | disponible
1           | Hamburguesa... | 1           | 45.00  | activo  | si
4           | Coca Cola      | 2           | 10.00  | activo  | si
5           | Papas Fritas   | 3           | 15.00  | activo  | si
```

#### 2. **insumos** (Ingredientes)
```sql
id_insumo | nombre           | costo_referencia | stock_actual | estado
1         | Carne Roja       | 20.00           | 50           | activo
2         | Queso Cheddar    | 5.00            | 30           | activo
3         | Pepinillos       | 1.00            | 100          | activo
4         | Tomate           | 2.00            | 80           | activo
```

#### 3. **categorias**
```sql
id_categoria | nombre              | descripcion
1            | Hamburguesas        | Hamburguesas de la casa
2            | Bebidas             | Refrescos y bebidas
3            | Acompañamientos     | Papas y extras
```

#### 4. **recetas** (Composición de productos)
```sql
id_producto | id_insumo | cantidad
5 (Papas)   | 30 (Papa) | 0.25 (kg)
4 (Coca)    | 31 (Botella) | 1
```

#### 5. **pedidos**
```sql
id_pedido | numero_pedido      | nombre_cliente | telefono | estado | total
1         | PED-20260401143025 | Juan           | 12345678 | confirmado | 90.00
```

#### 6. **pedido_detalle**
```sql
id_pedido | id_producto | cantidad | precio_unitario | subtotal
1         | 1 (carne)   | 1        | 45.00          | 45.00
1         | 5 (papas)   | 1        | 15.00          | 15.00
```

#### 7. **movimientos_inventario** (Auditoría)
```sql
id_insumo | tipo_movimiento | cantidad | referencia         | observacion | fecha
1         | salida_venta    | 1        | PED-20260401143025 | Descuento...| NOW()
```

---

## 🔧 Funciones Clave

### Resumen de Funciones:

| Función | Ubic | Parámetros | Retorna | Propósito |
|---------|------|-----------|---------|-----------|
| `menu_publico()` | public.py | - | HTML | Carga página principal |
| `personalizar_hamburguesa()` | public.py | form data | redirect | Agrega personalización al carrito |
| `confirmar_pedido()` | public.py | form data | JSON | Procesa venta y descuenta stock |
| `verificar_stock_carrito()` | inventario.py | conexion, carrito | (bool, msg) | Valida disponibilidad |
| `verificar_stock_personalizado()` | inventario.py | conexion, ids, qty | (bool, msg) | Valida ingredientes |
| `descontar_inventario_personalizado()` | inventario.py | conexion, ids... | - | Reduce stock |

---

## 💡 Ejemplos Prácticos

### EJEMPLO 1: Compra simple
```
ESCENARIO: Usuario compra 2 Hamburguesas Personalizadas con Papas y Bebida

┌─ PASO 1: Usuario en men_publico ────────────────────┐
│ Se cargan:                                           │
│ - Bebidas: [Coca Cola (ID:4)]                        │
│ - Papas: [Papas Fritas (ID:5)]                       │
│ - Insumos: [Carne, Queso, Pepinillos, Tomate, etc] │
└────────────────────────────────────────────────────┘

┌─ PASO 2: Usuario personaliza ──────────────────────┐
│ Selecciona:                                        │
│ - Pan: Integral                                    │
│ - Queso: Cheddar (ID:2)                            │
│ - Ingredientes: Pepinillos (3), Tomate (4)        │
│ - Papas: Papas Fritas (ID:5)                      │
│ - Bebida: Coca Cola (ID:4)                        │
│ - Cantidad: 2                                     │
│                                                   │
│ POST /personalizar recibe:                       │
│ {                                                │
│   pan: 'integral',                               │
│   queso: '2',                                    │
│   ingredientes: ['3', '4'],                      │
│   papas: '5',                                    │
│   bebida: '4',                                   │
│   cantidad: '2'                                  │
│ }                                                │
└────────────────────────────────────────────────────┘

┌─ PASO 3: Servidor procesa personalizar_hamburguesa() ──┐
│                                                        │
│ 1. Obtiene carne: Carne Roja (ID:1)                   │
│ 2. Obtiene precio: Q45.00 (Hamburguesa Clásica)      │
│ 3. Arma detalles: Pan Integral, Carne Roja, Queso... │
│ 4. Agrega al carrito:                                │
│                                                      │
│ {                                                   │
│   tipo: 'personalizado',                            │
│   id_base: 1,                                       │
│   pan: 'integral',                                  │
│   queso: 2,                                         │
│   ingredientes: [3, 4],                             │
│   papas: 5,                                         │
│   bebida: 4,                                        │
│   nombre: 'Hamburguesa Personalizada: Pan...',     │
│   precio: 45.00,                                    │
│   cantidad: 2,                                      │
│   subtotal: 90.00                                   │
│ }                                                   │
│                                                    │
│ ✅ Carrito: [ {...} ]                              │
└────────────────────────────────────────────────────┘

┌─ PASO 4: Usuario confirma pedido ──────────────────┐
│ POST /confirmar_pedido                             │
│ {                                                 │
│   nombre_cliente: 'Juan',                         │
│   telefono_cliente: '12345678'                    │
│ }                                                 │
└────────────────────────────────────────────────────┘

┌─ PASO 5: Servidor - verificar_stock_carrito() ────┐
│                                                   │
│ Para cada item en carrito:                        │
│   item.tipo == 'personalizado'?                  │
│   → Llama verificar_stock_personalizado()        │
│                                                   │
│   Verifica:                                       │
│   ✓ Carne Roja (ID:1): ¿stock >= 2? SÍ (50>2)  │
│   ✓ Queso (ID:2): ¿stock >= 2? SÍ (30>2)       │
│   ✓ Pepinillos (ID:3): ¿stock >= 2? SÍ (100>2) │
│   ✓ Tomate (ID:4): ¿stock >= 2? SÍ (80>2)      │
│                                                   │
│ ✅ RESULTADO: (True, None)                        │
│ → Puede proceder con la venta                    │
└────────────────────────────────────────────────────┘

┌─ PASO 6: Servidor - crear_pedido() ────────────┐
│                                                │
│ INSERT INTO pedidos (                          │
│   numero_pedido: 'PED-20260401143025',        │
│   nombre_cliente: 'Juan',                      │
│   telefono: '12345678',                        │
│   tipo: 'web',                                 │
│   estado: 'confirmado',                        │
│   total: 90.00                                 │
│ )                                              │
│ → id_pedido = 1                                │
│                                                │
│ INSERT INTO pedido_detalle (                   │
│   id_pedido: 1,                                │
│   id_producto: 1 (carne),                      │
│   cantidad: 2,                                 │
│   precio_unitario: 45.00,                      │
│   subtotal: 90.00                              │
│ )                                              │
│                                                │
│ INSERT INTO ventas (...)                       │
│ → id_venta = 1                                 │
│                                                │
│ INSERT INTO venta_detalle (...)                │
└────────────────────────────────────────────────┘

┌─ PASO 7: Servidor - descontar_inventario_personalizado() ┐
│                                                          │
│ Descuentos ejecutados:                                  │
│ UPDATE insumos SET stock = 50 - 2 WHERE id=1 (Carne)   │
│ UPDATE insumos SET stock = 30 - 2 WHERE id=2 (Queso)   │
│ UPDATE insumos SET stock = 100 - 2 WHERE id=3 (Pepini) │
│ UPDATE insumos SET stock = 80 - 2 WHERE id=4 (Tomate)  │
│                                                         │
│ + INSERT INTO movimientos_inventario (x4) para auditar │
│                                                         │
│ ✅ STOCK ACTUALIZADO                                   │
│                                                         │
│ session['carrito'] = [] (vacía carrito)               │
└────────────────────────────────────────────────────────┘

┌─ PASO 8: Servidor responde ──────────────────────┐
│                                                  │
│ response.json({                                  │
│   'numero_pedido': 'PED-20260401143025',        │
│   'total': 90.00,                                │
│   'estado': 'confirmado',                        │
│   'items': [                                     │
│     {                                            │
│       'cantidad': 2,                             │
│       'nombre': 'Hamburguesa Personalizada: ...'│
│       'subtotal': 90.00                         │
│     }                                            │
│   ]                                              │
│ })                                               │
│                                                  │
│ ✅ MODAL muestra: "Pedido Confirmado!"          │
│    Número: PED-20260401143025                   │
│    Total: Q90.00                                │
└────────────────────────────────────────────────┘

RESULTADO FINAL EN BD:
├─ pedidos[1]: PED-20260401143025, Juan, Q90.00, confirmado
├─ pedido_detalle[1]: ID 1 (carne), Qty 2, Q45 × 2
├─ ventas[1]: ID 1, Q90.00, automática
├─ venta_detalle[1]: ID 1, Qty 2
└─ insumos: Stock actualizado (Carne: 50→48, Queso: 30→28, etc.)
```

### EJEMPLO 2: Error de Stock
```
ESCENARIO: Usuario intenta comprar pero NO hay stock

┌─ Carrito:                          ┐
│ 5 Combos (Necesita 5 de algo)     │
├────────────────────────────────────┤
│ Combo tiene: Papas                │
│ Papas necesita: 0.25 kg por unidad│
│ Stock disponible: 1 kg (= 4 unid) │
│ ¡NO ALCANZA PARA 5 COMBOS!        │
└────────────────────────────────────┘

Resultado de verificar_stock():
❌ (False, "Producto 'Papas Fritas': No hay suficiente stock...")

Usuario ve: "Error: No hay suficiente stock de Papas Fritas"
Pedido: NO SE CREA
Stock: NO SE MODIFICA
Carrito: PERMANECE IGUAL
```

---

## 🎓 Conclusión

Este sistema es **robusto y seguro** porque:

1. ✅ **Verifica antes de procesar** - Chequea stock antes de crear venta
2. ✅ **Usa transacciones** - Todo se confirma juntos o ninguno
3. ✅ **Registra todo** - Movimientos de inventario para auditoría
4. ✅ **Sin costos extra** - Personalización SIN cargos adicionales
5. ✅ **Dinámico** - Papas y bebidas vienen de la BD
6. ✅ **Automático** - Crea venta sin intervención manual
7. ✅ **Flexible** - Soporta combos, productos, y personalizaciones

---

## 📞 Flujo de Contacto

```
Usuario Navegador
    ↓ (visita http://localhost)
    ↓
Flask Route (/menu_publico)
    ↓
Backend Python (public.py)
    ↓
Base de Datos MySQL
    ↓
Jinja2 Template (menu_publico.html)
    ↓
Navegador (HTML+CSS+JS)
    ↓
Usuario interactúa (click, personaliza)
    ↓
JavaScript (AJAX)
    ↓
Flask Route (/personalizar, /confirmar_pedido)
    ↓
Backend Python (inventario.py validaciones)
    ↓
Base de Datos (INSERT, UPDATE)
    ↓
Respuesta JSON
    ↓
JavaScript actualiza DOM
    ↓
Usuario ve confirmación ✅
```

---

**¡Sistema completamente funcional y listo para producción!** 🚀
