import unittest
import os
from create_keys_test import create_keys

class TestCreateKeys(unittest.TestCase):
    def test_parameters(self):

        private_key_name = 'private_test'
        public_key_name = 'public_test'
        save_path = os.getcwd()
        private_key_password = 'test'
        serialize_encryption= True
        public_exp=65537 
        keysize=2048

        result = create_keys(private_key_name=private_key_password, 
                            public_key_name=public_key_name,
                            private_key_password=private_key_password,
                            save_path = save_path, 
                            public_exp=public_exp,
                            keysize=keysize)
        
        print(result)
        
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
