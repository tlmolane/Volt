import pickle
import json
import os

# def decrypt(pickle_file, privatekey_password):
#
#     try:
#         path = os.path.join(os.getcwd(), pickle_file)
#         with open(path, 'rb') as f:
#             accounts_byte = pickle.load(f)
#         f.close()
#
#     except FileNotFoundError:
#         return


# def check_path():
#     abs_path = os.path.dirname(os.path.abspath(__file__))
#     path = os.path.join(abs_path, 'pickle_file')
#     print(path)
#     try:
#         with open(path, 'wb') as f:
#             print("file opened")
#         f.close()
#         return
#     except FileNotFoundError:
#         print("doesn't exist")
#         return


#check_path()

# print(os.path.dirname(os.path.abspath(__file__)))


def decrypt(pickle_file, privatekey_password):

    abs_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(abs_path, pickle_file)

    print(path)

    try:
        print('1')
        with open(path, 'rb') as f:
            accounts_byte = pickle.load(f)
        f.close()
    except FileNotFoundError as e:
        print('2')
        print(e)
        with open(path, 'wb') as f:
            accounts_byte = pickle.load(f)
        f.close()
    except EOFError as e:
        print('3')
        print(e)
    except Exception as e:
        print('4')
        print(e)
decrypt('pickle_file.pickle', 'password')
