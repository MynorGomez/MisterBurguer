# 🔧 Guía de Uso - Configuración Centralizada

## ¿Cómo funciona ahora?

Todo está centralizado en **`app/config.py`**. Cualquier archivo que necesite variables de configuración la importa desde ahí.

---

## 📋 Paso 1: Crear tu archivo `.env`

1. Copia los valores de tu `secret.env` a un archivo `.env` en la raíz del proyecto:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Minato15@
MYSQL_DB=restaurante

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña_app
```

2. **NO commits** el `.env` a git. Añade a `.gitignore`:
```
.env
*.env
secret.env
```

---

## 💻 Paso 2: Usar en cualquier archivo

### Opción A: Importar solo las variables que necesitas

```python
from app.config import Config

# Acceder a las configuraciones
correo = Config.MAIL_USERNAME
puerto = Config.MAIL_PORT
```

### Opción B: Usar la clase completa

```python
from app.config import Config

def conectar_email():
    servidor = Config.MAIL_SERVER
    puerto = Config.MAIL_PORT
    usuario = Config.MAIL_USERNAME
    contraseña = Config.MAIL_PASSWORD
    # ...hacer algo con esto
```

---

## 📁 Ejemplos en tu proyecto

### ✅ Ya configurado correctamente:

**`app/config.py`** - Carga `load_dotenv()` al inicio
```python
from dotenv import load_dotenv
load_dotenv()  # Esto carga tu .env automáticamente

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '...')
    # etc
```

**`app/utils/correo.py`** - Importa desde config
```python
from app.config import Config

def enviar_correo(...):
    servidor_smtp = Config.MAIL_SERVER
    puerto = Config.MAIL_PORT
    # etc - NO repites las credenciales
```

**`app/routes/public.py`** - Ya usa Config 
```python
from app.config import Config  # Si lo necesita
```

---

## 🎯 Si necesitas agregar nuevas variables

1. **Añade a tu `.env`:**
```env
MI_NUEVA_VARIABLE=valor_aqui
OTRA_VARIABLE=otro_valor
```

2. **Añade a `app/config.py`:**
```python
class Config:
    # ... otras variables ...
    MI_NUEVA_VARIABLE = os.getenv('MI_NUEVA_VARIABLE', 'valor_por_defecto')
    OTRA_VARIABLE = os.getenv('OTRA_VARIABLE', 'valor_default')
```

3. **Úsalo en cualquier archivo:**
```python
from app.config import Config

print(Config.MI_NUEVA_VARIABLE)  # ✅ Así de simple
```

---

## ⚙️ Instalación de dependencia (si no la tienes)

```bash
pip install python-dotenv
```

---

## ✅ Checklist

- [ ] Tengo mi `.env` en la raíz del proyecto
- [ ] `.env` está en `.gitignore`
- [ ] `app/config.py` tiene `load_dotenv()` al inicio
- [ ] Otros archivos importan: `from app.config import Config`
- [ ] `python-dotenv` está instalado

---

## 🔒 Seguridad

✅ Las credenciales están en `.env` (NO en el código)  
✅ `app/config.py` usa `os.getenv()` para leerlas  
✅ `.env` NO se sube a git (está en `.gitignore`)  
✅ La app puede leer de variables de entorno automáticamente

---

## 🆘 Problemas comunes

### "ModuleNotFoundError: No module named 'dotenv'"
**Solución:** `pip install python-dotenv`

### Las variables son `None` o valores por defecto
**Solución:** 
- Verifica que `.env` está en la raíz (mismo nivel que `run.py`)
- Revisa que las variables están escritas correctamente en `.env`
- Reinicia la app después de editar `.env`

### "ImportError: cannot import name 'Config' from 'app.config'"
**Solución:** Asegúrate que `app/config.py` existe y tiene la clase `Config`

---

¡Listo! Así tu código está limpio y centralizado. 🎉
