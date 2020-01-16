## Practica L3 Sistemas Distrbuidos 19/20

Grupo: SocaciuRuiz

## Integrantes:

1. IVAN RUIZ RUIZ
2. RAZVAN DAN SOCACIU

## Enlace del repositorio
https://github.com/rsoca/SocaciuRuiz/tree/entrega-3

## Manual de usuario
En el manual se indica el enunciado del problema y como resolverlo, además de un ejemplo de ejecución simple

### Enunciado

En la tercera fase el sistema se compondrá de un cliente, tres orchestrators, una factoría de downloaders y una factoría de transfers. El cliente tendrá que mandar un URL en forma de string a uno de los orchestrators que, a su vez, redirigirá la petición a un downloader creado a tal efecto siempre que el fichero de audio no haya sido descargado previamente en el sistema. El downloader descargará el archivo y notificará que se ha descargado correctamente en un canal de eventos para que todos los orchestrators sepan que el fichero existe, mandando la información de ese fichero. Al terminar se destruirá.

El cliente podrá solicitar la lista de ficheros descargados a uno de los orchestrators.

Además, el cliente también tendrá la opción de pedir la transferencia de un archivo de audio. Hará la petición a uno de los orchestrators que, a su vez, redirigirá la petición a un transfer creado a efecto siempre que el fichero de audio haya sido descargado previamente en el sistema. El transfer le mandará directamente al cliente el archivo. Al terminar se destruirá.
Los orchestrators se anunciarán al resto de orchestrators en su creación, que se anunciarán a su vez al nuevo orchestrator para actualizar las listas de orchestrators existentes de cada objeto. Además, un nuevo orchestrator ha de ser consciente de los ficheros de audio que ya han sido descargados en el sistema.

### Ejecución

**Parte del servidor**

1) Ejecutar el comando
```
make run
```
2) Ejecutar interfaz de ice
```
icegridgui
```

**Parte del cliente**

Ejecutamos el siguiente comando, que probará todas las peticiones disponibles al orchestrator.
```
./run_client.sh
```

### Componentes

**Parte del servidor**

1) transfer_factory.py
  * TransferI
  * TransferFactoryI
  * Server
  * __name__

2) downloader_factory.py
  * DownloadI
  * Server
  * NullLogger

3) orchestrator.py
  * OrchestratorEventI
  * FileUpdatesEventI
  * OrchestratorI
  * ManageOrchestrators
  * Server


**Parte del cliente**

1) client.py
  * Client



