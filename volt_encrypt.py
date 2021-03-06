from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import password_hex
import key_sorting
import traceback
import argparse
import logging
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
Git: tlmolane
email: tlmolane@protonmail.com
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

    def volt_exists(self):
        if os.path.exists(self.path):
            return True
        else:
            #print(os.path.exists(os.path.join(self.path)))
            return False

    def type_exists(self, type):
        if os.path.exists(os.path.join(self.path, type)):
            return (True, os.path.join(self.path, type))
        else:
            #print(os.path.exists(os.path.join(self.path)))
            return (False, os.path.join(self.path, type))

    def keys_exist(self, type, private_key_name = 'private_key', public_key_name = 'public_key'):

        try:
            public_key_name, private_key_name = public_key_name.split('.')[0], private_key_name.split('.')[0]

            if self.type_exists(type)[0] == True:
                # print(self.type_exists(type))
                # print('gets here first')

                private_key_path = os.path.join(self.path, type, private_key_name + '.pem')
                public_key_path  = os.path.join(self.path, type, public_key_name + '.pem')
                #print(private_key_path, public_key_path)
                if os.path.exists(private_key_path) and os.path.exists(public_key_path):
                    #print('gets here')
                    return (True,private_key_path, public_key_path)
                else:
                    # print('gets here')
                    return (False, private_key_path, public_key_path)
            else:
                raise FileNotFoundError

        except Exception as e:
            # print('gets here')
            #print(e)
            return (False, e)

    def dict_exist(self, type, dict_name):

        try:
            dict_name = dict_name.split('.')[0]

            if self.type_exists(type)[0] == True:

                dict_path = os.path.join(self.path, type, dict_name + '.pickle')

                if os.path.exists(dict_path):
                    return (True, os.path.join(self.path, type, dict_path))
                else:
                    return (False, os.path.join(self.path, type, dict_path))

        except Exception as e:
            print(e)
            return False

    def encrypt(self, type, decrypted_dict, password, account, dict_name = 'passwords.pickle',
                public_key_name = 'public_key', max_length=10):
        # decrypted_dict is a returned object from the function decrypt()
        try:
            dict_name = dict_name.split('.')[0]
            public_key_name = public_key_name.split('.')[0]

            final_password, final_password_hex_only, sha_3_hexdigest = password_hex.generate_hex_pass(str(password), max_length)


            if self.dict_exist(type, dict_name)[0] == True:
                accounts = decrypted_dict
                account = account.lower()

                if account not in list(accounts.keys()):
                    print('[INFO] specified account does not exist. \n[INFO] Adding {} account to dictionary'.format(account))
                    accounts[account] = (str(password), final_password, final_password_hex_only, sha_3_hexdigest)

                accounts[account] = (str(password), final_password, final_password_hex_only, sha_3_hexdigest) # change password of existing account on dict before encrypting

                accounts_str = json.dumps(accounts)
                accounts_byte = accounts_str.encode('utf-8')

                with open(os.path.join(self.path, type, public_key_name + '.pem'), 'rb') as key_file:

                    public_key = serialization.load_pem_public_key(
                                key_file.read(),
                                backend = default_backend()
                    )

                encrypted = public_key.encrypt(
                            accounts_byte,
                            padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm = hashes.SHA256(),
                            label=None
                        )
                    )

                try:
                    with open(os.path.join(self.path, type, dict_name + '.pickle'), 'wb') as f:
                        pickle.dump(encrypted, f)
                    f.close()
                    return
                except Exception as e:
                    print(e)
                    key_file.close()
                    return None
            else:
                raise FileNotFoundError("[INFO]: File {} does not exist".format(os.path.join(self.path, type, dict_name + '.pickle')))

        except Exception as e:
            print(e)
            return



    def pass_match(self, type, private_key_password, private_key_name, public_key_name):

        try:
            #print('gets here first')
            private_key_name = private_key_name.split('.')[0]
            #print('gets here first')
            #print('this', self.keys_exist(type, private_key_name, public_key_name))
            #print('gets here')
            if self.keys_exist(type, private_key_name, public_key_name)[0] == True:

                try:

                    with open(os.path.join(self.path, type, private_key_name + '.pem'), 'rb') as key_file:
                        private_key = serialization.load_pem_private_key(
                                    key_file.read(),
                                    password = b'%b' % private_key_password.encode('utf-8'),
                                    backend = default_backend()
                        )

                    key_file.close()

                    return True
                except ValueError as e:
                    #print(e)
                    return (False, e)
            else:
                raise FileNotFoundError("[INFO]: File {} does not exist".format(os.path.join(self.path, type, private_key_name + '.pem')))
        except Exception as e:
            #print('gets here')
            print(e)
            #return False

    @staticmethod
    def private_key_password_match(private_key_path, private_key_password=None):
        try:

            if not os.path.exists(private_key_path):
                raise FileNotFoundError("{} path does not exist".format(private_key_path))
                return None

            if private_key_password == None:
                # print("gets here 1")
                private_key_password = None
            elif len(private_key_password) != 0:
                # print("gets here 2")
                private_key_password = b'%b' % private_key_password.encode('utf-8')
            elif len(private_key_password) == 0:
                # print("gets here 3")
                private_key_password = None

            try:

                with open(private_key_path, 'rb') as key_file:
                    private_key = serialization.load_pem_private_key(
                                key_file.read(),
                                password = private_key_password,
                                backend = default_backend()
                    )

                    return True

            except ValueError as e:
                if str(e) == 'Bad decrypt. Incorrect password?':
                    return False
                else:
                    logging.error(traceback.format_exc())


            except TypeError as e:
                if str(e) == 'Password was given but private key is not encrypted.':
                    logging.error(traceback.format_exc())
                    return True
                else:
                    logging.error(traceback.format_exc())

        except Exception as e:
            logging.error(traceback.format_exc())
            return None



    def decrypt(self, type, private_key_password, dict_name, private_key_name = 'private_key',
                        public_key_name = 'public_key'):

        try:

            if self.keys_exist(type, private_key_name, public_key_name)[0] == True and self.dict_exist(type, dict_name)[0] == True:

                # d = self.keys_exist(type, private_key_name, public_key_name))[0]
                # p = self.keys_exist(type, private_key_name, public_key_name))[1]

                with open(self.dict_exist(type, dict_name)[1], 'rb') as f:
                    accounts_byte = pickle.load(f)
                f.close()

                try:

                    if private_key_password == None:
                        # print("gets here 1")
                        private_key_password = None
                    elif len(private_key_password) != 0:
                        # print("gets here 2")
                        private_key_password = b'%b' % private_key_password.encode('utf-8')
                    elif len(private_key_password) == 0:
                        # print("gets here 3")
                        private_key_password = None


                    with open(os.path.join(self.path, type, private_key_name + '.pem'), 'rb') as key_file:
                        private_key = serialization.load_pem_private_key(
                                    key_file.read(),
                                    password = private_key_password,
                                    backend = default_backend()
                        )

                    decrypted = private_key.decrypt(accounts_byte, padding.OAEP(
                                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                        algorithm=hashes.SHA256(),
                                        label=None
                        )
                    )

                    key_file.close()

                    decrypted_dictionary = json.loads(decrypted.decode('utf-8'))
                    # print(decrypted_dictionary)
                    return decrypted_dictionary

                except FileNotFoundError as e:
                    #print(e()
                    return (False, e)

            else:
                raise FileNotFoundError("[INFO]: File {} does not exist".format(os.path.join(self.path, type, private_key_name + '.pem')))
        except Exception as e:
            #print(e)
            return (False, e)

    @staticmethod
    def createKeys(private_key_name, public_key_name, save_path, ext ='.pem', private_key_password=None,
                    encrypt_private_key = False, replace = False, pb_exp = 65537, ky_size = 4096, fernet_key = False,
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
                                                                    path_pattern ='_%s',
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

                if fernet_key != False:
                    fernet_key_name  = 'fernet.key'
                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext


        except FileNotFoundError:
            raise FileNotFoundError("FileNotFoundError exception. Check if save_path exists")

        try:

            print("[INFO] creating keys...")

            if os.path.exists(os.path.join(save_path)):

                if fernet_key != False:

                    print("[INFO] generating fernet key...")

                    'generate fernet key'
                    fernet_ky= Fernet.generate_key()

                    with open(os.path.join(save_path, fernet_key_name), 'w') as f:
                        f.write(fernet_ky.decode())
                    f.close()

                print("[INFO] generating private key...")

                private_key = rsa.generate_private_key(
                                public_exponent = pb_exp,
                                key_size = ky_size,
                                backend = default_backend()

                )


                public_key = private_key.public_key()
                print("[INFO] extracted public key from private key...")


                if encrypt_private_key == True and (private_key_password == None or len(private_key_password) == 0):
                    raise ValueError("ValueError: encryption option is true but private key password was not provided")
                elif encrypt_private_key == False and (private_key_password !=None and len(private_key_password) != 0):

                    print("[INFO] Warning: serialization with encryption is False but password was provided. serialzing with encryption...")
                    serialize = serialization.BestAvailableEncryption(b'%b' % private_key_password.encode('utf-8'))


                elif encrypt_private_key == True and (private_key_password != None and len(private_key_name) != 0):
                    serialize = serialization.BestAvailableEncryption(b'%b' % private_key_password.encode('utf-8'))
                elif encrypt_private_key == False and (private_key_password == None or len(private_key_password) == 0):
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


                print("[INFO] saving private key {}...".format(private_key_name))
                with open(os.path.join(save_path, private_key_name), 'wb') as f:
                    f.write(pem)
                f.close()

                print("[INFO] saving public key {}...".format(public_key_name))
                with open(os.path.join(save_path, public_key_name), 'wb') as f:
                    f.write(pem_2)
                f.close()
                #print(save_path)
                # print(type(encrypt_fernet_key))

                if encrypt_fernet_key:
                    print("[INFO] encrypting {} with {}".format(fernet_key_name, public_key_name))
                    time.sleep(2)

                    Volt.encrypt_file_content(os.path.join(save_path, public_key_name),
                                            os.path.join(save_path, fernet_key_name),
                                            save_path,
                                            fernet_key_encryption=False,
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
                    print("[INFO] keys created. public key '{}', private key '{}' and fernet key '{}' are saved in '{}'".format(public_key_name, private_key_name, fernet_key_name,save_path))

                else:
                    print("[INFO] keys created. public key {} and private key {} saved in {}".format(public_key_name, private_key_name, save_path))


            else:
                raise FileNotFoundError("[INFO]: Volt {} does not exist".format(os.path.join(save_path)))


        except Exception as e:
            print(e)

        return

    @staticmethod
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


        except Exception:
            return logging.error(traceback.format_exc())

    @staticmethod
    def decrypt_file_content(private_key_path, private_key_password, encrypted_file_path, save_path,
                            fernet_key_decrypt=False, replace=True, file_type='document'):

        try:


            if not (os.path.exists(private_key_path) and os.path.exists(encrypted_file_path)):
                raise FileNotFoundError('Exception {} does not exist'.format(encrypted_file_path))

            encrypted_file_ext = encrypted_file_path.split('/')[-1]

            if encrypted_file_ext.count('.') == 1:
                encrypted_file_name, ext = encrypted_file_ext.split('.')
            elif encrypted_file_ext.count('.') > 1:
                ext = encrypted_file_ext.split('.')[-1]
                encrypted_file_name = re.sub(r'.{}$'.format(ext), '', encrypted_file_ext)
            else:
                ext, encrypted_file_name = '', encrypted_file_ext.split('.')[-1]

            if ext not in Volt.files_dict[file_type]:
                raise Exception("[Custom Exception] File type extention not found in Volt.file_dict class variable")

            with open(encrypted_file_path, 'rb') as file:
                data = file.read()
            file.close()

            if not fernet_key_decrypt:
                print('[INFO] decrypting using private key {} ...'.format(private_key_path))

                if private_key_password == None:
                    # print("gets here 1")
                    private_key_password = None
                elif len(private_key_password) != 0:
                    # print("gets here 2")
                    private_key_password = b'%b' % private_key_password.encode('utf-8')
                elif len(private_key_password) == 0:
                    # print("gets here 3")
                    private_key_password = None
                
                try:

                    with open(private_key_path, 'rb') as key_file:
                        private_key = serialization.load_pem_private_key(
                                    key_file.read(),
                                    password = private_key_password,
                                    backend = default_backend()
                        )

                    key_file.close()

                except ValueError:
                    logging.error(traceback.format_exc())

                try:

                    decrypted_data = private_key.decrypt(data, padding.OAEP(
                                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                        algorithm=hashes.SHA256(),
                                        label=None
                        )
                    )
                except ValueError as e:
                    logging.error(traceback.format_exc())
                    return


                if not replace:
                    #print("gets here")
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
                print('[INFO] decrypting using fernet key {} ...'.format(private_key_path))

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

                    print('[INFO] {} decrypted. saved as {}'.format(encrypted_file_name, new_file_name))

                elif replace:

                    # os.remove(encrypted_file_path)

                    with open(encrypted_file_path, 'wb') as file:
                        file.truncate(0)
                        file.write(decrypted_data)
                    file.close()

                    print('[INFO] {} decrypted. saved as {}'.format(encrypted_file_name, new_file_name))

        except Exception as e:
            logging.error(traceback.format_exc())


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
            print(e) 

    def create_keys(self, type, private_key_name = 'private_key', public_key_name = 'public_key',
                    pickle_file='passwords.pickle', ext = '.pem', private_key_password = None,
                    encryption = False, replace = False, pb_exp = 65537, ky_size = 4096):


        try:
            save_path = os.path.join(self.path, type)

            if replace != False:

                try:
                    private_key_name = private_key_name.split('.')[0] + ext
                    public_key_name  = public_key_name.split('.')[0]  + ext

                    print("[INFO] deleting existing keys...")
                    os.remove(os.path.join(self.path, type, private_key_name))
                    os.remove(os.path.join(self.path, type, public_key_name))

                    # save_path = os.path.join(self.path, type)

                except FileNotFoundError:
                    print("[INFO] creating new keys in path {}".format(save_path))
                    #save_path = os.path.join(self.path, type)
                    pass

            elif replace == False and self.keys_exist(type, private_key_name, public_key_name)[0] == True:

                try:
                    private_key_name = private_key_name.split('.')[0]
                    public_key_name  = public_key_name.split('.')[0]

                    print("[INFO] saving keys in {}".format(os.path.join(self.path, type)))
                    #save_path = os.path.join(self.path, type)
                    pri, pub = key_sorting.new_key_names(private_key_name,
                                                        public_key_name,
                                                        save_path,
                                                        path_pattern='_%s',
                                                        ext = ext
                                                        )

                    private_key_name, public_key_name = pri.split('/')[-1], pub.split('/')[-1]

                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError exception thrown")

            elif replace == False and self.keys_exist(type, private_key_name, public_key_name)[0] == False:
                print(self.keys_exist(private_key_name, public_key_name)[0])

                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext
                # save_path = os.path.join(self.path, type)
                pass
            else:
                raise ValueError("[INFO] ValueError; save_path must be default")

        except ValueError as e:
            print(e)

        #print('gets here')

        try:

            print("[INFO] creating keys...")

            type_trigger = True

            while type_trigger:
                if self.volt_exists() == True and self.type_exists(type)[0] == True:

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



                    with open(os.path.join(save_path, private_key_name), 'wb') as f:
                        f.write(pem)
                    f.close()

                    with open(os.path.join(save_path, public_key_name), 'wb') as f:
                        f.write(pem_2)
                    f.close()
                    #print(save_path)
                    print("[INFO] keys created. public key {} and private key {} saved in {}".format(public_key_name, private_key_name, save_path))

                    type_trigger = False


                    #return
                elif self.volt_exists() == True and self.type_exists(type)[0] == False:

                    print("[INFO] volt type {} does not exist".format(type))
                    print("[INFO] creating volt type '{}''")
                    self.create_volt_type(type)

                else:
                    raise FileNotFoundError("[INFO]: Volt {} does not exist".format(os.path.join(self.path)))


        except Exception as e:
            print(e)
            return None

        try:

            try:
                if replace == True and self.dict_exist(type, pickle_file)[0] == True:
                    print("[INFO] deleting existing dictionary...")
                    os.remove(os.path.join(self.path, type, pickle_file))
                elif replace == True and self.dict_exist(type, pickle_file)[0] == False:
                    print('FileNotFoundError: dictionary/file  not found. Proceeding to creating dict pickle file...')
                    pass
                elif replace == False and self.dict_exist(type, pickle_file)[0] == True:
                    new_pickle_file_path = key_sorting.new_file_name('passwords.pickle',
                                                                    save_path,
                                                                    path_pattern='_%s',
                                                                    ext = '.pickle')
                    pickle_file = new_pickle_file_path.split('/')[-1]
                elif replace == False and self.dict_exist(type, pickle_file)[0] == False:
                    pass
                else:
                    raise ValueError("ValueError: dict_name variable must be set to True if replace is variable is set to True or it must be False")

            except Exception as e:
                print(e)
                return




            accounts = {}
            accounts_str = json.dumps(accounts)
            accounts_byte = accounts_str.encode('utf-8')

            with open(os.path.join(self.path, type, public_key_name), 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                            key_file.read(),
                            backend = default_backend()
                )

            encrypted = public_key.encrypt(
                        accounts_byte,
                        padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label=None
                    )
                )


            with open(os.path.join(self.path, type, pickle_file), 'wb') as f:
                pickle.dump(encrypted, f)

            f.close()
            key_file.close()

            print("[INFO] new dictionary in {} has been encrypted. use corresponding private key to decrypt".format(pickle_file))
        except Exception as e:
            print(e)

    def view_keys(self, private_key_name = 'private_key', public_key_name = 'public_key', private=False, public= True):

        "Caution: this method is an iterator"
        try:
            private_key_name = private_key_name.split('.')[0]
            public_key_name = public_key_name.split('.')[0]

            if self.keys_exist(type, private_key_name, public_key_name)[0]:

                if private == True and public == False:
                    with open(os.path.join(self.path, type, private_key_name + '.pem'), 'r') as key_file:

                        # private_key = serialization.load_pem_private_key(
                        #             key_file.read(),
                        #             password = b'%b' % private_key_password.encode('utf-8'),
                        #             backend = default_backend())

                        for lines in key_file:
                            #print(lines, end ='')
                            yield(lines)


                elif private == False and public == True:

                    with open(os.path.join(self.path, type, public_key_name + '.pem')) as key_file:

                        for lines in key_file:
                            #print(lines, end='')
                            yield lines

                else:
                    raise ValueError("ValueError: Boolean Values. private variable and public variable must not have the same Boolean values.")
            else:
                raise FileNotFoundError("Entered key path does not exist")

        except Exception as e:
            print(e)


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
                raise FileNotFoundError("[INFO]: File {} does not exist".format(os.path.join(self.path, type)))

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



    