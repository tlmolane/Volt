from volt_encrypt_object import Volt
import password_hex
import key_sorting
import traceback
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


def main(args):

    try:

        if args.decrypt and not args.encrypt:
            #print("decryption!")

            number_of_attempts = 0
            max_attempts = 3

            if not os.path.exists(args.private_key):
                raise FileNotFoundError("{} path does not exist".format(args.private_key))
            
            print(args.fernet_key_decryption)
            if args.private_key_decryption and not args.fernet_key_decryption:
                print("private!")

                while number_of_attempts <= max_attempts:
                    private_key_password = getpass.getpass(prompt='Enter private key password: ')

                    if Volt.private_key_password_match(args.private_key, private_key_password) == False:
                        number_of_attempts += 1
                        print("[INFO] incorrect password: number of attempts left {}".format(max_attempts - number_of_attempts))
                        if number_of_attempts == 3:
                            print("[INFO] max tries exceeded.")
                            break
                    elif Volt.private_key_password_match(args.private_key, private_key_password) == None:
                        break
                    else:
                        # print("password is correct or not needed")
                        print("value of fernet_key_decryption", args.fernet_key_decryption)
                        try:
                            Volt.decrypt_file_content(args.private_key,
                                                    private_key_password,
                                                    args.file_path,
                                                    save_path = args.save_path,
                                                    fernet_key_decrypt=args.fernet_key_decryption,
                                                    replace = args.replace,
                                                    file_type=args.file_type
                                                    )
                        except Exception as e:
                            logging.error(e, exc_info=True)

                        break
            else:
                private_key_password = None
                # print("value of fernet_key_decryption", args.fernet_key_decryption)
                # print("value of private key encryption", args.private_key_decryption)
                # print(private_key_password)
                try:

                    Volt.decrypt_file_content(args.private_key,
                                            private_key_password,
                                            args.file_path,
                                            save_path = args.save_path,
                                            fernet_key_decrypt=args.fernet_key_decryption,
                                            replace = args.replace,
                                            file_type=args.file_type
                                            )
                except Exception as e:
                    logging.error(e, exc_info=True)

        if args.decrypt_dir and (args.all or args.file_type):

            number_of_attempts = 0
            max_attempts = 3

            if not os.path.exists(args.private_key):
                raise FileNotFoundError("{} path does not exist".format(args.private_key))

            if not args.fernet_key_decryption:
                #print(args.fernet_key_decryption)

                while number_of_attempts <= max_attempts:
                    private_key_password = getpass.getpass(prompt='Enter private key password: ')

                    if Volt.private_key_password_match(args.private_key, private_key_password) == False:
                        number_of_attempts += 1
                        print("[INFO] incorrect password: number of attempts left {}".format(max_attempts - number_of_attempts))
                        if number_of_attempts == 3:
                            print("[INFO] max tries exceeded.")
                        return
                    elif Volt.private_key_password_match(args.private_key, private_key_password) == None:
                        break
                    else:
                        private_key_password = None 
                        break
            else:
                private_key_password = None 
                pass 

            if args.all:

                try:
                    set_ = []
                    for type_ in Volt.all_types:
                        for file_path in list(set(Volt.type_list(Volt.files_dict, type_, args.dir_path))):
                            if file_path[1] not in set_:

                                """Changes between fernet key and private key depending on"""
                                """the truth value of args.fernet_key_decrypt."""

                                Volt.decrypt_file_content(args.private_key,
                                private_key_password,
                                file_path[1],
                                save_path = file_path[0],
                                fernet_key_decrypt=args.fernet_key_decryption,
                                replace = args.replace,
                                file_type=args.file_type
                                )
                                set_.append(file_path[1])
                    

                except Exception as e:
                    #print(e)
                    raise

            if args.file_type and (not args.all):

                try:
                    set_ = []
                    for file_path in Volt.type_list(Volt.files_dict, args.file_type, args.dir_path):

                        if file_path[1] not in set_:

                            Volt.decrypt_file_content(args.private_key,
                            private_key_password,
                            file_path[1],
                            save_path = file_path[0],
                            fernet_key_decrypt=args.fernet_key_decryption,
                            replace = args.replace,
                            file_type=args.file_type
                            )
                            set_.append(file_path[1])

                except Exception as e:
                    print(e)
                    raise 

        if args.encrypt:

            if not os.path.exists(args.public_key):
                raise FileNotFoundError("{} path does not exist".format(args.public_key))

            try:

                Volt.encrypt_file_content(args.public_key,
                                        args.file_path,
                                        save_path=args.save_path,
                                        fernet_key_encryption=args.fernet_key_encryption,
                                        replace = args.replace,
                                        file_type=args.file_type)
            except Exception as e:
                logging.error(traceback.format_exc())

        if args.create_key and not (args.encrypt or args.decrypt):

            try:
                Volt.createKeys(args.private_key_name,
                                args.public_key_name,
                                args.save_path,
                                ext =args.ext,
                                private_key_password=args.private_key_password,
                                encrypt_private_key = args.encrypt_private_key,
                                replace = args.replace,
                                pb_exp = args.public_exponent,
                                ky_size = args.key_size,
                                fernet_key = args.create_fernet_key,
                                encrypt_fernet_key=args.encrypt_fernet_key)

            except Exception as e:
                logging.error(e, exc_info=True)
            else:
                pass

            pass
        
        if args.encrypt_dir and (args.all or args.file_type):

            if not os.path.exists(args.dir_path):
                raise FileNotFoundError("{} path does not exist".format(args.dir_path))

            if not os.path.exists(args.public_key):
                raise FileNotFoundError("{} path does not exist".format(args.public_key))


            if args.all:
                try:
                    set_ = []
                    for type_ in Volt.all_types:
                        for file_path in list(set(Volt.type_list(Volt.files_dict, type_, args.dir_path))):

                            if file_path[1] not in set_:
                                Volt.encrypt_file_content(args.public_key,
                                file_path[1],
                                save_path=file_path[0],
                                fernet_key_encryption=args.fernet_key_encryption,
                                replace = args.replace,
                                file_type=type_)
                                set_.append(file_path[1])

                except Exception as e:
                    print(e)
                    raise

            if args.file_type and (not args.all):
                try:
                    for file_path in Volt.type_list(Volt.files_dict, args.file_type, args.dir_path):
                        Volt.encrypt_file_content(args.public_key,
                        file_path[1],
                        save_path=file_path[0],
                        fernet_key_encryption=args.fernet_key_encryption,
                        replace = args.replace,
                        file_type=args.file_type)
                except Exception as e:
                    print(e)
                    raise 


    except Exception as e:
        raise
    return


def parse_arguments(argv):

    # encrypt file(s) or decrypt file(s)
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encrypt', required=False, action='store_true',
        help ='encrypt file')
    parser.add_argument('-d','--decrypt', required=False, action='store_true',
        help ='decrypt file')
    parser.add_argument('--encrypt_dir', required=False, action='store_true',
    help ='encrypt direcotry')
    parser.add_argument('--decrypt_dir', required=False, action='store_true',
    help = 'decrypt direcotry')

    # key, file and save paths. Note, path to fernet can be used to as public key path
    parser.add_argument('-p','--private_key', required=False,
        help ='private key full path')
    parser.add_argument('-l','--public_key', required=False,
        help ='public/fernet key full path')
    parser.add_argument('-f','--file_path', required=False,
        help ='file_path full path')
    parser.add_argument('-s','--save_path', required=False, default='/home/zeefu/Desktop',
        help ='save path')
    parser.add_argument('-a', '--dir_path',required=False, 
        help='directory of files to encrypt')
    parser.add_argument('--all',required=False, action='store_true',
    help='encrypt all file types in given directory')


    # file type. see print Volt.files_dict to see dictionary
    parser.add_argument('-t','--file_type', required=False, default='document',
        help ='encrypted or decrypted file type')

    # replace exisiting private and public keys | replace existing encryped or decrypted files
    parser.add_argument('-i','--replace', required=False, default=False, action='store_true',
        help ='replace encrypted or decrypted file/replace existing private or public key')
    parser.add_argument('-r','--no_replace', required=False, dest='replace', action='store_false',
        help ='do not replace existing encrypted/decrypted file or existing private/public key')

    parser.add_argument('-j','--fernet_key_encryption', required=False, default=False, action='store_true',
        help ='encryption using fernet key')
    parser.add_argument('-b','--public_key_encryption', required=False, dest='fernet_key_encryption', action='store_false',
        help ='encryption using public key as opposed to fernet key')
    parser.add_argument('-k','--fernet_key_decryption', required=False, default=False, action='store_true',
        help ='decryption using fernet key')
    parser.add_argument('-q','--private_key_decryption', required=False, dest='private_key_decryption', action='store_true',
        help ='decryption using private key')

    # creating private, public and fernet keys.
    parser.add_argument('-c','--create_key', required=False, action='store_true',
        help ='create new private/fernet key')
    parser.add_argument('-n','--private_key_name', required=False, default='private_key',
        help ='name of new private key/fernet key')
    parser.add_argument('-m','--public_key_name', required=False, default='public_key',
        help ='name of new fernet key or public key')
    parser.add_argument('--create_fernet_key', required=False, default= False,
        help ='option to create fernet key', action='store_true')
    parser.add_argument('--no_fernet_key', required=False, dest='create_fernet_key', action='store_false')

    # file extention
    parser.add_argument('--ext', required=False, default='.pem',
        help ='file extention to store base64-encoded private/public key string')

        # encrypting private/fernet keys. These are switch boolean arguments.
        # Note: if encrypt_private_key is true, thus  must be followed by private_key_password argument
    parser.add_argument('--encrypt_private_key', required=False, default= False, action='store_true',
        help ='option to encrypt private key')
    parser.add_argument('--bare_private_key', required=False, dest='encrypt_private_key', action='store_false',
        help='do not encrypt private key')
    parser.add_argument('-u','--encrypt_fernet_key', required=False, default=False, action='store_true',
        help ='encrypt fernet key using corresponding public key')
    parser.add_argument('-v','--bare_fernet_key', required=False, dest='encrypt_fernet_key', action='store_false',
        help ='produce unencrypted fernet key')

        # password must be a string. If None a ValueError exception will be raised.
    parser.add_argument('--private_key_password', required=False,
        help ='private key password')

    # cryptography parameters
    parser.add_argument('--public_exponent', required=False, default= 65537, type=int,
        help ='public exponent value')
    parser.add_argument('--key_size', required=False, default= 4096, type=int,
        help ='public exponent value')




    # parser.add_argument('-p','--private_key_password', required=False, action='store_true',
    #     help ='password')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
