import hashlib
import urllib
import zlib
import pickle
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail

from members.models import Member

my_secret = "iojp}e;pp.P{dapoO{kjYY3RGT&*()urdt243522cvjbhknj0*&^65rdexrsfxg"
site="http://127.0.0.1:8000"
def encode_data(data):
    """
    Turn `data` into a hash and an encoded string, suitable for use with `decode_data`.
    Adapted from http://stackoverflow.com/questions/1360101/how-to-generate-temporary-urls-in-django
    """
    text = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    return m, text

def decode_data(hash, enc):
    """The inverse of `encode_data`."""
    # Django requests unquotes but we need "+"
    # So we quote_plus() the string again,
    # Then we unquote() hence leaving the "+"
    text = urllib.unquote(urllib.quote_plus(enc)) # Django requests unquotes but we need "+"
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    if m != hash:
        return Exception("Bad hash!")
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data

def send_invitation(email):
    expire = datetime.utcnow() + timedelta(minutes=60)
    timestamp = (expire - datetime(1970, 1, 1)).total_seconds()
    hash, info = encode_data({"email": email,
                              "secret": "bosaf34530d",
                              "expire": timestamp
                             })
    message = """
    Your registration link
    %s

    """ % (site + "/api/auth/registration/?h=" + hash + "&d=" + info)
    print send_mail('Subject', message, 'no-reply@gosacco.com', (email,))

def create_registration_link(id):
    exists = Member.objects.filter(user = id).exists()
    if not exists:
        hash, info = encode_data({"user": int(id),
                              "exists": exists})
        return (site + "/api/members/?h=" + hash + "&d=" + info)
    return None

def register_user(username, password, email, first_name, last_name):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return user.id

def jwt_response_payload_handler(token, user=None, request=None):
    """
    Response data after login or refresh
    """
    return {
        'token': token,
        'member': user.member.id
    }
