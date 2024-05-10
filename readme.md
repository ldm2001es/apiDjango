# Welcome to API Django!

## Descripción de los servicios

Se han creado servicios Rest para gestionar los pedidos y los artículos. 

Se ha usado la autenticación de Django para los servicios. Por lo que tendremos que crear un super usuario que nos valdrá tanto para la autenticación de los servicios como al acceso al frontal que por defecto genera Django.

Los servicios creados cuentan con el comportamiento general de los servicios Rest.

En el caso de la actualización de los pedidos utilizaremos el método UPDATE, donde podemos indicar nuevos artículos como modificar artículos que ya existen en el pedido. Por ejemplo:
`
    { "articles": [{
                "id": 19,
                "amount": 77,
                "article": {
                    "id": 1,
                    "url": "http://localhost:8000/articles/1/",
                    "reference": "1",
                    "name": "1",
                    "description": "1",
                    "price": 1.0,
                    "tax": 1.0,
                    "creation_date": "2024-05-10"
                }
            }
        , {"reference": "2", "amount": "22"}]
    }
`

Donde el artículo con id 1 lo estamos modificando (sólo se puede modificar la cantidad) y damos de alta un nuevo artículo con el artículo cuya referencia es 2.

Antes de crear pedidos debemos dar de alta los artículos que vayamos a usar en los pedidos.

Aunque tanto los artículos y los pedidos rellenan el campo creation_date con la fecha actual si no se indica el campo, también se puede indicar en la creación o modificar posteriormente.

## Descargar la aplicación
Mediante un cliente git hay que descargar la aplicación desde el repositorio

## Crear un esquema nuevo en MySQL/MariaDB
Esto se puede hacer mediante mySQL Workbench o mediante línea de comando. El nombre predeterminado para el esquema es "orders"
Debemos conocer los datos de la base de datos como son:
 - **Name**: Nombre de la base de datos. Por defecto, orders
 - **User**: Usuario con el que nos conectamos. Por defecto, root.
 - **Password**: Contraseña del usuario. Por defecto, root.
 - **Host**: Dirección IP del servidor de base de datos o localhost si es la misma máquina. Por defecto, localhost.
 - **Port**: Por defecto, 3306

Si los valores son diferentes a los valores por defecto deberemos ir al fichero settings.py y modificar la sección:
`
        DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.mysql",
           "NAME": "orders",
           "USER": "root",
           "PASSWORD": "root",        
           "HOST": "localhost",
           #"NAME": "db",
           "PORT": "3306",
       },
   }
`
## Ejecutar la aplicación en local
Para ejecutar la aplicación en local hay que realizar una serie de pasos:

 1. Nos vamos al directorio raiz donde hemos descargado la aplicación
 2. Actualizamos la base de datos con la información de la aplicación para ello ejecutamos:
`
    python manage.py makemigration api
    python manage.py migrate
`
 3. Creamos el usuario el super user que necesita Django
`
    python manage.py createsuperuser
`
 4. Arrancamos la aplicación
`
    python manage.py runserver
`
## Testear la aplicación en local
Si ya hemos hecho los tres primeros pasos de la sección "Ejecutar la aplicación en local", podemos arrancar los tests unitarios de la aplicación simplemente con:
`
    python manage.py test
`
Los tests dejan dos ficheros de logs en la carpeta api/logs donde podemos ver trazas de cada uno de los tests tanto de los artículos como de los pedidos. Estos ficheros solo contienen el resultado de la última prueba.

Para ejecutar los tests es necesario que la configuración de la base de datos sea para ejecutar en local y no con Docker por lo que en el fichero settings.py debemos comentar la linea que pone 'HOST': 'db' y descomentar la que pone 'HOST': 'localhost'

Si se quiere depurar los tests hay que hacer:
1. Importar pdb en el fichero para depurar
2. Donde se quiera empezar a depurar pondremos:
`
    pdb.set_trace()
`
3. Arrancaremos los tests con:
`
    python manage.py test --pdb
`
## Ejecutar la aplicación con Docker
Para ejecutar la aplicación con Docker debemos hacer lo siguiente:
1. En el fichero settings.py debemos comentar la linea que pone 'HOST': 'localhost' y descomentar la que pone 'HOST': 'db'
2. Crear la imagen docker con:
`
    docker build
`
3. Arrancar la imagen con:
`
    docker up
`
4. Para parar la imagen:
`
    docker down
`
## Colección Postman
Dentro de la carpeta del proyecto existe la carpeta postman donde encontramos una colección (apiDjango.postman_collection.json) para poder cargar en Postman y testear directamente el proyecto.
Antes de testear, deberemos arrancar la aplicación ya sea localmente o mediante Docker.
