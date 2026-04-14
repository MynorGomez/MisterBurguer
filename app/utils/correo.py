import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.config import Config

def enviar_correo(destinatario, asunto, cuerpo_html):
    """
    Envía un correo electrónico usando la configuración centralizada
    
    Args:
        destinatario: email del cliente
        asunto: asunto del correo
        cuerpo_html: contenido HTML del correo
    """
    try:
        # Usar configuración desde app.config (cargada desde .env)
        servidor_smtp = Config.MAIL_SERVER
        puerto = Config.MAIL_PORT
        remitente = Config.MAIL_USERNAME
        contraseña = Config.MAIL_PASSWORD
        
        # Crear mensaje
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = asunto
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        
        # Adjuntar contenido HTML
        parte_html = MIMEText(cuerpo_html, 'html', 'utf-8')
        mensaje.attach(parte_html)
        
        # Conectar y enviar
        with smtplib.SMTP(servidor_smtp, puerto) as servidor:
            servidor.starttls()
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        
        return True
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        return False


def enviar_confirmacion_pedido(nombre_cliente, correo_cliente, numero_pedido, total, detalles, url_seguimiento=None):
    """
    Envía correo de confirmación del pedido al cliente
    
    Args:
        nombre_cliente: nombre del cliente
        correo_cliente: email del cliente
        numero_pedido: número único del pedido
        total: total del pedido
        detalles: lista de items del pedido
        url_seguimiento: URL para que el cliente pueda seguir su pedido (opcional)
    """
    
    # Construir tabla de detalles
    tabla_detalles = ""
    for item in detalles:
        tabla_detalles += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{item.get('nombre', 'Producto')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{item.get('cantidad', 1)}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">Q {item.get('precio', 0):.2f}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;"><strong>Q {item.get('subtotal', 0):.2f}</strong></td>
        </tr>
        """
    
    # Construir enlace de seguimiento
    enlace_seguimiento = ""
    if url_seguimiento:
        enlace_seguimiento = f"""
                <a href="{url_seguimiento}" style="display: inline-block; margin-top: 12px; padding: 12px 25px; background-color: #ff6b35; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">
                    📍 Ver Estado del Pedido
                </a>
        """
    
    # Construir correo
    cuerpo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Confirmación de Pedido</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="text-align: center; border-bottom: 3px solid #ff6b35; padding-bottom: 20px; margin-bottom: 20px;">
                <h1 style="color: #333; margin: 0;">🍔 MisterBurger</h1>
                <p style="color: #666; margin: 5px 0 0 0;">¡Confirmación de Pedido!</p>
            </div>
            
            <p style="color: #333; font-size: 14px;">Hola <strong>{nombre_cliente}</strong>,</p>
            
            <p style="color: #666; font-size: 14px;">
                Tu pedido ha sido confirmado exitosamente. Aquí están los detalles:
            </p>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #ff6b35; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Número de Pedido:</strong> <span style="color: #ff6b35;">{numero_pedido}</span></p>
                <p style="margin: 5px 0;"><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p style="margin: 5px 0;"><strong>Estado:</strong> <span style="color: #4CAF50; font-weight: bold;">CONFIRMADO</span></p>
            </div>
            
            <h2 style="color: #333; border-bottom: 2px solid #eeeeee; padding-bottom: 10px; margin-top: 20px;">Detalles del Pedido</h2>
            
            <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                <thead>
                    <tr style="background-color: #f0f0f0;">
                        <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Producto</th>
                        <th style="padding: 12px; text-align: center; border-bottom: 2px solid #ddd;">Cantidad</th>
                        <th style="padding: 12px; text-align: right; border-bottom: 2px solid #ddd;">Precio</th>
                        <th style="padding: 12px; text-align: right; border-bottom: 2px solid #ddd;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {tabla_detalles}
                </tbody>
            </table>
            
            <div style="text-align: right; margin-top: 20px; padding-top: 15px; border-top: 2px solid #eeeeee;">
                <p style="font-size: 18px; color: #333; margin: 0;">
                    <strong>Total a Pagar: <span style="color: #ff6b35;">Q {total:.2f}</span></strong>
                </p>
            </div>
            
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center;">
                <p style="color: #2e7d32; margin: 0; font-weight: bold;">✓ Tu pedido está en preparación</p>
                <p style="color: #666; margin: 10px 0 0 0; font-size: 12px;">
                    Puedes ver el estado de tu pedido en tiempo real haciendo clic en el botón de abajo.
                </p>
                {enlace_seguimiento}
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <p style="color: #999; font-size: 12px; text-align: center; margin: 0;">
                MisterBurger © 2024. Todos los derechos reservados.
            </p>
        </div>
    </body>
    </html>
    """
    
    return enviar_correo(
        destinatario=correo_cliente,
        asunto=f"Confirmación de Pedido - {numero_pedido} 🍔",
        cuerpo_html=cuerpo_html
    )


def enviar_factura_pedido(nombre_cliente, correo_cliente, numero_pedido, fecha_pedido, total, subtotal, detalles):
    """
    Envía la factura del pedido al cliente
    
    Args:
        nombre_cliente: nombre del cliente
        correo_cliente: email del cliente
        numero_pedido: número del pedido
        fecha_pedido: fecha del pedido
        total: total del pedido
        subtotal: subtotal antes de impuestos
        detalles: lista de items con detalles
    """
    
    # Calcular IVA
    iva = total - subtotal
    
    # Construir tabla de detalles
    tabla_detalles = ""
    for item in detalles:
        tabla_detalles += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item.get('nombre', 'Producto')}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">{item.get('cantidad', 1)}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">Q {item.get('precio', 0):.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;"><strong>Q {item.get('subtotal', 0):.2f}</strong></td>
        </tr>
        """
    
    cuerpo_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Factura - {numero_pedido}</title>
    </head>
    <body style="font-family: 'Courier New', monospace; background-color: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border: 2px solid #333;">
            
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 15px;">
                <h1 style="color: #333; margin: 0; font-size: 28px;">MISTERBURGER</h1>
                <p style="color: #666; margin: 5px 0 0 0; font-size: 11px;">Comidas Rápidas - Guatemala</p>
            </div>
            
            <!-- Título Factura -->
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #ff6b35; margin: 0; font-size: 16px;">FACTURA / RECIBO</h2>
            </div>
            
            <!-- Info Cliente -->
            <div style="margin-bottom: 20px; font-size: 12px;">
                <p style="margin: 3px 0;"><strong>No. Pedido:</strong> {numero_pedido}</p>
                <p style="margin: 3px 0;"><strong>Cliente:</strong> {nombre_cliente}</p>
                <p style="margin: 3px 0;"><strong>Correo:</strong> {correo_cliente}</p>
                <p style="margin: 3px 0;"><strong>Fecha:</strong> {fecha_pedido.strftime('%d/%m/%Y %H:%M') if hasattr(fecha_pedido, 'strftime') else fecha_pedido}</p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #333; margin: 15px 0;">
            
            <!-- Tabla de Productos -->
            <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 11px;">
                <thead>
                    <tr style="border-bottom: 2px solid #333;">
                        <th style="padding: 8px; text-align: left;">DESCRIPCIÓN</th>
                        <th style="padding: 8px; text-align: center;">CANT</th>
                        <th style="padding: 8px; text-align: right;">PRECIO</th>
                        <th style="padding: 8px; text-align: right;">TOTAL</th>
                    </tr>
                </thead>
                <tbody>
                    {tabla_detalles}
                </tbody>
            </table>
            
            <hr style="border: none; border-top: 1px solid #333; margin: 15px 0;">
            
            <!-- Totales -->
            <div style="margin: 15px 0; font-size: 12px; text-align: right;">
                <p style="margin: 5px 0;"><strong>Subtotal:</strong> Q {subtotal:.2f}</p>
                <p style="margin: 5px 0; color: #666;"><strong>IVA (0%):</strong> Q {iva:.2f}</p>
                <div style="border-top: 2px solid #333; padding-top: 10px; margin-top: 10px;">
                    <p style="margin: 0; font-size: 14px;"><strong>TOTAL: Q {total:.2f}</strong></p>
                </div>
            </div>
            
            <hr style="border: none; border-top: 1px solid #333; margin: 15px 0;">
            
            <!-- Notas -->
            <div style="background-color: #f9f9f9; padding: 10px; border-left: 3px solid #ff6b35; margin: 15px 0; font-size: 11px;">
                <p style="margin: 0; color: #666;">Gracias por su compra 🍔</p>
                <p style="margin: 5px 0 0 0; color: #999; font-size: 10px;">
                    Comprobante válido. Conserve este recibo.
                </p>
            </div>
            
            <p style="color: #999; font-size: 10px; text-align: center; margin-top: 20px;">
                MisterBurger © 2024
            </p>
        </div>
    </body>
    </html>
    """
    
    return enviar_correo(
        destinatario=correo_cliente,
        asunto=f"Factura / Recibo - {numero_pedido} 🧾",
        cuerpo_html=cuerpo_html
    )
