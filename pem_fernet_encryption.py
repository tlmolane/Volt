from volt_encrypt import Volt
import password_hex
import key_sorting
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

#print(Volt.files_dict)



def main(args):
    try:
        if args.decrypt and not args.encrypt:
            #print("decryption!")

            number_of_attempts = 0
            max_attempts = 3

            if not os.path.exists(args.private_key):
                raise FileNotFoundError("{} path does not exist".format(args.private_key))

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
                    try:

                        Volt.decrypt_file_content(args.private_key,
                                                private_key_password,
                                                args.file_path,
                                                save_path = args.save_path,
                                                fernet_key_decrypt=args.fernet_key_decrypt,
                                                replace = args.replace,
                                                file_type=args.file_type
                                                )
                    except Exception as e:
                        logging.error(traceback.format_exc())


                    break

                    # while True:
                    #
        if args.encrypt and not args.decrypt:

            if not os.path.exists(args.public_key):
                raise FileNotFoundError("{} path does not exist".format(args.private_key))

            try:

                Volt.encrypt_file_content(args.public_key,
                                        args.file_path,
                                        save_path=args.save_path,
                                        fernet_key_encrypt=args.fernet_key_encrypt,
                                        replace = args.replace,
                                        file_type=args.file_type)
            except Exception as e:
                logging.error(traceback.format_exc())





    except Exception as e:
        raise
    return
# def main(args):
#     try:
#
#         if args.decrypt and not args.encrypt:
#             print("decryption!")
#
#             number_of_attempts = 0
#             max_attempts = 3
#
#             while number_of_attempts <= max_attempts:
#                 private_key_password = getpass.getpass(prompt='Enter private key password: ')
#
#                 if pass_match(private_key_password) == False:
#                     number_of_attempts += 1
#                     print("[INFO] number of attempts left {}".format(max_attempts - number_of_attempts))
#                     if number_of_attempts == 3:
#                         print("[INFO] Max tries exceeded. Goodbye!")
#                         break
#                 else:
#
#                     while True:
#
#                         account = str(input('name of account: '))
#                         #account_password = getpass.getpass(prompt='Enter your {} password: '.format(account)) #password
#
#                         confirmation = str(input('confirm details for {} ? (y/n) '.format(account)))
#
#                         if confirmation.lower().startswith('y'):
#                             decrypted_dict = decrypt(privatekey_password = private_key_password)
#                             pass_list = list(decrypted_dict[account])
#                             password_len = len(decrypted_dict[account])
#                             portion = int(round((1/3)*(password_len),0))
#                             #print(portion)
#
#                             for i in range(0, portion):
#
#                                 pass_list[i] = '*'
#                                 pass_list[-i] = '*'
#
#
#                             print("".join(pass_list))
#                             #print(decrypted_dict[account])
#
#                             #print(decrypted_dict[account])
#                             break
#                         elif confirmation.lower().startswith('n'):
#                             continue
#                         else:
#                             print("[INFO] program terminating. Goodbye!")
#                             break
#
#                     return
#             return
#
#         if args.create:
#             #variable = getpass.getpass(prompt='Enter private key password: ')
#             create_dict()
#             return
#
#         # if args.create_keys:
#         #
#         #     return
#         else:
#             print("Charlatan! what do you want!?")
#         return
#
#     except Exception as e:
#         print(e)
#
#

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encrypt', required=False, action='store_true',
        help ='encrypt file')
    parser.add_argument('-d','--decrypt', required=False, action='store_true',
        help ='decrypt file')
    parser.add_argument('-c','--create_key', required=False, action='store_true',
        help ='create new private/fernet key')
    parser.add_argument('-p','--private_key', required=False,
        help ='private key full path')
    parser.add_argument('-l','--public_key', required=False,
        help ='public/fernet key full path')
    parser.add_argument('-f','--file_path', required=False,
        help ='file_path full path')
    parser.add_argument('-s','--save_path', required=False, default='/home/zeefu/Desktop',
        help ='save path')
    parser.add_argument('-t','--file_type', required=False, default='document',
        help ='encrypted or decrypted file type')
    parser.add_argument('-r','--replace', required=False, default=False,
        help ='replace encrypted or decrypted file')
    parser.add_argument('-k','--fernet_key_decrypt', required=False, default=False,
        help ='decrypt with fernet key')
    parser.add_argument('-q','--fernet_key_encrypt', required=False, default=False,
        help ='fernet key encryption')

    # parser.add_argument('-p','--private_key_password', required=False, action='store_true',
    #     help ='password')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
