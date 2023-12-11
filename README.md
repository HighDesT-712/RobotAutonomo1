# ESP32-CAM-wireless-computer-vision-persona-detection

DETECCION DE PERSONAS CON ESP-EYE | VISION ARTIFICIAL PYTHON + OpenCV 

En un robot autonomo es importante la deteccion del entorno, como la deteccion de personas , que le da una referencia de seguimiento al robot, sin embargo la deteccion a traves de sensore es insuficiente para este tipo de aplicaciones por lo que se utilizó un modelo de deteccion de objetos para su implementacion. La comunicacion y envio de datos a traves de wifi fue vital, la libreria wifi.h hace posible el envio de los frames de video captados por un ESP-EYE a una computadora en donde se le hara su respectiva deteccion de objetos con la libreria open cv , sin esto se tendria que comunicar al ESP-EYE y a la computadora a traves de un cable, lo cual le quitaria la caracteristica de "autonomo" al robot. El protocolo de comunicacion MQTT permite que la permite envie instrucciones a un ESP32_DEVKIT_V1 acorde a la posicion del centroide la persona detectado, movilizando de esa manera a traves del devkitv1 a un motor paso a paso sobre el cual se ubica una camara(ESP-EYE). El proposito final del proyecto es la implementacion de un robot que pueda seguir una línea negra en lugares como un Supermercado y a la vez detenerse cuando la persona frente a el esta muy cerca (umbral limite) para poder apoyarla en algunas funciones(carga de materiales o productos , etc) que sean de utilidad para el usuario.

# RobotAutonomo1
implementacion de robot de compras inteligente para supermercados, proyecto de Fin de Carrera ee445 , UNI


