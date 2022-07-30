import cv2
import numpy as np
from datetime import datetime
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt


class Auto:
        def __init__(self):
            self.car_id = 0
            #self.nombre_foto_matricula = ""
            self.car_speed = 0
            self.info_auto = []
            self.tiempo = []
            self.centroides_aux_x = []
            self.centroides_aux_y = []
            self.string_time = ""
            self.savepathlocal = ""
            self.fileimage=""
            self.recorridolista = []
            

        def set_aws_values(self,string_time_aws,savepathlocal_aws,fileimage_aws):
            self.string_time = string_time_aws
            self.savepathlocal = savepathlocal_aws
            self.fileimage = fileimage_aws
        
        def get_aws_values(self):
            return self.string_time, self.savepathlocal,self.fileimage

        def agregar_info(self, objeto_auto):
            centro_x, centro_y,x1,y1,x2,y2 = objeto_auto
            self.info_auto.append([centro_x, centro_y,x1,y1,x2,y2])
        
        def asignar_id(self, identificador):
            self.car_id = identificador

        def get_variables(self):
            return self.car_id, self.info_auto

        def set_speed(self,rapidez):
            self.car_speed = rapidez
        
        def get_speed(self):
            return self.car_speed
        
        def get_time_array(self):
            return self.tiempo

        def get_centroides(self):
            return self.centroides_aux_x, self.centroides_aux_y

        def set_centroides(self,cx,cy):
            self.centroides_aux_x.append(cx)
            self.centroides_aux_y.append(cy)
            self.tiempo.append(datetime.now())
        
        def set_recorrido(self,recorrido):
            self.recorridolista.append(recorrido)
        
        def get_recorrido(self):
            return self.recorridolista

        def get_recorrido_promedio(self):
            return np.mean(self.recorridolista)



class Tracker:
    def __init__(self):
        self.autos_detectados = {}
        #self.autos_historial = []
        self.car_id = 1
        self.centroides = {}
        #self.copia_autos_detectados = {}
    
    #def auto_fuera_frame(self):
    #    self.autos_detectados=[]


    def tracking(self, info):

        for i in info:
            x1,y1,x2,y2 = i
            centro_y = (y2 + y1)//2
            centro_x = (x2 + x1)//2
            

            validador = False
            #validadorAgregado = False
            
            for id, obj_carro in self.autos_detectados.items():
                id_carro, info_carro = obj_carro.get_variables()
                centro_x_auto, centro_y_auto, x1_auto, y1_auto, x2_auto, y2_auto = info_carro[len(info_carro)-1]
                recorrido = np.sqrt((centro_x-centro_x_auto)**2+(centro_y-centro_y_auto)**2)
                cornerDistance= int(np.sqrt((x2_auto-x1_auto)**2+(y2_auto-y1_auto)**2))
                diferencia_cy = abs(centro_y-centro_y_auto)

                if  (recorrido <=100) and abs(centro_y_auto - centro_y) < cornerDistance//2:
                    info_aux = centro_x, centro_y,x1,y1,x2,y2 
                    obj_carro.agregar_info(info_aux)
                    self.centroides[id] = (centro_x, centro_y)
                    obj_carro.set_centroides(centro_x,centro_y)
                    validador = True
               
                    #validadorAgregado = True
                    break
         
        
            if validador is False and y2 <300:
                carro = Auto() 
                carro.asignar_id(self.car_id)
                info_objeto = centro_x, centro_y,x1,y1,x2,y2
                carro.agregar_info(info_objeto)
                self.centroides[self.car_id] = (centro_x,centro_y)
                self.autos_detectados[self.car_id] = (carro) 
                #self.autos_historial.append(carro)
                self.car_id = self.car_id +1
            
          
        return self.autos_detectados

