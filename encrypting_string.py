from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open('/home/zeefu/Documents/Volt/private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
                key_file.read(),
                password = b'test',
                backend = default_backend()
    )


with open('/home/zeefu/Documents/Volt/public_key.pem', 'rb') as key_file:
    public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend = default_backend()
    )

message = b'an attempt to encrypt'

encrypted = public_key.encrypt(
            message,
            padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label=None
        )
    )


print(encrypted)

original_message = private_key.decrypt(encrypted, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
    )
)

print(original_message)

key_file.close()
key_file.close()
