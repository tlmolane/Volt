from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


private_key = rsa.generate_private_key(
                public_exponent = 65537,
                key_size = 4096,
                backend = default_backend()
)

public_key = private_key.public_key()

pem = private_key.private_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PrivateFormat.PKCS8,
                #encryption_algorithm = serialization.BestAvailableEncryption(b'test')
                encryption_algorithm=serialization.BestAvailableEncryption(b'test')
                #encryption_algorithm=serialization.NoEncryption()
)

pem_2 = public_key.public_bytes(
                encoding = serialization.Encoding.PEM,
                format = serialization.PublicFormat.SubjectPublicKeyInfo
)


# for i in pem.splitlines():
#     print(i)


with open('/home/zeefu/Documents/Volt/private_key.pem', 'wb') as f:
    f.write(pem)
f.close()
#
with open('/home/zeefu/Documents/Volt/public_key.pem', 'wb') as f:
    f.write(pem_2)
f.close()



#
# with open('/home/zeefu/private_key.pem', 'rb') as f:
#     private_key = serialization.load_pem_private_key(
#                 f.read(),
#                 password = b'test',
#                 backend = default_backend()
#     )
