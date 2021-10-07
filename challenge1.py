import base64
import os
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def main():
    name = "stefano"
    alphabet = "ABCDEFGHILMNOPQRSTUVZXYW"
    base = "stefano"
    salt = b'\xd4\x1f\xceg\xe9\xafW\xad\xb7+Y\xc3\xd9t\xe1\xc6'

    cyphertext = b'gAAAAABgoqMJ17XcgGFW347sJ9q1cXjzd1Cl74v42sZVhmbGGer1_l1NFfZSM-FRCVpCaZ9' \
                 b'-JYjy5Ut0Ycy4E1GHyUxCSEgROSw2HFsJjX43qZgk2AyMG1Vzfxx8V212x3WWwszfCV1rR2KWHvUyorQB' \
                 b'-0asgI3NLcrZiLVjJSQHg2qOqqKNUyv-TQsR-EIo-GgI4FOnA1kyFymTQv2Vcjxq4zAtUO3' \
                 b'-nssuxuVC_n27xefX4eRd_GrnonCvRL_0b_3KYt-pQp4iT_hcbvuEnuM--Ue-F_BjYg== '

    passwd = b''

    for n in range(10):
        number = n
        for l in range(len(alphabet)):
            letter = alphabet[l]
            for k in range(9):
                basenum = base[:k] + str(number) + base[k:]
                for z in range(9):
                    basenumlet = basenum[:z] + letter + basenum[z:]
                    passwd = bytes(basenumlet, 'utf-8')
                    #print(passwd)
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    key = base64.urlsafe_b64encode(kdf.derive(passwd))
                    f = Fernet(key)
                    try:
                        cleartext = f.decrypt(cyphertext)
                        print(cleartext)
                        print(passwd)
                        return 0
                    except Exception:
                        pass


if __name__ == '__main__':
    main()

    ''''
#Codice di cifratura    
    passwd = b"……………"
    cleartext = b"…………………………"
    salt = os.urandom(16)
    print('salt = ', salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwd))
    f = Fernet(key)
    cyphertext = f.encrypt(cleartext)
    print(‘cyphertext = ', cyphertext)
    print(f.decrypt(cyphertext))
'''