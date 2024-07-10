## What is SecureSymmetric 🯄

In general it's a cool name for the project but actually it's just a simple program that encrypts file using 
*fernet's symmetric secret key based authenticated cryptography.*

Learn more about **Fernet** at https://cryptography.io/en/latest/fernet/

## DISCLAIMER

This program is intended for educational and legitimate purposes only. It provides encryption and decryption functionalities using Fernet cryptography, designed to protect data privacy and security. However, it is crucial to note that misuse of this software for malicious activities such as ransomware attacks is strictly prohibited and unlawful.

The developers of this program, do not endorse, promote, or encourage any illegal or unethical use of this software. Users are solely responsible for their actions and must comply with applicable laws and regulations in their jurisdictions.

By using this software, you agree to use it responsibly and ethically. The developer shall not be held liable for any misuse or unlawful activities conducted using this program.

## NOTE

As said earlier, this is just a simple code that we wrote to learn about how symmetric encrytion works and the usage of fernet. This is totally a personal project and we are not a good developer at all, so please test the code on test files before using on your important files. Feel free to make necessary changes from your side. 

## Usage

```
$ python3 secure.py
 
usage: secure.py [OPTIONS...] [PATH...]

Encrypts and Decrypts Data

options:
  -h, --help          show this help message and exit
  -e, --encrypt       Encrypt the file
  -d, --decrypt       Decrypt the file
  -p, --print         Print decrypted data directly
  -D, --dir           Work with a whole directory of files
  -x , --extensions   Specify specific file extensions
  -u, --upload        Upload file|s on discord
  -o , --output       Output directory path
  -r, --remove        Removes original file|s after encrytion or decryption
  -z, --zip           File|s get Zipped and then encrypted

Made with ❤ by @syr1ne && @1byteBoy
```

**While main options are self-explainatory but to understand more about what each flags/options actually does visit [Usage WiKi](https://github.com/RootMiner/SecureSymmetric/wiki#usage)**

## Problems && ToDo's

- Two archiving method is used namely `shutil` and `zipfile` for directory and single file respectively, but we are trying to impliment one if possible

- Certain functionality of windows is missing

- Update the WiKi Page

- A choice if user wants to delete the original files and directory while archiving, archive is currently saved in the directory where script is executed

- if file skipped and upload option is used, do user want to upload the existing file ?

- and option for decrypting the encrypted archive file and unzipping it 

-----

Made with <3 by [syr1ne](https://github.com/syr1ne) and [8bitBoy](https://github.com/1byteBoy)
