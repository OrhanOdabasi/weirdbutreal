import string
import random

def code_generator(size=7, chars=string.ascii_lowercase + string.digits):
    # creating a random unique urlcode for a story_title
    return ''.join(random.choice(chars) for _ in range(size))


def create_urlcode(instance):
    # creates a unique url for the story
    urlcode = code_generator()
    klass = instance.__class__
    urlcode_exists = klass.objects.filter(urlcode=urlcode)
    if urlcode_exists:
        return create_urlcode()
    return urlcode
