import os
from dotenv import load_dotenv
import time
import cv2
import numpy as np
from datetime import datetime, timedelta
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import buzzer

load_dotenv() 

buzzer.alarmaDoom()

PORT = 465
PASSWD = os.environ['EMAILSECRET']
print(PASSWD)
SENDER_EMAIL = os.environ['SENDEREMAIL']
RECIEVE_EMAIL = os.environ['EMAIL']

first_email = True

last_email = datetime.now()

def send_message():
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIEVE_EMAIL
    msg['Subject'] = "Movement Alert"
    body = "Movement Detected"
    bodyHTML = """
    <html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
<style>
		* {
			box-sizing: border-box;
		}

		body {
			margin: 0;
			padding: 0;
		}

		a[x-apple-data-detectors] {
			color: inherit !important;
			text-decoration: inherit !important;
		}

		#MessageViewBody a {
			color: inherit;
			text-decoration: none;
		}

		p {
			line-height: inherit
		}

		@media (max-width:520px) {
			.icons-inner {
				text-align: center;
			}

			.icons-inner td {
				margin: 0 auto;
			}

			.row-content {
				width: 100% !important;
			}

			.stack .column {
				width: 100%;
				display: block;
			}
		}
	</style>
 <script>
 function getCurrentTime() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    var time = hours + ":" + minutes + ":" + seconds;
    return time;
}
</script>
</head>
<body style="background-color: #FFFFFF; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
<tbody>
<tr>
<td class="column" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td style="width:100%;padding-right:0px;padding-left:0px;">
<div align="center" style="line-height:10px"><img src="https://mbgrp.com.mx/images/Untitled-4-p-1600.png" style="display: block; height: auto; border: 0; width: 150px; max-width: 100%;" width="150"/></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
<tbody>
<tr>
<td class="column" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="heading_block" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td style="width:100%;text-align:center;">
<h1 style="margin: 0; color: #555555; font-size: 23px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; line-height: 120%; text-align: center; direction: ltr; font-weight: normal; letter-spacing: normal; margin-top: 0; margin-bottom: 0;"><strong>Motion Alert</strong></h1>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
<tbody>
<tr>
<td class="column" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td>
<div style="font-family: sans-serif">
<div style="font-size: 14px; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
<p style="margin: 0; font-size: 14px;">We have detected movement.</p>
<p style="margin: 0; font-size: 14px;">Timestamp:</p> """ + str(datetime.now()) + """</p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
<tbody>
<tr>
<td class="column" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td style="color:#9d9d9d;font-family:inherit;font-size:15px;padding-bottom:5px;padding-top:5px;text-align:center;">
<table cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td style="text-align:center;">
<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
<!--[if !vml]><!-->
<table cellpadding="0" cellspacing="0" class="icons-inner" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;">
<!--<![endif]-->
<tr>
<td style="text-align:center;padding-top:5px;padding-bottom:5px;padding-left:5px;padding-right:6px;"><a href="https://mbgrp.com.mx"><img align="center" alt="MBGRP" class="icon" height="32" src="https://mbgrp.com.mx/images/Untitled-4-p-1600.png" style="display: block; height: auto; border: 0;" width="34"/></a></td>
<td style="font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:15px;color:#9d9d9d;vertical-align:middle;letter-spacing:undefined;text-align:center;"><a href="https://mbgrp.com" style="color:#9d9d9d;text-decoration:none;">By: MBGRP</a></td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>
</html>
    """
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(bodyHTML, 'html'))
    text = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWD)
        server.sendmail(SENDER_EMAIL, RECIEVE_EMAIL, text)

def send_email():
    time_now = datetime.now()
    global last_email
    global first_email
    if first_email == True:
        send_message()
        first_email = False
        buzzer.mentada()
    elif (last_email + timedelta(seconds=15) < time_now and first_email == False):
        send_message()
        last_email = datetime.now()
        buzzer.mentada()
    else:
        pass

static_back = None # ALMACENA LA IMAGEN DE REFERENCIA EN GRAYSCALE CON EL OBJETIVO DE DETECTAR MOVIMIENTO

listaMov = [None, None]

toM = []
v_feed = cv2.VideoCapture(0)#Creando el Feed de Video desde la cámara indexada 2

n_frameTime = 0 #Contador de frames
prevFtime = 0 #Contador de frames (ÚLTIMO FRAME)

while True:
    #Skip the first 10 seconds of the video feed
    if n_frameTime < 100:
        _, frame = v_feed.read()
        n_frameTime += 1
        prevFtime = n_frameTime
        continue
    
    check, frame = v_feed.read()
    motion = False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convirtiendo el frame a gris 
    gray = cv2.GaussianBlur(gray, (23, 23), 0)#Aplicando un filtro Gaussiano para eliminar el ruido de la imagen y mejorar la detección de movimiento con kernel de tamaño 23x23

    if static_back is None:
        static_back = gray #Almacenando la imagen de referencia
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