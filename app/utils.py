import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

UPLOAD_PATH = 'app/documents'


# def encrypt_file(input_file, output_file, key):
def encrypt_file(key, document, path):
    # Convert the key to bytes (UTF-8 encoded)
    key = key.encode('utf-8')

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(AES.block_size)

    # Create an AES cipher object for encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plain_data = document
    padded_data = pad(plain_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    with open(path, 'wb') as f:
        f.write(iv)
        f.write(encrypted_data)
    

# def decrypt_file(input_file, output_file, key):
def decrypt_file(key, path):
    
    with open(path, 'rb') as f:
            iv = f.read(AES.block_size)
            encrypted_data = f.read()
            
    try:
        # Convert the key to bytes (UTF-8 encoded)
        key = key.encode('utf-8')

        # Create an AES cipher object for decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = unpad(decrypted_data, AES.block_size)

        return unpadded_data, False
    except Exception as e:
        return encrypted_data, True