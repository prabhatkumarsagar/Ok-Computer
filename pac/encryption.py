import getpass
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


key = None
salt = b'$2b$12$3hbla5Xs2Ekx9SGVYfWQuO'
hashed_pswd = bcrypt.hashpw(pswd, salt)
kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
key = base64.urlsafe_b64encode(kdf.derive(hashed_pswd))
