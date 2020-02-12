from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle
import json

file_name = 'passwords.pickle'

with open('/home/zeefu/Documents/Volt/{}'.format(file_name), 'rb') as f:
    accounts_byte = pickle.load(f)
f.close()


print(accounts_byte)


with open('/home/zeefu/Documents/Volt/private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
                key_file.read(),
                password = b'test',
                backend = default_backend()
    )
#
#
decrypted = private_key.decrypt(accounts_byte, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
    )
)

key_file.close()

print(decrypted.decode('utf-8'))

decrypted_dictionary = json.loads(decrypted.decode('utf-8'))
print(decrypted_dictionary)
