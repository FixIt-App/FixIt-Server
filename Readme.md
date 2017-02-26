# Servidor del proyecto Fixit

Actualmente este servidor es un api rest que consume la aplicación móvil. La seguridad se maneja por tokens. Esto significa que hay que hacer una petición inicial a  api-token-auth/ para obenet el token. Una vez se tiene el token todas las peticiones posteriores deben ser enviadas utilizando el encabezdo Authorization: < token > a cada uno de los endpoints


# ¿Cómo ejecutar el servidor?

Para ejecutar el servidor es necesario tener instalado en el sistema las siguientes dependencias, se recomienda no usar Windows para el desarrollo ya qu este require de un proceso de instalación diferente.

 * Python 3, en FixIt solo se utilizará la versión 3 de python ya que la 2 prontamente perderá su soporte
 * Pip 3, pip es el gestor de paquetes de python, algo parecido a npm para nodejs o goget para golang
 * Virutalenv, este programa permite crear entornos virtuales para instalar las dependencias, de esta manera se pueden tener varias versiones de, por ejemplo django, en el sistema sin que estas entren en conflicto

 Ya con las dependencias instaladas clonar el proyecto

```sh
    git clone https://github.com/FixIt-App/FixIt-Server.git && cd FixIt-Server
```

Crear el entorno virtual, el siguiente comando crea un entorno virtual en la carpeta venv, este el nombre que se debe usar por convención, si usa otro debe agregarlo al .gitignore ya que estos entornos no deben versionarse. Además debe cambiar la condiguración del launch.json para una sesión de debugging en VSCode

```sh
    virtualenv -p python3 venv
```

Ya con el entornovirtual creado es necesario cargarlo a la sesión de shell actual, después de ejecutarlo se debe ver (venv) en el prompt.

```sh
    source venv/bin/activate
```

Instalar las dependencias en el entorno ya creado y cargado

```sh
    pip install -r requirements.txt
```

Ya está listo para ejecutar el servidor de desarrollo

```sh
    python manage.py runserver 0.0.0.0:8000
```
