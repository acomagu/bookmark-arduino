import record
import time
import totext
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
        rec = record.Recorder(device=MICDEVICE, nChannel=1, framerate=44100, nframePerBuffer=4096)
        wait_until_push_button()
        print("PUSHED")
        rec.start()
        wait_until_release_button()
        print("RELEASED")
        rec.end()
        audio = rec.close()
        text = totext.main(audio, framerate=44100)
        print(text)
