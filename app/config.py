import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Claves generales
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_super_segura_2025')
    
    # Base de datos
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Minato15@')
    MYSQL_DB = os.getenv('MYSQL_DB', 'restaurante')
    
    # Configuración de correo (SMTP)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'tu_correo@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'tu_contraseña_app')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@misterburger.com')