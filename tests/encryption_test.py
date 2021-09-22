import unittest
import os
from encryption_testing import Volt
import time

class TestCreateKeys(unittest.TestCase):
    def test_symmetric_encryption(self):
        
        # Encryption: Test parameters
        original_file_path = '/home/zeefu/Desktop/crypto_Stuff.txt'
        public_key_path = '/home/zeefu/Desktop/My Keys/Non Encrypted Keys/fernet.key'
        private_key_path = '/home/zeefu/Desktop/My Keys/Non Encrypted Keys/fernet.key'
        encrypted_file_path = '/home/zeefu/Desktop/crypto_Stuff_1.txt'
        #private_key_password =None
        full_file_path = '/home/zeefu/Desktop/crypto_Stuff.txt'
        save_path = '/home/zeefu/Desktop/'
        # fernet_key_encryption = True
        #fernet_key_decrypt=True
        # replace = False
        file_type = 'document'

        encrypted_file_result  = Volt.encrypt_file_content(public_key_path= public_key_path,
                                    full_file_path= full_file_path,
                                    save_path= save_path,
                                    fernet_key_encryption= True,
                                    replace= False,
                                    file_type=file_type)
        
        time.sleep(5)

        with open(full_file_path, 'r') as file:
            data = file.read()
            file.close()
        
        
        self.assertNotEqual(encrypted_file_result, data)

        decrypt_file_result = Volt.decrypt_file_content(private_key_path= private_key_path,
                            private_key_password= None,
                            encrypted_file_path = encrypted_file_path,
                            save_path= save_path,
                            fernet_key_decrypt= True,
                            file_type= file_type)

        with open(original_file_path, 'rb') as file:
            data = file.read()
            file.close()
        
        self.assertEqual(data, decrypt_file_result)

        
if __name__ == '__main__':
    unittest.main()
