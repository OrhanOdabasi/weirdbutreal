import string
import random

def generate_secure_key(size=69, chars=string.ascii_lowercase + string.digits):
    # generating a 40 chars length key to reset password or change e-mail address
    skey = ""
    for _ in range(size):
        skey = skey + str(random.choice(chars))
    return skey

def email_reset_key(instance):
    # creates a unique secure code if user wants to reset password or change mail addr.
    key = generate_secure_key()
    klass = instance.__class__
    key_exists = klass.objects.filter(secure_key=key)
    if key:
        return email_reset_key()
    return key
