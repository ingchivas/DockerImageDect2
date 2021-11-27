import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)

tono = GPIO.PWM(4, 100)
tono.start(50)

c = [32, 65, 131, 262, 523]
db= [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb= [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb= [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab= [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb= [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]

def escala(escala, pause):
    for i in range(0,5):
        for nota in escala:
            tono.ChangeFrequency(escala[i])
            time.sleep(pause)
    tono.stop()

starwars_notes = [c[1], g[1], f[1], e[1], d[1], c[2], g[1], f[1], e[1], d[1], c[2], g[1], 
              f[1], e[1], f[1], d[1]]
starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]

doom_notes = [e[1], e[1], b[2], e[1], e[1], a[2], e[1], e[1], g[2], e[1], e[1], gb[2], e[1], e[1], gb[2], g[2],
              e[1], e[1], b[2], e[1], e[1], a[2], e[1], e[1], g[2], e[1], e[1], gb[2]]
doom_beats = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4]

def reproducir(notas, beats, tempo):
    tono.ChangeDutyCycle(50)
    for i in range(0, len(notas)):
        tono.ChangeFrequency(notas[i])
        time.sleep(beats[i] * tempo)
    tono.ChangeDutyCycle(0)

def alarmaStarWars():
    reproducir(starwars_notes, starwars_beats, 0.2)

def alarmaDoom():
    reproducir(doom_notes, doom_beats, 0.15)

#alarmaStarWars()
#alarmaDoom()