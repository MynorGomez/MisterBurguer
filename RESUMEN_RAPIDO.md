# 🚀 RESUMEN RÁPIDO - PARA ENTENDER EN 10 MINUTOS

## ❓ ¿QUÉ ES MISTERBURGER?

Es una **aplicación web** donde los clientes pueden:
- Ver hamburguesas, combos y bebidas 🍔
- **Personalizar hamburguesas** eligiendo ingredientes 👨‍🍳
- Agregar al carrito 🛒
- Confirmar pedido 📦
- El sistema **descuenta automáticamente** del inventario ✅

---

## 🎯 LO MÁS IMPORTANTE (3 OPERACIONES CLAVE)

### 1️⃣ VER MENÚ - `menu_publico()`
**¿Qué hace?**
- Obtiene de la BD: productos, bebidas 🥤, papas 🍟, ingredientes 🥬
- Muestra todo en la página

**Código simplificado:**
```python
@public.route('/')  # El usuario entra en http://localhost
def menu_publico():
    # Obtener de la BD
    bebidas = BD.obtener(categoria=2)  # Coca, Fanta, etc.
    papas = BD.obtener(categoria=3)    # Papas pequeñas, medianas, grandes
    
    # Mostrar en HTML
    return render_template('menu_publico.html', bebidas=bebidas, papas=papas)
```

---

### 2️⃣ PERSONALIZAR - `personalizar_hamburguesa()`
**¿Qué hace?**
- Usuario selecciona: pan, queso, ingredientes, papas, bebida
- Sistema arma la descripción completa
- **Agrega al carrito CON PRECIO FIJO (sin extras)**

**Código simplificado:**
```python
@public.route('/personalizar', methods=['POST'])
def personalizar_hamburguesa():
    # Obtener selecciones del usuario
    pan = request.form.get('pan')           # 'integral'
    queso = request.form.get('queso')       # ID 2
    ingredientes = request.form.getlist('ingredientes')  # [3, 4, 5]
    papas = request.form.get('papas')       # ID 5
    bebida = request.form.get('bebida')     # ID 4
    
    # Obtener precio FIJO (sin extras)
    precio = BD.obtener("SELECT precio FROM productos WHERE nombre LIKE '%Clásica%'")
    # precio = 45.00 (SIN CARGO EXTRA)
    
    # Armar descripción
    descripcion = "Hamburguesa Personalizada: Pan Integral, Carne, Queso, Pepinillos, Papas, Coca"
    
    # Agregar al carrito
    carrito.agregar({
        'tipo': 'personalizado',
        'nombre': descripcion,
        'precio': 45.00,  # ← PRECIO FIJO
        'papas': 5,       # ID de papas
        'bebida': 4       # ID de bebida
    })
    
    return "Pedido agregado al carrito ✅"
```

---

### 3️⃣ CONFIRMAR - `confirmar_pedido()`
**¿Qué hace?**
1. Verifica que hay suficiente stock 📊
2. Si OK → crea el pedido en la BD 💾
3. Descuenta del inventario 📉
4. Muestra confirmación ✅

**Código simplificado:**
```python
@public.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    carrito = session['carrito']  # Obtener carrito
    
    # PASO 1: ¿HAY STOCK?
    ok = inventario.verificar_stock(carrito)
    if not ok:
        return ERROR_JSON("No hay suficiente stock")  # ❌
    
    # PASO 2: CREAR PEDIDO EN BD
    pedido_id = BD.crear_pedido(
        numero="PED-20260401143025",
        cliente="Juan",
        total=90.00
    )
    
    # PASO 3: DESCONTAR STOCK
    for item in carrito:
        if tipo == 'personalizado':
            inventario.descontar_personalizado(
                carne=item['id_base'],
                ingredientes=item['ingredientes'],
                papas=item['papas'],
                bebida=item['bebida'],
                cantidad=item['cantidad']
            )
    
    # PASO 4: RESPONDER
    return SUCCESS_JSON({
        'numero_pedido': 'PED-20260401143025',
        'total': 90.00
    })
```

---

## 🔄 FLUJO EN 5 PASOS

```
┌──────────────────────────────────────────────┐
│ PASO 1: Usuario entra a http://localhost    │
│ → menu_publico() carga todo desde BD        │
│ → Se ven: productos, bebidas, papas        │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ PASO 2: Usuario elige qué hamburguesa       │
│ → Selecciona: pan, queso, ingredientes      │
│ → Selecciona: papas y bebida                │
│ → Hace click en "Agregar"                   │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ PASO 3: Sistema personaliza                 │
│ → personalizar_hamburguesa() procesa datos  │
│ → Obtiene PRECIO FIJO (sin extras)          │
│ → Agrega al carrito en sesión               │
│ → Usuario ve "✅ Agregado al carrito"       │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ PASO 4: Usuario confirma pedido             │
│ → Hace click en "Confirmar"                 │
│ → POST /confirmar_pedido                    │
│ → confirmar_pedido() valida stock           │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ PASO 5: Sistema procesa venta               │
│ ✅ Verifica stock OK                        │
│ ✅ Crea pedido en BD                        │
│ ✅ Descuenta inventario                     │
│ ✅ Muestra número de pedido                 │
│ ✅ Carrito vacío                            │
└──────────────────────────────────────────────┘
```

---

## 📊 VERIFICAR STOCK - LA PARTE MÁS IMPORTANTE

**¿Por qué es importante?**
Si no verificamos, podríamos:
- Vender algo que no hay en stock ❌
- Tener BD inconsistente ❌
- Cliente reclama ❌

**¿Cómo funciona?**

```
Usuario quiere: 2 hamburguesas personalizadas

NECESITA:
├─ Carne Roja: 2 unidades
├─ Queso Cheddar: 2 unidades
├─ Pepinillos: 2 unidades
├─ Tomate: 2 unidades
├─ Papas Fritas: 0.5 kg (según receta)
└─ Coca Cola: 2 botellas (según receta)

STOCK ACTUAL EN BD:
├─ Carne Roja: 50 unidades → ¿50 >= 2? ✅ SÍ
├─ Queso Cheddar: 30 unidades → ¿30 >= 2? ✅ SÍ
├─ Pepinillos: 100 unidades → ¿100 >= 2? ✅ SÍ
├─ Tomate: 80 unidades → ¿80 >= 2? ✅ SÍ
├─ Papas: 2 kg → ¿2 >= 0.5? ✅ SÍ
└─ Coca Cola: 10 botellas → ¿10 >= 2? ✅ SÍ

RESULTADO: ✅ APROBADO - Proceder con la venta
```

---

## 👀 ARCHIVO QUE MANEJA TODO

**`app/utils/inventario.py`** - El Director de Orquesta

```
Funciones principais:

1. verificar_stock_carrito()
   ├─ Revisa TODO el carrito
   ├─ Si es combo → verifica combo
   ├─ Si es personalizado → verifica personalizado
   ├─ Si es producto → verifica producto
   └─ Si ALGUNO falla → RECHAZA TODO

2. verificar_stock_personalizado(id_base, ingredientes_ids, cantidad)
   ├─ Chequea: ¿hay carne?
   ├─ Chequea: ¿hay cada ingrediente?
   └─ Retorna: (True, None) o (False, "error")

3. descontar_inventario_personalizado(id_base, ingredientes_ids, papas_id, bebida_id)
   ├─ Resta carne
   ├─ Resta ingredientes
   ├─ Resta papas (busca receta)
   ├─ Resta bebida (busca receta)
   └─ Registra TODO en movimientos_inventario (auditoría)
```

---

## 🗄️ BASE DE DATOS - LAS 3 TABLAS CLAVE

### 1. **productos** (Qué vendemos)
```
ID | Nombre        | Categoría | Precio
4  | Coca Cola     | 2         | 10.00     ← BEBIDA
5  | Papas Fritas  | 3         | 15.00     ← PAPAS
```

### 2. **insumos** (Ingredientes)
```
ID | Nombre         | Stock
1  | Carne Roja     | 50
2  | Queso Cheddar  | 30
3  | Pepinillos     | 100
4  | Tomate         | 80
```

### 3. **movimientos_inventario** (Auditoría - quién sacó qué)
```
ID | Insumo        | Tipo      | Cantidad | Referencia         | Fecha
1  | Carne Roja    | salida    | 2        | PED-20260401143025 | 2026-04-01 14:30
2  | Queso Cheddar | salida    | 2        | PED-20260401143025 | 2026-04-01 14:30
3  | Pepinillos    | salida    | 2        | PED-20260401143025 | 2026-04-01 14:30
4  | Tomate        | salida    | 2        | PED-20260401143025 | 2026-04-01 14:30
```

---

## ✅ VENTAJAS DEL SISTEMA

| Ventaja | Razón |
|---------|-------|
| 🔒 **Seguro** | Verifica stock ANTES de procesar |
| 💰 **Sin errores de precio** | Precio fijo, sin cálculos complejos |
| 📊 **Auditable** | Todo movimiento se registra |
| 🚀 **Automático** | Sin intervención manual |
| 🔄 **Flexible** | Soporta combos, personalizados, productos |
| 👥 **Rápido** | Usuario obtiene confirmación al instante |

---

## ❌ ¿QUÉ OCURRE SI FALLA?

### Escenario 1: No hay stock
```
Usuario: "Quiero 10 hamburguesas personalizadas"
Sistema: Verifica → ❌ "Solo hay carne para 3"
Resultado: ERROR JSON → Usuario ve alerta → Carrito sin cambios
```

### Escenario 2: BD sin conexión
```
Sistema: Intenta conectar → ❌ Error conexión
Resultado: EXCEPCIÓN ATRAPADA → Usuario ve "Error del servidor"
```

### Escenario 3: Carrito vacío
```
Usuario: Intenta confirmar carrito vacío
Sistema: Chequea → ❌ Carrito está vacío
Resultado: ERROR JSON → Usuario regresa a menú
```

---

## 🎓 PALABRA CLAVE QUE DEFINE TODO

**TRANSACCIÓN** 🔄

```
O TODO sucede juntos:
  ✅ Crear pedido
  ✅ Crear venta
  ✅ Descontar stock
  ✅ Registrar movimiento

O NADA sucede:
  ❌ Ningún cambio en BD
  ❌ Carrito sin modificar
  ❌ Usuario ve error
  
NO HAY PUNTO MEDIO
```

---

## 📚 ARCHIVOS IMPORTANTES

| Archivo | Qué hace |
|---------|----------|
| `app/routes/public.py` | Maneja las rutas y lógica principal |
| `app/utils/inventario.py` | Verifica y descuenta stock |
| `app/templates/menu_publico.html` | Interfaz que ve el usuario |
| `DOCUMENTACION_SISTEMA.md` | Documentación detallada |
| `GUIA_TECNICA.md` | Pseudocódigo y arquitectura |

---

## 🎯 LO QUE TIENES QUE SABER

1. **3 operaciones principales:**
   - Ver menú (`menu_publico()`)
   - Personalizar (`personalizar_hamburguesa()`)
   - Confirmar (`confirmar_pedido()`)

2. **2 cosas que pasan siempre:**
   - Verificar stock
   - Descontar inventario

3. **1 principio fundamental:**
   - Seguridad: verificar ANTES, descontar DESPUÉS
   - Sin excepciones

---

**¡Eso es todo! 🎉**

Si tienes más dudas, consulta:
- `DOCUMENTACION_SISTEMA.md` → Explicación completa con ejemplos
- `GUIA_TECNICA.md` → Pseudocódigo y arquitectura técnica
