# Volt 

This ongoing project's name is called Volt which applies symmetric and asymmetric encryption. It is a simple program that creates a private key and public key to encypt and decrypt a file contents. The encrypt_file.py Volt class containts static methods that allow one to encrypt a file (.txt, .py, .docx, .odt etc ) using pem private/public keys and fernet keys.  

### Prerequisites

Python 3.6  
cryptography 2.8 (Python)

### Installation
Create and activate conda or virtualenv environment and pip install crptography 2.8

```
pip install cryptography
```
## Important Details

## Main script files
### Volt class script
This script cotains the Volt class which, for now, largely consists of static methods which encrypt and decrypt a set of file types using private, public and fernet keys. 
```
volt_encrypt.py
```

### Main static methods
```volt_encrypt.createKeys```: creates private and public key pair with a fernet key as an optional key.  
```volt_encrypt.encrypt_file_content```: encrypts file content using an existing public or fernet key.   
```volt_encrypt.decrypt_file_content```: decrypts file content using an existing private key or fernet key.   
```volt_encrypt.private_key_password_match```: for an encrypted .pem private key, this function takes in a password as a string and returns True if password for the encrypted private key is correct, returns False otherwise.

### Encryption script
```
pem_fernet_encryption.py
```
### Examples of Use
#### Creating Keys:

##### Create private key, public key, unencrypted fernet key to specified path (set fern_key_encrypt to True to encrypt fernet key with public key)
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop/ --encrypt_private_key False --replace False --public_exponent 65537 --key_size 4096 --create_fernet_key False --fernet_key_encrypt False ```

##### Create unencrypted private key, public key and unencrypted fernet key to specified path
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --bare_private_key --replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --fernet_key_encryption ```

##### Create encrypted private key with, public key and a public key encrypted fernet key
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --encrypt_private_key --private_key_password 'mypassword' --replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```

##### Create encrypted private key with, public key and a public key encrypted fernet key and keep existing keys.
``` $ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --encrypt_private_key --private_key_password 'apexsingularity01' --no_replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```
#### Encrypting files and direcotries:

##### Encrypt a document type using a .pem public key and keep original (delete original with --replace).
```$ python pem_fernet_encryption.py --encrypt --file_type document --public_key /path/to/public_key.pem --save_path /save/path/ --public_key_encryption --no_replace ```

##### Encrypt a document type using fernet key and keep original (delete original with --replace).
```$ python pem_fernet_encryption.py --encrypt --file_type document --public_key /path/to/public_key.pem --save_path /save/path/for/decrypted/document/ --fernet_key_encryption --no_replace ```

##### Encrypt document types in a directory recursively using a fernet key.
```$ python pem_fernet_encryption.py --encrypt_dir --file_type document --public_key /home/zeefu/Desktop/My\ Keys/Non\ Encrypted\ Keys/fernet.key --dir_path /path/to/directory --fernet_key_encryption ```

##### Encrypt all document types recursively using a fernet key.
```$ python pem_fernet_encryption.py --encrypt_dir --all --public_key /path/to/fernet.key --dir_path /path/to/directory/ --fernet_key_encryption --no_replace ```

#### Decrypting files and directories:

##### Decrypt file type content using fernet key (give path to fernet key)
```$ python pem_fernet_encryption.py --decrypt --private_key /path/to/fernet.key --file_path /path/to/encrypted/file --save_path /save/path/ --fernet_key_decryption ```

##### Decrypt file type content using private key 
```$ python pem_fernet_encryption.py --decrypt --private_key /path/to/private_key.pem --file_path /path/to/encrypted/file --save_path /save/path/ --fernet_key_decryption ```


##### Decrypt all file types in directory using fernet key (--all)
```$ python pem_fernet_encryption.py --decrypt_dir --private_key /path/to/fernet.key --file_path /path/to/encrypted/file --fernet_key_decryption --all --no_replace ```

##### Decrypt file of specified existing type in directory using fernet key 
```$ python pem_fernet_encryption.py --decrypt_dir --private_key /path/to/fernet.key --file_path /path/to/encrypted/file --fernet_key_decryption --file_type document --no_replace ```



## Versioning
This is the first code base (version 1).
## Authors

* **Tshepo L. Molane**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Inspiration: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
