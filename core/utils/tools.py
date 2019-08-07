import hashlib
import os
import random
import string
import sys
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from core.color import color


def GetStartupPath(fname):
    return os.path.dirname(os.path.realpath(fname))


def GetRandomString(stringlength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringlength))


def FileExists(filepath):
    if os.path.exists(filepath):
        return True
    else:
        return False


def GetHashFromPassword(passw):
    return pbkdf2_sha256.encrypt(passw, rounds=200000, salt_size=16)


def VerifyPassword(passw, hash_):
    return pbkdf2_sha256.verify(passw, hash_)


def CreateFolderIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False


def GetNewLogFileName():
    return datetime.now().strftime("%d_%m_%Y-%H_%M_%S.log")


def GetHashFromString(passw):
    return pbkdf2_sha256.encrypt(passw, rounds=200000, salt_size=16)


def GetUniqueHashFromString(string_):
    return hashlib.md5(string_.encode('utf-8')).hexdigest()


def Confirm(prompt):
    sys.stdout.write(color.ReturnQuestion('%s (Y/n): ' % prompt))
    choose = raw_input('')
    if choose == 'Y' or choose == 'y':
        return True
    else:
        return False


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def mkdir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
    except:
        return False

