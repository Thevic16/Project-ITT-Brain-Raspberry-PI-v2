# importing module of wheelchair-serial_ports
import wheelchair_serial_ports
from wheelchair_serial_ports import serialPortGPRS
# Importing time.
import time
import json
# Module that helps to send SMS message.
from curses import ascii

# Transmitting AT Commands to the Modem
def test_GPRS_connection():
    serialPortGPRS.write(b'AT\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'ATI\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+GMM\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+COPS?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+COPS=0\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CFUN?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CSQ\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CSCS="IRA"\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CSCS?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CREG?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CSCA?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)


def send_GPRS_FallEvent(username,password,latitude,longitude,dataTime,hour):
    serialPortGPRS.write(b'AT+SAPBR=3,1,"Contype","GPRS"\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+SAPBR=3,1,"APN","internet.ideasclaro.com.do"\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+CGREG?\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+SAPBR=1,1\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+SAPBR=2,1\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPINIT\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPPARA="CID",1\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPSSL=0\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPPARA="URL","http://telecos.me/api/FallEvent"\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPPARA="CONTENT","application/json"\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    serialPortGPRS.write(b'AT+HTTPDATA=10000,10000\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    #"data:image/jpeg;base64," + photo
    data = {
        "username": username,
        "password": password,
        "photo": "",
        "latitude": latitude,
        "longitude": longitude,
        "dateTime": dataTime,
        "hour": hour
    }
    json_send = json.dumps(data).encode()
    serialPortGPRS.write(json_send+b'')
    time.sleep(11)
    rcv =serialPortGPRS.readall()
    print(rcv)
    time.sleep(5)
    serialPortGPRS.write(b'AT+HTTPACTION=1\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    time.sleep(20)
    serialPortGPRS.write(b'AT+HTTPREAD\r\n')
    rcv =serialPortGPRS.readall()
    print(rcv)
    time.sleep(5)
    rcv = rcv.decode()
    rcv = rcv[rcv.find('{'):]
    rcv = rcv.replace('\\',"")
    clean_json = rcv[:rcv.index('"\r\n')]
    print(clean_json)
    return clean_json


def send_GPRS_SMS(num,username,name,lastname,latitute,longitude):
    time.sleep(15)
    serialPortGPRS.write(b'AT+CMGF=1\r\n')
    time.sleep(1)
    serialPortGPRS.write(b'AT+CMGS="' + num.encode() + b'"\r')
    output = "Se ha detectado una posible caida! \n"+"Informacion del usuario de la silla de ruedas:\n"+"Usuario: "+username+"\n"+"Nombre: "+name+"\n"+"Apellido: "+lastname+"\n"+"Para ver la ubicacion acceda al siguiente enlace:\n"+"https://www.google.com/maps/search/?api=1&query="+str(latitute)+","+str(longitude)+" \n"+"Para mas informacion visitar el sitio web https://telecos.me/ o revisar su correo electronico asociado a la aplicacion."
    rcv =serialPortGPRS.readall()
    print(rcv)
    time.sleep(1)
    serialPortGPRS.write(output.encode() + b"\r")
    time.sleep(1)
    serialPortGPRS.write(ascii.ctrl('z').encode())
    time.sleep(1)
    print(wheelchair_serial_ports.serialPortGPRS.readall())
    time.sleep(1)
    print("message to "+num+" have been sent")