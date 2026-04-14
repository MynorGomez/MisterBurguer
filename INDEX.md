# 📖 ÍNDICE DE DOCUMENTACIÓN - MISTERBURGER

¡Bienvenido! 👋 Aquí encontrarás toda la documentación del sistema.

---

## 📚 LOS 4 DOCUMENTOS PRINCIPALES

### 1️⃣ **RESUMEN_RAPIDO.md** ⚡ (EMPIEZA AQUÍ)
**Tiempo de lectura: 5-10 minutos**

📍 **Para quién:** Cualquiera que quiera entender rápido cómo funciona  
📍 **Qué tiene:**
- Conceptos básicos sin tecnicismos
- 3 operaciones clave
- Ejemplos simples
- Ventajas del sistema

✅ **Lee esto primero si es tu primera vez**

---

### 2️⃣ **DOCUMENTACION_SISTEMA.md** 📋 (LA COMPLETA)
**Tiempo de lectura: 20-30 minutos**

📍 **Para quién:** Desarrolladores que quieren entender a fondo  
📍 **Qué tiene:**
- Visión general del proyecto
- Flujo completo de la aplicación (con diagramas ASCII)
- Explicación detallada de cada módulo
- Estructura de la BD con ejemplos
- Funciones principales con parámetros
- Ejemplos prácticos paso a paso
- Casos de uso y errores

✅ **Lee esto después del resumen rápido**

---

### 3️⃣ **GUIA_TECNICA.md** 🔧 (PARA DEVELOPERS)
**Tiempo de lectura: 15-20 minutos**

📍 **Para quién:** Desarrolladores que van a editar el código  
📍 **Qué tiene:**
- Arquitectura MVC explicada
- Estructura de carpetas
- Flujo detallado de datos (REQUEST 1, 2, 3)
- Queries SQL específicas
- Pseudocódigo de cada función
- Mapeos de BD
- Puntos clave de seguridad

✅ **Lee esto si necesitas modificar el código**

---

### 4️⃣ **README.md** 📄 (SETUP DEL PROYECTO)
**Tiempo de lectura: 5 minutos**

📍 **Para quién:** Administradores y DevOps  
📍 **Qué tiene:**
- Instrucciones de instalación
- Dependencias
- Comandos para ejecutar
- Configuración inicial

✅ **Lee esto para poner la app a funcionar**

---

### 5️⃣ **ACTUALIZACIONES_ULTIMAS.md** 🆕 (NUEVAS FEATURES - ABRIL 2026)
**Tiempo de lectura: 15-20 minutos**

📍 **Para quién:** Desarrolladores que necesitan entender las nuevas funcionalidades  
📍 **Qué tiene:**
- Sistema de auto-actualización panel cocina (AJAX polling en tiempo real)
- Sistema de invoices/facturas con impresión
- Notificaciones por email automatizadas
- Cambio de contacto (teléfono → email)
- Loading overlay con UX mejorada
- Configuración centralizada (.env)
- Guía de setup con ejemplos prácticos
- Troubleshooting de nuevas features

✅ **Lee esto si usas las nuevas funcionalidades implementadas**

---

## 🗺️ MAPA DE LECTURA SEGÚN TU PERFIL

### 👤 "Soy Cliente/Usuario"
```
1. RESUMEN_RAPIDO.md (entender qué es)
2. ✅ LISTO
```

### 👨‍💻 "Soy Developer Junior"
```
1. RESUMEN_RAPIDO.md (conceptos básicos)
2. DOCUMENTACION_SISTEMA.md (cómo funciona todo)
3. ACTUALIZACIONES_ULTIMAS.md (si trabajas con nuevas features)
4. ✅ Ya puedes hacer cambios simples
```

### 🧑‍💼 "Soy Developer Senior / Arquitecto"
```
1. RESUMEN_RAPIDO.md (overview)
2. GUIA_TECNICA.md (arquitectura y queries)
3. DOCUMENTACION_SISTEMA.md (si necesitas detalles)
4. ACTUALIZACIONES_ULTIMAS.md (para nuevas features)
5. ✅ Puedes hacer cambios complejos y escalar el sistema
```

### 🚀 "Voy a desplegar a Producción"
```
1. README.md (setup y requisitos)
2. GUIA_TECNICA.md (seguridad y arquitectura)
3. DOCUMENTACION_SISTEMA.md (flujos críticos)
4. ACTUALIZACIONES_ULTIMAS.md (nueva configuración .env)
5. ✅ Configurar BD, variables, backups, etc.
```

---

## 🎯 BÚSQUEDA RÁPIDA

### ¿Quiero entender...?

| Tema | Documento | Sección |
|------|-----------|---------|
| Cómo funciona el sistema | RESUMEN_RAPIDO.md | Flujo en 5 pasos |
| Las 3 operaciones principales | DOCUMENTACION_SISTEMA.md | Módulos Principales |
| Cómo se verifica el stock | DOCUMENTACION_SISTEMA.md | Funciones Clave |
| Cómo se descuenta inventario | GUIA_TECNICA.md | Pseudocódigo |
| Estructura de carpetas | GUIA_TECNICA.md | Estructura de Carpetas |
| Flujo de REQUEST | GUIA_TECNICA.md | Flujo Detallado de Datos |
| Queries SQL | GUIA_TECNICA.md | Mapeos de Base de Datos |
| Las rutas Flask | DOCUMENTACION_SISTEMA.md | Rubrique: app/routes/public.py |
| Tablas de BD | DOCUMENTACION_SISTEMA.md | Base de Datos |
| Ejemplos prácticos | DOCUMENTACION_SISTEMA.md | Ejemplos Prácticos |
| Seguridad | GUIA_TECNICA.md | Puntos Clave de Seguridad |
| Cómo instalar | README.md | Instalación |
| Auto-actualización panel cocina | ACTUALIZACIONES_ULTIMAS.md | Auto-Actualización Panel Cocina |
| Sistema de invoices/facturas | ACTUALIZACIONES_ULTIMAS.md | Sistema de Invoices / Facturas |
| Emails de confirmación | ACTUALIZACIONES_ULTIMAS.md | Notificaciones por Email |
| Cambio teléfono a email | ACTUALIZACIONES_ULTIMAS.md | Cambio de Teléfono a Correo |
| Loading overlay | ACTUALIZACIONES_ULTIMAS.md | Loading Overlay de Espera |
| Archivo .env | ACTUALIZACIONES_ULTIMAS.md | Configuración Centralizada |
| Troubleshooting nuevas features | ACTUALIZACIONES_ULTIMAS.md | Troubleshooting |

---

## ✨ PUNTOS CLAVE DEL SISTEMA

1. **SIN EXTRAS en personalización** 💰
   - Precio fijo = Precio de Hamburguesa Clásica
   - No importa qué ingredientes elija el usuario

2. **PAPAS Y BEBIDAS dinámicas** 🔄
   - Se obtienen de la BD (no hardcodeadas)
   - id_categoria = 2 (bebidas)
   - id_categoria = 3 (papas/acompañamientos)

3. **VERIFICACIÓN DE STOCK antes de procesar** ✅
   - Si no hay → rechaza TODO el carrito
   - No hay excepciones

4. **AUDITORÍA COMPLETA** 📊
   - Todo movimiento se registra en movimientos_inventario
   - Trazabilidad 100%

5. **TRANSACCIONES** 🔐
   - O pasa TODO o no pasa nada
   - Evita inconsistencias en BD

---

## 🚨 SI TIENES PROBLEMAS

### "La app no arranca"
→ Ver README.md sección Instalación

### "No entiendo el código"
→ Leer RESUMEN_RAPIDO.md primero

### "Necesito agregar una función"
→ Leer GUIA_TECNICA.md pseu pseudocódigo

### "Quiero modificar la BD"
→ Leer DOCUMENTACION_SISTEMA.md sección Base de Datos

### "Hay un error en la lógica"
→ Leer DOCUMENTACION_SISTEMA.md sección Ejemplos Prácticos

### "No funciona el auto-actualización del panel cocina"
→ Leer ACTUALIZACIONES_ULTIMAS.md sección Auto-Actualización Panel Cocina

### "Quiero ver cómo funcionan los emails"
→ Leer ACTUALIZACIONES_ULTIMAS.md sección Notificaciones por Email

### "No sé cómo configurar el .env"
→ Leer ACTUALIZACIONES_ULTIMAS.md sección Configuración Centralizada

### "Tengo problemas con las nuevas features"
→ Leer ACTUALIZACIONES_ULTIMAS.md sección Troubleshooting

---

## 📞 CONTACTO RÁPIDO

| Archivos Importantes en el Código |
|-----------------------------------|
| `app/routes/public.py` - Lógica principal |
| `app/utils/inventario.py` - Gestión de stock |
| `app/templates/menu_publico.html` - Interfaz |
| `app/__init__.py` - Configuración Flask |

---

## 🎓 ORDEN RECOMENDADO DE APRENDIZAJE

```
Nivel 1: RESUMEN_RAPIDO.md
  └─ Entiende: Qué es, cómo funciona en alto nivel
  
Nivel 2: DOCUMENTACION_SISTEMA.md  
  └─ Entiende: Cada función, cada módulo, flujos
  
Nivel 3: GUIA_TECNICA.md
  └─ Entiende: Arquitectura, queries, pseudocódigo
  
Nivel 3b: ACTUALIZACIONES_ULTIMAS.md (si usas nuevas features)
  └─ Entiende: Auto-actualización, emails, invoices, configuración .env
  
Nivel 4: Revisar código actual
  └─ Entiende: Implementación concreta en Python
  
Nivel 5: ¡Modificar y extender!
  └─ Implementa: Tus cambios y mejoras
```

---

## ✅ VALIDACIÓN: ¿Entendiste el sistema?

Si puedes responder estas preguntas → ✅ LISTO

1. ¿Cuál es el precio de una hamburguesa personalizada?
   - Respuesta: El de Hamburguesa Clásica (sin extras)

2. ¿Qué pasa si no hay stock?
   - Respuesta: Se rechaza TODO el carrito

3. ¿De dónde salen las bebidas?
   - Respuesta: De la BD, categoría ID = 2

4. ¿De dónde salen las papas?
   - Respuesta: De la BD, categoría ID = 3

5. ¿Cuáles son las 3 operaciones principales?
   - Respuesta: Ver menú, Personalizar, Confirmar

6. ¿Qué archivo maneja el stock?
   - Respuesta: app/utils/inventario.py

Si respondiste todas → 🎉 **¡Entendiste el sistema!**

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Lee **RESUMEN_RAPIDO.md** 
2. ✅ Lee **DOCUMENTACION_SISTEMA.md**
3. ✅ Lee **GUIA_TECNICA.md** (opcional)
4. ✅ Revisa el código en `app/routes/public.py`
5. ✅ Prueba la app localmente
6. ✅ ¡Personalizayla a tus necesidades!

---

**¡Bienvenido al Team MisterBurger! 🍔** 🚀
