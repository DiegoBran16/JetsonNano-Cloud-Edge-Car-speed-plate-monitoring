# Se importan las librerías necesarias para le desarrollo del sistema
import os # manejo del sistema
import multiprocessing # multiprocesamientos
from sklearn.metrics import r2_score # calculo de r cuadrado
import jetson.inference # manejo de componentes de la Jetson NANO
import jetson.utils # manejo de componentes de la Jetson NANO
import cv2 # procesamiento de imágenes
import numpy as np # operaciones numéricas y vectoriales
from Car2 import* # archivo con funciones necesarias para el seguimieto e identificación de las detecciones
from datetime import datetime # obtner fechas y tiempos
import json # escritura de archivos en formato json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT # protocolo de comunicación MQTT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # configuración de cliente para comunicación MQTT
import boto3 # utilizar los servicios de AWS de forma programada
from botocore.exceptions import NoCredentialsError # verificación de credenciales
from matplotlib import pyplot as plt # gráficas

# seteo del ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, TOPIC, ACCESS_KEY_ID y SECRET_ACCESS_KEY
ENDPOINT = "xx" 
CLIENT_ID = "JetsonNano-S1-1"
PATH_TO_CERTIFICATE = "certificates/6837ec83d51d906362fb175d819d844667e54818c8be688bc276c6bdbdaafdc7-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/6837ec83d51d906362fb175d819d844667e54818c8be688bc276c6bdbdaafdc7-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.pem"
ACCESS_KEY_ID = 'xx'
SECRET_ACCESS_KEY = 'xx'
TOPIC = "$aws/things/JetsonNano-S1-1/shadow/name/detectCar"

# seteo de la red neuronal re-entrenada, sus etiquetas, sus entradas, y salidas
net = jetson.inference.detectNet(argv=['--model=Car2.onnx', '--labels=labels.txt',  '--input-blob=input_0',  '--output-cvg=scores',  '--output-bbox=boxes'])

# captura del video en donde transitan seis automóviles
cap = jetson.utils.videoSource("videotest2.mp4")

# creación de un objeto stalker de la clase Tracker
stalker = Tracker()

# creación de variables auxiliares para identificar los objetos fuera del área de análisis
sended_id = []
contador_out = 0

# función para eliminar del directorio la captura de imagen del automóvil
def delete_local_image(save):
    os.system('rm ' + save)
    print("removed " + save)

# función para subir imágenes al bucket configurado en el servicio S3 de AWS    
def upload_files(image_path, bucket, file_name):
   s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY) # se configura la llave de acceso privada y pública
   try:
       with open(image_path, 'rb') as data: # se accede a la imagen guardada en el directorio local
           s3.upload_fileobj(data, bucket, file_name) # se publica la imagen en el bucket 
       print("Upload Successful")
       return True
   # se verifica que exista el archivo y las credenciales
   except FileNotFoundError:
       print("The file was not found")
       return False
   except NoCredentialsError:
       print("Credentials not available")
       return False

# función para publicar el identificador concatenado y la rapidez a el servicio IoT Core por medio de MQTT
def data_to_aws(string_time, id, speed, save, fileimage):
    
    myAWSIoTMQTTClient= AWSIoTMQTTClient(CLIENT_ID)  # se configura el cliente
    myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883) # se configura el ENDPOINT
    myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE) # se configuran las credenciales
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(60) # se configura el tiempo de espera antes de desconectar
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(30) # se configura el tiempo de espera antes de finalizar la operación
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1) # se configura una cola de publicación sin conexión
    
    if fileimage == '': # verificación que exista un archivo 
        print("No hay fileimage") 
    
    else:    
        IDAWS =  str(id) + "_" + string_time # concatenación del tiempo para complementar el identificador
        SPEEDAWS = speed # se setea la rapidez obtenida
        dataidaws = "{}".format(IDAWS) # se configura el formato para insertar los valores dentro del string
        dataspeedaws = "{}".format(SPEEDAWS) # se configura el formato para insertar los valores dentro del string
        print("Filename: " + str(fileimage))
        
        print('Begin Publish')
        message = {"IDaws" : dataidaws, "dataspeedaws" : dataspeedaws}  # se configura el mensaje que se publica por MQTT     
        myAWSIoTMQTTClient.connect() # se conecta al cliente
        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0)  # se publica el mensaje en formato json en el TOPIC
        myAWSIoTMQTTClient.disconnect() # se desconecta al cliente
        print("Published: '" + json.dumps(message)  + "' to the topic: " + "'test/testing'")
        print('Publish End')
        uploaded = upload_files(save, 'carimages-traffic-jetson-nano-4gb', fileimage) # se ejecuta la función para subir imagen en s3
        delete_local_image(save) # se ejectua la función para eliminar la imagen en el directorio local

# función para obtener el r cuadrado de los tiempos y centros en la coordenada y
def rcuadrado(taux,cyaux,grado):
     
    coef = np.polyfit(taux,cyaux,grado) # se ajustan los coeficientes al grado y los datos con la función polyfit
    funcion = np.poly1d(coef) # brinda una función polinómica con la función poly1d
    yhat = funcion(taux)  # se obtienen los valores de la variable dependiente 
    return r2_score(yhat,cyaux) # se obtiene r cuadrado con la función r2_score
  
# función que obtiene la rapidez del automóvil detectado
def grafico_mrva(cx,cy,tc,idpop,val_string_time, val_savepath, val_fileimage):
    
    # se definen las variables de apoyo 
    tiempos_aux = [] 
    tiempo_grafico = []
    aux_cont = 0
    aux_vacio = 0
    
    
    for i in range(len(tc)):
        
        # se inicia la obtención de los tiempos a partir de la poción 1
        if i == 0:
            aux_vacio = 1
        else:
            # se obtiene el tiempo recorrido entre un nuevo centro detectado y el anterior en segundos
            tiempo_recorrido = (tc[i] - tc [i-1]).total_seconds()
            
            # al ser la primera ejecución se almacena el resultado del tiempo_recorrido en la lista
            if len(tiempos_aux) == 0:
                tiempos_aux.append(tiempo_recorrido)
                aux_cont = aux_cont+1
             
            # en las siguientes ejecuciones de suma el tiempo_recorrido anterior al actual y se agrega a la lista
            else:
                tiempos_aux.append(tiempo_recorrido + tiempos_aux[aux_cont-1])
                aux_cont = aux_cont+1
            
    cy_grafico = cy[1:] # se obtienen los centros en la coordenada y a partir de la primera posición
    
    model_1 = np.poly1d(np.polyfit(tiempos_aux,cy_grafico,1)) # se obtiene el modelo para grado 1
    deriv1 = model_1.deriv() # se deriva el modelo 

    model_2 = np.poly1d(np.polyfit(tiempos_aux,cy_grafico,2)) # se obtiene el modelo para grado 2
    deriv2 = model_2.deriv() # se deriva el modelo 

    rc1 = rcuadrado(tiempos_aux,cy_grafico,1) # se ejecuta la función rcuadrado para obtener el r cuadrado del modelo de grado 1
    rc2 = rcuadrado(tiempos_aux,cy_grafico,2) # se ejecuta la función rcuadrado para obtener el r cuadrado del modelo de grado 2
    #graphaux = np.linspace(0, max(tiempos_aux), max(cy_grafico))
    
    
    # se evalúa el r cuadrado de cada modelo para identificar el valor mayor
    if rc1 > rc2:
        #plt.scatter(tiempos_aux,cy_grafico)
        #plt.plot(graphaux, model_1(graphaux), color = 'green')
        #plt.title(str(idpop))
        #plt.show()
        for i in range(len(cy_grafico)):
            # se obtiene el indice del centro en y en un punto cercano y mayor a 280px 
            if cy_grafico[i] > 280:
                indice = i
                break
        # se calcula la rapidez al multiplicar el factor de conversión por la derivada del modelo de grado 1 
        # y se evalua el tiempo del centro cercano y mayor a 280 px
        rapidez_calculo  = 0.2664*deriv1(tiempos_aux[indice])
        data_to_aws(val_string_time, idpop, rapidez_calculo, val_savepath, val_fileimage) # se ejecuta la función para publicar por MQTT en AWS
        print("iniciando segundo multiproceso")
    else:
        #plt.scatter(tiempos_aux,cy_grafico)
        #plt.plot(graphaux, model_2(graphaux), color = 'red')
        #plt.title(str(idpop))
        #plt.show()
        for i in range(len(cy_grafico)):
            # se obtiene el indice del centro en y en un punto cercano y mayor a 280px 
            if cy_grafico[i] > 280:
                indice = i
                break
        # se calcula la rapidez al multiplicar el factor de conversión por la derivada del modelo de grado 2 
        # y se evalua el tiempo del centro cercano y mayor a 280 px
        rapidez_calculo  =0.2664*deriv2(tiempos_aux[indice])
        data_to_aws(val_string_time, idpop, rapidez_calculo, val_savepath, val_fileimage)# se ejecuta la función para publicar por MQTT en AWS
        print("iniciando segundo multiproceso")


# se comienza la lectura del video 
while True:
    
    img = cap.Capture() # se realiza la captura de los frames del video
    img = cv2.resize(np.array(img),(854,480)) # se redimencionan los frames
    mascara = np.zeros((img.shape[0], img.shape[1]) , dtype = np.uint8) # se define una máscara
    area = np.array([[[486,106], [809,106], [809,484] , [145,484]]]) # se establece el área de análisis
    
    cv2.fillPoly(mascara,area, 255) # se configura en la máscara el área que se conservará 
    zona = cv2.bitwise_and(img, img, mask= mascara) # se aplica un filtro para eliminar lo que se encuentre fuera del área definida
    
    imgCuda = jetson.utils.cudaFromNumpy(zona) # se transforma la imagen de formato numpy a tensor
    detections = net.Detect(imgCuda) # se ingresan los frames a la red neuronal re-entrenada para obtener las salidas
    detect = [] # se crea una variable de apoyo para almacenar las equinas inferior derecha y superior izquierda correspondiente al recuadro de detección
    
    
    for d in detections:
        x1,y1,x2,y2 = int(d.Left),int(d.Top), int(d.Right), int(d.Bottom) # se almacenan las variables de las equinas inferior derecha y superior izquierda del recuadro
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2) # se encierra la detección en un recuadro
        detect.append([x1,y1,x2,y2]) # se almacenan en la lista las equinas inferior derecha y superior izquierda del recuadro
  

    info_id = stalker.tracking(detect) # se envía a la función tracking del objeto stalker la lista detect
    
    len_info = len(info_id) # se obtiene la longitud de los automóviles retornados por el objeto stalker
    len_detect = len(detect) # se obtiene la longitud de los automóvles dentro del frame detectados por la red

    
    # se evalua si un automóvil se encuentra fuera del área de análisis deseada
    if len_detect < len_info:
        diferencia = len_info - len_detect
        # si hay más automóviles en el diccionario que retorna el objeto stalker que en la lista detect de la red neuronal
        # se infiere que el automóvil se encuentra fuera del área de análisis y debe ser removido del diccionario info_id
        while (diferencia > 0):
            try:
                if len_info > 0:
                    id_pop = sended_id[contador_out] # se obtiene el identificador del objeto que salió del área de análisis
                    # se obtiene el valor ID del automóvil correspondiente a ese identificador
                    autofuera = info_id[id_pop]  
                    id_autofuera, _ = autofuera.get_variables()
                    if(id_pop == id_autofuera):
                        contador_out = contador_out + 1 # se incrementa el contador auxiliar de automóviles fuera del área de análisis
                        # se obtienen los centros en la coordenada "y", y las esquinas superior izquiera e inferior derecha del recuadro de detección
                        _, auxes = autofuera.get_variables() 
                        _, cy,x1,y1,x2,y2 = auxes[len(auxes)-1]
                        # si la esquina inferior derecha de autofuera supera los 415 px se elimina el automóvil fuera del área de análisis 
                        if (y2>=415) : 
                            auto_out = info_id.pop(id_pop) # se elimina el automóvil del diccionario info_id
                            # se obtienen los valores del automóvil que fue eliminado del diccionario info_id
                            centrosx, centrosy = auto_out.get_centroides()
                            tiempo_centros = auto_out.get_time_array()
                            id_aux, _ = auto_out.get_variables()
                            value_string_time, value_savepath, value_fileimage = auto_out.get_aws_values()
                            # se ejecuta la función grafico_mrva como un multiproceso para que la lectura del video continue sin interrupciones
                            p1 = multiprocessing.Process(target=grafico_mrva, args = [centrosx,centrosy,tiempo_centros, id_aux,value_string_time, value_savepath, value_fileimage])
                            p1.start()
                            diferencia = diferencia-1 # se disminuye el valor de diferencia
                    elif (y2<415):  
                        break
            except:
                break
    
    for id, inf in info_id.items():

        _,lista_bordes = inf.get_variables() # se obtienen las variables del objeto en el diccionario info_id
        cx_aux, cy_aux, x1, y1, x2, y2 = lista_bordes[len(lista_bordes)-1] # se obtienen los centros y las coordenadas de las esquinas superior izquierda e inferior derecha del recuadro
        # en el último índice 
        cv2.putText(img, str(id), (x2,y2),cv2.FONT_HERSHEY_DUPLEX, 0.75,(255,0,255),2) # se escribe el identificador correspondiente a la detección del automóvil 
        
        # se toma la captura de la imagen del automóvil cuando este se encuentre entre 305 px y 320 px
        if cy_aux > 305 and cy_aux < 320 and id not in sended_id:
            sended_id.append(id) # se agrega el identificador a la lista sendend_id
            img_frame = np.copy(img) # se captura la imagen
            crop_image = img_frame[y1: y2,x1:x2,:] # se recorta la imagen 
            time_cap = datetime.now() # se obtiene el tiempo 
            string_time = time_cap.strftime("%d-%m-%y-%H:%M:%S") # se establece el formato del tiempo
            fileimage = str(id) + "_" + string_time + ".jpg" # se define el nombre de la imagen
            save = "imagen_auto/" +  fileimage # se establece el directorio local 
            cv2.imwrite(save,crop_image) # se guarda la imagen en el directorio local definido
            inf.set_aws_values(string_time,save,fileimage) # se establecen los valores del tiempo, directorio local y nombre de la imagen en el objeto inf
                
    cv2.imshow("imagenprueba",cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    








