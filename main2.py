# import RPi.GPIO as GPIO
import time
import telepot
from time import sleep, strftime
from datetime import datetime

# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.virtual import viewport
# from luma.led_matrix.device import max7219
# from luma.core.legacy import text, show_message
# from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT

# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, width=32, height=8, block_orientation=-90)
# device.contrast(5)
# virtual = viewport(device, width=32, height=16)
# show_message(device, 'Raspberry Pi MAX7219', fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)
    # text(draw, (0, 1), command, fill="white", font=proportional(CP437_FONT))

    if command == 'on':
        # bot.sendMessage(chat_id, on(11))
        bot.sendMessage(chat_id, "Kharkose Movahed")

    elif command == 'off':
        # bot.sendMessage(chat_id, off(11))
        bot.sendMessage(chat_id, "Jende Movahed")



bot = telepot.Bot('1408435159:AAE6P_WYThTl8O2ldqheabyrg_iOUOtkZnk')
bot.message_loop(handle)
print('I am listening...')

while 1:
    time.sleep(10)

    # except KeyboardInterrupt:
    #     print('\n Program interrupted')
    #     GPIO.cleanup()
    #     exit()
    #
    # except:
    #     print('Other error or exception occured!')
    #     GPIO.cleanup()

# try:
#     while True:
#         with canvas(virtual) as draw:
#             text(draw, (0, 1), "Idris", fill="white", font=proportional(CP437_FONT))
#             #text(draw, (0, 1), datetime.now().strftime('%I:%M'), fill="white", font=proportional(CP437_FONT))
#
# except KeyboardInterrupt:
#     GPIO.cleanup()
