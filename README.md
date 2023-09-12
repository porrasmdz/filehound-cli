#Instrucciones
##1. Configure un entorno virtual con

$python -m venv ./venv/

Se deberia crear una carpeta venv

##2. Active el entorno 

$./venv/Scripts/activate

Deberia salir en la terminal "venv" en verde

##3. Verifique configuracion correcta con

$pip list

Deberian salir todas las dependencias instaladas en entorno virtual.

##4. Cree el archivo .env con las variables de entorno necesarias.
Ejemplo de .env:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_DATABASE=sample_name