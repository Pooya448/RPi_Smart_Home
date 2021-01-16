TOKEN = '1408435159:AAE6P_WYThTl8O2ldqheabyrg_iOUOtkZnk'
import telebot
import RPi.GPIO as GPIO
import time
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


bot = telebot.TeleBot(TOKEN)

MATRIX_FLAG = False
LAST_TEXT = ""

STATUS = {"RELAY1": False,
          "RELAY2": False,
          "RELAY3": False,
          "RELAY4": False}

PIN = {"RELAY1": 32,
       "RELAY2": 36,
       "RELAY3": 38,
       "RELAY4": 40}

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

to use Raspberry Pi board pin numbers
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
    print('duh')
    while is_scrolling:
        with canvas(virtual) as draw:
            # show_message(device, text, fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)



@bot.message_handler(commands=['start'])
def start_command(message):
   global MATRIX_FLAG
   MATRIX_FLAG = False
   bot.send_message(
       message.chat.id,
       'Greetings! I can help ypu control your\n' +
       'home appliances through telegram!\n\n' +
       'To get help press /help.'
   )


@bot.message_handler(commands=['help'])
def help_command(message):
   global MATRIX_FLAG
   MATRIX_FLAG = False
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.row(
     telebot.types.InlineKeyboardButton(
         'Message the developer', url='telegram.me/Pooya448'
     )
   )
   keyboard.row(
     telebot.types.InlineKeyboardButton(
         'Message the developers Bitch', url='telegram.me/Alireza1044'
     )
   )
   keyboard.row(
     telebot.types.InlineKeyboardButton(
         'Message the developers Sex toy', url='telegram.me/Movahed708'
     )
   )

   bot.send_message(
       message.chat.id,
       'To modify a device connected to relay number n\n' +
       'please use the corresponding command from\n' +
       'the command list',
       reply_markup=keyboard
   )

@bot.message_handler(commands=['relay1'])
def r1_command(message):
    global MATRIX_FLAG, STATUS
    MATRIX_FLAG = False
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Toggle', callback_data='r1-tg')
    )
    keyboard.row(
    telebot.types.InlineKeyboardButton('OFF', callback_data='r1-off'),
    telebot.types.InlineKeyboardButton('ON', callback_data='r1-on')
    )

    bot.send_message(message.chat.id, 'You are modifying Relay1.\n' + 'Relay 1 status: '+ ps('RELAY1') + '\nClick on the action of choice:', reply_markup=keyboard)

@bot.message_handler(commands=['relay2'])
def r2_command(message):
    global MATRIX_FLAG, STATUS
    MATRIX_FLAG = False
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Toggle', callback_data='r2-tg')
    )
    keyboard.row(
    telebot.types.InlineKeyboardButton('OFF', callback_data='r2-off'),
    telebot.types.InlineKeyboardButton('ON', callback_data='r2-on')
    )

    bot.send_message(message.chat.id, 'You are modifying Relay2.\n' + 'Relay 2 status: '+ ps('RELAY2') + '\nClick on the action of choice:', reply_markup=keyboard)

@bot.message_handler(commands=['relay3'])
def r3_command(message):
    global MATRIX_FLAG, STATUS
    MATRIX_FLAG = False
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
       telebot.types.InlineKeyboardButton('Toggle', callback_data='r3-tg')
    )
    keyboard.row(
     telebot.types.InlineKeyboardButton('OFF', callback_data='r3-off'),
     telebot.types.InlineKeyboardButton('ON', callback_data='r3-on')
    )

    bot.send_message(message.chat.id, 'You are modifying Relay3.\n' + 'Relay 3 status: '+ ps('RELAY3') + '\nClick on the action of choice:', reply_markup=keyboard)

@bot.message_handler(commands=['relay4'])
def r4_command(message):
    global MATRIX_FLAG, STATUS
    MATRIX_FLAG = False
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Toggle', callback_data='r4-tg')
    )
    keyboard.row(
      telebot.types.InlineKeyboardButton('OFF', callback_data='r4-off'),
      telebot.types.InlineKeyboardButton('ON', callback_data='r4-on')
    )

    bot.send_message(message.chat.id, 'You are modifying Relay4.\n' + 'Relay 4 status: '+ ps('RELAY4') + '\nClick on the action of choice:', reply_markup=keyboard)

@bot.message_handler(commands=['display'])
def disp_command(message):
    global MATRIX_FLAG
    MATRIX_FLAG = True
    bot.send_message(message.chat.id, 'Please send me a text\nto display on MATRIX!')

@bot.message_handler(commands=['status'])
def status_command(message):
    global MATRIX_FLAG, STATUS
    MATRIX_FLAG = False

    bot.send_message(message.chat.id, status_message_const())

def status_message_const():
    global text
    message_to_send = 'Relay 1: ' + ps('RELAY1') + '\n' + 'Relay 2: ' + ps('RELAY2') + '\n' + 'Relay 3: ' + ps('RELAY3') + '\n' + 'Relay 4: ' + ps('RELAY4') + '\n' + 'Message on matrix:\n' + text
    return message_to_send

def ps(key):
    global STATUS
    if STATUS[key]:
        return 'ON'
    else:
        return 'OFF'

@bot.callback_query_handler(func=lambda call: True)
def ik_callback(query):
    multiplex_query(query)

def multiplex_query(query):
    data = query.data
    if data.startswith('r1-'):
        Relay('RELAY1', query.message, query.data[3:])
    elif data.startswith('r2-'):
        Relay('RELAY2', query.message, query.data[3:])
    elif data.startswith('r3-'):
        Relay('RELAY3', query.message, query.data[3:])
    elif data.startswith('r4-'):
        Relay('RELAY4', query.message, query.data[3:])
    bot.answer_callback_query(query.id)


def Relay(key, message, op_code):
    bot.send_chat_action(message.chat.id, 'typing')
    n = key[-1]
    if op_code == 'tg':
        last = ps(key)
        toggle_pin(key)
        now = ps(key)
        msg = 'Relay ' + n + ' toggled\n' +  'Status: ' + last + ' -> ' + now
        bot.send_message(message.chat.id, msg)

    elif op_code == 'on':
        last = ps(key)
        on(key)
        now = ps(key)
        msg = 'Relay ' + n + ' turned ON\n' +  'Status: ' + last + ' -> ' + now
        bot.send_message(message.chat.id, msg)

    elif op_code == 'off':
        last = ps(key)
        off(key)
        now = ps(key)
        msg = 'Relay ' + n + ' turned OFF\n' +  'Status: ' + last + ' -> ' + now
        bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda message: True)
def global_maessage(message):
  global MATRIX_FLAG
  global text, is_scrolling, is_first_time

  if MATRIX_FLAG:
      text = message.text
      if '/' not in text:
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
          bot.send_message(message.chat.id, 'Your text is scrolling on LED Dot Matrix.')
      MATRIX_FLAG = False
  else:
      bot.send_message(message.chat.id, 'Say what?')


bot.polling(none_stop=True)
