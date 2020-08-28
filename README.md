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
### Static Methods
```volt_encrypt.createKeys```: creates private and public key pair with a fernet key as an optional key.  
```volt_encrypt.encrypt_file_content```: encrypts file content using an existing public or fernet key.   
```volt_encrypt.decrypt_file_content```: decrypts file content using an existing private key or fernet key.   
volt_encrypt.private_key_password_match: for an encrypted .pem private key, this function takes in a password as a string and returns True if password is correct and False if it is not    
### Encryption script
```
pem_fernet_encryption.py
```
### Usage

Explain how to run the automated tests for this system

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
