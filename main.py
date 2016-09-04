import record
import re
import festival
import json
import time
import totext
import awsiot
import RPi.GPIO as gpio

BUTTONPIN = 12
MICDEVICE = 2
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(BUTTONPIN, gpio.IN)

def is_button_pressed():
    return gpio.input(BUTTONPIN)

def wait_until_release_button():
    while is_button_pressed():
        time.sleep(0.016)

def wait_until_push_button():
    while not is_button_pressed():
        time.sleep(0.016)

if __name__ == '__main__':
    while True:
        rec = record.Recorder(device=MICDEVICE, nChannel=1, framerate=44100, nFramePerBuffer=4096)

        wait_until_push_button()
        rec.start()

        wait_until_release_button()
        rec.end()
        timestamp = time.time()
        audio = rec.close()
        text = totext.main(audio, framerate=44100)

        print(text)
        if text:
            awsiot.mqtt.publish("bookmark_memo", json.dumps({
                "timestamp": timestamp,
                "content": text
            }), 1)
            if re.compile(r'^[sS]earch .*$').match(text):
                print(text)
                festival.sayText(text)
        else:
            festival.sayText("Sorry?")
