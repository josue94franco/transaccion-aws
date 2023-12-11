import os
import base64
import boto3

from resumen_trasacciones import generar_y_mostrar_resumen

def handler(event, context):
    try:
        # Generar y mostrar el resumen de transacciones
        resumen = generar_y_mostrar_resumen()

        # Configurar variables
        ses_region = "us-east-1"
        sender_email = "http.joshua@gmail.com"
        recipient_email = "josue_franco_94@hotmail.com"

        # Extraer el nombre antes del símbolo '@'
        email_receiver_name = recipient_email.split('@')[0]

        # Ruta del archivo del logotipo
        logotipo_path = os.path.join(os.path.dirname(__file__), 'Bank.png')

        # Leer el contenido del logotipo como bytes y codificarlo en base64
        with open(logotipo_path, 'rb') as imagen:
            contenido_base64 = base64.b64encode(imagen.read()).decode('utf-8')

        # Contenido del correo electrónico
        email_body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                /* Estilo para el encabezado h1 */
                h1 {{
                    font-size: 15px; /* Ajusta este valor según sea necesario */
                }}
            </style>
        </head>
        <body>
            <h1>Hola {email_receiver_name} - Resumen de cuenta y logotipo</h1>
            <p>{resumen}</p>
            <img src="data:image/png;base64, {contenido_base64}" alt="Logo" style="width: 100px; height: auto;">
        </body>
        </html>
        """

        # Configurar el cliente SES
        ses_client = boto3.client('ses', region_name=ses_region)

        # Enviar el correo electrónico
        response = ses_client.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': 'Resumen de cuenta y logotipo'},
                'Body': {'Html': {'Data': email_body_html}},
            },
        )

        return {'statusCode': 200, 'body': 'Correo electrónico enviado exitosamente!'}

    except Exception as e:
        # Manejar cualquier excepción e imprimir el mensaje de error
        print(f"Error: {e}")
        return {'statusCode': 500, 'body': 'Error al enviar el correo electrónico.'}
