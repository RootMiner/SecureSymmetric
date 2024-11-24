#!/usr/bin/env python3 

"""
random password generator
"""

import secrets
import string
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-l", "--length", help="length of pass (default: 20)")
args = parser.parse_args()


parser = ArgumentParser()
parser.add_argument("-l", "--length")
args = parser.parse_args()

if not args.length:
    args.length = 20

alphabet = string.ascii_letters + string.digits

password = ''.join(secrets.choice(alphabet) for i in range(int(args.length)))


print(password)



