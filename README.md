# JetsonNano-Cloud-Edge-Car-speed-plate-monitoring  
### Universidad Rafaél Landívar 
### Ingeniería Electrónica y Telecomunicaciones
### Trabajo de Graduación

En el presente repositorio se encuentra el proceso de desarrollo de un sistema de monitoreo de rapidez y obtención de matrículas de automóviles, dicho proceso se detalla en forma secuencial. Adicional se incluyen los documentos durante el desarrollo y los enlaces a las herramientas necesarias para la elaboración del mismo.

De forma general el sistema detecta automóviles que se mueven en un área delimitada, al mismo se le realiza un seguimiento y se asigna un identificador, luego se obtiene la rapidez que posee en un punto específico, y se captura una imagen del automóvil, tanto el identificador, la rapidez y la imagen del automóvil son enviados a los servicios de *Amazon Web Services* en donde se abstrae de la imagen los valores de la matrícula y junto al identificador y la rapidez se almacenan en una base de datos. Si el automóvil supera un límite de rapidez establecido se notifica por correo electrónico al infractor. 

https://user-images.githubusercontent.com/109677535/181665035-9422ff62-98dc-4065-982f-263fa0a75780.mp4

Las fases para desarrollo del sistema son: 
1. Instalación componentes *Hardware* complementarios a Jetson Nano
2. Configuraciones iniciales en la Jetson Nano
3. Entrenamiento de una red neuronal convolucional profunda
4. Registro de Jetson Nano en *AWS*
5. Configuración de servicios a utilizar en *AWS*
6. Elaboración de archivos Car2.py y my-detection3.py  
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

### Configuración memoria swap

**PASO 1:** En el directorio root@tesis:~# ejecutar el siguiente comando:

`sudo systemctl disable nvzramconfig`

**PASO 2:** Ejecutar el comando fallocate -l que permitirá manipular el espacio en disco SD

`sudo fallocate -l 4G /mnt/4GB.swap`

**PASO 3:** Correr el comando mkswap

`sudo mkswap /mnt/4GB.swap`

**PASO 4:** Correr el comando swapon

`sudo swapon /mnt/4GB.swap`

**PASO 5:** Ingresar al directorio root@tesis:/#

**PASO 6:** Descargar e instalar nano

`apt-get install nano`

**PASO 7:** Ingresara al directorio root@tesis:/etc# y modificar el archivo fstab

`nano fstab`
<p align="center">
  <img width="501" alt="image" src="https://user-images.githubusercontent.com/109677535/180253049-758fd669-c9da-4e27-85dc-1a1c40bbeb43.png">
</p>

**PASO 8:** Guardar los cambios del archivo 

### Instalación Visual Studio Code

Para la escritura y edición del código en Python se instaló Visual Studio Code con los siguientes pasos:

**PASO 1:** En el directorio tesis@tesis:~$ Descargar información actualizada de paquetes y actualizar dependencias 

`sudo apt-get update`

**PASO 2:** Dirigirse al directorio Descargas

`cd Descargas`

**PASO 3:** Descargar e instalar curl en el sistema, para descarga de archivos

`sudo apt-get install curl`

**PASO 4:** Descargar el archivo .deb con el comando curl -L

`curl -L tesis@tesis:~/Descargas$ curl -L https://github.com/toolboc/vscode/releases/download/1.32.3/code-oss_1.32.3-arm64.deb -o code-oss_1.32.3-arm64.deb`

**PASO 5:** Realizar la instalación del paquete .deb con el comando dpkg y la letra -i de install

`sudo dpkg -i code-oss_1.32.3-arm64.deb`

**PASO 6:** Abrir la aplicación Code OSS desde el buscador de aplicaciones en el escritorio

<p align="center">
  <img width="449" alt="image" src="https://user-images.githubusercontent.com/109677535/180257545-7c4c273f-2ee2-4a47-aa63-10b9a150490f.png">
</p>

## Entrenamiento de una red neuronal convolucional profunda

Para que el sistema cuente con la capacidad de detectar automóviles que se mueven a lo largo de un área delimitada, se implemento en la tajeta Jetson Nano una red neuronal convolucional, la cual fue re-entrenada en una máquina virtual del proveedor de la nube Azure. A continuación se enlistan las etapas:
- Aprovisionamiento de una máquina virtual en Azure
- Configuraciones e instalaciones en la máquina virtual
- Entrenamiento en la máquina virtual
- Creacción archivo onnx para traslado del modelo entrenado a Jetson Nano

### Aprovisionamiento de una máquina virtual en Azure 

Para el aprovisionamiento de la máquina virtual se necesita una cuenta de Azure con una suscripción activa, en el desarrollo del sistema se utilizó la versión de prueba que otorga $200.

**PASO 1:** En el menú de Azure dentro de la categoría "Servicios de Azure" se selecciona "Máquinas Virtuales"

<p align="center">
  <img width="592" alt="Azure1" src="https://user-images.githubusercontent.com/31348574/179875265-b5ad0775-b38a-4e5f-a3fb-6325cfe43ebc.png">
</p>

**PASO 2:** Dar click en "Crear"

<p align="center">
  <img width="592" alt="Azure2" src="https://user-images.githubusercontent.com/31348574/179875280-72d9bad7-e9ce-48fd-b1aa-d5fee7cd427a.png">
</p>

**PASO 3:** En la pestaña "Aspectos básicos", seleccionar la suscripción correcta y escribir el nombre para el grupo de recursos.

<p align="center">
  <img width="530" alt="image" src="https://user-images.githubusercontent.com/109677535/180265997-91682e62-06f7-4835-887c-81a88b25f6c9.png">
</p>

**PASO 4:** En la sección "Detalles de instancia" escribir el Nombre de la máquina virtual, la Región y Zona de disponibilidad.

<p align="center">
  <img width="532" alt="image" src="https://user-images.githubusercontent.com/109677535/180266927-5a640757-e8c1-4a9e-ae95-0549e6b58389.png">
</p>

**PASO 5:** Adicional en la sección "Detalles de instancia" seleccionar Tipo de seguridad, la Imagen, y el Tamaño.

<p align="center">
  <img width="533" alt="image" src="https://user-images.githubusercontent.com/109677535/180268097-227f7926-4f54-4f94-b869-4edaf971a6aa.png">
</p>

**PASO 6:** En la sección "Cuenta de administrador" se define el Tipo de autenticación, Nombre de usuario y Contraseña.

<p align="center">
  <img width="532" alt="image" src="https://user-images.githubusercontent.com/109677535/180269969-3f2657a6-25c8-4b0b-9f4c-2e866594ed96.png">
</p>

**PASO 7:** En la sección "Opciones de disco" seleccionar el tipo de disco del sistema operativo.

<p align="center">
  <img width="491" alt="image" src="https://user-images.githubusercontent.com/109677535/180271537-84d42340-d227-4899-a40f-f90835f04c8b.png">
</p>

**PASO 8:** Seleccionar el tamaño de disco.

<p align="center">
  <img width="524" alt="image" src="https://user-images.githubusercontent.com/109677535/180272009-7c00b161-d10b-458a-acde-b2a59f4393b4.png">
</p>

**PASO 9:** En la sección de "Crear un disco" se define el Nombre, Tipo de origen y Tamaño seleccionado en el paso 8.

<p align="center">
  <img width="443" alt="image" src="https://user-images.githubusercontent.com/109677535/180272323-8783a0d4-ed47-464e-b56b-ba3d6b1d787b.png">
</p>
<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/180272481-da316432-7d64-4988-8a91-05630e843e71.png">
</p>

**PASO 10:** En la sección de "Interfaz de red" se define la Red Virtual, Subred, e IP pública.

<p align="center">
  <img width="434" alt="image" src="https://user-images.githubusercontent.com/109677535/180272936-763bb5e4-86c2-4d45-a580-353b73349a21.png">
</p>

**PASO 11:** Finalmente Configurar el grupo de seguridad de red, y la seleccionar la Opción de equilibrio de carga.

<p align="center">
  <img width="506" alt="image" src="https://user-images.githubusercontent.com/109677535/180273442-c4494513-4246-498c-85c3-90fa3d1b839b.png">
</p>
<p align="center">
  <img width="506" alt="image" src="https://user-images.githubusercontent.com/109677535/180273528-1516c0fc-8bcd-48cd-96a2-35f13b9cea39.png">
</p>

### Configuraciones e instalaciones en la máquina virtual 

Durante la configuración de la máquina virtual se utilizó una máquina cliente con sistema operativo MacOS. Si se realizara en *Windows*, se recomienda utilizar [PuTTY](https://www.putty.org/)  

**PASO 1:** Se realizó una conexión por SSH a la máquina virtual por medio de la IP pública. Para ello se introdujo el siguiente comando en la máquina cliente:

`ssh tesis@xxx.xxx.xxx.xxx` 

Las 'x' deben reemplazarse por la dirección IP pública de la máquina virtual

**PASO 2:** Por comodidad se optó por instalar una interfaz gráfica para la máquina virtual, esta configuración se detalla a continuación. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.1:** Actualizar los repositorios. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo apt-get update`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.2** Instalar los componentes de la interfaz gráfica ejecutando los siguientes comandos:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo DEBIAN_FRONTEND=noninteractive apt-get -y install xfce4`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo apt install xfce4-session`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.3:** Configurar los servicios RDP con los siguientes comandos: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo apt-get -y install xrdp`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo systemctl enable xrdp`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`echo xfce4-session >~/.xsession`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sudo service xrdp restart`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para ver el estado del servicio se ejecuta el comando `sudo service xrdp status` y se observa una salida como la siguiente: 

<p align="center">
  <img width="516" alt="Captura de Pantalla 2022-07-19 a la(s) 19 46 07" src="https://user-images.githubusercontent.com/31348574/179877917-f91e0ffd-4915-47de-86db-6d7595df43e5.png">
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.4:** Por medio de la aplicación *Microsoft Remote Desktop* se accedió por RDP a la interfaz gráfica de la máquina virtual. 

<p align="center">
  <img width="388" alt="image" src="https://user-images.githubusercontent.com/109677535/180332795-3fe17d85-c7b6-4271-abb3-936f10057517.png">
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.5:** Se escribe la IP pública asignada por Azure, y en la sección *"User account"* se selecciona *"Add User Account"*

<p align="center">
  <img width="292" alt="image" src="https://user-images.githubusercontent.com/109677535/180332879-11575793-b32a-42de-8a7e-9c750a387d14.png">
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.6:** Se agrega el usuario de la máquina virtual, la contraseña y un identificador, luego dar click en *"Add"* para guardar la configuación del usuario

<p align="center">
  <img width="291" alt="image" src="https://user-images.githubusercontent.com/109677535/180332952-11653337-990d-423e-826b-185963c091d5.png">
  <img width="292" alt="image" src="https://user-images.githubusercontent.com/109677535/180332994-f4263019-70f8-4095-956a-40b5a3be4ec7.png">
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.7:** En la pestaña *"Display"* se selecciona la resolución de la pantalla y la calidad del color. Y dar click en *"Add"* 

<p align="center">
  <img width="297" alt="image" src="https://user-images.githubusercontent.com/109677535/180333036-0c71f74f-a719-4696-bb19-e7fa3bb71b78.png">
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**PASO 2.8:** Finalmente se puede ingresar a la máquina virtual al darle doble click.

<p align="center">
  <img width="290" alt="image" src="https://user-images.githubusercontent.com/109677535/180332721-8dad5685-a26e-49a8-8650-00708ca854eb.png">
</p>

**PASO 3:** Se creó una variable de entorno denominada tesisenv con los siguientes comandos:

`apt install python3.8-venv` 

`python3 -m venv tesisenv` 

`source tesisenv/bin/activate` 

<p align="center">
  <img width="263" alt="image" src="https://user-images.githubusercontent.com/109677535/180335980-99e90d05-8856-4a97-b9b0-bc5d2a60037d.png">
</p>

Dentro de la variable de entorno se realizan las instalación necesarias para el entrenamiento de la red neuronal.

**PASO 4:** Instalar Python 3.6 con los siguientes comandos:

`sudo add-apt-repository ppa:deadsnakes/ppa` 

`sudo apt-get install python3.6` 

`apt install python3-virtualenv` 

`virtualenv --python=/usr/bin/python3.6 /home/tesis/tesisenv/`

**PASO 5:** Clonar el repositorio jetson-inference

`git clone --recursive http://github.com/dusty-nv/jetson-inference/`

**PASO 6:** Ingrear al directorio `cd jetson-inference/python/training/detection/ssd`

**PASO 7:** Descargar la red Mobilenet V1 SSD que se utiliza como red base

`wget https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth -O models/mobilenet-v1-ssd-mp-0_675.pth`

**PASO 8:** Instalar los requerimientos del archivo requirements.txt

`pip3 install -v -r requirements.txt`

**PASO 9:** Instalar torch

`pip3 install torch`

**PASO 10:** Instalar torchvision

`pip3 install torchvision`

**PASO 11:** Instalar Open Cv

`pip3 install opencv-python`

**PASO 12:** Instalar Nvidia Cuda Toolkit 

`apt install nvidia-cuda-toolkit`

**PASO 13:** Instalar Nvidia Cuda Toolkit 

`apt install nvidia-cuda-toolkit`

**PASO 14:** Instalar Nvidia Cuda Toolkit 

`apt install nvidia-cuda-toolkit`

**PASO 15:** Instalar cvs 

`pip3 install cvs`

**PASO 16:** Instalar ONNX 

`pip3 install onnx`

**PASO 17:** Instalar boto3

`pip3 install boto3`

**PASO 18:** Montar el disco para el almacenamiento del set de datos que se descargará para el entrenamiento identificando la etiqueta del disco.

`lsblk -o NAME, HCTL, SIZE, MOUNTPOINT | grep -i "sd"`

**PASO 19:** Se formatea el disco.

`sudo parted /dev/sda --script mklabel gpt mkpart xfspart xfs 0% 100%`

**PASO 20:** Se monta el disco en la carpeta donde se almacena las imágenes del set de datos.

`sudo mount /dev/sda1 /home/tesis/jetson-inference/python/training/detection/ssd/data`

###  Entrenamiento en la máquina virtual

**PASO 1:** Descargar las imágenes utilizadas para el entrenamiento 

`python3 open_images_downloader.py --max-images=25000 --class-names "Car" --data=data/Cars`

**PASO 2:** Editar el archivo train.py para que escriba un csv con los valores de pérdida de entrenamiento y validación 

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180341824-6f591854-2552-4e85-b58c-05f1be08dbd6.png">
</p>

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180341889-5d0db410-bc0a-46f2-acf1-5496fb7c5115.png">
</p>

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180341950-bd87b514-0d02-4613-926e-c7cba860caf6.png">
</p>

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180342054-ca92cdb7-4188-48ae-85a6-c081530b16f1.png">
</p>

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180342179-fa63eea2-1418-4d39-abaa-7d3b1455af32.png">
</p>

<p align="center">
  <img width="400" alt="image" src="https://user-images.githubusercontent.com/109677535/180342265-7ab25e43-c62e-43bc-9e6e-409e94150051.png">
</p>

De las imágenes anteriores se estableció por *Default* la red Movilenet V1 SSD, se indica la ruta en dónde se almacena la red base, se importa la librería csv, y se incluye las modificaciones necesarias en el código para almacenar los valores de pérdida de entrenamieto y validación en formato csv.

**PASO 3:** Correr el archivo train_ssd.py indicando el *batch-size*, los *epochs*, el nombre de la carpeta donde se almacenaron las imágenes de la clase *Car* y el directorio en donde se almacenarán los *Checkpoints* del modelo. 

`python3 train_ssd.py --data=data/Car --model-dir=models/Car --batch-size=103 --epochs=60`

## Creacción archivo onnx para traslado del modelo entrenado a Jetson Nano

**PASO 1:** En el archivo onnx.py comentar la opción .cuda(), ya que la máquina virtual utilizada no cuenta con GPU NVIDIA. 

<p align="center">
  <img width="474" alt="image" src="https://user-images.githubusercontent.com/109677535/180343724-d27957f2-716f-4ce5-a79c-67147eef8a0e.png">
</p>

**PASO 2:** Utilizar el archivo onnx.py para convertir de formato Pythorch a ONNX. 

`python3 onnx_export.py --models-dir=models/Car`

**PASO 3:** Enviar por correo el archivo onnx, y el archivo labels para descargarlo en la Jetson Nano. 

## Registro de Jetson Nano en AWS 

Para otorgar acceso a los servicios de AWS se realizó el registro de la tarjeta Jetson Nano en IoT Core de AWS.


**PASO 1:**  Inicialmente se debe identificar la región con menor latencia para configurar los servicios. Para esto puede utilizarse la siguiente herramienta [Click aquí](https://ping.psa.fun/)
<p align="center">
  <img width="334" alt="Captura de Pantalla 2022-07-22 a la(s) 16 46 33" src="https://user-images.githubusercontent.com/31348574/180577780-eb2557eb-102c-46dd-b203-d4993e8ac172.png">
  <img width="327" alt="Captura de Pantalla 2022-07-22 a la(s) 16 45 47" src="https://user-images.githubusercontent.com/31348574/180577753-0ec29c41-637b-4cee-8ce5-846826213f96.png">
<p/>
En nuestro caso la región con menor latencia fue US East(Ohio)

**PASO 2:** Ingresar a la consola de Administración de AWS y buscar el servicio IoT Core 
<p align="center">
  <img width="500" alt="Captura de Pantalla 2022-07-22 a la(s) 17 05 18" src="https://user-images.githubusercontent.com/31348574/180578995-aeebd836-86a4-4c37-a4c6-ad2c004cf059.png">
<p/>


**PASO 3:** Expandir la sección *"Manage"* , dirigirse a *"Things"* y hacer click en *"Create Things"*
<p align="center">
  <img width="545" alt="Captura de Pantalla 2022-07-22 a la(s) 17 07 56" src="https://user-images.githubusercontent.com/31348574/180579177-d61458ed-3f90-4342-92ad-eadae6483b7a.png">
<p/>


**PASO 4:**  En la siguiente ventana se seleciona el número de cosas a crear y hacer click en *"next"*
<p align="center">
  <img width="507" alt="Captura de Pantalla 2022-07-22 a la(s) 17 11 06" src="https://user-images.githubusercontent.com/31348574/180579375-87e847d8-46d0-4563-a4fc-3bc78f89241e.png">
<p/>

**PASO 5:** Posteriormente tras definir un nombre al objeto que en este caso se tomo como "JetsonNano-S1-1" se debe de crear un *"thing type, thing group y un billing group"* para identificar el recurso. Como se observa en la imagen.

<p align="center">
  <img width="512" alt="Captura de Pantalla 2022-07-22 a la(s) 17 16 02" src="https://user-images.githubusercontent.com/31348574/180579622-cccd2e60-c1f3-40cc-b144-cb9dc9801798.png">
<p/>
  
 **PASO 6:**  En la sección *"Device Shadow"* se selecciona la opción *"No shadow"* y selecciona *"Next"*
<p align="center"> 
  <img width="511" alt="Captura de Pantalla 2022-07-22 a la(s) 17 22 53" src="https://user-images.githubusercontent.com/31348574/180580034-c00f527d-1c82-448a-bb25-881f8860ec1f.png">
<p/>

 **PASO 7:** En la sección *"Configure device certificate-optional"* se selecciona *"Auto-generate a new certificate (recommended)"* y seleccionar *"Next"*
<p align="center">
  <img width="514" alt="Captura de Pantalla 2022-07-22 a la(s) 17 29 21" src="https://user-images.githubusercontent.com/31348574/180580380-445a87ec-eeff-4a91-acf0-027d25378c29.png">
<p/>

**PASO 8:**  En la sección _"Attach policies to certificate-optional"_ se selecciona _"Create a policy"_ y se escribe la siguiente política 
<p align="center">
  <img width="514" alt="Captura de Pantalla 2022-07-22 a la(s) 17 32 25" src="https://user-images.githubusercontent.com/31348574/180580551-798b91cf-82f8-44ae-b306-9702e57ca72f.png">
<p/>

<p align="center">
  <img width="502" alt="Captura de Pantalla 2022-07-22 a la(s) 17 35 31" src="https://user-images.githubusercontent.com/31348574/180580694-f3c37e72-b373-45dc-91d6-0d5d6b3c957e.png">
<p/>


**PASO 9:** Se selecciona la política creada en el paso 8 y se selecciona _"Create thing"_
<p align="center">
  <img width="595" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180580959-19f38626-dc68-4576-9f9a-4a4bc98bc87d.png">
<p/>

**PASO 10:** Seguidamente se mostrarán los certificados y llaves del objeto, además del certificado raíz de la entidad certificadora de AWS. Deben de descargarse el certificado del dispositivo, el certificado Amazon Root CA 1 y las llaves pública y privada y dar click en done 

<p align="center">
  <img width="515" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180581247-311fb404-167c-4c1c-854d-5720f38eeaf2.png">
<p/>

**PASO 11:** Dirigirse a la sección _"Secure"_, luego en la opción _"Certificates"_  hacer click en el certificado y en _"Policies"_ se selecciona la opción _"Attach policies"_ y se selecciona la política. 

<p align="center">
  <img width="523" alt="Captura de Pantalla 2022-07-22 a la(s) 17 58 50" src="https://user-images.githubusercontent.com/31348574/180581805-1f8c4c07-84d1-413f-81d4-e41ceea57c7c.png">
<p/>


**PASO 12:** Dirigirse a la opción _"setting"s_ al final del menú lateral y guardar el  _"Endpoint"_ del servicio. Este debe ser indicado en el código que se realizará en la tarjeta.

<p align="center">
  <img width="525" alt="Captura de Pantalla 2022-07-22 a la(s) 18 23 53" src="https://user-images.githubusercontent.com/31348574/180582916-81774c41-e9c3-44c6-9895-c1f361120fb0.png">
<p/>



**PASO 13**  Posicionarse en la opción _"Things"_ que se encuentra dento de la sección _"All Devices"_ de la sección _"Manage"_ y seleccionar el objeto que se creó anteriormente 
<p align="center">
 <img width="469" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181401678-817eb37d-e863-442a-b426-922fe3fa441d.png">
<p/>

**PASO 14** Dirigirse a la sección _"Device Shadows"_ y seleccionar _"Create Shadow"_
<p align="center">
  <img width="749" alt="Screen Shot 2022-07-27 at 19 33 02" src="https://user-images.githubusercontent.com/31348574/181401153-4f7808f9-23aa-4940-a2d9-9b353070e1cf.png">
<p/>

**PASO 15** Seleccionar la opción _"Named Shadow"_, colocar un identificador para el tema MQTT y hacer click en_"Create"_, posteriormente se observara el prefijo del tema.

<p align="center">  
 
  <img width="623" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181402395-5cc8d999-3e34-4894-be8d-776576026c34.png">
  
  <img width="659" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181402815-a34956e3-13a6-41ef-a0f0-ae706ecc156e.png">  
<p/>


## Configuración de servicios en AWS

Los servicios configurados a continuación son los siguientes: 

- IAM
- S3
- DynamoDB
- Lambda
- Elaboración de Politicas y roles

### Configuración de IAM 

Este servico se utilizará para crear un grupo el cual poseerá permisos para colocar objetos en un bucket de S3 y se asignará un usuario, el cual se colocará en el código de la Jetson Nano.  


**PASO 1:** En el servicio IAM colocarse en _"User Groups"_, y hacer click en _"Create group"_ y se selecciona _"Create Group"_

<p align="center">
  <img width="606" alt="Screen Shot 2022-07-25 at 19 28 23" src="https://user-images.githubusercontent.com/31348574/180902888-31f572cb-aaa7-4450-8ab5-9540f420ca9c.png">
<p/>

**ACLARACIÓN:** De momento no se creará ninguna política, pues es neceario el ARN de S3.

**PASO 2:** En la sección _"Users"_ seleccionar _"Add Users"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 19 45 14" src="https://user-images.githubusercontent.com/31348574/180904602-a2a15998-2086-4275-af9e-d876a5e0180b.png">
<p/>


**PASO 3:** Se define un nombre de usuario y se marca el _checkbox_ _"Access Key-Programmatic Access"_ ya que se colocara en el codígo de la Jetson Nano y hacer click en _"Next:Permissions"_ 

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 19 47 59" src="https://user-images.githubusercontent.com/31348574/180904898-d90ba4e4-70a4-4258-9f80-f1ae6198a716.png">
<p/>


**PASO 4:** En _"Set permissions"_ seleccionamos _"Add user to group"_, seleccionar el grupo que se creó en el paso 3 y hacer click en _"Next"_ 

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 19 46 21" src="https://user-images.githubusercontent.com/31348574/180905978-6aae15be-f227-4299-a7d7-afad40f8f9f6.png">
<p/>

**PASO 5:** En  _"Add tags"_ seleccionamos _"Next:Review"_ 

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 19 54 48" src="https://user-images.githubusercontent.com/31348574/180905639-dde520db-695f-45f3-8ede-5f9d6e48c508.png">
<p/>

**PASO 6:** A continuación se mostrará un resumen y se debe hacer click en "Create User", posteriormente saldrá un mensaje de éxito y los detalles del usuario. En este momento se debe descargar el .CSV ya que es el único momento en el cual se pueden descargar las llaves de acceso, después de esta pantalla no es posible observar la llave de acceso privada. Después de descargar el .CSV hacer click en _"Close"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 20 05 49" src="https://user-images.githubusercontent.com/31348574/180906947-c60ad235-a72b-4d13-b83f-1ff9f3ac8cb3.png">
<p/>


### Configuración del Bucket de S3 

**PASO 1:** Dirigirse a el servicio Amazon Simple Storage Service (S3), en la sección _"Buckets"_ seleccionar la opción _"Create Bucket"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 20 10 52" src="https://user-images.githubusercontent.com/31348574/180907730-39a2f2ea-7e9a-44ee-ae2e-995e6fcb6183.png">
<p/>

**PASO 2:** Se coloca un identificador para el _"Bucket"_, la región en la que se creará el _"Bucket"_ y en _"Obejcts Ownership"_ marcar _"ACLs disabled (recomended)"_. 

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 20 14 47" src="https://user-images.githubusercontent.com/31348574/180908414-9d95c150-f435-4157-8459-326bc2562af2.png">
<p/>

**PASO 3:** Seleccionar _"Block all public access"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 20 20 54" src="https://user-images.githubusercontent.com/31348574/180908673-ede6d3d9-e601-4a48-b1cf-8191067bca50.png">
<p/>
  
**PASO 4:** En _"Bucket Versioning"_ y _"Default Encryption"_ se dejan los valores predeterminados y se da click en _"Create bucket"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-25 at 20 21 37" src="https://user-images.githubusercontent.com/31348574/180908749-0de7d9f3-e9fa-4d94-84eb-5bb0cf0ef02e.png">
<p/>

### Configuración de Dynamo DB

En la elaboración de este proyecto se configuraron dos tablas. Estas se describen a continuación:

- Detected_Cars_DB: En esta tabla se almacena el registro de automóviles. Incluye los campos _ID_, _timestamp_, _imageName_, _Multa_, _Plate_ y _speed_
- CarOwners: En esta tabla se almacenan los datos de los usuarios que poseen veiculos. Se incluyen los campos _Matricula_, _DriversLicence_, _Email_, _FirstName_, _FirstSurname_, _SecondName_ y _SecondSurname_


#### Configuración de la tabla _Detected_Cars_DB_ 

**PASO 1:** Dirigirse a el servicio _DynamoDB_ en la consola de _AWS_, ubicarse en _"Tables"_ y hacer click en _"Create Table"_

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181392018-db5d3b47-973f-4ddd-ba6f-88e2a9338e6a.png">
<p/>

**PASO 2:** Se colocá un nombre en la tabla, el parámetro para las llaves de partición y de ordenamiento y por último se debe hacer click en _"Create Table"_

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181392693-81388abf-5b36-421c-ae57-ee19393e4d80.png">
<p/>

#### Configuración de la tabla _CarOwners_

**PASO 1:** Dirigirse a el servicio _DynamoDB_ en la consola de _AWS_, ubicarse en _"Tables"_ y hacer click en _"Create Table"_ 
 
<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181392018-db5d3b47-973f-4ddd-ba6f-88e2a9338e6a.png">
<p/>
  
**PASO 2:** Se colocá un nombre en la tabla, el parámetro para la llave de partición (Para esta tabla no es necesario crear una llave de ordenamiento) y por último se debe hacer click en _"Create Table"_

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181393787-ebb50625-50d2-4502-9eb4-7796b10bc68a.png">
<p/>

#### Configuración de la función lambda

**PASO 1:** Dirigirse al servicio _"AWS Lambda"_, ubicarse en _"Functions"_ y hacer click en _"Create Function"_

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181394607-69398263-7179-4e32-bc51-20d51b69bec6.png">
<p/>

**PASO 2:** Se seleciona la opción _"Author from scratch"_ para crear la función con un pequeño código de ejemplo, seguidamente se coloca el nombre identificador de la función. En _"Runtime"_ se selecciona el lenguaje en el que se programará la función, en este caso fue Python3.9. En _"Architecture"_ se debe marcar la arquitectura de base para la ejecución de la función. En este caso se marcó la opción x86_64. En _"Execution role"_ se inidca el rol de ejecución de la función en caso de ya poseer una política creada, en caso de no poseerla se puede crear una política nueva o crear la función con una política básica. En este caso se marcó la opción _"Create a new role with basic Lambda permissions"_. Por último se debe hacer click en _"Create Function"_

<p align="center">
 <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181396183-70c36825-fe80-4303-89da-612761ab5b3d.png">
<p/>

**PASO 3:** Se debe de hacer click en el nombre de la función y posteriormente seleccionar la opción _"Add Triger"_ 

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181397483-e9d1e647-7cdc-4270-9fbc-0b93c74638eb.png">
<p/>

  
**PASO 4:** En _"Trigger configuration"_ debemos seleccionar IoT Core como fuente del desencadenador. 

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181399807-4aff76ec-36c6-4584-bf0f-bd4aeb3023e1.png">
<p/>


**PASO 5:**  En _"IoT type"_ se selecciona _"Custom IoT rule"_, en _"Rule"_ se marca la opción _"Create a new rule"_, se coloca el nombre de la regla, la descripción y en _"Rule query statement"_ se debe declarar que en cada publicación en el tema creado se invoque a la función. 

<p align="center">
  <img width="500" alt="imagen" src="https://user-images.githubusercontent.com/31348574/181399876-cc9a248a-8cde-4691-8570-f6941073367b.png">
<p/>


### Elaboración de Politicas y Roles 

Se crearon las políticas para cada uno de los servicios asignando únicamente los permisos necesarios para la interacción entre estos. 

Se crearón las siguientes politicas y roles:
- Política del grupo JetsonNano-car-traffic-accounts
- Política del Bucket de S3
- Rol de Lambda 

#### Política del grupo JetsonNano-car-traffic-accounts
**PASO 1:** Dirigirse al servicio IAM, ubicarse en _"Groups"_ y selecconar el grupo creado anteriormente

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 08 19 09" src="https://user-images.githubusercontent.com/31348574/181780867-67a80bda-1dd6-4b3e-9f8b-cb35ccba0f3a.png">
<p/>

**PASO 2:**  Ubicarse en la pestaña _"Permissions"_, desplegar las opciónes disponibles de _"Attach Permissions"_ y seleccionar la opción _"Attach policies"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 08 41 01" src="https://user-images.githubusercontent.com/31348574/181784737-84ed4414-1092-47ca-b25f-0943780059c7.png">
<p/>

**PASO 3:** Seguidamente hacer click sobre "Create Policy" y se abriara una nueva ventana.

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 08 41 22" src="https://user-images.githubusercontent.com/31348574/181785139-e8ed480a-3d92-458a-a888-302bb0b20c8d.png">
<p/>

**PASO 4:** Seleccionar la pestaña _"JSON"_, escribir la siguiente política y hacer click en _"Next:Tags"_. 

Esta política otorga los permisos necesarios para colocar objetos en el bucket. Esto permite que el usuario utilizado en el codigo de borde coloque las imagenes de los automoviles en el bucket. 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::carimages-trafic-jetson-nano-4gb"
        }
    ]
}


```

**PASO 5:** En _"Add Tags"_ hacer click en _"Next:Review"_
<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 09 02 26" src="https://user-images.githubusercontent.com/31348574/181788567-6528db45-17ac-4beb-ac8d-38a430cb8289.png">
<p/>

**PASO 6:** Colocar un nombre para la política y hacer click en "Create Policy"

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 09 02 47" src="https://user-images.githubusercontent.com/31348574/181789283-8c266762-ba86-4cab-9211-c01d6396ad43.png">
<p/>

**PASO 7:** Regresar a la pestaña de _"Attach permission policies to JetsonNano-car-traffic-accounts"_, seleccionar la política creada y hacer click en "Add Permissions"


<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 09 11 12" src="https://user-images.githubusercontent.com/31348574/181790388-46011d26-dac1-4c7d-9a9c-199b7467b20e.png">
<p/>

**PASO 8:** Posteriormente se observará la política asignada en el grupo.
<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 09 13 22" src="https://user-images.githubusercontent.com/31348574/181790649-8943e428-2432-4c85-8333-c7e773767732.png">

<p/>

#### Política del Bucket de S3 
**PASO 1:** Dirigirse al servicio S3 y en la sección _"Buckets"_ hacer click sobre el bucket que se creó anteriormente

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 08 03 29" src="https://user-images.githubusercontent.com/31348574/181777503-7111d6c7-14d2-4640-9714-6fde2eabb177.png">
<p/>

**PASO 2:** Ubicarse en la pestaña _"Permissions"_, dirigirse a _"Bucket Policy"_ hacer click en edit

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-29 at 08 02 51" src="https://user-images.githubusercontent.com/31348574/181778062-e4dcf1d1-20fd-4302-aba3-2103eebc9012.png">
<p/>

**PASO 3:** Se escribe la siguiente politica en el espació correspondiente y se hace click en "Save Changes"

```json

{
    "Version": "2012-10-17",
    "Id": "JetsonBucketPolicy",
    "Statement": [
        {
            "Sid": "JetsonBucketPolicyAllowPutObject",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::556216965853:user/JetsonNano-car-traffic-user-1"
            },
            "Action": [
                "s3:ListBucket",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::carimages-traffic-jetson-nano-4gb/*",
                "arn:aws:s3:::carimages-traffic-jetson-nano-4gb"
            ]
        },
        {
            "Sid": "LamndaAccessForS3",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::556216965853:role/service-role/MQTT-S3getCar-Recognition-Dynamodb-role-12j28le3"
            },
            "Action": "s3:GetObject",
            "Resource": [
                "arn:aws:s3:::carimages-traffic-jetson-nano-4gb/*",
                "arn:aws:s3:::carimages-traffic-jetson-nano-4gb"
            ]
        }
    ]
}

```




#### Rol de lambda

**PASO 1:** Dirigirse a la función lambda creada anteriormente y hacer click en el nombre de la función

<p align="center">
 <img width="500" alt="Screen Shot 2022-07-28 at 18 15 22" src="https://user-images.githubusercontent.com/31348574/181657690-117858ed-ee29-454a-a950-71ac31ab0f5b.png">
<p/>

**PASO 2:** Posteriormente colocarse en la pestaña _"configuration"_, dirigirse a _"Permissions"_ y hacer click en la politica predeterminada 

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-28 at 18 17 15" src="https://user-images.githubusercontent.com/31348574/181685772-fd4397c1-46af-43c3-9d52-b61d0155e072.png">
<p/>

**PASO 3:** Se abrirá la configuración del rol y se debe hacer click en _"Add Permissions"_ y posteriormente en _"Create inline policy"_

<p align="center">
  <img width="500" alt="Screen Shot 2022-07-28 at 23 11 40" src="https://user-images.githubusercontent.com/31348574/181687253-03a19462-1712-471c-9ae2-d28b48e6862d.png">

<p/>


**PASO 4:** Hacer click en _"JSON"_
<p align="center">
  <img width="500" alt="Screen Shot 2022-07-28 at 18 59 53" src="https://user-images.githubusercontent.com/31348574/181661273-7abc2744-ddb9-44a2-ae3c-6c2a7226860f.png">
<p/>


**PASO 5 :** En la política del rol se deben colocar los permisos necesarios para que la función pueda apoyarse de los serviciós _Rekognition, DynamoDB, y S3_. Se autorizarón todas las acciones para el servicio _Rekognition_, permisos para leer y escribir en la tabla _"Detected_Cars_DB"_, permisos de lectura en la tabla _"CarOwners"_ y permisos para colocar y recuperar objetos del _bucket_ de S3

```json 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-2:556216965853:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-2:556216965853:log-group:/aws/lambda/MQTT-S3getCar-Recognition-Dynamodb:*"
            ]
        },
        {
            "Sid": "ListAndDescribe",
            "Effect": "Allow",
            "Action": [
                "dynamodb:List*",
                "dynamodb:DescribeReservedCapacity*",
                "dynamodb:DescribeLimits",
                "dynamodb:DescribeTimeToLive"
            ],
            "Resource": "arn:aws:dynamodb:us-east-2:556216965853:table/Detected-Cars-DB"
        },
        {
            "Sid": "SpecificTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Update*",
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-2:556216965853:table/Detected-Cars-DB"
        },
        {
            "Sid": "SpecificTableRead",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*"
            ],
            "Resource": "arn:aws:dynamodb:us-east-2:556216965853:table/CarOwners"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "arn:aws:s3:::carimages-traffic-jetson-nano-4gb"
        }
    ]
} 

```



**PASO 6:** Colocar un nombre de identificación para la política y hacer click en _"Create Policy"_, posteriormente se obserbará la política creada en el rol. 
<p align="center">
  <img width="500" alt="Screen Shot 2022-07-28 at 23 05 05" src="https://user-images.githubusercontent.com/31348574/181686794-678503a7-4e59-49b3-bae8-f8597d42813f.png">
  <img width="500" alt="Screen Shot 2022-07-28 at 23 07 25" src="https://user-images.githubusercontent.com/31348574/181686956-6df22fc7-106d-4a95-8ea3-e356d666cd0c.png">
<p/>



## Elaboración de archivos Car2.py y my-detection3.py

### Car2.py

Durante el desarrollo del sistema fue necesario la elaboración del archivo Car2.py, que permite el seguimiento e identificación de los automóviles que fuesen detectados por la red neuronal convolucional profunda re-entrenada. Dicho archivo contiene las clases Auto y Tracker cuyos diagramas se muestran a continuación:

<p align="center">
  <img width="350" alt="image" src="https://user-images.githubusercontent.com/109677535/180842453-84ee36f9-d071-422b-a6e5-35d05e33fc28.png">
  <img width="350" alt="image" src="https://user-images.githubusercontent.com/109677535/180844900-26415fb7-c58c-4901-b6d1-f0be652ffa55.png">
<p/>

En la clase Tracker la función *"tracking"* recibe una lista que contiene los valores x1, y1, x2, y2; estos corresponden a las coordenadas de la detección que devuelve el modelo ya re-entrenado. Con estos valores se calculan las coordenadas del centro del rectángulo de detección aplicando la ecuación del punto medio. 

<p align="center">
  <img width="303" alt="image" src="https://user-images.githubusercontent.com/109677535/180845359-ac8bf047-a80e-424b-b6ea-7b9a1bd64139.png">
<p/>

A continuación se identifica si el automóvil en el *frame* actual ya se ha detectado anteriormente. Para ello es necesario evaluar con un *if* si la distancia euclidianda entre los centros de la detección anterior y la detección actual es mayor a 100 px y si la diferencia de los centros en la coordenada "y" del automóvil detectado actualmente y el automóvil detectado con anteriorirdad es menor a 1/2 de la distancia euclidiana de las esquinas del recuadro que encierra la detección.

**Si se cumple** la condición se utiliza una variable llamada "validador" a la que se le asigna el valor *True*, lo cual indica que este ya había sido detectado anteriormente, y por lo tanto se agrega la nueva información de este automóvil utilizando las funciones de la clase Auto: "agreagar_info" para almacenar los nuevos valores de coordenadas de x1,y1,x2,y2 y sus centros; "set_centroides" para agregar los nuevos valores de las coordenadas de centros, adicional en esta función se guarda el tiempo de esta detección en el arreglo "tiempo"; y en la clase Tracker se agregan al diccionario "centorides" los nuevos valores de centros.

Cuando **No se cumple** la condición, y la variable "validador" se mantiene con su valor original *False* y la esquina inferior derecha del recuadro de detección (y2) es menor a 300 px, quiere decir que el automóvil detectado en el *frame* actual es una detección nueva. Por lo tanto es necesario crear un nuevo objeto Auto, al que con las funciones de la clase Auto: "asignar_id" se asigna el identificador correspondiente, "agregar_info" almacena los primeros valores de las coordenadas de los centros y x1, y1, x2, y2;  y en la clase Tracker se agrega al diccionario "centorides" los valores de los centros y en el diccionario "autos_detectados" se agrega el Auto que se detectó. Finalmente a la variable "car_id" correspondiente a la identificación del automóvil, se le incrementa a su valor uno, para que la siguiente detección siga la secuencia apropiada. 

Dicho proceso se describe gráficamente a continuación:

<p align="center">
  <img width="726" alt="image" src="https://user-images.githubusercontent.com/109677535/180866487-8ef1add4-51f3-482e-9baf-113d43c9bebe.png">
<p/>

### my-detection3.py

Para que la tarjeta Jetson Nano realice la lectura de un video, detecte los automóviles que se mueven en el mismo, obtenga la rapidez aproximada del automóvil y envíe una imagen, su identificador y la rapidez del mismo a los servicios de AWS, son necesarias las funciones dentro del archivo my-detection3.py. Es importante resaltar que al archivo se le importa Car2.py para acceder a sus clases además de importar también distintas librerías que apoyan en el desarrollo del sistema.

Inicialmente es necesario declarar las variables globales utilizadas a lo largo del código, estas incluyen los valores obtenidos del registro de la Jetson Nano en el servicio IoT Core: *"ENPOINT"*, *"CLIENT_ID"*, *"PATH_TO_CERTIFICATE"*, *"PATH_TO PRIVATE_KEY"*, *"PATH_TO_AMAZON_ROOT_CA_1"* y *"TOPIC"*; y los valores de las llaves obtenidas en la configuración del servicio S3: *"ACCESS_KEY_ID"* Y *"SECRET_ACCESS_KEY"*.

Adicional se define la variable que contendrá el modelo "Car2.onnx", es decir el modelo Mobilenet SSD v1 ya re-entrenado en la máquina virtual de Azure, la misma se nombra como "net", y el video que será analizado "cap". Finalmente dos variables auxiliares del proceso del sistema: "sended_id" y "contador_out" 

Dentro del archivo, se utiliza un *while* que realiza la lectura de una grabación en la que transitan seis automóviles. Inicialmente los *frames* del video son redimensionados, luego se selecciona un área que contendrá solamente la carretera donde transitan los automóviles de la grabación y a la misma se le aplica un filtro con la función *bitwise_and* de la librería OpenCv. A esta sección de carretera filtrada se le denomina como **zona** y es esta la cual es ingresada a la red neuronal *"net"*, esta devuelve las esquinas del recuadro que encierran la detección de un automóvil, las cuales como se mencionó con anterioridad son x1, y1, x2, y2, estos valores son guardados en una lista denominada "detect". 

Luego se crea un objeto Tracker al cual a su función tracking se le envía la lista "detect", la misma retorna el diccionario autos_detectados y este se asigna a la variable "info_id".

A continuación tras obtener el largo del diccionario "info_id" y la lista "detect", se realiza una validación con un *if* en el cual si el largo de la lista "detect" es **menor** a la de "info_id" se obtiene la diferencia de largo entre "info_id" y "detect", y si esta diferencia es mayor a cero se infiere que alguno de los automóviles detectados por "net" ya se encuentra fuera de la zona de análisis de la grabación y por lo tanto se utilizan como apoyo la lista "sended_id" que contiene los identificadores de los automóviles cuyos centros en la coordenada "y" se encuentran entre 310 y 330 px y "contador_out" que se utiliza como índice para ubicarse en la posición del ítem de la lista "sended_id" que se encuentra fuera de la zona de interés.

A continuación se obtiene el identificador, los centros y las coordenadas del recuadro de detección del automóvil dentro el diccionario "info_id" que será eliminado, este se eliminará si la esquina inferior derecha de su recuadro de detección y2 supera el valor de 420 px.

Al automóvil eliminado se le denomina como "auto_out" y sus atributos se almacenan en las variables "centosx", "centrosy", "tiempo_centros", "id_aux", "value_string_time", "value_savepath" y "value_fileimage" y son enviados a la función "grafico_mvra" que funciona como un multiproceso permitiendo que comience a ejecutarse mientras se sigue corriendo el *while* que realiza la lectura del video. 

Si el largo de la lista "detect" es **mayor** a la de "info_id" se continua con la detección del automóvil colocando sobre el mismo un cuadro delimitador y el identificador del mismo.  A continuación se realiza una evaluación con un *if*, en el cual si el centro en la coordenada y esta entre los valores 310 y 330 px, se agrega el identificador el automóvil en la lista ya mencionada anteriormente "sended_id", luego se recorta la imagen del automóvil haciendo uso de las coordenadas x1,y1,x2,y2 del cuadro delimitador, a continuación se registra la fecha y hora en que se realizó el recorte para complementar el valor del identificador, posteriormente se guarda la imagen en el directorio local imagen_auto y finalmente se ejecuta la función "set_aws_values" para almacenar la fecha, hora, ruta de la imagen y nombre de la imagen en las variables del objeto automóvil. 

Cuando se ejecuta el multiproceso, en la función "grafico_mrva" se utiliza la variable arreglo "tiempos_aux" en la cual se almacenan los tiempos correspondientes a los centros en la coordenada "y" de los automóviles detectados. En el sistema los centros en la coordenada "y" represnetan el cambio de la posición del automóvil. Y es con estos valores y su relación con los valores del tiempo, en que se encuentran estas posiciones, que se obtienen dos modelos: Un modelo en forma de recta, y un modelo polinómico de grado dos. Para los modelos se utilizan las funciones poly1d y polyfit de la librería numpy, luego de obtener los modelos estos son derivados con la función deriv(), a continuación con una fucnión denomiada "rcuadrado" se selecciona el modelo con mejor ajuste a los datos de posición vs tiempo del automóvil que se esta analizando, a esta función se le envía los parámetros "tiempos_aux" y la lista de centros en la coordenada y.

Al obtener el modelo que mejor se ajusta a los datos, la derivada del modelo es evaluada en un valor del tiempo en que se encuentre una posición "y" cercana al límite final del área establecida que sea mayor a 280 px. Este resultado tendrá las dimensionales en px/s por lo cual es necesario convertir este valor a una estimación cercana en km/h. Para ello se procedió a centrar la perspectiva sin comprometer las medidas de la imagen original. Como se muestra en la imagen a continuación:

<p align="center">
  <img width="542" alt="image" src="https://user-images.githubusercontent.com/109677535/181078569-00ecdca7-5c17-4ca8-97ba-df52bedc1fa9.png">
<p/>

De la imagen anterior se marca la medida que se toma de referencia, esta corresponde a un Suzuki Swift, y la medida en pixeles tomada con la aplicación Paint fue de 52 px, dando un factor de conversión 0.266, dicho valor se utiliza para convertir px/s en km/h.

A continuación se procede con ejecutar la función "data_to_aws" en ella se utiliza el protocolo de mensajería MQTT para el envío de los valores de rapidez e identificador del automóvil al servicio de IoT Core de AWS. La función recibe: la variable que contiene el tiempo en que el valor de centro de la coordenada "y" del automóvil supera el valor de 310 px, el identificador, la rapidez obtenida, el directorio local donde esta guardada la imagen del automóvil, y el nombre de la imagen. 

En la función se configura el *"ENDPOINT"*, *"CLIENT_ID"*, *"PATH_TO_CERTIFICATE"*, *"PATH_TO PRIVATE_KEY"*, *"PATH_TO_AMAZON_ROOT_CA_1"*, se establece el *Timeout* de conexión y se configura la cola de publicación sin conexión. Se asigna en la variable "dataidaws" la concatenación del identificador con el tiempo recibido, en la variable "dataspeddaws" se asigna la rapidez del automóvil obtenida, y ambas variables son contenidas en un mensaje con formato json.

A continuación se conecta al cliente y se publica en el *"TOPIC"* el mensaje en el servicio de AWS IoT Core, tras publicarse se desconecta al cliente y se ejecuta la función "upload_files".

En esta función se recibe el directorio local donde se encuentra la imagen del automóvil, el nombre del *bucket* (carimages-traffic-jetson-nano-4gb) y el nombre de la imagen. Haciendo uso de la librería boto3, se configura el *"ACCESS_KEY_ID"* y *"SECRET_ACCESS_KEY"*, luego se accede al directorio donde se encuentra la imagen y se sube al *bucket* establecido.

Finalmente se ejecuta la función "delete_local_image" que recibe el directorio donde se encuentra la imagen del automóvil y esta es eliminada.

Lo descrito anteriormente se representa gráficamente a continuación:

<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181090653-fad79f6c-96e1-48b7-b40e-960d0931038a.png">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181090749-9bf316c6-e097-43a1-b405-2cbd2951d6e7.png">
<p/>

<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181116172-e9c3d01f-e8e3-4fd6-a372-46d95e4efb57.png">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181116082-6835fd7c-5400-4167-a36a-c52ec5e10451.png">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181116880-97e2a990-d46f-4ac2-aa91-4e30c48bdba8.png">
<p/>

## Elaboración de función en servicio Lamnda para integración de servicios de AWS

Para la integración de los servicios configurados de AWS, se desarrolló una función en el servicio Lambda, la cual tiene como desencadenador el servicio de AWS IoT Core, lo que indica que cada vez que se publique un mensaje MQTT en el *"TOPIC"* definido anteriormente, se activarán las funciones dentro de la función lambda denominada "MQTT-S3getCar-Rekognition-DynamoDB".

Esta cuenta con una función "lambda_handler" en la cual se recibe el mensaje en formato json del servicio IoT Core, los valores "IDaws" y "dataspeedaws" que contienen la rapidez y el identificador concatenado del automóvil.

Se ejecuta la función "Sistema_multa" la cual recibe la rapidez del automóvil y en la cual se establece una "rapidez_aceptada" y una variable denominada "multa". A continuación con un evaluador *if* se evalúa si la rapidez recibida es mayor al valor de "rapidez_aceptada" de ser así la variable "multa" se asigna como un "Sí" de lo contrario se asigna un "no", finalmente se retorna el valor de la rapidez. 

A continuación se establece una variable llamada *"bucket"* que contiene el nombre del *bucket* configurado en el servicio S3 "carimages-traffic-jetson-nano-4gb" donde se guardan las imágenes de los automóviles detectados y se establece una variable "plateimage" que contiene el valor de "IDaws" con la terminación .jpg. Tanto la variable "plateimage" como *"bucket"* es enviada a la función "call_rekognition".

En esta función inicialmente se define una variable "plate", luego con la librería boto3 se comunica con el servicio Rekognition para que el mismo obtenga el texto en la imagen del automóvil guardada en el *bucket*. Tras sustituir cualquier espacio detectado por un guion, se asignan a la variable "plate" los valores detectados y se retornar la variable "plate".

A continuación se ejecuta la función "normalize" que recibe "plate" en la misma se elimina cualquier acentuación que se haya identificado en los caracteres de la detección de texto de Rekognition y se ponen en mayúsculas.

Luego se ejecuta la función "Dynamo_write" que recibe los valores de "IDaws", "dataspeedaws", "plate", y "multa". Esta utiliza la librería boto3 para agregar a la tabla "Detected-Cars-DB" el identificador concatenado de la imagen, el *timestamp* de la detección del automóvil el cual se obtiene utilizando la función "get_timestamp", la matrícula, la rapidez, el nombre de la imagen y finalmente la indicación de la multa.

En la función "get_timestamp" se recibe como parámetro el identificador del automóvil detectado concatenado, en la función se busca el guión bajo que separa la concatenación y se retorna solamente la parte del *timestamp*. 

Finalmente se ejecuta la función "sendmail" cuando el valor de "multa" sea "Si", esta función recibe la matrícula, el *timestamp*, y la rapidez. Inicialmente fue neceario acceder con la librería boto3 a la tabla "CarOwners" de la cual se obtuvieron los valores del email, primer nombre y primer apellido del dueño del vehículo al cual se le aplicaría la multa, posteriormente se define una variable denominada "message" con el contenido:
'CIUDADANO ' + str(firstname) + ' ' + str(surname) + ' USTED INCLUMPLIO CON EL LÍMITE DE RAPIDEZ ESTABLECIDO AL MANEJAR A ' + str(speed) + ' KM/H'.

Luego con la librería MIMEMultipart se crea un objeto msg, al cual se le indica el correo emisor, contraseña del correo emisor, asunto del correo y se adjunta el mensaje que llevaría el correo. A continuación con la librería smtplib se crea el objeto "server" y se define el *host* y puerto que se utiliza (smtp.office365.com y 587). 

Finalmente se ingresa al "server" indicando el correo emisor y la contraseña y se envía el correo electrónico al infractor del límite de rapidez.

Lo descrito anteriormente se representa gráficamente a continuación:

<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181604339-7c929c2a-3ad9-4ec5-85f2-2478154cc417.png">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/109677535/181604847-83a55a5c-0990-49f6-993c-49044eb3040e.png">
<p/>


## Autores:

### Sara Elizabeth Castro Arriaga
### Diego Fernando Bran Arriola

