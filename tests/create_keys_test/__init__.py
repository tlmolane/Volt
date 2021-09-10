from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os


def create_keys(private_key_name, public_key_name,
                save_path, private_key_password, serialize_encryption= True, public_exp=65537, keysize=2048):


    try:

        if serialize_encryption == True and private_key_password == None:
            raise Exception("private key password cannot be None")
        if serialize_encryption == False and private_key_password !=None:
            raise Exception("serialization with encryption is False but password is provided")

        if serialize_encryption == True and private_key_password != None:
            serialize = serialization.BestAvailableEncryption(b'%b' % private_key_password.encode('utf-8'))
        else:
            serialize = serialization.NoEncryption()


        private_key = rsa.generate_private_key(
            public_exponent=public_exp,
            key_size=keysize,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        pem = private_key.private_bytes(
                        encoding = serialization.Encoding.PEM,
                        format = serialization.PrivateFormat.PKCS8,
                        #encryption_algorithm = serialization.BestAvailableEncryption(b'test')
                        encryption_algorithm=serialize)

        "Public key"
        pem_2 = public_key.public_bytes(
                        encoding = serialization.Encoding.PEM,
                        format = serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(os.path.join(save_path, private_key_name +'.pem'), 'wb') as f:
            f.write(pem)
            f.close()


        with open(os.path.join(save_path, public_key_name + '.pem'), 'wb') as f:
            f.write(pem_2)
            f.close()

        print(os.path.exists(os.path.join(save_path,private_key_name + '.pem')))
        return os.path.exists(os.path.join(save_path,private_key_name + '.pem'))

    except Exception as e:
        print(e)
        

# abs_path = os.path.dirname(os.path.abspath(__file__))

# create_keys('test_private_key', 'test_public_key',
#                 abs_path, 'test', serialize_encryption= True)
