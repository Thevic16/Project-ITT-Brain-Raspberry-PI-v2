# Modules for Speech Recognition ------------------------------------------------------------
import json
# Import Speech Recognition Module.
import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

# Defining Queue that will be use in the Speech Recognition
import wheelchair_serial_ports
from wheelchair_api_rest_request_thread import api_rest_request_thread
from wheelchair_gprs import send_GPRS_SMS, send_GPRS_FallEvent, test_GPRS_connection

q = queue.Queue()


# Functions that will be use in the Speech Recognition module
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def speech_recognition_thread():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)

    try:
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            print("Please download a model for your language from https://alphacephei.com/vosk/models")
            print("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            # Defining variable to compare
            text_str = ""
            past_text_str = ""
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    text_str = str(json.loads(rec.Result() + "")['text'])
                    # print("Mensaje voz: "+text_str)
                else:
                    text_str = str(json.loads(rec.PartialResult() + "")['partial'])
                    # print("Mensaje voz: "+text_str)
                if dump_fn is not None:
                    dump_fn.write(data)

                if text_str != past_text_str:
                    # Conditions.
                    if "sofía" in text_str and "delante" in text_str:
                        wheelchair_serial_ports.serialPortSTM32.write(b"w \r\n")
                        print("Comando de voz hacia adelante")
                    elif "sofía" in text_str and "derecha" in text_str:
                        wheelchair_serial_ports.serialPortSTM32.write(b"d \r\n")
                        print("Comando de voz hacia la derecha")
                    elif "sofía" in text_str and "atrás" in text_str:
                        wheelchair_serial_ports.serialPortSTM32.write(b"s \r\n")
                        print("Comando de voz hacia atras")
                    elif "sofía" in text_str and "izquierda" in text_str:
                        wheelchair_serial_ports.serialPortSTM32.write(b"a \r\n")
                        print("Comando de voz hacia la izquierda")
                    elif ("sofía" in text_str and "deten" in text_str) or (
                            "sofía" in text_str and "párate" in text_str) or (
                            "sofía" in text_str and "alto" in text_str):
                        wheelchair_serial_ports.serialPortSTM32.write(b"x \r\n")
                        print("Comando de voz detener silla")

                past_text_str = text_str


    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))