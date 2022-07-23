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
  <img width="585" alt="Captura de Pantalla 2022-07-22 a la(s) 17 07 56" src="https://user-images.githubusercontent.com/31348574/180579177-d61458ed-3f90-4342-92ad-eadae6483b7a.png">
<p/>


**PASO 4:**  En la siguiente ventana se seleciona el número de cosas a crear y hacer click en *"next"*
<p align="center">
  <img width="507" alt="Captura de Pantalla 2022-07-22 a la(s) 17 11 06" src="https://user-images.githubusercontent.com/31348574/180579375-87e847d8-46d0-4563-a4fc-3bc78f89241e.png">
<p/>

**PASO 5:** Posteriormente se debe de crear un *"thing type, thing group y un billing group"* para identificar el recurso. Como se observa en la imagen.

<p align="center">
  <img width="612" alt="Captura de Pantalla 2022-07-22 a la(s) 17 16 02" src="https://user-images.githubusercontent.com/31348574/180579622-cccd2e60-c1f3-40cc-b144-cb9dc9801798.png">
<p/>
  
 **PASO 6:**  En la sección *"Device Shadow"* se selecciona la opción *"No shadow"* y selecciona *"Next"*
<p align="center"> 
  <img width="611" alt="Captura de Pantalla 2022-07-22 a la(s) 17 22 53" src="https://user-images.githubusercontent.com/31348574/180580034-c00f527d-1c82-448a-bb25-881f8860ec1f.png">
<p/>
**PASO 7:** En la sección *"Configure device certificate-optional"* se selecciona *"Auto-generate a new certificate (recommended)"* y seleccionar *"Next"*
<p align="center">
  <img width="614" alt="Captura de Pantalla 2022-07-22 a la(s) 17 29 21" src="https://user-images.githubusercontent.com/31348574/180580380-445a87ec-eeff-4a91-acf0-027d25378c29.png">
<p/>

**PASO 8:**  En la sección _"Attach policies to certificate-optional"_ se selecciona _"Create a policy"_ y se escribe la siguiente política 
<p align="center">
  <img width="614" alt="Captura de Pantalla 2022-07-22 a la(s) 17 32 25" src="https://user-images.githubusercontent.com/31348574/180580551-798b91cf-82f8-44ae-b306-9702e57ca72f.png">
<p/>

<p align="center">
  <img width="602" alt="Captura de Pantalla 2022-07-22 a la(s) 17 35 31" src="https://user-images.githubusercontent.com/31348574/180580694-f3c37e72-b373-45dc-91d6-0d5d6b3c957e.png">
<p/>


**PASO 9:** Se selecciona la política creada en el paso 8 y se selecciona _"Create thing"_
<p align="center">
  <img width="495" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180580959-19f38626-dc68-4576-9f9a-4a4bc98bc87d.png">
<p/>

**PASO 10:** Seguidamente se mostrarán los certificados y llaves del objeto, además del certificado raíz de la entidad certificadora de AWS. Deben de descargarse el certificado del dispositivo, el certificado Amazon Root CA 1 y las llaves pública y privada y dar click en done 

<p align="center">
  <img width="615" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180581247-311fb404-167c-4c1c-854d-5720f38eeaf2.png">
<p/>

**PASO 11:** Dirigirse a la sección _"Secure"_, luego en la opción _"Certificates"_  hacer click en el certificado y en _"Policies"_ se selecciona la opción _"Attach policies"_ y se selecciona la política. 

<p align="center">
  <img width="823" alt="Captura de Pantalla 2022-07-22 a la(s) 17 58 50" src="https://user-images.githubusercontent.com/31348574/180581805-1f8c4c07-84d1-413f-81d4-e41ceea57c7c.png">
<p/>


**PASO 11:** Dirigirse a la opción _"setting"s_ al final del menú lateral y guardar el  _"Endpoint"_ del servicio. Este debe ser indicado en el código que se realizará en la tarjeta.

<p align="center">
  <img width="825" alt="Captura de Pantalla 2022-07-22 a la(s) 18 23 53" src="https://user-images.githubusercontent.com/31348574/180582916-81774c41-e9c3-44c6-9895-c1f361120fb0.png">
<p/>

**PASO 12: ** Ya que el objeto fue creado, es necesario modificar la política de los certificados para garantizar que solamente el dispositivo con estos certificados pueda utilizar los recursos. Para ello dirigirse a _"all devices"_, seleccionar _"Things"_, y copiar el ARN del objeto.

<p align="center">
  <img width="1785" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180584052-c71eeaca-afaa-4e98-8f9a-27be1629ece4.png">
<p/>


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **PASO 12.1** Dirigirse a la sección _"security"_, seleccionar _"Policy"_ y hacer click en la política. 
<p align="center">
  <img width="1785" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180584178-ad2dcee5-298d-4c56-b7ae-95304cdd5bd9.png">
<p/>



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **PASO 12.2** Seleccionar la versión activa de la política

<p align="center">
  <img width="1474" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180584275-57ced402-4cf5-48ed-823e-80a48f7dca25.png">
<p/>



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **PASO 12.3** Colocar la vista de la política en formato JSON y editar el parámetro _"Resource"_  y colocamos el ARN que se copió en el paso 12.


<p align="center">
  <img width="1507" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180584356-e4809230-8935-4dab-a67e-1b3df84fc14f.png">
<p/>


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **PASO 12.4** Posteriormente se generará una nueva versión de la política, se debe seleccionar esta última versión y hacer click en _"set as active"_ 

<p align="center">
  <img width="1476" alt="imagen" src="https://user-images.githubusercontent.com/31348574/180584543-5478a2c2-cad3-4d3d-a1d3-2c7e5f57e083.png">
<p/>


## Configuración de servicios en AWS

Los servicios configurados a continuación son los siguientes: 

- IAM
- S3
- DynamoDB
- Lambda

### Configuración de IAM 

Este servico se utilizará para crear un grupo el cual poseerá permisos para colocar objetos en un bucket de S3 y se asignará un usuario, el cual se colocará en el código de la Jetson Nano. 

**PASO 1:** En el servicio IAM colocarse en _"User Groups"_, y hacer click en _"Create group"_.











