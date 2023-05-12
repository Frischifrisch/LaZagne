#!/usr/bin/python

# A simple implementation of pbkdf2 using stock python modules. See RFC2898
# for details. Basically, it derives a key from a password and salt.

# (c) 2004 Matt Johnston <matt @ ucc asn au>
# This code may be freely used and modified for any purpose.

import hmac

from hashlib import sha1
from struct import pack

BLOCKLEN = 20


# this is what you want to call.
def pbkdf2(password, salt, itercount, keylen, hashfn=sha1):
    # l - number of output blocks to produce
    l = keylen / BLOCKLEN
    if keylen % BLOCKLEN != 0:
        l += 1

    h = hmac.new(password, None, hashfn)

    T = "".join(pbkdf2_F(h, salt, itercount, i) for i in range(1, l + 1))
    return T[: -(BLOCKLEN - keylen % BLOCKLEN)]


def xorstr(a, b):
    if len(a) != len(b):
        raise "xorstr(): lengths differ"

    return ''.join(chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a)))


def prf(h, data):
    hm = h.copy()
    hm.update(data)
    return hm.digest()


# Helper as per the spec. h is a hmac which has been created seeded with the
# password, it will be copy()ed and not modified.
def pbkdf2_F(h, salt, itercount, blocknum):
    U = prf(h, salt + pack('>i', blocknum))
    T = U

    for _ in range(2, itercount + 1):
        U = prf(h, U)
        T = xorstr(T, U)

    return T
