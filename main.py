import record
import totext
import RPi.GPIO as gpio

BUTTONPIN = 12
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(BUTTONPIN, gpio.IN)

def is_button_pressed():
    return gpio.input(BUTTONPIN)

def wait_until_release_button():
    while is_button_pressed():
        pass

def wait_until_push_button():
    while not is_button_pressed():
        pass

if __name__ == '__main__':
    while True:
        wait_until_push_button()
        print("PUSHED")
        wait_until_release_button()
        print("RELEASED")
    #
    # rec = record.Recorder(device=2, nChannel=1, framerate=44100, framesPerBuffer=4096)
    # text = totext.main(audio, framerate=44100)
    # print(text)
