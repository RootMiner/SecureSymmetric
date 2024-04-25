#!/usr/bin/env python3

import os
import stat
from hashlib import md5
from platform import system
from getpass import getpass
# from shutil import make_archive
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from argparse import ArgumentParser, SUPPRESS

# Shell colors, originally these are light version of the colors
R = '\033[91m'  # Light Red
G = '\033[92m'  # Light Green
B = '\033[94m'  # Light Blue
C = '\033[96m'  # Cyan
Y = '\033[93m'  # Yellow
P = '\033[95m'  # Purple
r = '\033[0m'   # reset color value

# Shell Font Style
I = '\033[3m'  # Italic

# Success, Error and Question prompt color coding
S = f'{G}*{r}'
E = f'{R}!{r}'
Q = f'{Y}?{r}'

if   system() == 'Linux'  : separator = '/'
elif system() == 'Windows': separator = '\\'

write_file    = True
overwrite_all = False

# generates a key with the provided password using fernet symmetric encryption algorithm
def gen_fernet_key (masterpass:bytes) -> bytes:
    assert isinstance(masterpass, bytes)
    hlib = md5()
    hlib.update(masterpass)
    return urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


# takes the master password as to create the original key value 
def input_master_key ():
    if   args.encrypt: for_what = 'Encryption'
    elif args.decrypt: for_what = 'Decryption'
    masterpass = getpass(f"{P}[Œ]{r} Enter {for_what} Password: "); print()
    key = gen_fernet_key(masterpass.encode('utf-8'))
    return Fernet(key)


# encryption and decryption in one function
def process_data (file_name, path, data, fernet):
    global write_file, overwrite_all
    dec_failed = False
    if args.encrypt: enc_data = fernet.encrypt(data)
    elif args.decrypt:
        try:
            dec_data = fernet.decrypt(data)
        except:
            print(f"[{E}] Decryption Failed for {R}{file_name}{r}")
            # variable implimented not to write or remove files if the decryption failed
            dec_failed = True
            write_file = False

    # output file naming for both encrypted and decrypted file
    if args.encrypt:
        mod_file_name = 'enc_' + file_name
        if path != file_name: file_path = path + mod_file_name
        else: file_path = mod_file_name
    elif args.decrypt:
            if 'enc_' in file_name: mod_file_name = file_name[4:]
            else: mod_file_name = file_name
            if path != file_name: file_path = path + mod_file_name
            else: file_path = mod_file_name

    if os.path.exists(file_path) and not overwrite_all and not dec_failed:
        print(f"\n[{E}] The file named {C}{mod_file_name}{r} already exists.")
        y_or_n = input(f"[{Q}] Do you want to overwrite [Y]es/[A]ll/[N]o: ")
        if y_or_n.lower() != 'y' and y_or_n.lower() != 'a': write_file = False
        if y_or_n.lower() == 'a': overwrite_all = True

    if write_file == True:
        with open(file_path, 'wb') as output_file:
            output_file.seek(0)
            if args.encrypt:
                output_file.write(enc_data)
                if system() == 'Linux'  : os.chmod(file_path, 0o600)        # read only permission set for linux
                if system() == 'Windows': os.chmod(file_path, stat.S_IREAD) # read only permission set for windows
                print(f"[{S}] Successfully Encrypted {G}{file_name}{r}")
            elif args.decrypt and dec_failed == False:
                output_file.write(dec_data)
                os.chmod(file_path, 0o644)
                print(f"[{S}] Successfully Decrypted {G}{file_name}{r}")


# i have no idea why i have to work so hard on this, but i do
def path_handling (path):
    bogus_path = 1
    try:
        if path.find(separator) >= 0:
            obj_name = path.split(separator)[-1]
            while obj_name == '':
                obj_name = path.split(separator)[-1 - bogus_path]
                bogus_path = bogus_path + 1
        else: obj_name = path
    except AttributeError:
        if args.dir: print(f"[{E}] Please provide a directory path")
        else: print(f"[{E}] Please provide a file path")
        exit()

    obj_path = separator.join(path.split(separator)[:-bogus_path])
    if path[0] == separator : obj_path = separator + obj_path
    if len(obj_path) != 0: obj_path = obj_path + separator
    else: obj_path = obj_name
    return obj_name, obj_path


# checks if a perticular file is valid and prints related errors
def validate_file (file_path):
    fileName, path = path_handling(file_path)

    # to prevent encrypting an already encrypted file
    if args.encrypt and 'enc_' in fileName: return False, None, None, None
    # to prevent checking files that doesn't have enc_ before them
    # a better logic will be applied in future to deal with any sort of file
    elif args.decrypt and not 'enc_' in fileName: return False, None, None, None

    if fileName != path: filePath = path + fileName
    else: filePath = fileName
    try:
        with open(filePath, 'rb') as theFile:
            theFile.seek(0)
            data = theFile.read()
            return True, fileName, path, data
    except FileNotFoundError : print(f"[{E}] The specified file {C}{fileName}{r} does not exist")
    except PermissionError   : print(f"[{E}] Permission denied for file {C}{fileName}{r}")
    except IsADirectoryError : print(f"[{E}] {B}{fileName}{r} is a directory")
    except NotADirectoryError: print(f"[{E}] What the $%&* is {Y}{fileName}{r}")
    except UnicodeDecodeError: print(f"[{E}] Sorry, binary file ({G}{fileName}{r}) support coming soon!")
    return False, None, None, None


# check directory 
def is_valid_directory (dir_path, is_out_dir=None):
    directory_name, path = path_handling(dir_path)
    if is_out_dir:
        if directory_name == path: path = path + separator
        else: path = path + directory_name + separator
    try:
        dirContent = os.listdir(dir_path)
        if len(dirContent) > 0 or is_out_dir:
            if is_out_dir: return True, path
            else: return True
        else: print(f"[{E}] {B}{directory_name}{r} is an empty directory"); exit()
    except FileNotFoundError:
        if is_out_dir: print(f"[{E}] Invalid output directory {B}{directory_name}{r} "); exit()
        else: print(f"[{E}] The specified directory {B}{directory_name}{r} does not exist")
    except PermissionError   : print(f"[{E}] Permission denied for folder {B}{directory_name}{r}")
    except NotADirectoryError: print(f"[{E}] {B}{directory_name}{r} is not a directory")
    return False


def process_file (fernet, file_path):
    is_file, file_name, path, data = validate_file(file_path)
    if its_out_dir : path = out_dir_path
    # This is only for one single file instead of a directory of files
    if not args.dir and is_file : fernet = input_master_key()
    if is_file: process_data(file_name, path, data, fernet)
    if args.remove and write_file : os.remove(file_path)


# initial logic and condition sets
def main () :
    # had to make it global, currently no idea how to access it otherwise
    # i don't want to send this as arguments for some reason
    global its_out_dir, out_dir_path
    its_out_dir = False
    if not any(vars(args).values()): parser.print_help()
    elif args.encrypt and args.decrypt:
        print(f"[{R}!{r}] Please use only one cryptographic process")
    elif args.encrypt or args.decrypt:
        try:
            if args.output :
                its_out_dir, out_dir_path = is_valid_directory(args.output, True)
            if args.dir:
                if args.extensions is not None:
                    extensions = [ext.strip() for ext in args.extensions.split(",")]
                if is_valid_directory(args.path):
                    fernet = input_master_key()
                    dirContent = os.listdir(args.path)
                    for content in dirContent:
                        # the file path is also needed in case of no extension provided
                        file_path = os.path.join(args.path, content)
                        if args.extensions:
                            for extension in extensions:
                                if content.endswith(extension):
                                    process_file(fernet, file_path)
                                    break
                        else: process_file(fernet, file_path)
            # a logic is placed at function called, to cope with the fernet key
            else: process_file(None, args.path)
        except KeyboardInterrupt: print(f"\n\n[»] Bye")
    else: print(f"[{E}] Please choose a cryptographic process")


# lots of flags and arguments o_0
print()
parser = ArgumentParser(description=f'{I}Encrypts and Decrypts Data{r}',
                         epilog='Made with <3 by @Syrine && @1byteBoy',
                         usage="%(prog)s [OPTIONS...] [PATH...]")

parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the file")
parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file")
parser.add_argument("-D", "--dir", action="store_true", help="Work with a whole directory of files")
parser.add_argument("-x", "--extensions", type=str, metavar='', help="Specify specific file extensions")
parser.add_argument("-o", "--output", type=str, metavar='', help="Output directory path")
parser.add_argument("-r", "--remove", action="store_true", help="Removes original file|s after encrytion or decryption")
# parser.add_argument("-z", "--zip", action="store_true", help="File|s get Zipped and then encrypted")
parser.add_argument('path', type=str, nargs='?', help=SUPPRESS)
args = parser.parse_args()

if __name__ == '__main__': main()

