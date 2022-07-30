import os
import multiprocessing 
from sklearn.metrics import r2_score
import jetson.inference
import jetson.utils 
import cv2
import numpy as np
from Car2 import*
import time
from datetime import datetime
import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
from botocore.exceptions import NoCredentialsError
from matplotlib import pyplot as plt
#from torchsummary import summary

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "aepu6tvccafn1-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "JetsonNano-S1-1"
PATH_TO_CERTIFICATE = "certificates/6837ec83d51d906362fb175d819d844667e54818c8be688bc276c6bdbdaafdc7-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/6837ec83d51d906362fb175d819d844667e54818c8be688bc276c6bdbdaafdc7-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.pem"
#IDAWS = ""
#SPEEDAWS = 0
ACCESS_KEY_ID = 'AKIAYDAI5LLOU7NXJP7U'
SECRET_ACCESS_KEY = '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'
TOPIC = "$aws/things/JetsonNano-S1-1/shadow/name/detectCar"

net = jetson.inference.detectNet(argv=['--model=Car2.onnx', '--labels=labels.txt',  '--input-blob=input_0',  '--output-cvg=scores',  '--output-bbox=boxes'])

#print(summary(net, input_size=(854,480)))
cap = jetson.utils.videoSource("videotest2.mp4")
stalker = Tracker()

#auto_zona_in = {}
#auto_zona_out = {}
sended_id = []
contador_out = 0

def delete_local_image(save):
    os.system('rm ' + save)
    print("removed " + save)

def upload_files(image_path, bucket, file_name):
   s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
   try:
       with open(image_path, 'rb') as data:
           s3.upload_fileobj(data, bucket, file_name)
       print("Upload Successful")
       return True
   except FileNotFoundError:
       print("The file was not found")
       return False
   except NoCredentialsError:
       print("Credentials not available")
       return False

def data_to_aws(string_time, id, speed, save, fileimage):
    
    myAWSIoTMQTTClient= AWSIoTMQTTClient(CLIENT_ID) 
    myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
    myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(60)
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(30)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    if fileimage == '':
        print("No hay fileimage") 
    else:
        
        IDAWS =  str(id) + "_" + string_time
        SPEEDAWS = speed
        dataidaws = "{}".format(IDAWS)
        dataspeedaws = "{}".format(SPEEDAWS)
        print("Filename: " + str(fileimage))
        
        print('Begin Publish')
        message = {"IDaws" : dataidaws, "dataspeedaws" : dataspeedaws}      
        myAWSIoTMQTTClient.connect()
        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 0) 
        myAWSIoTMQTTClient.disconnect()
        print("Published: '" + json.dumps(message)  + "' to the topic: " + "'test/testing'")
        print('Publish End')
        uploaded = upload_files(save, 'carimages-traffic-jetson-nano-4gb', fileimage)
        delete_local_image(save)

def rcuadrado(taux,cyaux,grado):
     
    coef = np.polyfit(taux,cyaux,grado)
    funcion = np.poly1d(coef)
    yhat = funcion(taux)
    return r2_score(yhat,cyaux)    
  
def grafico_mrva(cx,cy,tc,idpop,val_string_time, val_savepath, val_fileimage):
    tiempos_aux = []
    tiempo_grafico = []
    aux_cont = 0
    aux_vacio = 0
    for i in range(len(tc)):
        if i == 0:
            aux_vacio = 1
        else:
            tiempo_recorrido = (tc[i] - tc [i-1]).total_seconds()
            if len(tiempos_aux) == 0:
                tiempos_aux.append(tiempo_recorrido)
                aux_cont = aux_cont+1
            else:
                tiempos_aux.append(tiempo_recorrido + tiempos_aux[aux_cont-1])
                aux_cont = aux_cont+1
            
    cy_grafico = cy[1:]
    
    model_1 = np.poly1d(np.polyfit(tiempos_aux,cy_grafico,1))
    deriv1 = model_1.deriv()

    model_2 = np.poly1d(np.polyfit(tiempos_aux,cy_grafico,2))
    deriv2 = model_2.deriv()

    rc1 = rcuadrado(tiempos_aux,cy_grafico,1)
    rc2 = rcuadrado(tiempos_aux,cy_grafico,2)
    #graphaux = np.linspace(0, max(tiempos_aux), max(cy_grafico))
    if rc1 > rc2:
        #plt.scatter(tiempos_aux,cy_grafico)
        #plt.plot(graphaux, model_1(graphaux), color = 'green')
        #plt.title(str(idpop))
        #plt.show()
        for i in range(len(cy_grafico)):
            if cy_grafico[i] > 280:
                indice = i
                break
        rapidez_calculo  = 0.2664*deriv1(tiempos_aux[indice])
        data_to_aws(val_string_time, idpop, rapidez_calculo, val_savepath, val_fileimage)
        print("iniciando segundo multiproceso")
    else:
        #plt.scatter(tiempos_aux,cy_grafico)
        #plt.plot(graphaux, model_2(graphaux), color = 'red')
        #plt.title(str(idpop))
        #plt.show()
        for i in range(len(cy_grafico)):
            if cy_grafico[i] > 280:
                indice = i
                break
        rapidez_calculo  =0.2664*deriv2(tiempos_aux[indice])
        data_to_aws(val_string_time, idpop, rapidez_calculo, val_savepath, val_fileimage)
        print("iniciando segundo multiproceso")


while True:
    
    img = cap.Capture()
    img = cv2.resize(np.array(img),(854,480))
    mascara = np.zeros((img.shape[0], img.shape[1]) , dtype = np.uint8)
    area = np.array([[[486,106], [809,106], [809,484] , [145,484]]])
    cv2.fillPoly(mascara,area, 255)


    zona = cv2.bitwise_and(img, img, mask= mascara)
    imgCuda = jetson.utils.cudaFromNumpy(zona)
    detections = net.Detect(imgCuda)
    detect = []
    #cv2.line(img,(215,421),(831,421),(255,0,0),1)
    for d in detections:
        x1,y1,x2,y2 = int(d.Left),int(d.Top), int(d.Right), int(d.Bottom)
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
        detect.append([x1,y1,x2,y2])
  

    info_id = stalker.tracking(detect)
    len_info = len(info_id)
    len_detect = len(detect)

    if len_detect < len_info:
        diferencia = len_info - len_detect
        while (diferencia > 0):
            try:
                if len_info > 0:
                    id_pop = sended_id[contador_out]
                    autofuera = info_id[id_pop]
                    id_autofuera, _ = autofuera.get_variables()
                    if(id_pop == id_autofuera):
                        contador_out = contador_out + 1 
                        _, auxes = autofuera.get_variables()
                        _, cy,x1,y1,x2,y2 = auxes[len(auxes)-1]
                        if (y2>=415) : #20
                            auto_out = info_id.pop(id_pop)
                            centrosx, centrosy = auto_out.get_centroides()
                            tiempo_centros = auto_out.get_time_array()
                            id_aux, _ = auto_out.get_variables()
                            value_string_time, value_savepath, value_fileimage = auto_out.get_aws_values()
                            p1 = multiprocessing.Process(target=grafico_mrva, args = [centrosx,centrosy,tiempo_centros, id_aux,value_string_time, value_savepath, value_fileimage])
                            p1.start()
                            diferencia = diferencia-1
                    elif (y2<415):  #20
                        break
            except:
                break
    
    for id, inf in info_id.items():


        _,lista_bordes = inf.get_variables()
        cx_aux, cy_aux, x1, y1, x2, y2 = lista_bordes[len(lista_bordes)-1]
        cv2.putText(img, str(id), (x2,y2),cv2.FONT_HERSHEY_DUPLEX, 0.75,(255,0,255),2)
        
        #310 330
        if cy_aux > 305 and cy_aux < 320 and id not in sended_id:
            sended_id.append(id)
            img_frame = np.copy(img)
            crop_image = img_frame[y1: y2,x1:x2,:]
            time_cap = datetime.now()
            string_time = time_cap.strftime("%d-%m-%y-%H:%M:%S")
            fileimage = str(id) + "_" + string_time + ".jpg"
            save = "imagen_auto/" +  fileimage
            cv2.imwrite(save,crop_image)
            inf.set_aws_values(string_time,save,fileimage)
                
    cv2.imshow("imagenprueba",cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    








