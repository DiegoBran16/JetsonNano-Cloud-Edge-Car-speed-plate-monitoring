# JetsonNano-Cloud-Edge-Car-speed-plate-monitoring  
### Universidad Rafaél Landívar 
### Ingeniería Electrónica y Telecomunicaciones
### Trabajo de Graduación

En el presente repositorio se encuentra el proceso de desarrollo de un sistema de monitoreo de rapidez y obtención de matrículas de automóviles, dicho proceso se detalla en forma secuencial. Adicional se incluyen los documentos durante el desarrollo y los enlaces a las herramientas necesarias para la elaboración del mismo.

De forma general el sistema detecta automóviles que se mueven en un área delimitada, al mismo se le realiza un seguimiento y se asigna un identificador, luego se obtiene la rapidez que posee en un punto específico, y se captura una imagen del automóvil, tanto el identificador, la rapidez y la imagen del automóvil son enviados a los servicios de *Amazon Web Services* en donde se abstrae de la imagen los valores de la matrícula y junto al identificador y la rapidez se almacenan en una base de datos. Si el automóvil supera un límite de rapidez establecido se notifica por correo electrónico al infractor. 
**** Agregar un video de como se van moviendo los vehículos y son detectados ****

Las fases para desarrollo del sistema son: 
1. Instalación componentes *Hardware* complementarios a Jetson Nano
2. Configuraciones iniciales en la Jetson Nano
3. Entrenamiento de una red neuronal convolucional profunda
4. Registro de Jetson Nano en *AWS*
5. Elaboración de Archivos Car.py y Tracker.py
6. Elaboración de función en servicio Lamnda para integración de servicios de *AWS*

## Intalación componentes *Hardware* complementarios a Jetson Nano

La primer fase del desarrollo se relaciona con la conexión de los componentes de *Hardware* auxiliares a la tarjeta Jetson Nano. Estos componentes son: 
- Tarjeta de red 
- Antenas 
- Ventilador

A continuación se detallan los pasos para conectar estos componentes en la tarjeta: 

### Conexión Tarjeta de Red ###

**PASO 1:** Desatornillar los dos tornillos en el disipador de calor y removerlo
**PASO 2:** Conectar el cable de extensión al Wireless-AC8265 en el conector IPEX, apretar la tuerta y la arandela a cada conector SMA
**PASO 3:** Desatornillar el tornillo NIC en el centro
**PASO 4:** Insertar el Wireless-AC8265 en la cuenca M.2 y atornillar nuevamente el tornillo NIC
**PASO 5:** Atornillar nuevamente el disipador de calor 

### Conexión Antenas

**PASO 1:** Conectar las antenas en el conectro IPEX

## Configuraciones iniciales en Jetson Nano

Al finalizar las conexiones *Hardware* descritas anteriormente, se monta el JetPack en la Jetson Nano y se realizan las configuraciones iniciales.   

**Paso 1**
De la pagina de NVIDIA debemos deescargar la versión del JetPack compatible con nuestra tarjeta.En este caso se descargó la versión 4.6.1. Para la Jetson Nano Developer kit se puede desvargar desde el siguiente enlce -->[NVIDIA Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write-mac). AL terminar la descarga observaremos el seguiente archivo:
<img width="868" alt="jetsonnanoiso" src="https://user-images.githubusercontent.com/31348574/179869364-78bbea81-dbd7-4b95-9b1b-d9c4a9934740.png">

**Paso 2** 
Se debe descargar el software balena etcher, este software nos ayudará a montar el JetPack en la tarjeta microSD. EL software se puede descargar desde [aquí](https://www.balena.io/etcher/)
Al abrir el programa veremos el siguiente menu: 
<img width="864" alt="BalenaEtcher01" src="https://user-images.githubusercontent.com/31348574/179869885-593fe51c-c9ff-4df7-84a6-fc507eea93de.png">


**Paso 3**

Seleccionamos la opcion "Flash from file" y buscaremos el archivo que descargamos en el paso 2 

<img width="854" alt="BalenaEtcher02" src="https://user-images.githubusercontent.com/31348574/179875686-45b95685-0236-4bd7-b279-ff8eea6704aa.png">

**Paso 4**


Introduciremos la tarjeta microSD en la ranura de la compuradora y selecionaremos en el menu de Balena Etcher la opción "Select Targer" y selecionaremos la tarjeta microSD. Seguidamente Hacemos click en "Falsh" para montar el JetPack e iniciará el proceso

<img width="853" alt="BalenaEtcher03" src="https://user-images.githubusercontent.com/31348574/179871249-01019f3f-d7f0-47f0-b518-769deea9aed6.png">
<img width="860" alt="BalenaEtcher04" src="https://user-images.githubusercontent.com/31348574/179871333-02dcaebd-4896-4bce-8ef4-283b8b4fc279.png">

**Paso 5**
Conectamos la Jetson Nano a corriente, conectamos el monitor por medio de display port, el teclado y mouse por usb. Al iniciar el sistema operativo nos solicitará la configuración inicial tipica de ubuntu como la zona horaria, el usuario y la contraseña. 

**insertar imagen de el sistema conectado**
**Insertar imagen del setup ubuntu**

## Configuración del Contenedor dusty-nv/Jetson-Inference
---

Al completar la instalación y configuración del JetPack, debemos iniciar el setup del contenedor de docker. 

**Paso 1**
Iniciamos con clonar el repositorio de github [dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference) para ello corremos el siguiente comando en la terminal de linux 

`git clone --recursive https://github.com/dusty-nv/jetson-inference/`


**Paso 2** 




## Aprovisionamiento de la VM en Azure para el entrenamiento de la red neuronal
Para el aprovisionamiento de la maquina virtual se debe poseer una cuenta de Azure con una suscripción activa, para el desarrolo de este sistema utilizamos la version de $200 de prueba.

**Paso 1** 
En el menu de Azure dentro de la categoria *Servicios de Azure* seleccionamos *Máquinas Virtuales*  y luego hacemos click en *crear*



<img width="1592" alt="Azure1" src="https://user-images.githubusercontent.com/31348574/179875265-b5ad0775-b38a-4e5f-a3fb-6325cfe43ebc.png">


<img width="1792" alt="Azure2" src="https://user-images.githubusercontent.com/31348574/179875280-72d9bad7-e9ce-48fd-b1aa-d5fee7cd427a.png">

**Paso 2** 





## Configuración de la VM en Azure para el entrenamiento. 
**Paso1**
Se inicio por conectarse por SSH a la maquina virtual por medio de la IP publica. Para ello se introdujo el siguiente comando en la maquina cliente

`ssh tesis@xxx.xxx.xxx.xxx` 


Las 'x'deben reemplazarse por la direccion IP publica de la VM


**Paso2** Por comodidad se optó por instalar una interfaz grafica, esta configuración se detalla desde este paso hasta el paso X. Para iniciar actualizamos los repositorios con el siguiente comando. 


`sudo apt-get update`

**Paso 3** Iniciamos la instalación de los componentes de la interfaz grafica ejecutando los siguientes comandos:

`sudo DEBIAN_FRONTEND=noninteractive apt-get -y install xfce4`

`sudo apt install xfce4-session`

**Paso 4** Configutamos los servicios RDP con los siguientes comandos 

`sudo apt-get -y install xrdp`

`sudo systemctl enable xrdp`

`echo xfce4-session >~/.xsession`

`sudo service xrdp restart`

Para ver el status del servicio ejecutamos el comando `sudo service xrdp status` y observaremos una salida como la siguiente: 

<img width="716" alt="Captura de Pantalla 2022-07-19 a la(s) 19 46 07" src="https://user-images.githubusercontent.com/31348574/179877917-f91e0ffd-4915-47de-86db-6d7595df43e5.png">
