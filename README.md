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
#### Create private key, public key, unencrypted fernet key to specified path (set fern_key_encrypt to True to encrypt fernet key with public key)
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop/ --encrypt_private_key False --replace False --public_exponent 65537 --key_size 4096 --create_fernet_key False --fernet_key_encrypt False ```

#### Create unencrypted private key, public key and unencrypted fernet key to specified path
``` $ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --bare_private_key --replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --fernet_key_encryption ```

#### Create encrypted private key with, public key and a public key encrypted fernet key
```$ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --encrypt_private_key --private_key_password 'mypassword' --replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key
 ```

#### Create encrypted private key with, public key and a public key encrypted fernet key and keep existing keys.
``` $ python pem_fernet_encryption.py --create_key --private_key_name private_key.pem --public_key_name public_key.pem --save_path /home/user/Desktop --encrypt_private_key --private_key_password 'apexsingularity01' --no_replace  --public_exponent 65537 --key_size 4096 --create_fernet_key --encrypt_fernet_key ```

### Encrypt a document types in a directory recursively using a fernet key.
``` $ python pem_fernet_encryption.py --encrypt_dir --file_type document --public_key /home/zeefu/Desktop/My\ Keys/Non\ Encrypted\ Keys/fernet.key --dir_path /path/to/directory --fernet_key_encryption ```

#### Encrypt all document types recursively using a fernet key. delete unencrypted file types.
```$ python pem_fernet_encryption.py --encrypt_dir --all --public_key /path/to/fernet.key --dir_path /home/zeefu/Desktop/test/ --fernet_key_encryption --no_replace
 ```











### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
=======
# Volt
>>>>>>> 95737e387ec31937325741da0626af230620b22b
