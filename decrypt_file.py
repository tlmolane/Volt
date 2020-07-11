from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import json
import traceback
import logging


# with open('/home/zeefu/Documents/Volt/{}'.format(file_name), 'rb') as f:
#     accounts_byte = pickle.load(f)
# f.close()
#
#
# print(accounts_byte)

try:

    try:

        with open('/home/zeefu/Desktop/private_key.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password = b'apexsingularityMIM',
                        backend = default_backend()
            )
    except ValueError as e:
        print("gets here")
        logging.error(traceback.format_exc())
        print(str(e) == 'Bad decrypt. Incorrect password?')
    except TypeError as e:
        #logging.error(traceback.format_exc())
        if str(e) == 'Password was given but private key is not encrypted.':
            print(True)

except Exception as e:
    print("gets here_2")
    logging.error(traceback.format_exc())
    print(e)

#
#
# decrypted = private_key.decrypt(accounts_byte, padding.OAEP(
#                     mgf=padding.MGF1(algorithm=hashes.SHA256()),
#                     algorithm=hashes.SHA256(),
#                     label=None
#     )
# )
#
# key_file.close()
#
# print(decrypted.decode('utf-8'))
#
# decrypted_dictionary = json.loads(decrypted.decode('utf-8'))
# print(decrypted_dictionary)
