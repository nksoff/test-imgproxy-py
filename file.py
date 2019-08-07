import base64
import hashlib
import hmac
import textwrap


def fromhex(ustring):
    if str is bytes:
        return bytearray.fromhex(ustring)
    return bytes.fromhex(ustring)


def bytes_to_string(maybe_string):
    try:
        return maybe_string.decode()
    except AttributeError:
        return maybe_string


key = fromhex(u"943b421c9eb07c830af81030552c86009268de4e532ba2ee2eab8247c6da0881")
salt = fromhex(u"520f986b998545b4785e0defbc4f3c1203f22de2374a3d53cb7a7fe9fea309c5")

url = b"http://img.example.com/pretty/image.jpg"

encoded_url = base64.urlsafe_b64encode(url).rstrip(b"=").decode()
# You can trim padding spaces to get good-looking url
encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))

path = "/{resize}/{width}/{height}/{gravity}/{enlarge}/{encoded_url}.{extension}".format(
    encoded_url=encoded_url,
    resize="fill",
    width=300,
    height=300,
    gravity="no",
    enlarge=1,
    extension="png",
).encode()
digest = hmac.new(key, msg=salt+path, digestmod=hashlib.sha256).digest()

protection = base64.urlsafe_b64encode(digest).rstrip(b"=")

url = '/%s%s' % (
    protection.decode(),
    path.decode(),
)

print(bytes_to_string(url))

