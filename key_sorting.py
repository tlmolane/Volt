
import glob
import os

def key_list_numbers(directory, ext):
    folders = glob.glob(directory)
    key_list = []
    for folder in folders:
        #os.path.join()
        for f in glob.glob(folder+'/*.{}'.format(ext)):
            key_list.append(f)
        key_list_size = len(key_list)


    return (key_list, key_list_size)

def new_key_names(private_key_name, public_key_name, directory, path_pattern='_%s', ext='pem'):

    two_patterns = []
    new_patterns = []

    ext = ext.split('.')[-1]
    private_key_name, public_key_name = private_key_name.split('.')[0], public_key_name.split('.')[0]

    path_pattern_1 = os.path.join(directory, private_key_name + path_pattern + '.' + ext)
    path_pattern_2 = os.path.join(directory, public_key_name + path_pattern +'.' + ext)



    two_patterns.append(path_pattern_1)
    two_patterns.append(path_pattern_2)


    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    for path_pat in two_patterns:


        i = 1
        #print(path_pat % 2)

        # First do an exponential search
        while os.path.exists(path_pat % i):
            i = i*2

        # Result lies somewhere in the interval (i/2..i]
        # We call this interval (a..b] and narrow it down until a + 1 = b
        a, b = (i // 2, i)
        while a + 1 < b:
            c = (a + b) // 2 # interval midpoint
            a, b = (c, b) if os.path.exists(path_pat % c) else (a, c)

        new_patterns.append(path_pat % b)

    private_key_path_new, public_key_path_new = new_patterns[0], new_patterns[1]


    return private_key_path_new, public_key_path_new


def missing_key_check():
    pass

def new_file_name(file_name, directory, path_pattern='_%s', ext='pickle'):
    file_name = file_name.split('.')[0]
    ext = ext.split('.')[-1]

    path_pattern = os.path.join(directory, file_name + path_pattern + '.' + ext)


    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i*2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2 # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)


    return path_pattern % b

# private_key_name = 'private_key'
# public_key_name = 'public_key_name'
# path = os.path.join('home', 'zeefu', 'Documents', 'Volt', 'tshepo_molane', 'development')
# print(new_file_name('passwords.pickle',path, path_pattern='_%s', ext = '.pickle'))

# print(pri.split('/')[-1],
#       pub.split('/')[-1])
