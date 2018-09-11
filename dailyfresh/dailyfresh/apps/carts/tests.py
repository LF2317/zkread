from django.test import TestCase
import pickle
import base64
# Create your tests here.

if __name__ == "__main__":
    # cart_dict = {
    #     1: {
    #         'count': 2,
    #         'selected': True
    #     },
    #     5: {
    #         'count': 3,
    #         'selected': False
    #     }
    # }
    #
    # res = pickle.dumps(cart_dict) # bytes
    # print(res)
    # res = base64.b64encode(pickle.dumps(cart_dict)) # bytes
    # print(res)
    # res = base64.b64encode(pickle.dumps(cart_dict)).decode()
    # print(res)

    # cart_data = b'\x80\x03}q\x00(K\x01}q\x01(X\x08\x00\x00\x00selectedq\x02\x88X\x05\x00\x00\x00countq\x03K\x02uK\x05}q\x04(h\x02\x89h\x03K\x03uu.'
    # res = pickle.loads(cart_data)

    cart_data = 'gAN9cQAoSwF9cQEoWAUAAABjb3VudHECSwJYCAAAAHNlbGVjdGVkcQOIdUsFfXEEKGgCSwNoA4l1dS4='

    res = base64.b64decode(cart_data)
    print(res)
    res = pickle.loads(base64.b64decode(cart_data))
    print(res)

