# Implementación de Auto-Actualización de Pedidos y Sistema de Facturas

## 🚀 Resumen de Cambios

Se han implementado tres funcionalidades principales:

1. **Auto-Actualización de Pedidos** - El panel de cocina se actualiza automáticamente cada 5 segundos
2. **Sistema de Factura/Recibo** - Los clientes pueden descargar e imprimir su factura
3. **Envío de Correo** - Los detalles del pedido se envían al correo del cliente

---

## 📋 Requisitos de Base de Datos

**⚠️ IMPORTANTE:** Necesitas actualizar tu tabla de pedidos para usar correo en lugar de teléfono.

### Script SQL

```sql
-- Cambiar campo telefono_cliente_invitado a correo_cliente_invitado
ALTER TABLE pedidos 
MODIFY COLUMN telefono_cliente_invitado VARCHAR(255) COMMENT 'Será reemplazado por correo',
ADD COLUMN correo_cliente_invitado VARCHAR(255) DEFAULT NULL;

-- Si tienes datos antiguos, puedes migrar así:
UPDATE pedidos SET correo_cliente_invitado = 'cliente@example.com' WHERE correo_cliente_invitado IS NULL;

-- Finalmente, puedes eliminar la columna antigua si lo deseas
-- ALTER TABLE pedidos DROP COLUMN telefono_cliente_invitado;
```

---

## ⚙️ Configuración de Correo

El sistema usa Gmail SMTP por defecto. Necesitas configurar tus credenciales:

### Paso 1: Obtener contraseña de aplicación (Gmail)

1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Mail" y "Windows Computer" (o tu dispositivo)
3. Google te generará una contraseña de 16 caracteres
4. **Copia esta contraseña** (sin espacios)

### Paso 2: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (o copia `.env.example`):

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  # (sin espacios en la app)
```

### Paso 3: Cargar variables de entorno

Modifica `run.py` o usa python-dotenv. Ejemplo:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📊 Estructura de Archivos Nuevos/Modificados

### Nuevos Archivos:
- `app/utils/correo.py` - Módulo para envío de correos
- `app/templates/factura.html` - Template de factura/recibo
- `.env.example` - Archivo de configuración de ejemplo

### Archivos Modificados:
- `app/routes/public.py` - Nuevas rutas API y cambio de teléfono a correo
- `app/routes/cocina.py` - Cambio de teléfono a correo
- `app/config.py` - Configuración de correo
- `app/templates/carrito.html` - Cambio de teléfono a correo en el modal
- `app/templates/estado_pedido.html` - Cambio de teléfono a correo y link a factura
- `app/templates/cocina_pedidos.html` - Auto-actualización con AJAX

---

## 🔄 Auto-Actualización de Pedidos (Cocina)

### ¿Cómo funciona?

1. El panel de cocina ahora se actualiza automáticamente cada 5 segundos
2. Usa una API REST (`/api/pedidos_cocina`) que devuelve JSON
3. El JavaScript renderiza dinámicamente los pedidos sin refrescar la página
4. Hay un control checkbox para pausar/reanudar la actualización

### APIs Nuevas:

```
GET /api/pedidos_cocina
└─ Retorna lista de todos los pedidos activos en JSON

GET /api/pedido/<numero_pedido>
└─ Retorna detalles de un pedido específico con auto-actualización
```

---

## 📄 Sistema de Facturas

### Rutas Nuevas:

```
GET /factura/<numero_pedido>
└─ Muestra la factura formateada lista para imprimir
```

### Características:

- ✅ Diseño de factura estilo "recibo"
- ✅ Botón de impresión (`window.print()`)
- ✅ Información del cliente y detalles del pedido
- ✅ Número de pedido prominente
- ✅ Totales desglosados

---

## 📧 Envío de Correos

### ¿Cuándo se envía?

1. **Confirmación de Pedido** - Cuando el cliente confirma el pedido
2. Los detalles incluyen:
   - Número de pedido único
   - Detalles de todos los items
   - Total a pagar
   - Fecha y hora

### Funciones en `correo.py`:

```python
enviar_confirmacion_pedido()
└─ Envía correo con confirmación del pedido

enviar_factura_pedido()
└─ Envía correo con la factura formateada
```

### HTML de ejemplo

Los correos se envían en HTML formateado con:
- Branding de MisterBurger
- Tabla de productos
- Total desglosado
- Información de contacto

---

## 🛠️ Solución de Problemas

### Error: "SMTPAuthenticationError"

**Causa:** Contraseña incorrecta  
**Solución:** 
- Verifica que usaste "Contraseña de aplicación" (16 caracteres)
- No uses tu contraseña de Gmail normal
- Va sin espacios en el .env

### Error: "ConnectionRefusedError" al enviar correo

**Causa:** Servidor SMTP no accesible  
**Solución:**
- Verifica que tienes internet
- Prueba con otro servidor (ej: smtp.outlook.com en puerto 587)

### Los pedidos no se actualizan en cocina

**Causa:** API no disponible  
**Solución:**
- Verifica que `/api/pedidos_cocina` retorna datos
- Abre la consola (F12) y revisa errores de red
- Asegúrate que la BD tiene pedidos con estado 'confirmado', 'en_preparacion' o 'listo'

---

## 📱 Flujo de Usuario

### Cliente:
1. Completa su carrito
2. **Nuevo:** Ingresa su **CORREO** (antes era teléfono)
3. Confirma el pedido
4. Recibe un correo de confirmación automáticamente
5. Puede ver/descargar su factura desde el link en el correo o en la web

### Staff de Cocina:
1. Entra al panel de cocina
2. **Nuevo:** La página se actualiza automáticamente cada 5 segundos
3. Ya no necesita refrescar manualmente
4. Ve los estado cambios en tiempo casi real

---

## ✅ Validación

Para verificar que todo funciona:

1. **Base de datos:**
   ```sql
   SELECT * FROM pedidos LIMIT 1; 
   -- Debe tener columna correo_cliente_invitado
   ```

2. **Correr la app:**
   ```bash
   python run.py
   ```

3. **Prueba en navegador:**
   - Crear un pedido de prueba
   - Verificar que se crea con correo (no teléfono)
   - Revisar tu bandeja de entrada por el correo

4. **Panel de cocina:**
   - Ir a `/cocina/pedidos`
   - Verificar que el control de auto-actualización funciona
   - Cambiar estado de un pedido y ver que se actualiza automáticamente

---

## 🔒 Seguridad

- Las contraseñas de correo se guardan en `.env` (NO en el código)
- `.env` debe agregarse a `.gitignore`
- No commits la contraseña real al repositorio

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de la consola (F12 en navegador)
2. Revisa los logs del servidor Flask en la terminal
3. Verifica que tu servidor SMTP es accesible
4. Comprueba que tus credenciales son correctas

---

**¡Implementación completada!** 🎉
