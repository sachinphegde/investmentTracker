#!/usr/bin/env python3

"""
utils.py
---------

Utility functions

Functions:
- generate_key: Brief description of what the function does.
- load_key:
- encrypt_file: 
- decrypt_file:
"""

from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open('secret.key', 'rb').read()

def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(f'{file_path}.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(encrypted_file_path, output_file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_file_path, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(output_file_path, 'wb') as dec_file:
        dec_file.write(decrypted)
