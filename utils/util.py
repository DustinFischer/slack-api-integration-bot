import random
import string


def block_id(length=3):
    return ''.join(random.choice(string.ascii_uppercase) for i in range(length))
