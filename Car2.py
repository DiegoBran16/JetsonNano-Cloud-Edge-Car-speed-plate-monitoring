import cv2
import numpy as np
from datetime import datetime
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt


class Auto:
        # Se crea el constructor con las variables de clase
        def __init__(self):
            self.car_id = 0 #ID del automóvil
            self.info_auto = [] #Lista que almacena la los centroides y las coordenadas de esquina superior izquierda y la esquina inferior derecha del cuadro delimitador
            self.tiempo = [] #Lista que almacena el tiempo cada vez que se detecta un nuevo centroide
            self.centroides_aux_x = [] # Lista que almacena las coordenadas en el eje horizontas de los centroides
            self.centroides_aux_y = [] # Lista que almacena las coordenadas en el eje vertical de los centroides
            self.string_time = "" # se almacena el timestamp en una variable string 
            self.savepathlocal = "" # se almacena el la ruta en la que se colocarán las imágenes de los automóviles
            self.fileimage="" #Se almacena el nombre de la imagen en una variable string
            
            
                
         # Función que setea los valores de las variables relacionadas con la captura de la imagen
        def set_aws_values(self,string_time_aws,savepathlocal_aws,fileimage_aws):
            self.string_time = string_time_aws
            self.savepathlocal = savepathlocal_aws
            self.fileimage = fileimage_aws
        
        #Función para obtener los valores relacionadas con la captura de la imagen
        def get_aws_values(self):
            return self.string_time, self.savepathlocal,self.fileimage

        #Función para agregar los centros y las coordenadas del cuadro delimitador a la lista 
        def agregar_info(self, objeto_auto):
            centro_x, centro_y,x1,y1,x2,y2 = objeto_auto
            self.info_auto.append([centro_x, centro_y,x1,y1,x2,y2])
               
        #Función para setear el ID 
        def asignar_id(self, identificador):
            self.car_id = identificador
        
        #Función para obtener el ID y la lista que contiene los centroides y las coordenadas del cuadro delimitador. 
        def get_variables(self):
            return self.car_id, self.info_auto
        
        #Obtiene la lista que almacena los tiempos 
        def get_time_array(self):
            return self.tiempo

        #Obtiene las listas que contienen los centroides
        def get_centroides(self):
            return self.centroides_aux_x, self.centroides_aux_y

        #función que agrega a las listas los valores de los centros y el tiempo
        def set_centroides(self,cx,cy):
            self.centroides_aux_x.append(cx)
            self.centroides_aux_y.append(cy)
            self.tiempo.append(datetime.now())
        
  


class Tracker:
        
        
    def __init__(self):
        self.autos_detectados = {}  #
        self.car_id = 1
        self.centroides = {}
     


    def tracking(self, info):

        for i in info:
            x1,y1,x2,y2 = i
            centro_y = (y2 + y1)//2
            centro_x = (x2 + x1)//2
            

            validador = False
          
            
            for id, obj_carro in self.autos_detectados.items():
                id_carro, info_carro = obj_carro.get_variables()
                centro_x_auto, centro_y_auto, x1_auto, y1_auto, x2_auto, y2_auto = info_carro[len(info_carro)-1]
                recorrido = np.sqrt((centro_x-centro_x_auto)**2+(centro_y-centro_y_auto)**2)
                cornerDistance= int(np.sqrt((x2_auto-x1_auto)**2+(y2_auto-y1_auto)**2))
               

                if  (recorrido <=100) and abs(centro_y_auto - centro_y) < cornerDistance//2:
                    info_aux = centro_x, centro_y,x1,y1,x2,y2 
                    obj_carro.agregar_info(info_aux)
                    self.centroides[id] = (centro_x, centro_y)
                    obj_carro.set_centroides(centro_x,centro_y)
                    validador = True
        
                    break
         
        
            if validador is False and y2 <300:
                carro = Auto() 
                carro.asignar_id(self.car_id)
                info_objeto = centro_x, centro_y,x1,y1,x2,y2
                carro.agregar_info(info_objeto)
                self.centroides[self.car_id] = (centro_x,centro_y)
                self.autos_detectados[self.car_id] = (carro) 
                self.car_id = self.car_id +1
            
          
        return self.autos_detectados

