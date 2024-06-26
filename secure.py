#!/usr/bin/env python3

import os
import asyncio
from hashlib import md5
from getpass import getpass
from platform import system
from zipfile import ZipFile
from tempfile import mkdtemp
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from argparse import ArgumentParser, SUPPRESS
from shutil import make_archive, copy, rmtree

# prints plain text data on terminal in beautified way
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer_for_filename

# Custom import 
from src.discord import uploadFile
from src.file_tweak import file_tweak
from src.colors import *

if   system() == 'Linux'  : separator = '/'
elif system() == 'Windows': separator = '\\'
write_file    = False
overwrite_all = False

file_count = 0
skip_count = 0

# for saving files paths first and then working with them
file_dict = {}
zip_arr   = []


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
  masterpass = getpass(f"{P}[Œ]{r} Enter {for_what} Password: ")
  confirm_masterpass = getpass(f"{P}[Œ]{r} Confirm {for_what} Password: ")
  if masterpass != confirm_masterpass:
    print("masterpass and confirmed masterpass did not match. try again!")
    exit()
  print(f"{R}--------{G}-----------{B}----------{C}-----------{r}")
  key = gen_fernet_key(masterpass.encode('utf-8'))
  return Fernet(key)


# prints plain text data directly on terminal interface
def print_decrypted_data(dec_data, mod_file_name):
  try:
    content = dec_data.decode('UTF-8')
    try:
      lexer = guess_lexer_for_filename(mod_file_name, content)
      # Themes : monokai, dracula, solarized-dark
      syntax = Syntax(content, lexer, theme="dracula", line_numbers=True)
      console = Console()
      syntax_with_border = Panel(syntax, title=mod_file_name)
      console.print(syntax_with_border)
    except ClassNotFound: 
      print(f"\n[{E}] No valid file extension, trying to read..\n")
      print(dec_data.decode('UTF-8')) 
      pass
  except UnicodeDecodeError: print(f"[{E}] Error reading data in {R}{mod_file_name}{r}")


# encryption and decryption in one function
def process_data (file_name, path, data, fernet):
  global write_file, overwrite_all
  dec_failed = False
  if args.encrypt: 
    enc_data = fernet.encrypt(data)
    write_file = True
  elif args.decrypt:
    try:
      dec_data = fernet.decrypt(data)
      write_file = True
    except:
      print(f"[{E}] Decryption Failed for {R}{file_name}{r}")
      # variable implimented not to write or remove files if the decryption failed
      dec_failed = True

  # output file naming for both encrypted and decrypted file
  # it's recomended not to change the encrypted file name
  # and neither rename a non encrypted file to enc_ intensinally for the harcoded nature
  if args.encrypt: 
    file_path, mod_file_name = file_tweak(file_name, path, True)
  elif args.decrypt: 
    file_path, mod_file_name = file_tweak(file_name, path)

  if os.path.exists(file_path) and not overwrite_all and not dec_failed:
    print(f"\n[{E}] A file named {C}{mod_file_name}{r} already exists.")
    while True:
      y_or_n = input(f"[{Q}] Do you want to overwrite [Y]es/[A]ll/[N]o: ").lower()
      if y_or_n == 'y': pass; break
      elif y_or_n == 'a': overwrite_all = True; break
      elif y_or_n == 'n':  write_file = False; break            
  if write_file == True:
    with open(file_path, 'wb') as output_file:
        output_file.seek(0)
        if args.encrypt:
          output_file.write(enc_data)
          if system() == 'Linux': os.chmod(file_path, 0o600)
          # if system() == 'Windows': 
          # os.chmod(file_path, stat.S_IREAD) # read only permission set for windows
          print(f"[{S}] Successfully Encrypted {G}{file_name}{r}")
        elif args.decrypt and dec_failed == False:
          output_file.write(dec_data)
          os.chmod(file_path, 0o644)
          print(f"[{S}] Successfully Decrypted {G}{file_name}{r}")
          if args.print and not dec_failed and not args.encrypt:
            print_decrypted_data(dec_data, mod_file_name)
    if args.upload and args.encrypt:
      file_dict[mod_file_name] = file_path


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


# checks if a particular file is valid and prints related errors
def validate_file (file_path):
  fileName, path = path_handling(file_path)
  global skip_count
  # to prevent encrypting an already encrypted file
  if args.encrypt and 'enc_' in fileName:
    skip_count = skip_count + 1
    print (f"[{E}] Skipping {fileName}")
    return False, None, None, None
  # to prevent checking files that doesn't have enc_ before them
  # a better logic will be applied in future to deal with any sort of file
  elif args.decrypt and not 'enc_' in fileName: 
    print (f"[{E}] Skipping {fileName}") 
    return False, None, None, None

  if fileName != path: filePath = path + fileName
  else: filePath = fileName
  try:
    with open(filePath, 'rb') as theFile:
      theFile.seek(0)
      data = theFile.read()
      return True, fileName, path, data
  except FileNotFoundError : print(f"[{E}] The specified file {C}{fileName}{r} does not exist")
  except PermissionError   : print(f"[{E}] Permission denied for file {C}{fileName}{r}")
  except IsADirectoryError : print(f"[{E}] {B}{fileName}{r} is a directory"); exit()
  except NotADirectoryError: print(f"[{E}] What the $%&* is {Y}{fileName}{r}")
  # except UnicodeDecodeError: print(f"[{E}] Sorry, binary file ({G}{fileName}{r}) support coming soon!")
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
  global file_count
  file_count = file_count + 1
  if is_file:
    if args.zip and fernet is None: return True
    if its_out_dir: path = out_dir_path
    # This is only for one single file instead of a directory of files
    # temp fix, trying to change in future
    if not args.dir and is_file and not args.zip: 
      fernet = input_master_key()
    process_data(file_name, path, data, fernet)
    if args.remove and write_file: 
      # print(f"Deleting : {file_name}")
      if args.upload and not args.decrypt: pass
      else:
        if input("do you want to delete " + file_path + " [Y/n]: ") in ["", "y", "Y"]: os.remove(file_path)
        else: pass


def upload_online ():
  if args.upload and args.encrypt and file_count != skip_count:
    print(f"\n[{Y}...{r}] Trying to connect to discord")
    asyncio.run(uploadFile(file_dict, args.remove))


def dir_contents (fernet=None):
  if args.extensions is not None:
    extensions = [ext.strip() for ext in args.extensions.split(",")]
  dirContent = os.listdir(args.path)
  for content in dirContent:
    # the file path is also needed in case of no extension provided
    file_path = os.path.join(args.path, content)
    if args.extensions:
      for extension in extensions:
        if content.endswith(extension):
          if args.zip: zip_arr.append(file_path)
          else: process_file(fernet, file_path)
          break
    else: process_file(fernet, file_path)
  if args.zip: return zip_arr


def process_zip ():
  def zipping():
      fernet = input_master_key()
      print(f"\n[{S}] Archived Successfully")
      # print(f"{archive_name}.{archive_format}"); exit()
      process_file(fernet, f"{archive_name}.{archive_format}")

  if args.zip and args.encrypt:
      archive_format = 'zip' # 'zip', 'tar', 'gztar', 'bztar', 'xztar'
      obj_name, archive_path = path_handling(args.path)
      if obj_name != archive_path: 
        archive_path = archive_path + obj_name # original directory path
      if '.' in obj_name: 
        archive_name = obj_name.split('.')[0]
      else:  archive_name = obj_name
      # custom output zip file directory
      if its_out_dir:
        archive_name = out_dir_path + archive_name
      if args.dir:
          if is_valid_directory(args.path):
              if args.extensions: 
                zip_files = dir_contents()
                archive_path = mkdtemp()
                for file in zip_files:
                  copy(file, archive_path)
              make_archive(archive_name, archive_format, archive_path)
              zipping()
              # removes the temorary directory
              if args.extensions: rmtree(archive_path, ignore_errors=True)
      else:
          if process_file(None, args.path):
              with ZipFile(f'{archive_name}.{archive_format}', 'w') as zipf:
                zipf.write(archive_path, arcname=obj_name)
              zipping()
  elif args.zip and not args.encrypt: 
      print(f"[{E}] Zipping can only be performed while encrypting")    
  # -- nOte: adding option to remove the initial directory and files

# initial logic and condition sets
def main () :
  global its_out_dir, out_dir_path
  its_out_dir = False
  if not any(vars(args).values()): parser.print_help()
  elif args.encrypt and args.decrypt:
      print(f"[{E}] Please use only one cryptographic process")
  elif args.encrypt or args.decrypt:
      if args.upload and args.decrypt: 
        print(f"[{E}] Non Encrypted files will not be stored online for security reasons.\n") 
      try:
          if args.output :
            its_out_dir, out_dir_path = is_valid_directory(args.output, True)
          if args.zip: process_zip()
          elif args.dir:
              if is_valid_directory(args.path):
                fernet = input_master_key()
                dir_contents(fernet)
          else: 
            process_file(None, args.path)
          upload_online()
      except KeyboardInterrupt: print(f"\n\n[»] Bye")
  else: print(f"[{E}] Please choose a cryptographic process")


# Available Options and Flags
print()
parser = ArgumentParser(description=f'{I}Encrypts and Decrypts Data{r}', epilog='Made with <3 by @syr1ne && @1byteBoy', usage="%(prog)s [OPTIONS...] [PATH...]")

parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the file")
parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file")
parser.add_argument("-p", "--print", action="store_true", help="Print decrypted data directly")
parser.add_argument("-D", "--dir", action="store_true", help="Work with a whole directory of files")
parser.add_argument("-x", "--extensions", type=str, metavar='', help="Specify specific file extensions")
parser.add_argument("-u", "--upload", action="store_true", help="Upload file|s on discord")
parser.add_argument("-o", "--output", type=str, metavar='', help="Output directory path")
parser.add_argument("-r", "--remove", action="store_true", help="Removes original file|s after encrytion or decryption")
parser.add_argument("-z", "--zip", action="store_true", help="File|s get Zipped and then encrypted")
parser.add_argument('path', type=str, nargs='?', help=SUPPRESS)
args = parser.parse_args()

if __name__ == '__main__': main()

