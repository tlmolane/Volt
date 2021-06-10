from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import key_sorting
import password_hex
import argparse
import getpass
import logging
import pickle
import shutil
import json
import time
import sys
import os
import re

"""
Author: Tshepo L. Molane
Git: ZeefuApx
email: tmolane@gmail.com
"""


class Volt:

    abs_path = os.path.dirname(os.path.abspath(__file__))

    account_types = ["social", "development", "personal", "other"]
    files_dict = {'image': ['jpg', 'PNG', 'png', 'JPG', 'jpeg', 'JPEG', 'gif'],
                'video': ['avi', 'mpeg', 'mkv', 'mp4', 'MP4'],
                'document': ['', 'PDF', 'pdf', 'txt', 'xlsx', 'docx', 'odt'],
                'file': ['zip', 'tar', 'pickle', 'pub', 'key'],
                'script': [ 'py', 'java', 'key', '']}
                
    all_files = list(set([y for x in list(files_dict.values()) for y in x]))
    all_types = [i for i in list(files_dict.keys())]



    def __init__(self, first, last):

        self.first = first
        self.last = last
        #self.account = account_type
        self.path = os.path.join(Volt.abs_path,  "{}_{}".format(self.first.lower(),
                    self.last.lower()))
        #self.type_path = os.path.join(self.path, )

    @property
    def full_name(self):
        return '{} {}'.format(self.first, self.last)
        
    @staticmethod
    def createKeys(private_key_name, public_key_name, save_path, ext ='.pem', private_key_password=None,
                    encryption = False, replace = False, pb_exp = 65537, ky_size = 4096, fernet_key = False,
                    encrypt_fernet_key=False):
        try:

            if replace != False and os.path.exists(os.path.join(save_path, private_key_name)):

                if fernet_key != False:
                    fernet_key_name = 'fernet.key'

                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext

            if replace != False and not os.path.exists(os.path.join(save_path, private_key_name)):

                if fernet_key != False:
                    fernet_key_name = 'fernet.key'

                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext



            elif replace == False and os.path.exists(os.path.join(save_path, private_key_name)):

                try:

                    if fernet_key != False:
                        fernet_key_name = key_sorting.new_file_name('fernet',
                                                                    save_path,
                                                                    path_pattern='_%s',
                                                                    ext='key')
                        fernet_key_name = fernet_key_name.split('/')[-1]


                    private_key_name = private_key_name.split('.')[0]
                    public_key_name  = public_key_name.split('.')[0]



                    print("[INFO] saving keys in {}".format(os.path.join(save_path)))
                    #save_path = os.path.join(self.path, type)
                    pri, pub = key_sorting.new_key_names(private_key_name,
                                                        public_key_name,
                                                        save_path,
                                                        path_pattern='_%s',
                                                        ext = ext
                                                        )

                    private_key_name, public_key_name = pri.split('/')[-1], pub.split('/')[-1]



                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError exception thrown. Check if save_path exists")

            elif replace == False and os.path.exists(os.path.join(save_path, private_key_name)) == False:

                fernet_key_name  = 'fernet.key'
                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext


        except FileNotFoundError:
            raise FileNotFoundError("FileNotFoundError exception. Check if save_path exists")

        try:

            print("[INFO]: creating keys...")

            if os.path.exists(os.path.join(save_path)):

                if fernet_key != False:

                    print("[INFO]: creating fernet key...")

                    'generate fernet key'
                    fernet_ky= Fernet.generate_key()

                    with open(os.path.join(save_path, fernet_key_name), 'w') as f:
                        f.write(fernet_ky.decode())
                    f.close()

                private_key = rsa.generate_private_key(
                                public_exponent = pb_exp,
                                key_size = ky_size,
                                backend = default_backend()

                )

                public_key = private_key.public_key()


                if encryption == True and (private_key_password == None or len(private_key_password) == 0):
                    raise ValueError("ValueError: encryption option is true but private key password was not provided")
                elif encryption == False and (private_key_password !=None and len(private_key_password) != 0):

                    print("[INFO] Warning: serialization with encryption is False but password was provided. serialzing with encryption...")
                    serialize = serialization.BestAvailableEncryption(b'%b' % private_key_password.encode('utf-8'))


                elif encryption == True and (private_key_password != None and len(private_key_name) != 0):
                    serialize = serialization.BestAvailableEncryption(b'%b' % private_key_password.encode('utf-8'))
                elif encryption == False and (private_key_password == None or len(private_key_password) == 0):
                    serialize = serialization.NoEncryption()

                else:
                    print("[INFO] Warning: serializing private key with no encryption")
                    serialize = serialization.NoEncryption()

                "Private Key"
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


                print("[INFO]: saving private key {}...".format(private_key_name))
                with open(os.path.join(save_path, private_key_name), 'wb') as f:
                    f.write(pem)
                f.close()

                print("[INFO]: saving public key {}...".format(public_key_name))
                with open(os.path.join(save_path, public_key_name), 'wb') as f:
                    f.write(pem_2)
                f.close()
                #print(save_path)

                if encrypt_fernet_key:
                    print("[INFO]: encrypting {} with {}".format(fernet_key_name, public_key_name))
                    time.sleep(2)
                    Volt.encrypt_file_content(os.path.join(save_path, public_key_name),
                                            os.path.join(save_path, fernet_key_name),
                                            save_path,
                                            fernet_key_encrypt=(False,'password'),
                                            replace=True,
                                            file_type='file')
                    #os.remove()
                    #Volt.encrypt_file_content('/home/zeefu/Desktop/public_key.pem',
                    #                            '/home/zeefu/Desktop/crypto_stuff.txt',
                    #                            '/home/zeefu/Desktop/',
                    #                            hash_sig=True,
                    #                            replace=False,
                    #                            file_type='document')



                if fernet_key:
                    print("[INFO]: keys created. public key {}, private key {} and fernet key {} are saved in {}".format(public_key_name, private_key_name, fernet_key_name,save_path))

                else:
                    print("[INFO]: keys created. public key {} and private key {} saved in {}".format(public_key_name, private_key_name, save_path))


            else:
                raise FileNotFoundError("[INFO]: Volt {} does not exist".format(os.path.join(save_path)))


        except Exception as e:
            print(e)

        return

    @staticmethod
    def encrypt_file_content(public_key_path, full_file_path, save_path,
                             fernet_key_encrypt=False, replace=False,
                             file_type='document'):
                             
        try:

            if fernet_key_encrypt:
                print('[INFO] encrypting using fernet key {}'.format(public_key_path))
                #public_key_path = fernet_key_encrypt[1]
            else:
                print('[INFO] encrypting using public key {}'.format(public_key_path))


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
                raise Exception("[Custom Exception]: File type extention not found in Volt.file_dict class variable")

            with open(public_key_path, 'rb') as key_file:
                print(public_key_path)

                if not fernet_key_encrypt:
                    public_key = serialization.load_pem_public_key(
                                key_file.read(),
                                backend = default_backend()

                            )
                elif fernet_key_encrypt:
                    key = key_file.read() #this is bytes!

            if not replace:

                new_file_name = key_sorting.new_file_name(file_name, save_path, path_pattern='_%s', ext=ext)

                with open(full_file_path, 'rb') as file:
                    data = file.read()
                file.close()


                with open(os.path.join(save_path, new_file_name), 'wb') as new_file:
                    #new_file.seek(0)

                    if not fernet_key_encrypt:

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
                        #new_file.truncate()

                    elif fernet_key_encrypt:
                        fernet_cipher = Fernet(key.decode())
                        encrypted_data = fernet_cipher.encrypt(data)

                        new_file.write(encrypted_data)


            else:

                with open(os.path.join(full_file_path), 'rb') as file:
                    data = file.read()
                file.close()

                os.remove(full_file_path)

                with open(os.path.join(full_file_path), 'wb') as file:
                    #data = file.read()
                    #file.seek(0)
                    if not fernet_key_encrypt:
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

                    elif fernet_key_encrypt:
                        fernet_cipher = Fernet(key.decode())
                        encrypted_data = fernet_cipher.encrypt(data)

                        file.write(encrypted_data)
                        # you can append hmac here


        except Exception as e:
            print(e)

    @staticmethod
    def decrypt_file_content(private_key_path, private_key_password, encrypted_file_path, save_path,
                            fernet_key_decrypt=False, replace=True, file_type='document'):

        try:


            if not (os.path.exists(private_key_path) and os.path.exists(encrypted_file_path)):
                raise FileNotFoundError('Exception: {} does not exist'.format(encrypted_file_path))

            encrypted_file_ext = encrypted_file_path.split('/')[-1]

            if encrypted_file_ext.count('.') == 1:
                encrypted_file_name, ext = encrypted_file_ext.split('.')
            elif encrypted_file_ext.count('.') > 1:
                ext = encrypted_file_ext.split('.')[-1]
                encrypted_file_name = re.sub(r'.{}$'.format(ext), '', encrypted_file_ext)
            else:
                ext, encrypted_file_name = '', encrypted_file_ext.split('.')[-1]

            if ext not in Volt.files_dict[file_type]:
                raise Exception("[Custom Exception]: File type extention not found in Volt.file_dict class variable")

            with open(encrypted_file_path, 'rb') as file:
                data = file.read()
            file.close()

            if not fernet_key_decrypt:
                print('[INFO]: decrypting using private key {}'.format(private_key_path))

                if private_key_password == None:
                    # print("gets here 1")
                    private_key_password = None
                elif len(private_key_password) != 0:
                    # print("gets here 2")
                    private_key_password = b'%b' % private_key_password.encode('utf-8')
                elif len(private_key_password) == 0:
                    # print("gets here 3")
                    private_key_password = None


                with open(private_key_path, 'rb') as key_file:
                    private_key = serialization.load_pem_private_key(
                                key_file.read(),
                                password = private_key_password,
                                backend = default_backend()
                    )

                decrypted_data = private_key.decrypt(data, padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm=hashes.SHA256(),
                                    label=None
                    )
                )

                key_file.close()

                if not replace:

                    new_file_name = key_sorting.new_file_name(encrypted_file_name +'_'+'decrypted',
                                                            save_path,
                                                            path_pattern='_%s',
                                                            ext=ext)


                    with open(new_file_name, 'wb') as new_file:
                        new_file.write(decrypted_data)
                    new_file.close()

                elif replace:

                    with open(encrypted_file_path, 'wb') as file:
                        file. truncate(0)
                        file.write(decrypted_data)
                    file.close()



            elif fernet_key_decrypt:
                print('[INFO]: decrypting using fernet key {}'.format(private_key_path))

                with open(private_key_path, 'rb') as file:
                    #file.seek(0)
                    key = file.read()
                file.close()

                fernet_cipher = Fernet(key.decode())
                decrypted_data = fernet_cipher.decrypt(data)

                if not replace:

                    new_file_name = key_sorting.new_file_name(encrypted_file_name +'_'+'decrypted',
                                                            save_path,
                                                            path_pattern='_%s',
                                                            ext=ext)


                    with open(new_file_name, 'wb') as new_file:
                        new_file.write(decrypted_data)
                    new_file.close()

                    print('[INFO]: {} decrypted. saved as {}'.format(encrypted_file_name, new_file_name))

                elif replace:

                    with open(encrypted_file_path, 'wb') as file:
                        file.truncate(0)
                        file.write(decrypted_data)
                    file.close()

                    print('[INFO]: {} decrypted. saved as {}'.format(encrypted_file_name, new_file_name))

        except Exception as e:
            print(e)


    @staticmethod
    def extention(path_to_file):
        return path_to_file.split('/')[-1].split('.')[-1]

    @staticmethod
    def type_list(dictionary, type_,folder_path):
        try:
            path_list = []
            for r, d, f in os.walk(folder_path):
                for file in f:
                    if Volt.extention(os.path.abspath(file)) in dictionary[type_]:
                        path_list.append((r, (os.path.join(r, file))))
            return path_list
        except Exception as e:
            pass 




    # def key_pair_paths(self, type):
    #     try:
    #         print('this')
    #         if self.volt_exists() == True and self.type_exists(type) == True:
    #             private_key_location = os.path.join(self.path)
    #
    #         else:
    #             raise FileNotFoundError
    #
    #     except Exception as e:
    #         print(e)
    #     pass


#-------------------------------------------------------------------test field 1
# volt_1 = Volt('Tshepo', 'Molane')
# volt_2 = Volt("zeefu", "apx")
# save_path = volt_1.path
# save_path = volt_2.path
# type = "social"
# type_2 = "social"
# type_3 = 'development'


# print(volt_1.full_name)
# print(volt_1.path)
#print(volt_1.create_volt('development'))
#volt_2.create_volt_profile()
#print(volt_2.volt_exists())
#volt_2.remove_volt_profile()

#print(volt_2.volt_exists())
#print(volt_1.keys_exist(type = type))
#print(volt_1.dict_exist(type = type, dict_name = 'passwords.pickle'))

# ----- pass match test:
# end of pass match test.

# view key test
# f = volt_1.view_keys(private_key_name = 'private_key',
#             public_key_name = 'public_key', private=True, public=False)
#
# for i in f:
#     print(i, end='')

# end of view key_test

# decrypt test:

# d = volt_1.decrypt(type, private_key_password = 'test',  dict_name = 'passwords.pickle', private_key_name = 'private_key',
#                     public_key_name = 'public_key')
# print(d)
#-------- ---------------------------------------------------end of test field 1

# ------------------------------------------------------------------test field 2

# volt_1.create_volt_type(type="social")
# volt_1.create_keys(type='social',
#                     private_key_name = 'private_key',
#                     public_key_name = 'public_key',
#                     pickle_file='passwords.pickle', ext = '.pem',
#                     private_key_password = None,
#                     encryption = False,
#                     replace = False,
#                     pb_exp = 65537,
#                     ky_size = 4096)
#
# lines = volt_1.view_keys(private_key_name = 'private_key.pem',
#                         public_key_name = 'public_key.pem',
#                         private=False, public= True)
#
# for line in lines:
#     print(line, end = '')
#------------------------------------------------------------end of test field 2


# test field 3
# private_key_name = 'private_key.pem'
# public_key_name = 'public_key.pem'
# save_path = '/home/zeefu/Desktop/'
# Volt.createKeys(private_key_name,
#                 public_key_name,
#                 save_path,
#                 ext ='.pem',
#                 private_key_password=None,
#                 encryption = False,
#                 replace = False,
#                 pb_exp = 65537,
#                 ky_size = 4096,
#                 fernet_key = True,
#                 encrypt_fernet_key=False)
# end of test field 3


#------------------------------------------------------------------test_field 4
# p = volt_1.decrypt(type='social',
#             private_key_password = '',
#             dict_name='passwords.pickle',
#             private_key_name = 'private_key',
#             public_key_name = 'public_key')
#
# print(p)
# e = volt_1.encrypt(type = 'social',
#             decrypted_dict = p,
#             password = 'test_',
#             account = 'test_account',
#             dict_name = 'passwords.pickle',
#             public_key_name = 'public_key')
#
#
#
#
# # print(Volt.files_dict['document
#
# test_func = Volt.encrypt_file_content('/home/zeefu/Desktop/public_key.pem',
#                                     '/home/zeefu/Desktop/crypto_stuff.txt',
#                                     '/home/zeefu/Desktop/',
#                                     hash_sig=True,
#                                     replace=False,
#                                     file_type='document')
#

#----------------------------------------------------------------------------------
# public_key_path = '/home/zeefu/Desktop/public_key.pem'
# private_key_path = '/home/zeefu/Desktop/private_key.pem'
# full_file_path = '/home/zeefu/Desktop/github-recovery-codes.txt'
# fernet_key_path = '/home/zeefu/Desktop/fernet.key'
# save_path = '/home/zeefu/Desktop/'
# Volt.encrypt_file_content(fernet_key_path,
#                     full_file_path,
#                     save_path,
#                     fernet_key_encrypt=True,
#                     replace=False,
#                     file_type='document')
#--------------------------------------------------------------------------------------

# Volt.decrypt_file_content(private_key_path,
#                         private_key_password='',
#                         encrypted_file_path=fernet_key_path,
#                         save_path=save_path,
#                         fernet_key_decrypt=False,
#                         replace=True,
#                         file_type='file')

# -----------------------------------------------------------end of test_field 4

# -----------------------------------------------------------test field 5



# print(Volt.files_dict)
# print(Volt.type_list(Volt.files_dict, 'document','/home/zeefu/Desktop/'))

# print(Volt.extention('/home/zeefu/Desktop/0_eLsEoykT1ImBEw_L_decrypted.jpg'))

# -----------------------------------------------------end of test field 5

# print(Volt.type_list(Volt.files_dict, 'document','/home/zeefu/Desktop/test/'))