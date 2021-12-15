#!/usr/bin/python3.7

# Import threading module.
import threading
#Module for API-REST-Request----------------------------------------------------------------
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
    
