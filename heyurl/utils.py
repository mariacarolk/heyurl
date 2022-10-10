from django.conf import settings
from random import choice
from string import ascii_letters, digits
import requests

def create_random_code(avaiable_chars):
    """
    Creates a random string with the predetermined size
    """
    size = 5
    return "".join([choice(avaiable_chars) for _ in range(size)])

def create_short_url(Url):
    avaiable_chars = ascii_letters + digits
    random_code = create_random_code(avaiable_chars)

    #gets the model class
    url = Url.__class__

    if url.objects.filter(short_url=random_code).exists():
        # Run the function again
        return create_short_url(Url)

    return random_code


def valid_url(url):
    try:
        response = requests.head(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return False
