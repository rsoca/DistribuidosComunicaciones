## Practica L3 Sistemas Distrbuidos 19/20

Grupo: SocaciuRuiz

## Integrantes:

1. IVAN RUIZ RUIZ
2. RAZVAN DAN SOCACIU

## Enlace del repositorio
https://github.com/rsoca/SocaciuRuiz/tree/entrega-3

## Manual de usuario
En el manual se indica el enunciado del problema y la ejecución de la solución a este.

### Enunciado

En la tercera fase el sistema se compondrá de un cliente, tres orchestrators, una factoría de downloaders y una factoría de transfers. El cliente tendrá que mandar un URL en forma de string a uno de los orchestrators que, a su vez, redirigirá la petición a un downloader creado a tal efecto siempre que el fichero de audio no haya sido descargado previamente en el sistema. El downloader descargará el archivo y notificará que se ha descargado correctamente en un canal de eventos para que todos los orchestrators sepan que el fichero existe, mandando la información de ese fichero. Al terminar se destruirá.

El cliente podrá solicitar la lista de ficheros descargados a uno de los orchestrators.

Además, el cliente también tendrá la opción de pedir la transferencia de un archivo de audio. Hará la petición a uno de los orchestrators que, a su vez, redirigirá la petición a un transfer creado a efecto siempre que el fichero de audio haya sido descargado previamente en el sistema. El transfer le mandará directamente al cliente el archivo. Al terminar se destruirá.
Los orchestrators se anunciarán al resto de orchestrators en su creación, que se anunciarán a su vez al nuevo orchestrator para actualizar las listas de orchestrators existentes de cada objeto. Además, un nuevo orchestrator ha de ser consciente de los ficheros de audio que ya han sido descargados en el sistema.

### Ejecución

Para la ejecución de la practica debemos realizar los siguientes pasos: 

** 1º - Ejecutar Makefile **

	Abrimos un terminal y nos dirigimos a nuestra carpeta que contiene el proyecto y procedemos a ejecutar el comando: 

```
make run
```

Con esto ejecutaremos los nodos. 

** 2º - Ejecutar interfaz **

	Abrimos otro terminal y nos volvemos a dirigir a la carpeta que contiene nuestro proyecto. 
A continuación, ejecutaremos la interfaz de Ice mediante el comando:

```
icegridgui
```

Y se nos abria el programa. 

** 3º - Apertura archivo YoutubeDownloaderApp.xml **

	Nos dirigiremos a la pestaña de arriba “File”, le daremos click, bajaremos hasta “Open” y seleccionaremos “Application from File”. Le daremos click y nos dirigiremos a la carpeta donde tendremos nuestro archivo “YoutubeDownloaderApp.xml”, lo seleccionaremos y le daremos a abrir. 

** 4º - Creación de la conexión ** 

Pasos a seguir son: 

* - Pulsaremos sobre el botón que tendremos a la izquierda arriba llamado “Los into an IceGrid Registry”.
* - Se nos abre una ventana, y a la derecha encontraremos una casilla que pone “New Connection” y le daremos click.
* - En la siguiente ventana seleccionaremos “Direct Connection” y pulsamos “Next” abajo.
* - En la siguiente ventana nos aparecerá marcada la casilla “Connect to a Master Registry”, la dejaremos seleccionada y pulsaremos “Next”.
* - En la siguiente ventana nos parecerá la conexion de nuestro equipo, simplemente pulsamos “Next”, y en la siguiente ventana seguimos pulsando “Next”.
* - Ahora nos aparece un ventana donde debemos introducir un usuario y una contraseña, donde podemos poner lo que queramos, en nuestro caso: Usuario: L3 , contraseña: L3. Y pulsamos “Finalizar”.

** 5º - Save Registry **

	Ahora, estando en la pestaña “YoutubeDownloaderApp” pulsaremos el botón “Save to Registry”. 

** 6º - Distribuir la aplicación **

	Una vez hemos llegado hasta aquí, nos situaremos sobre la pestaña “Live Deployment” y nos iremos a la pestaña “Tools” de arriba. Le damos click, después bajamos a “Application” y le daremos click a “Patch Distribution” se nos abrirá una ventana donde tenemos que seleccionar nuestra aplicación “YoutubeDownloaderApp”, pulsamos “Aceptar”. 

** 7º - Ejecución de los servicios de los nodos **

Para la ejecución de los nodos debemos seguir el siguiente orden: 

* 1º - IceStorm (YoutubeDownloaderApp.IceStorm)
* 2º - TransferFactory
* 3º - DownloaderFactory
* 4º - Los servidores orchestrator (OrchestratorAdapter, cada uno por separado)

La ejecución es tan simple como colocarnos encima del nodo, click derecho y Start.

** 8º - Ejecución del cliente **

	Una vez tengamos todos los pasos anteriores listos y funcionando, solo nos falta ejecutar el cliente. 

Para ello:

- Abrimos otra terminal y nos dirigimos a la carpeta de nuestro proyecto
- Ejecutamos la siguiente orden:

```
./client.py --Ice.Config=client.config "--download" "url_a_descargar" "orchestrator"
```

** 9º - Escuchar la canción **

	Para ello debemos tener instalado un reproductor de música, nosotros nos hemos decantado por Sox

Instalación de Sox:

```
sudo apt-get install sox
```

```
sudo apt-get install libsox-fmt-all
```

Nos dirigimos al lugar donde se encuentra las canciones descargadas

```
cd /tmp/db/downloads-node/distrib/YoutubeDownloaderApp/downloads/
```
Y ejecutamos el siguiente comando

```
play nombre_de_la_cancion
```

Para finalizar la reproducción antes de tiempo debemos pulsar Control+C
