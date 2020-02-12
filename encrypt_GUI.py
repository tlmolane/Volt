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


"premise: google has more resources to protect your passwords. keeping your password on your machine makes you more vulnerable..."
"to bigger organizations or persons with pertinent computer expertise - so there is a big asymmetry in risk."
"In other words, this small project was created for two reasons: for personal use, inspired by the personal goal to improve on python programming skills"


abs_path = os.path.dirname(os.path.abspath(__file__))

def decrypt(privatekey_password, pickle_file = 'passwords.pickle', private_key = 'private_key.pem'):

    global abs_path
    # path = os.path.join(abs_path, pickle_file)

    try:
        with open(os.path.join(abs_path, pickle_file), 'rb') as f:
            accounts_byte = pickle.load(f)
        f.close()

        try:

            with open(os.path.join(abs_path, private_key), 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                            key_file.read(),
                            password = b'%b' % privatekey_password.encode('utf-8'),
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
            print('[INFO] private key not found')
            print(e)
            return None

        # except ValueError:
        #     print("incorrect password")

    except FileNotFoundError as e:
        print(e)
        return None
        # print['[INFO] creating pickle file....']
        # accounts = {}
        # accounts_str = json.dumps(accounts)
        # accounts_byte = accounts_str.encode('utf-8')
        # file_name = pickle_file


    except  EOFError as e:
        print(e)
        return None

def remove_account(decrypted_dict, account, pickle_file = 'passwords.pickle', public_key = 'public_key.pem'):
    global abs_path

    try:
        accounts = decrypted_dict
        account = account.lower()

        if account in list(accounts.keys()):
            del accounts[account]

            accounts_str = json.dumps(accounts)
            accounts_byte = accounts_str.encode('utf-8')

            with open(os.path.join(abs_path, public_key), 'rb') as key_file:
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

                print('[INFO] encrypting updated dictionary...')

                with open(os.path.join(abs_path, pickle_file), 'wb') as f:
                    pickle.dump(encrypted, f)
                f.close()

                print('[INFO] done')

                return

            except FileNotFoundError as e:
                print(e)
                key_file.close()
                return None



    except KeyError:
        print("[INFO] {} does not exist in dictionary. \n [INFO] encrypting...".format(account))
        return decrypted_dict

    except Exception as e:
        print(e)
        return decrypted_dict


def encrypt(decrypted_dict, account, password, pickle_file = 'passwords.pickle', public_key = 'public_key.pem'):

    """this encrypts an existing pickle file after updating its dictionary object"""

    global abs_path

    try:

        #accounts = {'facebook': 'password1', 'twitter': 'password2'} # default account keys - these need to be decrypted first.
        accounts = decrypted_dict
        account = account.lower()
        if account not in list(accounts.keys()):
            print('[INFO] specified account does not exist. \n[INFO] Adding {} account to dictionary'.format(account))
            accounts[account] = str(password)

        accounts[account] = str(password) #change password of existing account on dict before encrypting

        accounts_str = json.dumps(accounts)
        accounts_byte = accounts_str.encode('utf-8')


        with open(os.path.join(abs_path, public_key), 'rb') as key_file:
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

            with open(os.path.join(abs_path, pickle_file), 'wb') as f:
                pickle.dump(encrypted, f)
            f.close()
            return

        except FileNotFoundError as e:
            print(e)
            key_file.close()
            return None

        key_file.close()

    except FileNotFoundError as e:
        print('[INFO] public key not found')
        print(e)
        key_file.close()
        return None


def create_dict(public_key = 'public_key.pem', pickle_file = 'passwords.pickle'):

    "creates empty dictionary and then encrypts it, using pre-existing public key file"


    global abs_path


    try:

        accounts = {}
        accounts_str = json.dumps(accounts)
        accounts_byte = accounts_str.encode('utf-8')


        with open(os.path.join(abs_path, public_key), 'rb') as key_file:
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


        with open(os.path.join(abs_path, pickle_file), 'wb') as f:
            pickle.dump(encrypted, f)

        f.close()
        key_file.close()

        print("[INFO] new dictionary has been encrypted \n use corresponding private key to decrypt" )
    except Exception as e:
        print(e)

    return

def pass_match(privatekey_password, private_key = 'private_key.pem' ):

    "Checks if entered private key password is correct"

    global abs_path

    try:

        with open(os.path.join(abs_path, private_key), 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password = b'%b' % privatekey_password.encode('utf-8'),
                        backend = default_backend()
            )

        key_file.close()

        return True

    except ValueError as e:
        print(e)
        return False

    except Exception as e:
        print(e)


def main(args):
    try:

        if args.encrypt and not args.decrypt:
            print(" [INFO] encryption!")

            number_of_attempts = 0
            max_attempts = 3

            while number_of_attempts <= max_attempts:
                private_key_password = getpass.getpass(prompt='Enter private key password: ')

                if pass_match(private_key_password) == False:
                    number_of_attempts += 1
                    print("[INFO] number of attempts left {}".format(max_attempts - number_of_attempts))
                    if number_of_attempts == 3:
                        print("[INFO] Max tries exceeded. Goodbye!")
                        break
                else:

                    while True:

                        account = str(input('name of account: '))
                        account_password = getpass.getpass(prompt='Enter your {} password: '.format(account)) #password

                        confirmation = str(input('confirm details for {} ? (y/n) '.format(account)))

                        if confirmation.lower().startswith('y'):
                            decrypted_dict = decrypt(privatekey_password = private_key_password)
                            print("[INFO] encrypting new details...")
                            encrypt(decrypted_dict, account, account_password)
                            print("[INFO] details successfully encrypted")
                            break
                        elif confirmation.lower().startswith('n'):
                            continue
                        else:
                            print("[INFO] program terminating. Goodbye!")
                            break

                    return

            return

        if args.decrypt and not args.encrypt:
            print("decryption!")

            number_of_attempts = 0
            max_attempts = 3

            while number_of_attempts <= max_attempts:
                private_key_password = getpass.getpass(prompt='Enter private key password: ')

                if pass_match(private_key_password) == False:
                    number_of_attempts += 1
                    print("[INFO] number of attempts left {}".format(max_attempts - number_of_attempts))
                    if number_of_attempts == 3:
                        print("[INFO] Max tries exceeded. Goodbye!")
                        break
                else:

                    while True:

                        account = str(input('name of account: '))
                        #account_password = getpass.getpass(prompt='Enter your {} password: '.format(account)) #password

                        confirmation = str(input('confirm details for {} ? (y/n) '.format(account)))

                        if confirmation.lower().startswith('y'):
                            decrypted_dict = decrypt(privatekey_password = private_key_password)
                            print(decrypted_dict[account])
                            break
                        elif confirmation.lower().startswith('n'):
                            continue
                        else:
                            print("[INFO] program terminating. Goodbye!")
                            break

                    return
            return

        if args.create:
            #variable = getpass.getpass(prompt='Enter private key password: ')
            create_dict()
            return

        if args.remove:

            number_of_attempts = 0
            max_attempts = 3

            while number_of_attempts <= max_attempts:
                private_key_password = getpass.getpass(prompt='Enter private key password: ')

                if pass_match(private_key_password) == False:
                    number_of_attempts += 1
                    print("[INFO] number of attempts left {}".format(max_attempts - number_of_attempts))
                    if number_of_attempts == 3:
                        print("[INFO] Max tries exceeded. Goodbye!")
                        break
                else:

                    while True:

                        account = str(input('name of account: '))
                        confirmation = str(input('confirm details for {} ? (y/n) '.format(account)))

                        if confirmation.lower().startswith('y'):
                            decrypted_dict = decrypt(privatekey_password = private_key_password)
                            print("[INFO] deleting entry {} from dictionary".format(account))
                            remove_account(decrypted_dict, account)
                            break
                        elif confirmation.lower().startswith('n'):
                            continue
                        else:
                            print("[INFO] program terminating. Goodbye!")
                            break
                    return
        else:
            print("Charlatan! what do you want!?")
        return

    except Exception as e:
        print(e)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--encrypt', required=False, action='store_true',
        help ='encrypt new passwords')
    parser.add_argument('-c','--create', required=False, action='store_true',
        help ='encrypt new empty dictionary')
    parser.add_argument('-d','--decrypt', required=False, action='store_true',
        help ='decrypt new passwords')
    parser.add_argument('-r','--remove', required=False, action='store_true',
        help ='remove existing account in encrypted dictionary')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
