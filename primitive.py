import RPi.GPIO as GPIO
import time
import telepot
import threading
from time import sleep, strftime
from datetime import datetime

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(5)
virtual = viewport(device, width=32, height=16)
show_message(device, 'Hello World !', fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)

STATUS = {"RELAY1": False,
          "RELAY2": False,
          "RELAY3": False,
          "RELAY4": False}

PIN = {"RELAY1": 32,
       "RELAY2": 36,
       "RELAY3": 38,
       "RELAY4": 40}


# LED
def toggle_pin(pin):
    global STATUS, PIN

    if STATUS[pin]:
        GPIO.output(PIN[pin], GPIO.HIGH)
        STATUS[pin] = False
    else:
        GPIO.output(PIN[pin], GPIO.LOW)
        STATUS[pin] = True

def on(pin):
    global PIN
    GPIO.output(PIN[pin], GPIO.LOW)
    STATUS[pin] = True

def off(pin):
    global PIN
    GPIO.output(PIN[pin], GPIO.HIGH)
    STATUS[pin] = False


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
GPIO.setup(PIN["RELAY1"], GPIO.OUT)
GPIO.setup(PIN["RELAY2"], GPIO.OUT)
GPIO.setup(PIN["RELAY3"], GPIO.OUT)
GPIO.setup(PIN["RELAY4"], GPIO.OUT)

GPIO.output(PIN["RELAY1"], GPIO.HIGH)
GPIO.output(PIN["RELAY2"], GPIO.HIGH)
GPIO.output(PIN["RELAY3"], GPIO.HIGH)
GPIO.output(PIN["RELAY4"], GPIO.HIGH)

text = ""
is_scrolling = True
is_first_time = True

def scroll():
    global text
    while is_scrolling:
        with canvas(virtual) as draw:
            show_message(device, text, fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)

def handle(msg):
    global text, is_scrolling, is_first_time
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    command = str.lower(command)

    if "relay 1" in command and "off" in command:
        off("RELAY1")
        print("Relay 1 Off")
    elif "relay 2" in command and "off" in command:
        off("RELAY2")
        print("Relay 2 Off")
    elif "relay 3" in command and "off" in command:
        off("RELAY3")
        print("Relay 3 Off")
    elif "relay 4" in command and "off" in command:
        off("RELAY4")
        print("Relay 4 Off")

    elif "relay 1" in command and "on" in command:
        on("RELAY1")
        print("Relay 2 On")
    elif "relay 2" in command and "on" in command:
        on("RELAY2")
        print("Relay 3 On")
    elif "relay 3" in command and "on" in command:
        on("RELAY3")
        print("Relay 4 On")
    elif "relay 4" in command and "on" in command:
        on("RELAY4")
        print("Relay 4 On")

    elif "relay 1" in command:
        toggle_pin("RELAY1")
        print("Relay 1 Toggle")
    elif "relay 2" in command:
        toggle_pin("RELAY2")
        print("Relay 2 Toggle")
    elif "relay 3" in command:
        toggle_pin("RELAY3")
        print("Relay 3 Toggle")
    elif "relay 4" in command:
        toggle_pin("RELAY4")
        print("Relay 4 Toggle")

    else:
        if '/' not in command:
            text = command
            is_scrolling = False
            if not is_first_time:
                for thread in threading.enumerate():
                    if thread.name == "text_scroll":
                        thread.join()
            t = threading.Thread(target=scroll, name="text_scroll")
            t.daemon = True
            is_scrolling = True
            t.start()
            is_first_time = False


bot = telepot.Bot('1408435159:AAE6P_WYThTl8O2ldqheabyrg_iOUOtkZnk')
bot.message_loop(handle)
bot.deleteWebhook()
print('I am listening...')

while 1:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        print('\n Program interrupted')
        GPIO.cleanup()
        exit()

    except:
        print('Other error or exception occured!')
        GPIO.cleanup()




# try:
#     while True:
#         with canvas(virtual) as draw:
#             text(draw, (0, 1), "Idris", fill="white", font=proportional(CP437_FONT))
#             #text(draw, (0, 1), datetime.now().strftime('%I:%M'), fill="white", font=proportional(CP437_FONT))
#
# except KeyboardInterrupt:
#     GPIO.cleanup()
