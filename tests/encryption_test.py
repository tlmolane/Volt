import unittest
import os
from encryption_testing import Volt

class TestCreateKeys(unittest.TestCase):
    def test_encrypt_file_contnet(self):
        
        # Testing parameters
        public_key_path = '/home/zeefu/Desktop/My Keys/Non Encrypted Keys/fernet.key'
        full_file_path = '/home/zeefu/Desktop/crypto_Stuff.txt'
        save_path = '/home/zeefu/Desktop/'
        # fernet_key_encryption = True
        # replace = False
        file_type = 'document'

        encrypt_file_result  = Volt.encrypt_file_content(public_key_path= public_key_path,
                                    full_file_path= full_file_path,
                                    save_path= save_path,
                                    fernet_key_encryption= True,
                                    replace= False,
                                    file_type=file_type)

        with open(full_file_path, 'r') as file:
            data = file.read()
            file.close()
        
        
        self.assertNotEqual(encrypt_file_result, data)

        # print(full_file_path)
    
    def test_decrypt_file_content(self):
        original_file_path = 
        private_key_path = '/home/zeefu/Desktop/My Keys/Non Encrypted Keys/fernet.key'
        #private_key_password =None
        encrypted_file_path = '/home/zeefu/Desktop/crypto_Stuff_1.txt'
        save_path = '/home/zeefu/Desktop/'
        #fernet_key_decrypt=True
        file_type='document'

        decrypt_file_result = Volt.decrypt_file_content(private_key_path= private_key_path,
                                    private_key_password= None,
                                    encrypted_file_path = encrypted_file_path,
                                    save_path= save_path,
                                    fernet_key_decrypt= True
                                    file_type= file_type)
        
        with open(full_file_path, 'r') as file:
            data = file.read()
            file.close()
            self.assertEqual


        pass

        

if __name__ == '__main__':
    unittest.main()
