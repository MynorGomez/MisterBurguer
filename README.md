# MisterBurger - Sistema de Pedidos en Línea

## Descripción General

MisterBurger es una aplicación web completa para la gestión de pedidos en un restaurante de hamburguesas. Permite a los clientes navegar por un menú digital, agregar productos a un carrito de compras virtual, confirmar pedidos con datos personales y recibir confirmación inmediata. Por el lado administrativo, ofrece herramientas para gestionar empleados, inventario, compras, ventas y monitoreo de pedidos en cocina.

### Propósito del Sistema
- **Para Clientes**: Facilitar pedidos sin necesidad de ir físicamente al restaurante, con una experiencia intuitiva similar a apps de delivery.
- **Para Administradores**: Optimizar operaciones del restaurante mediante control de stock, seguimiento de pedidos y reportes financieros.
- **Beneficios Generales**: Reducción de errores en pedidos, mejor control de inventario, aumento en eficiencia operativa y satisfacción del cliente.

El sistema está diseñado para ser escalable, con una arquitectura modular que permite agregar nuevas funcionalidades como pagos en línea, notificaciones push o integración con delivery.

## Funcionalidades Principales

### Para Clientes (Público)
1. **Navegación de Menú**: Visualización atractiva de productos con imágenes, precios y descripciones.
2. **Carrito de Compras**: Sistema de carrito persistente con sesiones de Flask.
3. **Confirmación de Pedidos**: Modal interactivo con resumen de pedido y formulario de datos personales.
4. **Seguimiento de Pedidos**: Página de estado de pedido con número único de seguimiento.
5. **Sistema de Combos**: Opciones predefinidas de combos con precios especiales.
6. **Personalización de Hamburguesas**: Selección de base e ingredientes adicionales con cálculo automático de precios.

### Para Administradores
1. **Gestión de Empleados**: CRUD completo de empleados con roles.
2. **Control de Inventario**: Seguimiento de stock de insumos con alertas.
3. **Gestión de Compras**: Registro de compras a proveedores.
4. **Reportes de Ventas**: Análisis financiero y de productos.
5. **Monitoreo de Cocina**: Visualización en tiempo real de pedidos pendientes.

### Funcionalidades Técnicas
- **Control de Stock**: Verificación automática de disponibilidad antes de confirmar pedidos.
- **Gestión de Sesiones**: Carrito persistente entre visitas.
- **AJAX**: Confirmación asíncrona de pedidos sin recarga de página.
- **Responsive Design**: Adaptable a móviles y desktop.
- **Validación de Datos**: Tanto del lado cliente como servidor.

## Sistema de Combos y Personalización

### Descripción
El sistema ha sido actualizado para ofrecer dos nuevas formas de pedido además de los productos individuales:

1. **Combos Predefinidos**: Paquetes promocionales con productos combinados a precios especiales.
2. **Hamburguesas Personalizadas**: Selección de base de hamburguesa con ingredientes adicionales opcionales.

### Estructura de Base de Datos
Se agregaron las siguientes tablas:

- **`combos`**: Almacena información de combos (nombre, descripción, precio, imagen).
- **`combo_detalle`**: Detalla qué productos y cantidades componen cada combo.
- **`ingredientes`**: Ingredientes disponibles para personalización con precios extra.

### Funcionamiento

#### Combos
- Los combos se muestran en una sección dedicada del menú.
- Al agregar un combo al carrito, se verifica el stock de todos sus componentes.
- El descuento de inventario se realiza automáticamente al confirmar el pedido.

#### Personalización
- Los clientes seleccionan una base de hamburguesa de los productos disponibles.
- Pueden elegir múltiples ingredientes adicionales con precios extra.
- El precio total se calcula dinámicamente en el frontend.
- El stock se verifica tanto para la base como para los ingredientes seleccionados.

### Control de Inventario
- **Para Combos**: Se verifica y descuenta el stock de cada producto componente según las cantidades definidas en `combo_detalle`.
- **Para Personalizados**: Se descuenta la base (1 unidad) y cada ingrediente seleccionado (1 unidad por ingrediente).
- **Integración**: El sistema de inventario existente se extendió para manejar estos nuevos tipos de items.

### Estructura del Proyecto
```
MisterBurger/
├── app/
│   ├── __init__.py          # Inicialización de la app Flask con configuración de DB y blueprints
│   ├── config.py            # Variables de configuración (host DB, usuario, etc.)
│   ├── routes/
│   │   ├── public.py        # Endpoints públicos: menú, carrito, confirmación
│   │   ├── auth.py          # Autenticación de administradores
│   │   ├── admin.py         # Gestión de empleados, inventario, compras
│   │   └── cocina.py        # Visualización de pedidos pendientes para cocina
│   ├── templates/           #  HTML con herencia (base_panel.html)
│   │   ├── base_panel.html  # Layout base para admin
│   │   ├── menu_publico.html # Página principal con menú y carrito emergente
│   │   ├── carrito.html     # Vista completa del carrito
│   │   └── admin/           # Templates específicos de admin (dashboard, empleados, etc.)
│   ├── static/
│   │   ├── css/             # Hojas de estilo: menu.css, carrito.css, admin.css
│   │   └── img/             # Imágenes: logo.png, productos en MENU/
│   └── utils/
│       └── inventario.py    # Funciones auxiliares para control de stock
├── requirements.txt         # Lista de dependencias Python (Flask, mysqlclient, etc.)
├── run.py                   # Script de inicio: crea app y ejecuta servidor
└── README.md               # Esta documentación
```

### Flujo de Arquitectura
1. **Cliente accede** a `/` → Flask renderiza `menu_publico.html`.
2. **Interacción**: JS maneja clics, envía AJAX a rutas en `public.py`.
3. **Backend procesa**: Consulta DB, actualiza sesiones, devuelve JSON/HTML.
4. **Respuesta**: Frontend actualiza UI dinámicamente.

## Funcionalidades Principales Detalladas

### 1. Menú Público (`/`)
**Descripción**: Página de inicio donde los clientes ven el catálogo de productos.

**Características**:
- **Categorización**: Productos agrupados por categorías (ej. Hamburguesas, Bebidas).
- **Información por producto**: Nombre, descripción, precio, imagen.
- **Interacción**:
  - Campo de cantidad (por defecto 1).
  - Botón "Agregar" que envía POST a `/agregar_carrito/<id>`.
- **Carrito emergente**: Modal lateral que se abre con `🛒 (n)` en la barra superior.
  - Muestra resumen de items, total.
  - Botón "Siguiente" para proceder a confirmación.
- **Responsive**: Diseño adaptable a móviles y desktop.

**Flujo de uso**:
1. Usuario navega por categorías.
2. Selecciona producto, ajusta cantidad, hace clic "Agregar".
3. Contador en barra superior se actualiza.
4. Clic en carrito muestra modal con detalles.

### 2. Carrito de Compras
**Rutas**: `/carrito` (vista completa) y modal en menú público.

**Funcionalidades**:
- **Vista de items**: Lista con nombre, precio unitario, cantidad, subtotal.
- **Modificación**:
  - Botones +/- para cambiar cantidad (llaman a `/sumar_item/<id>` o `/restar_item/<id>`).
  - Botón "Eliminar" para remover item.
  - "Vaciar carrito" para limpiar todo.
- **Resumen**: Total calculado dinámicamente.
- **Transición**: Botón "Siguiente" abre modal de datos del cliente.

**Lógica de negocio**:
- Carrito almacenado en sesión de Flask (no requiere login).
- Subtotal = precio_unitario * cantidad.
- Total = suma de todos los subtotales.

### 3. Confirmación de Pedido (`/confirmar_pedido`)
**Proceso completo**:
1. **Modal de datos**: Aparece al hacer "Siguiente".
   - Campos: Nombre (requerido), Teléfono (opcional).
   - Validación: Nombre no vacío.
2. **Envío AJAX**: POST con datos del cliente.
   - Backend verifica stock disponible.
   - Si OK: Crea pedido, detalle, venta automática, descuenta inventario.
   - Si no: Devuelve error (ej. "Producto X sin stock").
3. **Modal de confirmación**: Muestra detalles completos.
   - Número de pedido único (ej. PED-20260330120000).
   - Datos del cliente.
   - Lista de productos con cantidades y subtotales.
   - Total final.
   - Estado: "Confirmado".
4. **Post-confirmación**: Carrito se vacía, contador se actualiza a 0, modales se cierran.

**Ejemplo de flujo**:
- Usuario agrega 2 Hamburguesas ($5 c/u) y 1 Papas ($3).
- Total: $13.
- Confirma con nombre "Juan Pérez".
- Recibe pedido #PED-20260330123045.
- Cocina ve el pedido en su panel.

### 4. Panel Administrativo (`/admin/*`)
**Módulos principales**:
- **Dashboard**: Resumen de ventas diarias, pedidos pendientes.
- **Empleados**: CRUD de personal (cocineros, meseros).
- **Inventario**: Control de stock por producto.
- **Compras**: Registro de compras a proveedores.
- **Proveedores**: Gestión de suministradores.
- **Ventas**: Reportes históricos.
- **Cocina**: Lista de pedidos pendientes con estados (pendiente, preparando, listo).

**Características**:
- Autenticación requerida.
- Formularios para agregar/editar.
- Tablas con paginación y filtros.

## Base de Datos

### Esquema Relacional
```
productos (id, nombre, descripcion, precio, imagen, id_categoria, estado, disponible)
categorias (id, nombre)
pedidos (id, id_cliente, nombre_cliente_invitado, telefono, numero_pedido, tipo_pedido, estado, fecha, subtotal, total)
pedido_detalle (id, id_pedido, id_producto, cantidad, precio_unitario, subtotal)
ventas (id, id_pedido, id_cliente, id_empleado, fecha, tipo_venta, metodo_pago, subtotal, total, estado)
venta_detalle (id, id_venta, id_producto, cantidad, precio_unitario, subtotal)
empleados (id, nombre, apellido, rol, etc.)
inventario (id, id_producto, cantidad_actual, etc.)
proveedores (id, nombre, contacto)
compras (id, id_proveedor, fecha, total)
```

### Relaciones Clave
- Un pedido tiene muchos detalles (productos).
- Una venta se genera automáticamente por pedido.
- Inventario se actualiza al confirmar pedido o registrar compra.

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MySQL Server
- Git

### Pasos de Instalación
1. **Clonar repositorio**:
   ```bash
   git clone <url-del-repo>
   cd MisterBurger
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**:
   - Crear base de datos MySQL llamada `restaurante`
   - Ejecutar scripts de creación de tablas (incluyendo las nuevas para combos)
   - Configurar credenciales en `app/config.py`

4. **Ejecutar aplicación**:
   ```bash
   python run.py
   ```

### Configuración de Base de Datos
Ejecutar el script `database_schema.sql` para crear las nuevas tablas:
```bash
mysql -u root -p restaurante < database_schema.sql
```

Para datos de ejemplo, ejecutar:
```bash
python insert_sample_data.py
```

## Cambios Recientes

### v2.0 - Sistema de Combos y Personalización
- ✅ **Nuevas funcionalidades**:
  - Sistema de combos predefinidos con precios especiales
  - Personalización de hamburguesas con ingredientes adicionales
  - Control de inventario extendido para nuevos tipos de items

- ✅ **Cambios técnicos**:
  - Nuevas tablas: `combos`, `combo_detalle`, `ingredientes`
  - Funciones de inventario actualizadas para combos y personalizados
  - Rutas backend extendidas para manejo de nuevos tipos de pedido
  - Frontend actualizado con secciones de combos y personalización

- ✅ **Mejoras de UX**:
  - Menú reorganizado con secciones claras
  - Cálculo automático de precios para personalizaciones
  - Validación de stock en tiempo real

## Uso del Sistema

### Para Clientes
1. Acceder a la página principal del menú
2. Elegir entre productos individuales, combos o personalización
3. Agregar items al carrito
4. Revisar carrito y confirmar pedido con datos personales
5. Recibir número de pedido para seguimiento

### Para Administradores
1. Iniciar sesión en `/login`
2. Gestionar empleados, inventario y proveedores
3. Monitorear pedidos en cocina
4. Revisar reportes de ventas

## API Endpoints Principales

### Público
- `GET /` - Menú principal
- `POST /agregar_carrito/<id>` - Agregar producto individual
- `POST /agregar_combo/<id>` - Agregar combo
- `POST /personalizar_hamburguesa` - Crear hamburguesa personalizada
- `GET /carrito` - Ver carrito
- `POST /confirmar_pedido` - Confirmar pedido

### Administrativo
- `GET /admin/dashboard` - Panel principal
- `GET /admin/empleados` - Gestión de empleados
- `GET /admin/inventario` - Control de stock
- `GET /cocina/pedidos` - Vista de cocina

## Consideraciones de Seguridad
- Validación de entrada en todos los formularios
- Protección contra SQL injection mediante consultas parametrizadas
- Sesiones seguras para autenticación de administradores
- Control de acceso basado en roles

## Próximas Mejoras
- Integración con pasarelas de pago
- Sistema de notificaciones push
- App móvil nativa
- API REST para integraciones externas
- Sistema de delivery con geolocalización

### Configuración
- Archivo: `app/config.py`
- Variables: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- Conexión: `mysql = MySQL(app)`

## API Endpoints Detallados

### Públicas
| Método | Ruta | Descripción | Parámetros | Respuesta |
|--------|------|-------------|------------|-----------|
| GET | `/` | Menú público | - | HTML con productos |
| POST | `/agregar_carrito/<id>` | Agregar producto | cantidad (form) | Redirect a `/` |
| GET | `/carrito` | Ver carrito completo | - | HTML con items |
| GET | `/sumar_item/<id>` | +1 cantidad | - | Redirect a `/carrito` |
| GET | `/restar_item/<id>` | -1 cantidad | - | Redirect a `/carrito` |
| GET | `/eliminar_item/<id>` | Remover item | - | Redirect a `/carrito` |
| GET | `/vaciar_carrito` | Limpiar carrito | - | Redirect a `/carrito` |
| POST | `/confirmar_pedido` | Confirmar orden | nombre_cliente, telefono | JSON: {numero_pedido, total, items} |
| GET | `/pedido/<numero>` | Ver estado | - | HTML con detalles |

**Ejemplo de request/response para `/confirmar_pedido`**:
```json
// Request POST
{
  "nombre_cliente": "Ana López",
  "telefono_cliente": "555-1234"
}

// Response JSON (éxito)
{
  "numero_pedido": "PED-20260330120000",
  "estado": "confirmado",
  "total": 15.50,
  "items": [
    {"id_producto": 1, "nombre": "Hamburguesa", "cantidad": 2, "subtotal": 10.00},
    {"id_producto": 2, "nombre": "Papas", "cantidad": 1, "subtotal": 3.50}
  ]
}
```

### Administrativas
- `/admin/dashboard`: Panel principal.
- `/admin/empleados`: CRUD empleados.
- `/admin/inventario`: Gestión stock.
- `/admin/compras`: Registro compras.
- `/admin/ventas`: Reportes.
- `/admin/cocina`: Pedidos activos.

## Instalación y Configuración Paso a Paso

### Prerrequisitos
- Python 3.8+ instalado.
- MySQL Server corriendo.
- Git (opcional para clonar).

### Pasos Detallados
1. **Descargar proyecto**:
   - Copiar carpeta `MisterBurger` a tu máquina.

2. **Instalar dependencias**:
   ```
   cd MisterBurger
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**:
   - Crear DB: `CREATE DATABASE misterburger;`
   - Ejecutar scripts SQL para crear tablas (asumiendo que tienes los CREATE TABLE).
   - Editar `app/config.py` con tus credenciales MySQL.

4. **Ejecutar aplicación**:
   ```
   python run.py
   ```
   - Accede a `http://localhost:5000`

5. **Configuración inicial**:
   - Agregar productos e imágenes en `app/static/img/MENU/`.
   - Crear usuario admin en DB.

## Uso del Sistema - Guías Detalladas

### Para Clientes
1. **Navegar menú**: Ver productos por categoría.
2. **Agregar al carrito**: Seleccionar cantidad, clic "Agregar".
3. **Revisar carrito**: Clic en `🛒` para modal emergente.
4. **Ajustar pedido**: Modificar cantidades o eliminar items.
5. **Confirmar**:
   - Clic "Siguiente".
   - Llenar nombre y teléfono.
   - Clic "Realizar pedido".
6. **Recibir confirmación**: Ver número de pedido y detalles.

### Para Administradores
1. **Login**: Acceder a `/admin` con credenciales.
2. **Gestionar empleados**: Agregar cocineros, meseros.
3. **Controlar inventario**: Ver stock, ajustar cantidades.
4. **Registrar compras**: Ingresar compras de proveedores.
5. **Monitorear ventas**: Ver reportes diarios/mensuales.
6. **Cocina**: Cambiar estados de pedidos (preparando → listo).

## Problemas Resueltos y Mejoras Implementadas

### 1. Modal de Carrito Emergente Dinámico
**Problema**: El carrito se cargaba como HTML estático sin JS funcional.
**Solución**: Usar `fetch()` para cargar `/carrito` en modal, luego `recargarScriptsModal()` para inicializar event listeners.
**Impacto**: Carrito funcional en modal sin recargar página.

### 2. Confirmación de Pedido con Detalles Completos
**Problema**: Modal solo mostraba número de pedido.
**Solución**:
- Backend devuelve `items` en JSON.
- Frontend renderiza lista `<ul>` con productos.
- Botón cambia de "Ver detalles" a "Cerrar".
**Impacto**: Cliente ve resumen completo sin navegación extra.

### 3. Limpieza de Datos en Modal
**Problema**: Datos previos quedaban al reabrir modal.
**Solución**: Función `resetModalConfirmacion()` vacía textos e ítems.
**Impacto**: Evita confusión con pedidos anteriores.

### 4. Cierre Completo de Modales
**Problema**: Cerrar confirmación regresaba a modal anterior.
**Solución**: Al cerrar, ocultar todos los modales y resetear contador.
**Impacto**: Experiencia limpia, carrito vacío tras pedido.

### 5. Visualización de Imágenes
**Problema**: DB tenía rutas absolutas, causando URLs inválidas.
**Solución**: Extraer basename con `producto[4].split('\\')[-1]`.
**Impacto**: Imágenes se muestran correctamente.

## Estilos y Diseño

### Filosofía de Diseño
- **Colores**: Rojo (#d32f2f) para acentos, blanco/gris para fondo.
- **Tipografía**: Arial sans-serif, legible.
- **Responsive**: Media queries para móviles.
- **Animaciones**: Slide-in para modales, hover effects.

### Componentes Clave
- **Modales**: Overlay con blur, centrados.
- **Botones**: Gradientes, sombras en hover.
- **Cards**: Bordes redondeados, sombras suaves.
- **Formularios**: Campos con focus styles.

## Seguridad y Validaciones

- **Input sanitization**: Flask-WTF para formularios.
- **SQL Injection**: Consultas parametrizadas.
- **Stock validation**: Chequeo antes de confirmar pedido.
- **Sesiones**: Carrito seguro sin persistencia en DB hasta confirmación.
- **Autenticación**: Para admin (futuro: hashing de passwords).

## Próximas Mejoras Sugeridas

- **Pagos en línea**: Integración con Stripe/PayPal.
- **Notificaciones**: Email/SMS para confirmaciones.
- **App móvil**: Versión React Native.
- **Analytics**: Reportes avanzados con gráficos.
- **Multi-idioma**: Soporte para español/inglés.
- **API REST**: Para integraciones de delivery.

## Contribución y Desarrollo

### Estándares de Código
- Usar PEP8 para Python.
- Commits descriptivos.
- Pruebas unitarias con pytest.

### Debugging
- Logs en consola para JS.
- Flask debug mode activado.
- MySQL logs para queries.

## Licencia y Contacto

Proyecto privado para MisterBurger.
Para soporte: [tu-email@ejemplo.com]

---

*Documentación actualizada al 30 de marzo de 2026. Versión del sistema: 1.0*w