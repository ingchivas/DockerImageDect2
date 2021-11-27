import os
from dotenv import load_dotenv
import time
import cv2
import numpy as np
from datetime import datetime, timedelta
import smtplib, ssl

load_dotenv()

PORT = 465
PASSWD = os.environ['EMAILSECRET']
print(PASSWD)
SENDER_EMAIL = os.environ['SENDEREMAIL']
RECIEVE_EMAIL = os.environ['EMAIL']

first_email = True

last_email = datetime.now()

def send_email():
    time_now = datetime.now()
    global last_email
    global first_email
    if first_email == True:
        message ="""
        Asunto: Alerta de Movimiento
        
        Motion detected at """ + str(datetime.now()) + """
        
        Nya
        """
        pasen_contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=pasen_contexto) as server:
            server.login(SENDER_EMAIL, PASSWD)
            server.sendmail(SENDER_EMAIL,RECIEVE_EMAIL,message)
            
        print("Email sent")
        last_email = datetime.now()
        first_email = False
    elif (last_email + timedelta(seconds=15) < time_now and first_email == False):
        message ="""
        Subject: Alerta de Movimiento
        
        Motion detected at """ + str(datetime.now()) + """
        
        Nya
        """
        pasen_contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=pasen_contexto) as server:
            server.login(SENDER_EMAIL, PASSWD)
            server.sendmail(SENDER_EMAIL,RECIEVE_EMAIL,message)
            
        print("Email sent")
        last_email = datetime.now()
    else:
        pass
    

static_back = None # ALMACENA LA IMAGEN DE REFERENCIA EN GRAYSCALE CON EL OBJETIVO DE DETECTAR MOVIMIENTO

listaMov = [None, None]

toM = []
v_feed = cv2.VideoCapture(0)#Creando el Feed de Video desde la cámara indexada 2

n_frameTime = 0 #Contador de frames
prevFtime = 0 #Contador de frames (ÚLTIMO FRAME)

while True:
    check, frame = v_feed.read()
    motion = False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (23, 23), 0)#Aplicando un filtro Gaussiano para eliminar el ruido de la imagen y mejorar la detección de movimiento con kernel de tamaño 21x21

    if static_back is None:
        static_back = gray
        continue

    FrameDiferencia = cv2.absdiff(static_back, gray)#calculamos la dif emtre nuestro background y el frame en grayscale
    frameThresh = cv2.threshold(FrameDiferencia, 32, 255, cv2.THRESH_BINARY)[1]#Aplicando threshold
    frameThresh = cv2.dilate(frameThresh, None, iterations = 2)#aplicamos dilatación
    
    #Calculando FPS mediante contador de frames de la diferencia entre el frame actual y el último
    n_frameTime = time.time()
    fps = np.around(1/(n_frameTime-prevFtime), 0)
    prevFtime = n_frameTime

    # Añadiendo el contador al FFED
    cv2.putText(frame, "FPS: "+str(fps), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)

    ctr,_ = cv2.findContours(frameThresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #calculamos el contorno del motiondetect usando aproximación del contorno en este caso simople, almacenamos solo los vértices para mejorar runtime
    
    #  cv2.RETR_EXTERNAL – Solo capturamos los contornos externos
    for contorno in ctr:
        if cv2.contourArea(contorno) < 10000: #si nuestro contorno es mayor a 10000 entonces:
            continue
        motion = True
        cv2.putText(frame, "Movimiento DETECTADO", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
        (x, y, w, h) = cv2.boundingRect(contorno) #Calcular el rectangulo más pequeño que contiene el contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)#Dibujamos el rectangulo en el frame
        send_email()#mandamos correo de detección de movimiento
        

    listaMov.append(motion)
    listaMov = listaMov[-2:]

    if listaMov[-1] == 1 and listaMov[-2] == 0:
        toM.append(datetime.now())
    if listaMov[-1] == 0 and listaMov[-2] == 1:
        toM.append(datetime.now())

    #FEEDS
    cv2.imshow("EscalaGrises", gray)
    cv2.imshow("FrameDelta", FrameDiferencia)
    cv2.imshow("Threshold", frameThresh)
    cv2.imshow("Feed", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion == True:
            toM.append(datetime.now())            
        break

with open('movimientos.txt', 'w') as f:
    for item in toM:
        f.write("%s\n" % item)

v_feed.release()
cv2.destroyAllWindows()