# Defining Thread for API REST REQUEST.
import wheelchair_gps
import wheelchair_serial_ports
from wheelchair_gprs import send_GPRS_SMS, send_GPRS_FallEvent

# Import picamara from PiCamara module.
from picamera import PiCamera
import json
# Importing time.
import time
# Importing base64 (encoding and decoding functionality).
import base64
# Import date class from datetime module.
from datetime import date
# Import the entire datetime module.
from datetime import datetime
#Import geocoder module.
import geocoder
#Import modulo to ensure internet conection
import urllib.request
# Import requests to make HTTP requests.
import requests

#Defining fuction to know if there is internet conexion.
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        print("Internet connection")
        return True
    except Exception as E:
        print("No Internet connection")
        return False


def api_rest_request_thread():
    while (True):
        try:
            # If a fall event is receive.
            messageSTM32 = wheelchair_serial_ports.serialPortSTM32.readline()
            # print(messageSTM32)
            if (messageSTM32 == b'Fall Event \n'):
                # PiCamara -----------------------------------------------------------------------------------
                print("Fall Event have been detected. \n")

                camera = PiCamera()  # Start PiCamara.
                camera.resolution = (460, 340)  # setup resolution
                time.sleep(2)  # Delay to give time to the module to start.
                camera.capture("/home/pi/Pictures/fallEvent.jpg")  # Capture a image and then save it.

                # Base64 encode and decode -------------------------------------------------------------------

                image = open('/home/pi/Pictures/fallEvent.jpg', 'rb')  # Open the image from the path saved before.
                image_read = image.read()
                image_64_encode = base64.b64encode(image_read)  # Encode the image in bytes in format Base64.
                photo = image_64_encode.decode('ascii')  # Decode the image from bytes Base64 to text Base64.
                # print(photo) #check that everything is ok.

                # Preparing to obtain hour.
                dt = datetime.now()

                # Defining parameter Json
                username = "usuariosilla1"
                password = "12345678"

                try:
                    # Verify the module GPS resturn data
                    location = wheelchair_gps.get_location()
                    latitude = location[0]
                    longitude = location[1]
                except:
                    # Preparing to obtain localization by ip address.
                    myloc = geocoder.ip('me')  # Get coordinate base on ip address.
                    latitude = myloc.lat
                    longitude = myloc.lng
                    

                dataTime = str(date.today())
                hour = dt.strftime("%H:%M")

                # True: There is internet connection, false: There is not
                if connect():
                    # Make HTTP request to the API-REST aplication of the project.
                    response = requests.post('http://telecos.me/api/FallEvent', json={
                        "username": username,
                        "password": password,
                        "photo": "data:image/jpeg;base64," + photo,
                        "latitude": latitude,
                        "longitude": longitude,
                        "dateTime": dataTime,
                        "hour": hour
                    })

                    dataFromServer = json.loads(response.json() + "")

                    print(dataFromServer)

                    for phoneNumber in dataFromServer["numbers"]:
                        send_GPRS_SMS(phoneNumber, dataFromServer["username"], dataFromServer["name"],
                                      dataFromServer["lastname"], latitude, longitude)

                else:
                    dataFromServer = json.loads(
                        send_GPRS_FallEvent(username, password, latitude, longitude, dataTime, hour))
                    for phoneNumber in dataFromServer["numbers"]:
                        send_GPRS_SMS(phoneNumber, dataFromServer["username"], dataFromServer["name"],
                                      dataFromServer["lastname"], latitude, longitude)

                # Close camara.
                camera.close()
                time.sleep(600)  # Delay to avoid over messages to the page.

        # Handle errors.
        except Exception as ex:
            print("Error occured trying to do API-REST-Request: \n")
            print(ex)