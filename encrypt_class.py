from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import argparse
import getpass
import pickle
import json
import sys
import os

class Volt:

    abs_path = os.path.dirname(os.path.abspath(__file__))

    account_types = ["social", "banking", "development", "cloud", "personal", "other"]

    def __init__(self, first, last):

        self.first = first
        self.last = last
        #self.account = account_type
        self.path = os.path.join(Volt.abs_path,  "{}_{}".format(self.first.lower(),
                    self.last.lower()))

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def volt_exists(self):
        if os.path.exists(self.path):
            return True
        else:
            #print(os.path.exists(os.path.join(self.path)))
            return False


    def create_keys(self, save_path, private_key_name = 'private_key.pem', public_key_name = 'public_key.pem' ,
                    privatekey_password = None, encryption = False, replace = False, pb_exp = 65537, ky_size = 4096):

        try:
            if replace != False:
                print("[deleting existing keys...]")
        except Exception as e:
            raise
            return

        try:

            if self.volt_exists() == True:

                private_key = rsa.generate_private_key(
                                public_exponent = pb_exp,
                                key_size = ky_size,
                                backend = default_backend()

                )

                public_key = private_key.public_key()

                if encryption == True and private_key_name != None:

                    pem = private_key.private_bytes(
                                    encoding = serialization.Encoding.PEM,
                                    format = serialization.PrivateFormat.PKCS8,
                                    #encryption_algorithm = serialization.BestAvailableEncryption(b'test')
                                    encryption_algorithm=serialization.BestAvailableEncryption(b'%b' % privatekey_password.encode('utf-8'))
                    )

                else:
                    #print("gets here when encryption is false")
                    "Private key"
                    pem = private_key.private_bytes(
                                    encoding = serialization.Encoding.PEM,
                                    format = serialization.PrivateFormat.PKCS8,
                                    #encryption_algorithm = serialization.BestAvailableEncryption(b'test')
                                    #encryption_algorithm=serialization.BestAvailableEncryption(b'%b' % privatekey_password.encode('utf-8'))
                                    encryption_algorithm=serialization.NoEncryption()
                    )

                    "Public key"
                    pem_2 = public_key.public_bytes(
                                    encoding = serialization.Encoding.PEM,
                                    format = serialization.PublicFormat.SubjectPublicKeyInfo
                    )

                with open(os.path.join(save_path, private_key_name), 'wb') as f:
                    f.write(pem)
                f.close()

                with open(os.path.join(save_path, public_key_name), 'wb') as f:
                    f.write(pem_2)
                f.close()


                return

            else:
                print("volt does not exist")
                return None


        except Exception as e:
            print(e)
            return None




    def create_volt(self ,type):
        try:
            #print(os.path.join(user_path))
            if type.lower() in Volt.account_types:
                os.mkdir(self.path)
                os.mkdir(os.path.join(self.path, type))
                return "[INFO] Volt type '{}' created".format(type)
            else:
                os.mkdir(self.path)
                os.mkdir(os.path.join(self.path, type))
                return  "[INFO] Volt created under {}".format("other")
        except FileExistsError:
            return "[INFO] {} Volt for {} {} already exists".format(type, self.first, self.last)







volt_1 = Volt('Tshepo', 'Molane')

print(volt_1.fullname)
print(volt_1.path)
#print(volt_1.create_volt('social'))
print(Volt('Tshepo', 'Molane').volt_exists())

#volt_1.create_keys(save_path = '/home/zeefu/Desktop', encryption=False)
