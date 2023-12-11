
# Bienvenido a tu proyecto CDK Python!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

# Email Transacción

![Logo del banco](/Lambdas/Bank.png)

Programa que permite procesar un archivo CSV que contiene las transacciones realizadas por un usuario tanto de débito como de crédito, el programa procesa el archivo leyendo el contenido, crea u resumen de las transacciones "crédito y débito", y envía el resumen por E-mail al usuario.
Tecnología que se usó para esta aplicación:

- Python
- AWS CDK
- AWS Lambda
- AWS SES
- Consola AWS
- HTML

## Interfaz del programa
Dentro de la carpeta de nuestro programa en CDK hay dos archivos principales que permiten que nuestro programa funcione de manera correcta.
- requirements.txt
- transaccion_aws/transaccion_aws_stack.py

Una vez que tengamos nuestro proyecto es importante crear nuestro entorno virtual e instalar nuestras dependencias requirements.txt, de la siguiente manera.
desde nuestra consola.
En MacOS o Linux:
```sh
$ python -m venv .venv
$ source .venv/bin/activate
```
En Windows
```sh
$ python -m venv .venv
$ % .venv\Scripts\activate
```
Instalamos requirements.txt
```sh
pip install -r requirements.txt
```
### Interfaz de transaccion_aws_stack
Se define una función Lambda llamada "func_transaccion" y se le agrega una política IAM que permite enviar correos a través de [Simple Email Service (SES)][df1].
La política IAM creada anteriormente se añade al rol de la función Lambda, lo que le otorga los permisos necesarios para enviar correos a través de SES.
**ft.add_to_role_policy(ses_policy)**

Seguidamente, tenemos una carpeta llamada Lambdas, dentro de esta carpeta tenemos los archivos necesarios para crear la lógica de nuestro programa.
- Bank.png
- handler.py
- resumen_trasacciones.py
- transaccion.py
- transacciones.csv  

#### transacciones.csv
contiene las transacciones del usuario  teniendo encuneta los valores de Id,Date, donde los movimientos de credito estan reprentados con un signo de mas 0,7/15,**+60.**  y los de debito un un signo de menos 1,7/28,**-10.3**

#### transaccion.py
Se define una clase llamada ProcesadorCSV que se utiliza para cargar y procesar datos desde un archivo CSV que contiene transacciones financieras.
Este código utiliza la biblioteca estándar de Python para trabajar con archivos CSV y defaultdict para manejar la agrupación de transacciones por mes. La clase ProcesadorCSV tiene métodos para cargar transacciones desde un archivo CSV, procesar esas transacciones y generar un resumen financiero. El resumen incluye el saldo total, el número de transacciones por mes y los montos promedio de crédito y débito por mes, 

### resumen_trasacciones.py
Se importa la clase ProcesadorCSV desde el módulo transaccion. Esta clase contiene métodos para cargar transacciones desde el archivo CSV y generar un resumen de esas transacciones.

Se define la función generar_y_mostrar_resumen(): que no toma argumentos.
**def generar_y_mostrar_resumen():**
Se define una función llamada generar_y_mostrar_resumen 

archivo_csv = "transacciones.csv"
procesador = ProcesadorCSV(archivo_csv)
Se especifica el nombre del archivo CSV (transacciones.csv) y se crea un objeto ProcesadorCSV con este archivo.

**Carga de transacciones:**
procesador.cargar_transacciones()
Se llama al método cargar_transacciones del objeto procesador para cargar las transacciones desde el archivo CSV.

**Generación del resumen:**

**resumen = procesador.generar_resumen()**
Se llama al método generar_resumen del objeto procesador para obtener un resumen de las transacciones.

**Construcción de la cadena de texto del resumen:**

resumen_t = f"El saldo total es {resumen['Saldo total']:.2f}\n"
Se inicia una cadena de texto resumen_t con el saldo total.

Luego, se utiliza un bucle for para agregar información sobre el número de transacciones, el monto promedio del crédito y débito por mes, y el importe medio del débito al resumen.

**Retorno de la cadena de texto del resumen:**
return resumen_t
La función retorna la cadena de texto del resumen.
Llamada a la función y almacenamiento del resumen:

**resumen = generar_y_mostrar_resumen()**
Se llama a la función generar_y_mostrar_resumen y se almacena el resumen resultante en la variable resumen.

En resumen, este código carga transacciones desde un archivo CSV, genera un resumen de esas transacciones y devuelve el resumen como una cadena de texto.

## handler.py
El código está diseñado para enviar un correo electrónico al usuario con un resumen de sus transacciones y el logotipo del banco adjunto utilizando el servicio Simple Email Service (SES) de AWS.

La función handler es la función principal que se ejecutará cuando el evento sea activado (por ejemplo, cuando se llama a la función Lambda). La interfaz de esta función es estándar para una función Lambda de AWS y toma dos parámetros: event y context. 

La función realiza las siguientes acciones:
**def handler(event, context):**
- Genera y muestra un resumen de transacciones llamando a la función generar_y_mostrar_resumen.

- Configura algunas variables, como la región de SES, la dirección de correo electrónico del remitente y del destinatario.

- Extrae el nombre del destinatario del correo electrónico.

- Lee el contenido del logotipo como bytes, lo codifica en base64 y lo almacena en la variable contenido_base64.

- Construye el cuerpo del correo electrónico en formato HTML, incorporando el resumen y el logotipo.

- Configura el cliente SES utilizando la biblioteca boto3.

- Envía el correo electrónico utilizando la función send_email del cliente SES.

- Devuelve un diccionario indicando que el correo electrónico se envió exitosamente.

Para que el correo electrónico pueda ser enviado es necesario que los correos del que envía y el que recibe deben estar verificados por AWS SES 
Puedes seguir las instrucciones de la documentación oficial de amazon.

> https://docs.aws.amazon.com/es_es/ses/latest/dg/creating-identities.html#just-verify-email-proc 


En este punto, ahora puedes sintetizar la plantilla de CloudFormation para este código.
```sh
cdk synth
```
si todo ha salido puedes desplegar tu proyecto en la nube, recuerda que si tienes dos cuentas debes definir tu cuenta 
```sh
cdk deploy --profile nombre_de_tu_perfil
```
en caso de que solo tengas una cuenta se tomara el perfil por defecto haciendo solo:
```sh
cdk deploy
```

ahora en tu consola abres abres el servicio de lambda te debe aparecer toda la logica del programa, para ya poder empezar a hacer pruebas es necesario crear un test en formato de json simple para luego correr ese test, 

```json
{
   "key1": "value1",
  "key2": "value2"
}

Este es el resultado que nos deveria de dar.
Response

```json
{
  "statusCode": 200,
  "body": "Correo electrónico enviado exitosamente!"
}

Function Logs
START RequestId: 3019abc4-ebae-40ec-8a35-679af5633c98 Version: $LATEST
END RequestId: 3019abc4-ebae-40ec-8a35-679af5633c98
REPORT RequestId: 3019abc4-ebae-40ec-8a35-679af5633c98	Duration: 1939.40 ms	Billed Duration: 1940 ms	Memory Size: 128 MB	Max Memory Used: 72 MB	Init Duration: 281.36 ms

En la bandeja de entrada o de correos no deseados del cliente debe aparecer un correo con el resumen de sus tracciones.
