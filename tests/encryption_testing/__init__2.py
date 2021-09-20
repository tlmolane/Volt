import os
import sys
sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath("../../.."))
from Volt import password_hex
from Volt import key_sorting
import traceback
import argparse
import getpass
import logging
import pickle
import shutil
import json
import time
import re


from Volt import volt_encrypt

def encrypt_file_content(public_key_path, full_file_path, save_path,
                             fernet_key_encryption=False, replace=False,
                             file_type='document'):

        try:

            if fernet_key_encryption:
                print("[INFO] Warning: symmetric encryption using '{}'".format(public_key_path))
                #public_key_path = fernet_key_encryption[1]
            else:
                print("[INFO] Warning: asymmetric encryption using public key '{}'".format(public_key_path))


            if not (os.path.exists(public_key_path) and os.path.exists(full_file_path)):
                raise FileNotFoundError("[INFO] FileNotFoundError: {} or {} does not exist".format(public_key_path, full_file_path))

            file_name_ext = full_file_path.split('/')[-1]

            if file_name_ext.count('.') == 1:
                file_name, ext = file_name_ext.split('.')
            elif file_name_ext.count('.') > 1:
                ext = file_name_ext.split('.')[-1]
                file_name = re.sub(r'.{}$'.format(ext), '', file_name_ext)
            else:
                ext = ''
                file_name = file_name_ext.split('.')[-1]


            if ext not in Volt.files_dict[file_type]:
                raise Exception("[Custom Exception] File type extention '{}' not found in '{}' dict key".format(ext, file_type))

            with open(public_key_path, 'rb') as key_file:
                #print(public_key_path)

                if not fernet_key_encryption:
                    public_key = serialization.load_pem_public_key(
                                key_file.read(),
                                backend = default_backend()

                            )
                elif fernet_key_encryption:
                    key = key_file.read() #this is bytes!

            if not replace:

                new_file_name = key_sorting.new_file_name(file_name, save_path, path_pattern='_%s', ext=ext)

                with open(full_file_path, 'rb') as file:
                    data = file.read()
                file.close()


                with open(os.path.join(save_path, new_file_name), 'wb') as new_file:


                    if not fernet_key_encryption: # encrypt new file using public key

                        encrypted_data = public_key.encrypt(
                                    data,
                                    padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm = hashes.SHA256(),
                                    label=None
                                )
                        )

                        # you can append hmac here
                        new_file.write(encrypted_data)
                        print("[INFO] encrypted file {} saved".format(os.path.join(save_path, new_file_name)))

                    elif fernet_key_encryption: # encrypt new file  using fernet key
                        fernet_cipher = Fernet(key.decode())
                        encrypted_data = fernet_cipher.encrypt(data)

                        new_file.write(encrypted_data)
                        print("[INFO] fernet encrypted file {} saved".format(os.path.join(save_path, new_file_name)))
                
                return encrypted_data


            else:

                with open(os.path.join(full_file_path), 'rb') as file:
                    data = file.read()
                file.close()

                os.remove(full_file_path)

                with open(os.path.join(full_file_path), 'wb') as file:
                    #data = file.read()
                    #file.seek(0)

                    #print(fernet_key_encryption)
                    if not fernet_key_encryption:
                        encrypted_data = public_key.encrypt(
                                    data,
                                    padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm = hashes.SHA256(),
                                    label=None
                                )
                        )
                        # you can append hmac here
                        file.write(encrypted_data)

                        print("[INFO] encrypted file {} saved".format(os.path.join(save_path, file_name)))

                    elif fernet_key_encryption:
                        print("gets here")
                        fernet_cipher = Fernet(key.decode())
                        encrypted_data = fernet_cipher.encrypt(data)

                        file.write(encrypted_data)

                        print("[INFO] fernet encrypted file {} saved".format(os.path.join(save_path, file_name)))
                        # you can append hmac here
                    
                return encrypted_data


        except Exception:
            return logging.error(traceback.format_exc())


