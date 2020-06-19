import hashlib #
import random #
random.seed(0)

def generate_hex_pass(password_string, max_length=10):

    try:
        max_length = max_length - 2
        password = password_string.encode('utf-8')
        sha_3 = hashlib.sha3_512(password)
        sha_3_hexdigest = sha_3.hexdigest()

        alpha_string = [a for a in sha_3_hexdigest if a.isalpha()]
        char_select = random.choice([char for char in '!@#$%^&*_'])
        alpha = alpha_string[random.randint(0,len(alpha_string)-1)].capitalize()

        hash_slice = sha_3_hexdigest[0:max_length]
        final_password = ''.join(hash_slice + alpha +char_select)
        final_password_hex_only = sha_3_hexdigest[0:max_length + 2]

        return (final_password, final_password_hex_only, sha_3_hexdigest )

    except Exception as e:
        print(e)

#print(generate_hex_pass('hello'))
