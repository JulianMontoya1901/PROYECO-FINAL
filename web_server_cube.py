from machine import Pin, PWM
from time import sleep
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket
from machine import Pin
import utime
from machine import Pin, I2C
import ssd1306
import math

L11 = Pin(19, Pin.OUT)
L12 = Pin(18, Pin.OUT)
L21 = Pin(17, Pin.OUT)
L22 = Pin(16, Pin.OUT)
servo1 = Pin(13, Pin.OUT)
servo2 = Pin(12, Pin.OUT)
motor_pin1 = Pin(20, Pin.OUT) # Por ejemplo, GPIO 6
motor_pin2 = Pin(21, Pin.OUT)

# Configuración del I2C para la pantalla OLED
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# Inicialización de la pantalla OLED (128x64)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Valores iniciales para las ruedas
velocidad_rueda_derecha = 0
velocidad_rueda_izquierda = 0
nivel_bateria = 100

v_i = 0
v_d = 0

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = 'moto_g52'
pw = 'mateus07'

wlan.connect(ssid, pw)



# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)


    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed ',wlan_status)
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# pantalla

# Función para dibujar un círculo
def dibujar_circulo(oled, x0, y0, radio):
    x = radio
    y = 0
    err = 0

    while x >= y:
        oled.pixel(x0 - x, y0 - y, 1)
        oled.pixel(x0 - y, y0 - x, 1)
        oled.pixel(x0 + y, y0 - x, 1)
        oled.pixel(x0 + x, y0 - y, 1)
        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

# Función para dibujar una línea desde el centro del velocímetro
def dibujar_lineas(oled, x0, y0, length, angle):
    x1 = int(x0 + length * math.cos(math.radians(angle)))
    y1 = int(y0 + length * math.sin(math.radians(angle)))
    oled.line(x0, y0, x1, y1, 1)
    
def lineas_cortas(oled, x0, y0, radio_interior, radio_exterior, angle):
    x1 = int(x0 + radio_interior * math.cos(math.radians(angle)))
    y1 = int(y0 + radio_interior * math.sin(math.radians(angle)))
    x2 = int(x0 + radio_exterior * math.cos(math.radians(angle)))
    y2 = int(y0 + radio_exterior * math.sin(math.radians(angle)))
    oled.line(x1, y1, x2, y2, 1)

# Función para dibujar la batería
def dibujar_bateria(oled, x, y, ancho, altura, level):
    # Dibujar el contorno de la batería
    oled.rect(x, y, ancho, altura, 1)  # Contorno de la batería
    oled.rect(x + ancho, y + altura//4, 2, altura//2, 1)  # Terminal positivo
    
    # Dibujar el nivel de la batería
    inner_width = int((ancho - 2) * level / 100)
    oled.fill_rect(x + 1, y + 1, inner_width, altura - 2, 1)

# Función para mostrar el velocímetro
def mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria):
    oled.fill(0)  # Limpiar la pantalla
    
    # Dibujar el velocímetro
    centro_x, centro_y = 96, 32
    radio = 30
    
    dibujar_circulo(oled, centro_x, centro_y, radio)
    
    # Dibujar las líneas del velocímetro
    angulos = [-150, -120, -90, -60, -30]
    for angulo in angulos:
        lineas_cortas(oled, centro_x, centro_y, radio - 8, radio, angulo)
     
    # Dibujar líneas de referencia del velocímetro
    lineas_cortas(oled, centro_x, centro_y, 0, radio-25, 90)
    lineas_cortas(oled, 67, centro_y, 0, radio-25, 90)
    lineas_cortas(oled, 123, centro_y, 0, radio-25, 90)

    # Dibujar la línea horizontal en la mitad del círculo
    oled.line(centro_x - radio, centro_y, centro_x + radio, centro_y, 1)
    
    # Dibujar las agujas del velocímetro
    angulo_derecha = 180 + (180 * velocidad_rueda_derecha / 100)
    angulo_izquierda = 180 + (180 * velocidad_rueda_izquierda / 100)
    
    # Aguja para la rueda derecha
    dibujar_lineas(oled, centro_x, centro_y, radio-1, angulo_derecha)
    
    # Aguja para la rueda izquierda (más corta)
    dibujar_lineas(oled, centro_x, centro_y, radio - 10, angulo_izquierda)
    
    # Dibujar la batería
    dibujar_bateria(oled, 0, 0, 20, 10, nivel_bateria)
    
    oled.show()  # Actualizar la pantalla OLED con los dibujos
   
    # Porcentaje batería
    oled.text('%'+str(nivel_bateria), 25, 3)
    
    # Valores referencia velocímetro
    oled.text('0', 65, 40)
    oled.text('50', 85, 40)
    oled.text('100', 105, 40)
    
    # Mostrar los valores de las ruedas
    oled.text('R.D:', 0, 40)
    oled.text(str(velocidad_rueda_derecha), 30, 40)
    oled.text('R.I:', 0, 50)
    oled.text(str(velocidad_rueda_izquierda), 30, 50)
    
    oled.show()


# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
while True:
    try:
#         pantalla
        L11.value(0)
        L12.value(0)
        L21.value(0)
        L22.value(0)

        motor_pin1.value(0)
        motor_pin2.value(0)
        velocidad_rueda_derecha = v_d
        velocidad_rueda_izquierda = v_i
        nivel_bateria = 90

        mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
        
#         pantalla

        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        adelante = r.find('?adelante')
        atras = r.find('?atras')
        derecha = r.find('?derecha')
        izquierda = r.find('?izquierda')
        baile = r.find('?bailar')
        arriba1 = r.find('?arriba1')
        arriba2 = r.find('?arriba2')
        abajo1 = r.find('?abajo1')
        abajo2 = r.find('?abajo2')
        


        if adelante > -1:
            print('adelante')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L21.value(0)
            L22.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            
            
              
        if atras > -1:
            print('atras')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L22.value(0)
            L21.value(1)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)

            
        if derecha > -1:
            print('derecha')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L21.value(1)
            L22.value(0)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
           
            
        if izquierda > -1:
            print('izquierda')
            led.value(1)
            L11.value(1)
            L12.value(0)
            L21.value(0)
            L22.value(1)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            
            
        if baile > -1:
            print('Prendiendo motor')
            motor_pin1.value(1)
            motor_pin2.value(0)
            utime.sleep(1)      # Esperar 5 segundos
            print('Apagando motor')
            motor_pin1.value(0)
            motor_pin2.value(0)


            
        if arriba1 > -1:
            pwm = PWM(servo1)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 7
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            

        if arriba2 > -1:
            pwm = PWM(servo2)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 2
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
               
        if abajo1 > -1:
            pwm = PWM(servo1)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 2
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
        if abajo2 > -1:
            pwm = PWM(servo2)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 7
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
        response = get_html('web_server_cube.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()

