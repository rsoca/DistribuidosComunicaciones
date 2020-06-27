## Practica Extraordinaria Sistemas Distrbuidos 19/20

Grupo: SocaciuRuiz

## Integrantes:

1. RAZVAN DAN SOCACIU
2. IVAN RUIZ RUIZ

## Enlace del repositorio
https://github.com/rsoca/SocaciuRuiz/tree/entrega-extra

## Manual de usuario

Para la ejecución de la practica debemos realizar los siguientes pasos: 

**1º - Apertura de terminales**

Para la correcta ejecucion de dicha practica lo que tendremos que haces es abrir 2 terminales y dirigirnos en cada una de ellas hacia la localizacion de la carpeta que contiene los archivos correspondientes a la practica.

**2º - Ejecución de los servidores en terminal 1**

En uno de los dos terminales que tenemos abiertos vamos a ejecutar 2 los servidores.
Ambas ejecuciones estan en el archivo run_server.sh. 

Por tanto, el comando correcto para ejecutar ambos servidores es:

```
./run_server.sh
```

En caso de que no nos deje ejecutarlo lo mas probable es que falten los permisos de ejecucion. Por tanto, para ello usaremos el siguiente comando:

```
chmod +x run_server.sh
```

Una vez realizado esto nos mostrara por pantalla los proxys de cada servidor, asi sabremos que el arranque ha sido el correcto. 

Otro fallo a controlar es que no tengamos la carpeta correspondiente para meter los archivos que se van a enviar, por tanto debemos crearla. 

La carpeta se debe llamar " files " y estar en el mismo lugar que los demas archivos. 


**3º - Ejecucion del cliente**

En la terminal numero dos lo que vamos a hacer es invocar el cliente mediante el comando de mas abajo. En el comando se puede apreciar como se indican entre comillas simples se indica el nombre del archivo que queremos recibir del servidor. Aqui debemos tener especial cuidado puesto que a veces el nombre puede llevar o no la extension del tipo de archivo, asi que debemos ver segun el sistema operativo si la extension del archivo se debe poner o no. 
Destacar que se pueden solicitar cuantos archios se quiera. 

```
./run_client.sh 'nombre_archivo1' 'nombre_archivo2' 
```

En caso de que no nos deje ejecutarlo debemos darle los permisos correspondientes de ejecucion con el siguiente comando:

```
chmod +x run_client.sh
```

Una vez el cliente ha sido ejecutado se puede ver en ambos terminales la secuencia que sigue el programa para los archivos solicitados. 

En caso de que unos de los archivos solicitados no se encuentre en la carpeta de "files" automaticamente el programa se parar y no habra envio de ningun archivo. 

Los archivos descargados se encontraran en la carpeta "downloads" que se creara automaticamente en nuestro repositorio donde esten los archivos. 

**4º - Finalizar la conexión** 

Para finalizar la conexion de forma correcta nos debemos dirigir a la terminal donde tenemos ejecutados los servidores y pulsar Control+C, con ello detendremos correctamente ambos servidores. 
En cuanto al cliente, se detiene solo al finalizar las conexiones. 

