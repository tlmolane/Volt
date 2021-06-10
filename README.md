# Volt 

This ongoing project's name is called Volt which applies symmetric and asymmetric encryption. It is a simple program that allows one to generate a private and public key using an RSA algorithm to encypt and decrypt file contents. The encrypt_file.py Volt class containts static methods that allow one to encrypt a file (.txt, .py, .docx, .odt etc ) using pem private/public keys and fernet keys.  

### Prerequisites

Python 3.6  
cryptography 2.8 (Python)

### Installation
Create and activate conda or virtualenv environment and pip install cryptography 2.8

```
pip install cryptography
```
## Important Details
WARNING: Be sure to keep your public and fernet keys safe as losing these may result in loss of infromation. Store passwords for your encrypted private_key passwords some place you can remember and access.

### On using generated asymmetric keys (.pem private and private keys) 
Since it is an RSA algorithm that is used to generate these asymmetric keys, one is limited to 256 bytes of plaintext data to encrypt (at most). To encrypt longer plaintexts,  the solution is to increase the key size (max value being 4096, see script arguments). If the plaintext data is too long, first encrypting the plaintext data using a fernet key (symmetric encryption) followed by encrypting the same fernet key using a public key (asymmetric key encryption) is a viable solution.  



## Main script files
### Volt class script
```
volt_encrypt.py
```
This script cotains the Volt class which, for now, largely consists of static methods which encrypt and decrypt a set of file types using private, public and fernet keys. 

### Main static methods
```volt_encrypt.createKeys```: creates private and public key pair with a fernet key as an optional key.  
```volt_encrypt.encrypt_file_content```: encrypts file content using an existing public or fernet key.   
```volt_encrypt.decrypt_file_content```: decrypts file content using an existing private key or fernet key.   
```volt_encrypt.private_key_password_match```: for an encrypted .pem private key, this function takes in a password as a string and returns True if password for the encrypted private key is correct, returns False otherwise.

### Encryption script
```
pem_fernet_encryption.py
```
This script can be used to create encryption key pairs and to encrypt or decrypt document file types.

### Examples of Use
#### Creating Keys:

##### Create private key, public key, unencrypted fernet key to specified path (fern_key_encrypt is True by default)
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop/ --encrypt_private_key False --replace False --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```

##### Create unencrypted private key, public key and unencrypted fernet key to specified path.
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --bare_private_key --replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```

##### Create encrypted private key with public key and a public key encrypted fernet key. Replace existing keys.
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key_test.pem --public_key_name public_key_test.pem --save_path /home/user/Desktop/ --encrypt_private_key --private_key_password 'testpassword' --replace --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```

##### Create encrypted private key with, public key and a public key encrypted fernet key and keep existing keys.
``` $ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --encrypt_private_key --private_key_password 'testpassword' --no_replace --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```
#### Encrypting files and direcotries:

##### Encrypt a document type using a .pem public key and keep original (delete original with --replace).
```$ python pem_fernet_encryption.py --encrypt --file_type document --public_key /path/to/public_key.pem --save_path /save/path/ --public_key_encryption --replace --file_path /path/to/file ```

##### Encrypt a document type using fernet key and keep original (delete original with --replace).
```$ python pem_fernet_encryption.py --encrypt --file_type document --public_key /path/to/fernet.key --save_path /save/path/for/decrypted/document/ --fernet_key_encryption --replace --file_path /path/to/file ```

##### Encrypt document types in a directory recursively using a fernet key.
```$ python pem_fernet_encryption.py --encrypt_dir --file_type document --public_key /path/to/fernet.key --dir_path /path/to/directory --fernet_key_encryption ```

##### Encrypt all document types recursively using a fernet key.
```$ python pem_fernet_encryption.py --encrypt_dir --all --public_key /path/to/fernet.key --dir_path /path/to/directory/ --fernet_key_encryption --no_replace ```

#### Decrypting files and directories:

##### Decrypt file type content using fernet key (give path to fernet key)
```$ python pem_fernet_encryption.py --decrypt --private_key /path/to/fernet.key --file_path /path/to/encrypted/file --save_path /save/path/ --fernet_key_decryption --no_replace --file_type <file type> ```

##### Decrypt file type content using private key (keep original with --no_replace) 
```$ python pem_fernet_encryption.py --decrypt --private_key /path/to/private_key.pem --file_path /path/to/encrypted/file --save_path /save/path/ --private_key_decryption --file_type <file type> --no_replace --private_key_decryption -file_type <file_type> ```

##### Decrypt all file types in directory using fernet key (--all)
```$ python pem_fernet_encryption.py --decrypt_dir --private_key /path/to/fernet.key --dir_path /path/to/encrypted/file --fernet_key_decryption --all --no_replace ```

##### Decrypt file of specified existing type in directory using fernet key 
```$ python pem_fernet_encryption.py --decrypt_dir --private_key /path/to/fernet.key --file_path /path/to/encrypted/file --fernet_key_decryption --file_type document --no_replace ```

##### Decyrpt file using fernet key 
```$ python pem_fernet_encryption.py --decrypt --private_key /path/to/fernet.key --file_path /full/path/to/file/ --save_path  /save/path/ --no_replace --fernet_key_decryption --file_type <file type> ```

## Project status
Slow development because of other commitments but would like to add new features:  
- cloud storage of encrypted keys and documents using available APIs (Mega Cloud/ Google Drive)
- Database for stored encrypted keys

## Versioning
This is the first code base (version 1).
## Authors

* **Tshepo L. Molane**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Inspiration: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
