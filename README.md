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
5. Configuración de servicios a utilizar en *AWS*
6. Elaboración de archivos my-detection3.py y Car2.py
7. Elaboración de función en servicio Lamnda para integración de servicios de *AWS*

  
## Intalación componentes *Hardware* complementarios a Jetson Nano

La primer fase del desarrollo se relaciona con la conexión de los componentes de *Hardware* auxiliares a la tarjeta Jetson Nano. Estos componentes son: 
- Tarjeta de red 
- Antenas 
- Ventilador

A continuación se detallan los pasos para conectar estos componentes en la tarjeta: 

### Conexión Tarjeta de Red ###

**PASO 1:** Desatornillar los dos tornillos en el disipador de calor y removerlo
<p align="center">
  <img width="503" alt="image" src="https://user-images.githubusercontent.com/109677535/180099511-08a7eb5d-701f-472e-992d-66f63a2da984.png">
</p>

**PASO 2:** Conectar el cable de extensión al Wireless-AC8265 en el conector IPEX, apretar la tuerta y la arandela a cada conector SMA
<p align="center">
  <img width="303" alt="image" src="https://user-images.githubusercontent.com/109677535/180099577-8f0b983a-7078-4092-b379-70dd27cb175d.png">
</p>

**PASO 3:** Desatornillar el tornillo NIC en el centro
<p align="center">
  <img width="173" alt="image" src="https://user-images.githubusercontent.com/109677535/180099920-f1a3ae12-adb9-4873-bcee-9a2ce77fce4f.png">
</p>

**PASO 4:** Insertar el Wireless-AC8265 en la cuenca M.2 y atornillar nuevamente el tornillo NIC
<p align="center">
  <img width="272" alt="image" src="https://user-images.githubusercontent.com/109677535/180100075-f5d31ea0-37ce-495d-9d68-cd517ea6181b.png">
</p>

**PASO 5:** Atornillar nuevamente el disipador de calor 
<p align="center">
  <img width="290" alt="image" src="https://user-images.githubusercontent.com/109677535/180100196-78b897bc-13c5-42ac-bf57-0a6a966939d7.png">
</p>

### Conexión Antenas

**PASO 1:** Conectar las antenas en el conector IPEX
<p align="center">
  <img width="217" alt="image" src="https://user-images.githubusercontent.com/109677535/180100475-b0b5dc10-6cd4-4942-b0be-077dfd59e71c.png">
</p>

### Conexión Ventilador

**PASO 1:** Conectar el ventilador a la tarjeta Jetson Nano en el puerto correspondiente
<p align="center">
  <img width="165" alt="image" src="https://user-images.githubusercontent.com/109677535/180100616-4c22c547-1fb1-40a9-b630-4804149d79fa.png">
</p>

**PASO 2:** Atornillar las cuatro esquinas del ventilador
<p align="center">
  <img width="272" alt="image" src="https://user-images.githubusercontent.com/109677535/180100865-b38e2f59-86d5-4a7f-92f6-59263e99431f.png">
</p>

## Configuraciones iniciales en Jetson Nano

Al finalizar las conexiones *Hardware* descritas anteriormente,en la segunda fase del desarrollo se monta el JetPack en la Jetson Nano y se realizan sus configuraciones iniciales. Las secciones que incluyen esta fase son:   
- Descarga de JetPack y configuración inicial Ubuntu
- Configuración ventilador
- Descarga y configuración contenedor dusty-nv/jetson-inference/
- Configuración Memoria Swap
- Instalación Visual Studio Code

### Descarga de JetPack y configuración inicial Ubuntu

**PASO 1:** De la página de NVIDIA se descarga la versión del JetPack compatible con la Jetson Nano; en este caso se descargó la versión 4.6.1. Para la descarga se utilizó el siguiente enlace -->[NVIDIA Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write-mac). 
Al terminar la descarga se obtiene el siguiente archivo:
<p align="center">
  <img width="368" alt="jetsonnanoiso" src="https://user-images.githubusercontent.com/31348574/179869364-78bbea81-dbd7-4b95-9b1b-d9c4a9934740.png">
</p>

**PASO 2:** Se descarga el *Software* Balena Etcher, este se utiliza para montar el JetPack en una tarjeta microSD con un mín de 32 GB. El *Software* se puede descargar desde [aquí](https://www.balena.io/etcher/)

Al abrir el programa se muestra el siguiente menu: 
<p align="center">
  <img width="364" alt="BalenaEtcher01" src="https://user-images.githubusercontent.com/31348574/179869885-593fe51c-c9ff-4df7-84a6-fc507eea93de.png">
</p>

**PASO 3:** Se selecciona la opción *"Flash from file"*, y se busca el archivo que se descargó en el paso 2 
<p align="center">
  <img width="354" alt="BalenaEtcher02" src="https://user-images.githubusercontent.com/31348574/179875686-45b95685-0236-4bd7-b279-ff8eea6704aa.png">
</p>

**PASO 4:** Se inserta la tarjeta microSD en la ranura de la computadora y se selecciona en el menú de Balena Etcher la opción *"Select Target"*. Se selecciona la tarjeta microSD y se hace click en *"Flash"* para montar el JetPack.
<p align="center">
  <img width="360" alt="BalenaEtcher04" src="https://user-images.githubusercontent.com/31348574/179871333-02dcaebd-4896-4bce-8ef4-283b8b4fc279.png">
</p>

**PASO 4.1** Si el paso 4 se esta realizando en *Windows* aparecerá un mensaje la siguiente notificación de la cual se selecciona "Cancelar"
<p align="center">
  <img width="269" alt="image" src="https://user-images.githubusercontent.com/109677535/180103119-ee4e4418-d951-49e2-ac3f-0b98678c2dda.png">
</p>

**Paso 5:** Se conecta la Jetson Nano a corriente con un cable de alimentación que entrega 5V y 4A, adicional se conecta un monitor por medio de *display port*, y un teclado y *mouse* a los puertos USB. Finalmente se inserta la tarjeta microSD al puerto corresepondiente. 
<p align="center">
  <img width="369" alt="image" src="https://user-images.githubusercontent.com/109677535/180103529-dd8c38f2-2707-493e-bfa3-d43b7da1db2f.png">
  <img width="212" alt="image" src="https://user-images.githubusercontent.com/109677535/180103762-816d991f-a51d-40d7-b96e-6ea5f5be6e36.png">
</p>

**PASO 6:** Al encender por primera vez la tarjeta Jetson Nano, el sistema operativo solicita la configuración inicial tipica de Ubuntu como la zona horaria, el usuario y la contraseña. El usuario establecido fue "tesis" 


### Configuración Ventilador

**PASO 1:** Instalar python3-dev en la tarjeta Jetson Nano

`apt install python3-dev`

**PASO 2:** Diriguirse al directorio Descargas

`cd Descargas`

**PASO 3:** Clonar el repositorio Pyrestone/jetson-fan-ctl-git para la instalación del control automático del ventilador

`git clone https://github.com/Pyrestone/jetson-fan-ctl.git`

**PASO 4:** Acceder a directorio jetson-fan-ctl

`cd jetson-fan-ctl`

**PASO 5:** Ejecutar archivo install.sh

`./install.sh`


### Descarga y configuración del contenedor dusty-nv/jetson-inference/

A continuación se realiza el *setup* del contenedor de Docker. 

**PASO 1:** Clonar el repositorio de GitHub [dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference)

`git clone --recursive https://github.com/dusty-nv/jetson-inference/`

**PASO 2:** Ingresar al directorio jetson-inference 

`cd jetson-inference/`

**PASO 3:** Iniciar el contenedor

`docker/run.sh`

**PASO 4:** Al correr por primera vez el archivo run.sh, se inicia la imagen del contenedor desde Docker Hub, y se solicita la instalación de modelos entrenados y Pytorch para Python3. Se presiona la barra espaciadora en la opción de "Aceptar" para la instalación de los modelos seleccionados por *default*

<p align="center">
  <img width="438" alt="image" src="https://user-images.githubusercontent.com/109677535/180108479-ac2bc354-ede5-409f-8c43-0366cc6456b5.png">
</p>

**PASO 5:** Salir del contenedor al finalizar la instalación de los modelos

`exit`

**PASO 6:** En el directorio *home* crear un archivo Dockerfile que importa toda la configuración del contenedor dusty-nv/jetson-inference/ y librerías adicionales para el sistema como se muestra a continuación:

```
FROM dustynv/jetson-inference:r32.7.1

ENV LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

RUN pip install AWSIoTPythonSDK
RUN pip3 install --upgrade pip
RUN apt-get update
RUN pip install matplotlib
RUN apt-get install -y python3-tk
RUN pip install sklearn
```

**PASO 7:** Se construye el contenedor nuevo en el mismo directorio donde se creó el Dockerfile mencionado en el paso 6

`sudo docker build-tag docker-jetson`

**PASO 8:** Cambiar a directorio jetson-inference

`cd jetson-inference/`

**PASO 9:** Para la creación del directorio para la configuración y almacenamiento de los archivos con el código. Se crea una carpeta en el directorio *home* con el nombre "my-detection3" 

`mkdir my-detection3`

**PASO 10:** Ingresar al directorio my-detection3 

`cd my-detection3`

**PASO 11:** Crear un archivo vacío denominado my-detection3.py que se modificará posteriormente 

`touch my-detection3.py`

**PASO 12:** Crear un archivo vacío denominado Car2.py que se modificará posteriormente 

`touch Car2.py`

**PASO 13:** Ingresar al directorio jetson-inference

`cd jetson-inference`

**PASO 14:** Correr y montar carpeta my-detection3 en el nuevo contenedor

`docker/run.sh -container docker-jetson:latest -volume~/my-detection3:/my-detection3`


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
