# 🚀 ACTUALIZACIONES RECIENTES - ABRIL 2026

**Versión: 1.1 - Fecha: 2026-04-02**

## 📚 CARACTERÍSTICAS NUEVAS AGREGADAS

1. [Auto-Actualización Panel Cocina](#auto-actualización-panel-cocina)
2. [Sistema de Invoices/Facturas](#sistema-de-invoicesfacturas)
3. [Notificaciones por Email](#notificaciones-por-email)
4. [Cambio de Teléfono a Correo](#cambio-de-teléfono-a-correo)
5. [Loading Overlay de Espera](#loading-overlay-de-espera)
6. [Configuración Centralizada](#configuración-centralizada-env)

---

## 🔄 AUTO-ACTUALIZACIÓN PANEL COCINA

### ¿Qué es?
El panel de cocina ahora se **actualiza automáticamente cada 5 segundos** sin que el usuario tenga que recargar la página.

### Archivos Modificados
- `app/routes/public.py` - Rutas API
- `app/templates/cocina_pedidos.html` - Template con AJAX
- `app/templates/cocina_detalle.html` - Vista de detalles

### Nuevas Rutas API

#### **GET `/api/pedidos_cocina`**
```python
@public.route('/api/pedidos_cocina')
def api_pedidos_cocina():
    """
    Retorna todos los pedidos confirmados/en-preparación/listos
    Formato JSON para AJAX
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT numero_pedido, nombre_cliente_invitado, estado, 
               fecha_orden, total
        FROM pedidos 
        WHERE estado IN ('confirmado', 'en_preparacion', 'listo')
        ORDER BY fecha_orden DESC
    """)
    pedidos = cur.fetchall()
    
    return jsonify([{
        'id': p[0],
        'numero': p[1],
        'cliente': p[2],
        'fecha': p[3],
        'total': p[4]
    } for p in pedidos])
```

**¿Cuándo se usa?**
- Cada 5 segundos en `cocina_pedidos.html`

**Respuesta JSON:**
```json
[
  {
    "id": 1,
    "numero": "PED-001",
    "cliente": "Juan",
    "fecha": "2026-04-02 10:30",
    "total": 85.50,
    "estado": "confirmado"
  }
]
```

---

#### **GET `/api/pedido/<numero_pedido>`**
```python
@public.route('/api/pedido/<numero_pedido>')
def api_pedido_detalle(numero_pedido):
    """Retorna detalles de un pedido específico"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.numero_pedido, p.nombre_cliente_invitado, 
               p.estado, p.total, GROUP_CONCAT(i.nombre)
        FROM pedidos p
        LEFT JOIN pedido_items i ON p.id_pedido = i.id_pedido
        WHERE p.numero_pedido = %s
        GROUP BY p.id_pedido
    """, (numero_pedido,))
    
    pedido = cur.fetchone()
    return jsonify({
        'numero_pedido': pedido[0],
        'cliente': pedido[1],
        'estado': pedido[2],
        'total': pedido[3],
        'items': pedido[4].split(',')
    })
```

---

### JavaScript - Polling cada 5 segundos

**Archivo:** `app/templates/cocina_pedidos.html`

```javascript
// Obtener pedidos cada 5 segundos
setInterval(() => {
    fetch('/api/pedidos_cocina')
        .then(r => r.json())
        .then(data => {
            console.log('✓ Pedidos actualizados:', data.length);
            
            // Limpiar contenedor
            const container = document.getElementById('pedidosContainer');
            container.innerHTML = '';
            
            // Renderizar cada pedido
            data.forEach(pedido => {
                const card = document.createElement('div');
                card.className = 'pedido-card';
                card.innerHTML = `
                    <h3>${pedido.numero}</h3>
                    <p>Cliente: ${pedido.cliente}</p>
                    <p>Estado: ${pedido.estado}</p>
                    <p>Total: Q ${pedido.total}</p>
                `;
                container.appendChild(card);
            });
        })
        .catch(err => console.error('Error:', err));
}, 5000); // 5000ms = 5 segundos
```

**¿Cómo funciona?**
1. Cada 5 segundos llama a `/api/pedidos_cocina`
2. Recibe JSON con pedidos actuales
3. Limpia el HTML anterior
4. Renderiza nuevos pedidos dinámicamente
5. **SIN RECARGA DE PÁGINA** ⚡

---

## 📄 SISTEMA DE INVOICES/FACTURAS

### ¿Qué es?
Cada pedido tiene un **número único** y se puede Ver su **recibo/factura** en PDF-ready HTML.

### Archivos Modificados
- `app/routes/public.py` - Ruta de factura
- `app/templates/factura.html` - Template de factura
- `app/templates/estado_pedido.html` - Link a factura

### Ruta: GET `/factura/<numero_pedido>`

```python
@public.route('/factura/<numero_pedido>')
def factura_pedido(numero_pedido):
    """
    Muestra/imprime factura de un pedido.
    Formato imprimible con CSS para print.
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.numero_pedido, p.nombre_cliente_invitado,
               p.correo_cliente_invitado, p.fecha_orden,
               p.total, p.estado
        FROM pedidos p
        WHERE p.numero_pedido = %s
    """, (numero_pedido,))
    
    pedido = cur.fetchone()
    
    # Obtener items del pedido
    cur.execute("""
        SELECT nombre, cantidad, precio, subtotal
        FROM pedido_items
        WHERE id_pedido = (
            SELECT id_pedido FROM pedidos 
            WHERE numero_pedido = %s
        )
    """, (numero_pedido,))
    items = cur.fetchall()
    
    return render_template('factura.html', 
                          pedido=pedido, 
                          items=items)
```

### HTML Factura: `app/templates/factura.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Factura - {{ pedido[0] }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            border: 2px solid #333;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        .header h1 {
            color: #d32f2f;
            margin: 0;
        }
        .number {
            font-size: 24px;
            font-weight: bold;
            color: #1f8ef1;
        }
        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .details p {
            margin: 5px 0;
        }
        .items-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .items-table th {
            background: #f0f0f0;
            padding: 10px;
            text-align: left;
            border-bottom: 2px solid #333;
        }
        .items-table td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .total-row {
            background: #f9f9f9;
            font-weight: bold;
            font-size: 18px;
        }
        @media print {
            body { border: none; }
            .print-btn { display: none; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>MisterBurger 🍔</h1>
        <p class="number">Recibo #{{ pedido[0] }}</p>
        <p>Fecha: {{ pedido[3] }}</p>
    </div>
    
    <div class="details">
        <div>
            <p><strong>Cliente:</strong> {{ pedido[1] }}</p>
            <p><strong>Email:</strong> {{ pedido[2] }}</p>
        </div>
        <div>
            <p><strong>Estado:</strong> {{ pedido[5] }}</p>
            <p><strong>Fecha Orden:</strong> {{ pedido[3] }}</p>
        </div>
    </div>
    
    <table class="items-table">
        <thead>
            <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio</th>
                <th>Subtotal</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>Q {{ "%.2f"|format(item[2]) }}</td>
                <td>Q {{ "%.2f"|format(item[3]) }}</td>
            </tr>
            {% endfor %}
            <tr class="total-row">
                <td colspan="3" style="text-align: right;">TOTAL:</td>
                <td>Q {{ "%.2f"|format(pedido[4]) }}</td>
            </tr>
        </tbody>
    </table>
    
    <button class="print-btn" onclick="window.print()">
        Imprimir Factura 🖨️
    </button>
</body>
</html>
```

**¿Cómo se usa?**
1. Usuario hace pedido
2. Recibe email con enlace a `/factura/PED-123`
3. Abre factura en navegador
4. Presiona "Imprimir" para PDF
5. Tiene formato profesional ✅

---

## 📧 NOTIFICACIONES POR EMAIL

### ¿Qué es?
**Automáticamente se envía email** con detalles del pedido al cliente después de confirmar.

### Archivos
- `app/utils/correo.py` - Módulo de email
- `app/config.py` - Configuración Email (desde `.env`)
- `.env` - Credenciales Gmail

### Configuración (`.env`)

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_especial
MAIL_FROM=MisterBurger <tu_email@gmail.com>

# Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=restaurante
```

**⚠️ IMPORTANTE - Gmail:**
1. Activa "Verificación en 2 pasos"
2. Crea "Contraseña de aplicación" (16 caracteres)
3. Úsala en `MAIL_PASSWORD` (NO tu contraseña normal)

### Código: `app/utils/correo.py`

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config

def enviar_confirmacion_pedido(pedido_numero, cliente_nombre, 
                               cliente_correo, items, total):
    """
    Envía email de confirmación al cliente
    """
    try:
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'✅ Pedido Confirmado #{pedido_numero}'
        msg['From'] = Config.MAIL_USERNAME
        msg['To'] = cliente_correo
        
        # HTML del email
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #d32f2f;">¡Tu pedido está confirmado!</h2>
                
                <p>Hola <strong>{cliente_nombre}</strong>,</p>
                
                <p>Tu pedido número <strong>#{pedido_numero}</strong> 
                ha sido confirmado.</p>
                
                <h3>Detalles:</h3>
                <ul>
                {' '.join([f'<li>{item["nombre"]} x{item["cantidad"]}</li>' 
                          for item in items])}
                </ul>
                
                <p><strong>Total: Q {total:.2f}</strong></p>
                
                <p>Tu pedido será preparado pronto.</p>
                
                <p>Gracias por tu compra,<br>
                <strong>MisterBurger 🍔</strong></p>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Conectar y enviar
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)
        
        print(f'✅ Email enviado a {cliente_correo}')
        return True
        
    except Exception as e:
        print(f'❌ Error enviando email: {e}')
        return False
```

### Cuándo se envía

En la ruta `POST /confirmar_pedido`:

```python
@public.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    # ... código de crear pedido ...
    
    # ENVIAR EMAIL
    from app.utils.correo import enviar_confirmacion_pedido
    
    enviar_confirmacion_pedido(
        pedido_numero=numero_pedido,
        cliente_nombre=nombre_cliente,
        cliente_correo=correo_cliente,
        items=items_pedido,
        total=total_pedido
    )
    
    return jsonify({'numero_pedido': numero_pedido, ...})
```

---

## 📝 CAMBIO DE TELÉFONO A CORREO

### ¿Qué cambió?
- ❌ Campo `telefono_cliente_invitado` **REMOVIDO**
- ✅ Campo `correo_cliente_invitado` **AGREGADO**
- Todos los formularios usan ahora **EMAIL** en lugar de teléfono

### Base de Datos

```sql
-- ANTES:
ALTER TABLE pedidos ADD COLUMN telefono_cliente_invitado VARCHAR(20);

-- AHORA:
ALTER TABLE pedidos ADD COLUMN correo_cliente_invitado VARCHAR(120);
```

### Templates Modificados

**carrito.html:**
```html
<label>Correo electrónico <span class="requerido">*</span></label>
<input type="email" 
       id="inputCorreoCliente" 
       name="correo_cliente" 
       placeholder="tu@correo.com" 
       required>
```

**menu_publico.html:**
```html
<!-- Mismo cambio - confirmación en modal del carrito también -->
<input type="email" name="correo_cliente" required>
```

### JavaScript

```javascript
// Antes:
const telefonoCliente = formDatos.querySelector('input[name="telefono_cliente"]').value;

// Ahora:
const correoCliente = formDatos.querySelector('input[name="correo_cliente"]').value;

// Validación con regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(correoCliente)) {
    alert('Por favor ingresa un correo válido');
    return;
}
```

---

## ⏳ LOADING OVERLAY DE ESPERA

### ¿Qué es?
Mientras se procesa un pedido, se muestra un **overlay oscuro con spinner** que dice "Procesando tu pedido...".

### Ubicaciones
1. **Carrito modal** (cuando haces click en 🛒)
2. **Página directa** `/carrito`
3. Duraciones personalizables

### Archivos

**CSS:** `app/static/css/carrito.css`
```css
/* LOADING OVERLAY */
.loading-overlay {
    display: none !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background: rgba(0, 0, 0, 0.6) !important;
    z-index: 99999 !important;  /* Delante de TODO */
    align-items: center !important;
    justify-content: center !important;
}

.loading-overlay.show {
    display: flex !important;
}

.loading-container {
    background: white;
    padding: 40px;
    border-radius: 16px;
    z-index: 100000;  /* Encima del overlay */
    text-align: center;
}

.spinner {
    width: 80px;
    height: 80px;
    border: 6px solid #f0f0f0;
    border-top: 6px solid #d32f2f;  /* Rojo MisterBurger */
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

**HTML:** `app/templates/carrito.html`
```html
<!-- Loading Overlay -->
<div id="loadingOverlay" class="loading-overlay">
    <div class="loading-container">
        <div class="spinner"></div>
        <h2>Procesando tu pedido...</h2>
        <p>Enviando confirmación por correo</p>
    </div>
</div>
```

**JavaScript:** 
```javascript
// Mostrar loading
const loadingOverlay = document.getElementById('loadingOverlay');
loadingOverlay.classList.add('show');

// Hacer fetch...

// Ocultar después de 2.5 segundos
setTimeout(() => {
    loadingOverlay.classList.remove('show');
    // Mostrar modal de confirmación
    modalConfirmacion.style.display = 'flex';
}, 2500);
```

### Apariencia
- ✅ Fondo oscuro semitransparente (60% opacidad)
- ✅ Contenedor blanco centrado
- ✅ Spinner rojo rotando
- ✅ Mensaje claro
- ✅ Z-index altísimo (99999-100000)
- ✅ Dura 2.5 segundos

---

## 🔧 CONFIGURACIÓN CENTRALIZADA (`.env`)

### Archivo: `.env`

```env
# ========== FLASK ==========
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=tu_clave_super_segura_2025

# ========== DATABASE ==========
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Minato15@
MYSQL_DB=restaurante

# ========== EMAIL ==========
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app

# ========== OPCIONES ==========
MAX_ITEMS_CARRITO=100
TIEMPO_POLLING_COCINA=5000  # ms
```

### Cómo cargarla

**`run.py`:**
```python
from dotenv import load_dotenv

# Cargar variables del .env ANTES de crear app
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**`app/config.py`:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
```

### ⚠️ Seguridad
- **NUNCA** commites el `.env` a Git
- Agrega a `.gitignore`:
  ```
  .env
  __pycache__/
  *.pyc
  .venv/
  ```

---

## 📊 Resumen de Cambios

| Característica | Archivo | Tipo | Status |
|---|---|---|---|
| Auto-update cocina | `public.py`, `cocina_pedidos.html` | API + JS | ✅ |
| Invoices | `public.py`, `factura.html` | Route + Template | ✅ |
| Emails | `correo.py`, `config.py` | Module + Config | ✅ |
| Email en forms | `carrito.html`, `menu_publico.html` | HTML + JS | ✅ |
| Loading overlay | `carrito.css`, `carrito.html` | CSS + HTML | ✅ |
| Env config | `.env`, `config.py`, `run.py` | Config | ✅ |

---

## 🚨 Troubleshooting

### Loading no aparece
- Verifica z-index es 99999+
- Revisa consola (F12) para errores JS
- Asegúrate que `loadingOverlay` existe en DOM

### Emails no llegan
- Verifica credenciales en `.env`
- Revisa que Gmail tenga "Aplicaciones menos seguras" activado
- Mira logs de aplicación

### API cocina no actualiza
- Revisa que `/api/pedidos_cocina` retorna JSON válido
- Verifica fetch interval (5 segundos por defecto)
- Abre DevTools → Network para ver requests

### Factura no se genera
- Verifica que número de pedido existe
- Chequea SQL query en `factura_pedido()`
- Asegúrate que items están en `pedido_items`

---

## 📞 Próximos Pasos (Futuro)

- [ ] WhatsApp notifications (twilio)
- [ ] Push notifications (FCM/OneSignal)
- [ ] SMS alerts
- [ ] Reportes avanzados
- [ ] Dashboard analytics

---

**Documento actualizado:** 2026-04-02  
**Versión:** 1.1  
**Próxima actualización:** TBD
