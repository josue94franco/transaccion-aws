import os
import base64
import boto3

from resumen_trasacciones import generar_y_mostrar_resumen

def handler(event, context):
    resumen = generar_y_mostrar_resumen()
    #Imprimir el valor del resumen para verificar
    #print("Resumen:", resumen)
    
    ses_region = "us-east-1"
    sender_email = "http.joshua@gmail.com"
    recipient_email = "josue_franco_94@hotmail.com"
    
     # Extraer el nombre antes del símbolo '@'
    email_receiver_name = recipient_email.split('@')[0]
    # Set the subject and body of the email
    subject = 'Resumen general de su cuenta y logotipo'
    
    # Ruta del archivo del logotipo
    #logotipo = 'Bank.png'
    logotipo = os.path.join(os.path.dirname(__file__), 'Bank.png')
    # Leer el contenido del logotipo como bytes y codificarlo en base64
    with open(logotipo, 'rb') as imagen:
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