from base64 import b64encode
from codecs import decode


# function takes the absolute path of the image and returns the converted base64 string for json transfer
def toByteString(path):

    try:

        with open(path, 'rb') as image:
            return b64encode(image.read()).decode("utf-8")

    except Exception as message:

        print("[ERROR]", message)
        return message
