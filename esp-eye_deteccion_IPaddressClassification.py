import cv2 #opencv
import urllib.request #para abrir y leer URL
import numpy as np
import requests
import paho.mqtt.client as mqtt
import time

#no funciona el example de esp32simpleserver, no es para mensajes, ni bidireccional, solo http y cosas internas de wifi.h
#urlesp32 = 'http://192.168.0.132/'

#urlespeye = 'http://192.168.0.210/cam-hi.jpg'   #SAMANEZ 2.4GHZ
urlespeye = 'http://192.168.190.25/cam-hi.jpg'  #redmi11

# urlbrokerwindows = '192.168.0.153'   # SAMANEZ 2.4GHZ
urlbrokerwindows= '192.168.190.61'  # REDMI11 RED

def on_connect(client, userdata, flags, rc):
    print("Conectado al servidor MQTT")
    client.subscribe("esp/test")

def on_message(client, userdata, msg):   # CUANDO RECIBE UN MENSAJE DESDE EL ESP32DEVKITV1 o desde cualquiera en el topic
    print(f"Mensaje recibido: {msg.payload.decode()}")

    # Envío de un mensaje de respuesta al ESP32

    client.publish("esp/control", "Mensaje de respuesta al ESP32")


#url = 'http://192.168.1.6/'
winName = 'ESP32 CAMERA'
cv2.namedWindow(winName,cv2.WINDOW_AUTOSIZE)
#scale_percent = 80 # percent of original size    #para procesamiento de imagen

classNames = []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
#net.setInputSize(480,480)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

client = mqtt.Client()
client.connect(urlbrokerwindows, 1883, 60) # Reemplaza con la dirección IP del ESP32
message = "izquierda" #valor inicial de la variable message para pruebas al quitar partes de codigo.


# client.loop_forever() # PARA QUE ESCUCHE TODO EL TIEMPO A LOS MENSAJES QUE VAN LLEGANDO , PERO SE QUEDA EN ESTE BUCLE
# el esp32devkitv1, indicara si necesita recibir DIRECCION o no. y el periodo de tiempo en el cual lo ira solicitando

next_publish_time = time.time() + 1  # Publicar inmediatamente en el primer ciclo

while(1):

    imgResponse = urllib.request.urlopen (urlespeye) #abrimos el URL
    imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
    img = cv2.imdecode (imgNp,-1) #decodificamos

    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # vertical
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #black and white

    # Definir los límites izquierdo y derecho de la ventana , PARA ANALITICA DE CENTROIDE
    window_left = 200
    window_right = img.shape[1] - 200  # Ancho de la imagen menos 100 píxeles

    # DETECCION
    classIds, confs, bbox = net.detect(img,confThreshold=0.5)
    print(classIds,bbox)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            if classId == 1:

                # PARAMETROS PAR CENTROIDE
                x, y, width, height = box[0], box[1], box[2], box[3]
                x_center = x + (width // 2)
                y_center = y + (height // 2)

                # Coordenadas del rectángulo
                cv2.rectangle(img,box,color=(0,255,0),thickness = 3) #mostramos en rectangulo lo que se encuentra
                cv2.putText(img, classNames[classId-1], (box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)

                # dibujo de centroide
                cv2.circle(img, (x_center, y_center), 10, (0, 255, 0), -1)



                # Determinar la posición del centroide con respecto a los límites de la ventana
                if x_center < window_left:
                    message = "izquierda"
                elif x_center > window_right:
                    message = "derecha"
                else:
                    message = "centrado"

    # que se dibuje siempre, no solo cuando detecte
    cv2.line(img, (window_left, 0), (window_left, img.shape[0]), color=(255, 0, 0),
             thickness=2)  # Umbral izquierdo
    cv2.line(img, (window_right, 0), (window_right, img.shape[0]), color=(0, 0, 255),
             thickness=2)  # Umbral derecho


    cv2.imshow(winName,img) # mostramos la imagen
    window_size = cv2.getWindowImageRect(winName)  # Obtiene las dimensiones de la ventana

    #esperamos a que se presione ESC para terminar el programa
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

    # ENVIO DE LOGICA AL ESP32DEVKITV1
    valor = 1
    # Realiza la solicitud GET con el valor como parámetro
    #url_envio = urlesp32 + str(valor)
    #url_envio = urlesp32 + "H"
    #response = requests.get(urlesp32)
    #respuesta = urllib.request.urlopen(url_envio)
    #print("envio realizado")

    if time.time() >= next_publish_time:  # cada 1 segundo ENVIARA porque asi lo determine, sino enviaria miles de veces en 1 segundo
        #client.publish("esp/control", "derecha") # retorna la direccion en la que debe girar el motor paso a paso
        client.publish("esp/control", message)  # retorna la direccion en la que debe girar el motor paso a paso
        next_publish_time = time.time() + 1  # Establece el próximo tiempo de publicación
       # print("Dimensiones de la ventana:", window_size)  #con esto confirme que el tamaño de la imagen que recibo es 600(ancho)x800(largo)

    #client.publish("esp/control", message)  # retorna la direccion en la que debe girar el motor paso a paso
    # print("Dimensiones de la ventana:", window_size)  #con esto confirme que el tamaño de la imagen que recibo es 600(ancho)x800(largo)
cv2.destroyAllWindows()
