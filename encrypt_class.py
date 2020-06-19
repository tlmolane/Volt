from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import key_sorting
import argparse
import getpass
import logging
import pickle
import shutil
import json
import sys
import os

"""
Author: Tshepo L. Molane
Git: ZeefuApx
email: tmolane@gmail.com
"""
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
                public_key_name = 'public_key'):
        # decrypted_dict is a returned object from the function decrypt()
        try:
            dict_name = dict_name.split('.')[0]
            public_key_name = public_key_name.split('.')[0]

            if self.dict_exist(type, dict_name)[0] == True:
                accounts = decrypted_dict
                account = account.lower()

                if account not in list(accounts.keys()):
                    print('[INFO] specified account does not exist. \n[INFO] Adding {} account to dictionary'.format(account))
                    accounts[account] = (str(password), 'hash')

                accounts[account] = (str(password), 'hash') # change password of existing account on dict before encrypting

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
                    encryption = False, replace = False, pb_exp = 65537, ky_size = 4096):
        try:


            if replace != False and os.path.exists(os.path.join(save_path, private_key_name)):
                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext


            elif replace == False and os.path.exists(os.path.join(save_path, private_key_name)):

                try:
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
                private_key_name = private_key_name.split('.')[0] + ext
                public_key_name  = public_key_name.split('.')[0]  + ext


        except FileNotFoundError:
            raise FileNotFoundError("FileNotFoundError exception thrown. Check if save_path exists")

        try:

            print("[INFO]: creating keys...")

            if os.path.exists(os.path.join(save_path)):

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
                print("[INFO]: keys created. public key {} and private key {} saved in {}".format(public_key_name, private_key_name, save_path))



            else:
                raise FileNotFoundError("[INFO]: Volt {} does not exist".format(os.path.join(save_path)))


        except Exception as e:
            print(e)
            return None

        return

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
                print("ValueError: save_path must be default")
                raise ValueError

        except ValueError:
            print(e)

        #print('gets here')

        try:

            print("[INFO]: creating keys...")

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
                    print("[INFO]: keys created. public key {} and private key {} saved in {}".format(public_key_name, private_key_name, save_path))

                    type_trigger = False


                    #return
                elif self.volt_exists() == True and self.type_exists(type)[0] == False:

                    print("[INFO]: volt type {} does not exist".format(type))
                    print("[INFO]: creating volt type '{}''")
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


#---------------Test Field 1
volt_1 = Volt('Tshepo', 'Molane')
volt_2 = Volt("zeefu", "apx")
save_path = volt_1.path
save_path = volt_2.path
type = "social"
type_2 = "social"
type_3 = 'development'


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
#-------- end of test field 1
# test field 2

#volt_1.create_volt_type(type="social")
# volt_1.create_keys(type='social',
#                     private_key_name = 'private_key',
#                     public_key_name = 'public_key',
#                     pickle_file='passwords.pickle', ext = '.pem',
#                     private_key_password = None,
#                     encryption = False,
#                     replace = False,
#                     pb_exp = 65537,
#                     ky_size = 4096)
# lines = volt_1.view_keys(private_key_name = 'private_key.pem', public_key_name = 'public_key.pem', private=False, public= True)
#
# for line in lines:
#     print(line, end = '')
# end of test field 2


# test field 3
# private_key_name = 'private_key.pem'
# public_key_name = 'public_key.pem'
# save_path = '/home/zeefu/Desktop/'
# Volt.createKeys(private_key_name,
#                 public_key_name,
#                 save_path,
#                 ext ='.pem',
#                 private_key_password='test',
#                 encryption = True,
#                 replace = False,
#                 pb_exp = 65537,
#                 ky_size = 4096)
# end of test field 3

p = volt_1.decrypt(type='social',
            private_key_password = '',
            dict_name='passwords.pickle',
            private_key_name = 'private_key',
            public_key_name = 'public_key')

print(p['test_account'])
# e = volt_1.encrypt(type = 'social',
#             decrypted_dict = p,
#             password = 'test_password',
#             account = 'test_account',
#             dict_name = 'passwords.pickle',
#             public_key_name = 'public_key')




#print(volt_2.volt_exists())
#creating key
#
# print(volt_1.create_volt('personal'))



#print(Volt('Tshepo', 'Molane').volt_exists())

#volt_1.create_keys(save_path = '/home/zeefu/Desktop', encryption=False)
