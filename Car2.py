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
        
     #Constructor de la clase Tracker con las variables de clase
    def __init__(self):
        self.autos_detectados = {}  #Diccionario de los autos detectados 
        self.car_id = 1  # Contador de los ids asignados
        self.centroides = {} #Diccionario donde se almacenan los centroides 
     

     #Función que realiza el seguimiento de los vehiculos
    def tracking(self, info):
                
        #Función ciclica que se ejecuta por cada elemento de la lista de autos detectados por la red. 
        
        for i in info:
            x1,y1,x2,y2 = i # se recuperan las coordenadas del cuadro delimitador 
            centro_y = (y2 + y1)//2 #Se obtiene la coordenada del centroide en y 
            centro_x = (x2 + x1)//2 #Se obtiene la coordenada del centroide en x 
            

            validador = False #Variable para validar si el auto fue detectado ateriormente
          
            
            for id, obj_carro in self.autos_detectados.items(): #Se ejecuta el ciclo para cada elemento del diccionario 
                id_carro, info_carro = obj_carro.get_variables() # se obtienen el ID y la lista que contiene los centroides y las coordenadas del cuadro delimitador. 
                centro_x_auto, centro_y_auto, x1_auto, y1_auto, x2_auto, y2_auto = info_carro[len(info_carro)-1] #Se obteien los centroides y las coordenadas del cuadro delimitador del ultimo registro en la lista
                recorrido = np.sqrt((centro_x-centro_x_auto)**2+(centro_y-centro_y_auto)**2) # Se obtiene la distancia euclidiana entre las coordenadas actuales de los centroides y las coordenadas del ultimo registro de la lista de centroides.
                cornerDistance= int(np.sqrt((x2_auto-x1_auto)**2+(y2_auto-y1_auto)**2)) # Se obtiene la distancia entre las coordenadas del cuadro delimirador y se divide entre 2
               
                 #Se valida que la distancia euclidiana sea menor a 100 pixeles y a la mitad de la distancia entre las coordenadas 
                if  (recorrido <=100) and abs(centro_y_auto - centro_y) < cornerDistance//2: 
                    info_aux = centro_x, centro_y,x1,y1,x2,y2  # se agregan a la lista info_aux las coordenadas de los centroides y las coordenadas del cuadro delimitador
                    obj_carro.agregar_info(info_aux) # se agregan las coordenadas los centroides y las coordenadas del cuadro delimitador al objeto carro
                    self.centroides[id] = (centro_x, centro_y) # Se agregan los centroides al diccionario de ventroides según el ID 
                    obj_carro.set_centroides(centro_x,centro_y) # Se agregan los centroides a las listas de centroides auxiliares  y se agrega el tiempo a la lista de tiempos 
                    validador = True
        
                    break
         
        
            if validador is False and y2 <300: # Si el validador es falso y la coordenada vertical de la esquina inferior derecha supera 300 pixeles se define como un auto nuevo en el diccionario 
                carro = Auto() # se crea un objeto auto
                carro.asignar_id(self.car_id) # Se asigna un ID numerico
                info_objeto = centro_x, centro_y,x1,y1,x2,y2 # se agregan las coordenadas de los centroides y las coordenadas del cuadro delimitador a una variable 
                carro.agregar_info(info_objeto)              # Las coordenadas en la variable se agregan a la lista del objeto 
                self.centroides[self.car_id] = (centro_x,centro_y). # Se agregan las coordenadas de los centroides al diccinario de centroides de la clase Tracker
                self.autos_detectados[self.car_id] = (carro)  # se agrega el objeto al diccionario de autos detectados de la calse Tracker
                self.car_id = self.car_id +1 # Se incrementa el contador de IDs
            
          
        return self.autos_detectados # Se retorna la lisa de objetos automoviles detectados 

