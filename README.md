# JetsonNano-Cloud-Edge-Car-speed-plate-monitoring
## Proyecto de Graduación 2022 

### Realizado por Diego Bran y Sara Castro 

En el presente repositorio se encuntran el proceso de implementaicón del sistema detallado en forma secuencial. Ademas se incluyen los documentos utilizados en la implementacion y los enlaces a las herramientas necesarias para la elaboración del mismo.
Inicialmente se implementan los componentes de Hardware complementarios en la terjeta Jetson Nano. 

La primera fase de la implementación se relaciona con la conexión de los componentes de Hardware auxiliares a la tarjeta Jetson Nano. Estos componentes son: 
1. Tarjeta de red 
2. Ventilador 
3. Camara

A continuación se detallan los pasos para conectar estos componentes en la tarjeta: 

**Conexión de la Tarjeta de Red**
---
**Paso1** 


**Conexión del Ventilador**
---
**Paso1** 

**Conexión de la Camara**
---
**Paso1** 


## Jetson Nano first steps
---
Al finalizar las conexiones fisicas del hardware de debe montar el JetPack en la Jetson Nano y realizar las configutaciones del primer inicio.   

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





## COnfiguración de la VM en Azure para el entrenamiento. 
**Paso1**
Se inicio por conectarse por SSH a la maquina virtual por medio de la IP publica. Para ello se introdujo el siguiente comando en la maquina cliente

`ssh tesis@xxx.xxx.xxx.xxx` 


Las 'x'deben reemplazarse por la direccion IP publica de la VM
