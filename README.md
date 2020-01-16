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



