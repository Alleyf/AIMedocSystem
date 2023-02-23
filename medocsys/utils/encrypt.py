from django.conf import settings
import hashlib


def md5(data_str):
    salt = settings.SECRET_KEY.encode('utf-8')
    obj = hashlib.md5(salt)
    obj.update(data_str.encode('utf-8'))
    return obj.hexdigest()
