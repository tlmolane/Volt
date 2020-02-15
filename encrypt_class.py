from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import argparse
import getpass
import pickle
import shutil
import json
import sys
import os

class Volt:

    abs_path = os.path.dirname(os.path.abspath(__file__))

    account_types = ["social", "development", "personal", "other"]

    def __init__(self, first, last):

        self.first = first
        self.last = last
        #self.account = account_type
        self.path = os.path.join(Volt.abs_path,  "{}_{}".format(self.first.lower(),
                    self.last.lower()))
        #self.type_path = os.path.join(self.path, )

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def volt_exists(self):
        if os.path.exists(self.path):
            return True
        else:
            #print(os.path.exists(os.path.join(self.path)))
            return False

    def type_exists(self, type):
        if os.path.exists(os.path.join(self.path, type)):
            return True
        else:
            #print(os.path.exists(os.path.join(self.path)))
            return False



    def create_keys(self, save_path, type, private_key_name = 'private_key', public_key_name = 'public_key' ,  ext = '.pem',
                    privatekey_password = None, encryption = False, replace = False, pb_exp = 65537, ky_size = 4096):

        private_key_name = private_key_name + ext
        public_key_name  = public_key_name  + ext

        try:
            if replace != False:
                print("[INFO] deleting existing keys...")
                os.remove(os.path.join(self.path, type, private_key_name))
                os.remove(os.path.join(self.path, type, public_key_name))
            else:
                raise FileNotFoundError('keys do not exist')
        except Exception as e:
            print(e)
            pass

        try:

            print("[INFO]: Creating Keys...")

            if self.volt_exists() == True and self.type_exists(type) == True:

                private_key = rsa.generate_private_key(
                                public_exponent = pb_exp,
                                key_size = ky_size,
                                backend = default_backend()

                )

                public_key = private_key.public_key()

                if encryption == True and private_key_name != None:

                    "Private Key"
                    pem = private_key.private_bytes(
                                    encoding = serialization.Encoding.PEM,
                                    format = serialization.PrivateFormat.PKCS8,
                                    #encryption_algorithm = serialization.BestAvailableEncryption(b'test')
                                    encryption_algorithm=serialization.BestAvailableEncryption(b'%b' % privatekey_password.encode('utf-8'))
                    )

                    "Public key"
                    pem_2 = public_key.public_bytes(
                                    encoding = serialization.Encoding.PEM,
                                    format = serialization.PublicFormat.SubjectPublicKeyInfo
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

                with open(os.path.join(save_path, type,  private_key_name), 'wb') as f:
                    f.write(pem)
                f.close()

                with open(os.path.join(save_path, type, public_key_name), 'wb') as f:
                    f.write(pem_2)
                f.close()


                return

            else:
                raise FileNotFoundError("[INFO]: File {} does not exist".format(os.path.join(self.path, type)))
                return None


        except Exception as e:
            print(e)
            return None


    def create_volt_type(self, type="default"):

        try:
            if self.volt_exists() == True  and type.lower() != 'default':
                if type.lower() in Volt.account_types:
                    #os.mkdir(self.path)
                    os.mkdir(os.path.join(self.path, type))
                    print("[INFO] Volt type '{}' created".format(type))
                    return
                else:
                    os.mkdir(os.path.join(self.path, "other"))
                    print("[INFO] Volt type '{}' created".format(type))
                    return


            elif self.volt_exists() == False:
                if type.lower() == 'default':
                    os.mkdir(self.path)
                    #os.mkdir(os.path.join(self.path))
                    print("[INFO] Volt type '{}' created".format(type))
                    return
        except FileExistsError:
            print("[INFO] {} Volt for {} {} already exists".format(type, self.first, self.last))
            return

    def remove_volt_type(self, type="default"):

        try:
            if self.volt_exists() == True:
                    #os.mkdir(self.path)
                shutil.rmtree(os.path.join(self.path, type))
                print("[INFO] Volt type '{}' removed".format(type))
                return

            else:
                raise FileNotFoundError

        except FileNotFoundError:
            print("[INFO] {} Volt for {} {} already exists".format(type, self.first, self.last))
            return


    def create_volt_profile(self):

        try:
            if self.volt_exists() == False:
                os.mkdir(self.path)
                return "[INFO] Volt type '{}' created".format(type)
            else:
                raise FileExistsError
            #     os.mkdir(self.path)
            #     os.mkdir(os.path.join(self.path, type))
            #     return  "[INFO] Volt created under {}".format("other")
        except FileExistsError:
            print("[INFO] '{}' Volt for {} {} already exists".format(type, self.first, self.last))
            return

    def remove_volt_profile(self):

        try:
            if self.volt_exists() == True:
                shutil.rmtree(self.path)
                #os.sys("ls -l")
                return "[INFO] Volt type '{}' removed".format(type)
            else:
                raise FileNotFoundError
            #     os.mkdir(self.path)
            #     os.mkdir(os.path.join(self.path, type))
            #     return  "[INFO] Volt created under {}".format("other")
        except FileNotFoundError:
            print("[INFO] '{}' Volt for {} {} does not exists".format(type, self.first, self.last))
            return None


volt_1 = Volt('Tshepo', 'Molane')
volt_2 = Volt("zeefu", "apx")
save_path = volt_1.path
save_path = volt_2.path
type = "social"
type_2 = "social"
# print(volt_1.fullname)
# print(volt_1.path)
#print(volt_1.create_volt('development'))
#volt_2.create_volt_profile()
#print(volt_2.volt_exists())
volt_2.remove_volt_profile()
print(volt_2.volt_exists())
#print(volt_2.volt_exists())
#creating key
# volt_1.create_keys(volt_1.path, type, privatekey_password='apexsingularitymim01', encryption=True, replace=True)
#
# print(volt_1.create_volt('personal'))



#print(Volt('Tshepo', 'Molane').volt_exists())

#volt_1.create_keys(save_path = '/home/zeefu/Desktop', encryption=False)
