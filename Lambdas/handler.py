#import os
import boto3

def handler(event, context):
    ses_region = "us-east-1"
    sender_email = "http.joshua@gmail.com"
    recipient_email = "josue_franco_94@hotmail.com"

    # Contenido del correo electrónico en formato HTML
    email_body_html = """
    <html>
        <body>
            <h1>Hola, este es un correo electrónico de prueba</h1>
            <p>Este es el contenido del cuerpo del correo electrónico en formato HTML.</p>
        </body>
    </html>
    """

    # Configurar el cliente SES
    ses_client = boto3.client('ses', region_name=ses_region)

    # Enviar el correo electrónico
    response = ses_client.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [recipient_email],
        },
        Message={
            'Subject': {
                'Data': 'Asunto del correo electrónico',
            },
            'Body': {
                'Html': {
                    'Data': email_body_html,
                },
            },
        },
    )

    return {
        'statusCode': 200,
        'body': 'Correo electrónico enviado exitosamente!',
    }