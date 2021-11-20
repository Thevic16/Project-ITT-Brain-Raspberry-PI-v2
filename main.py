# Import threading module.
import threading
#Module for API-REST-Request----------------------------------------------------------------
# Import picamara from PiCamara module.
from picamera import PiCamera
# Importing time.
import time
# Importing base64 (encoding and decoding functionality).
import base64
# Import requests to make HTTP requests.
import requests
import json
# Import date class from datetime module.
from datetime import date
# Import the entire datetime module.
from datetime import datetime
#Import geocoder module.
import geocoder
#Import modulo to ensure internet conection
import urllib.request
# Module that helps to send SMS message.
from curses import ascii
# importing module of wheelchair-gps
import wheelchair_gps
# importing module of wheelchair-serial_ports
import wheelchair_serial_ports
from wheelchair_api_rest_request_thread import api_rest_request_thread
from wheelchair_gprs import test_GPRS_connection
from wheelchair_speech_recognition_thread import speech_recognition_thread


def main():
    test_GPRS_connection()
        
    thread1 = threading.Thread(target=api_rest_request_thread)
    
    thread2 = threading.Thread(target=speech_recognition_thread)
    
    thread1.start()
    thread2.start()
    


if __name__ == "__main__":
    main()
    
