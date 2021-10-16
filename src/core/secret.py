from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


class Secret:
    def __init__(self, key, algo, expires_in):
        self.key = key
        self.algorithm = algo
        self.expires_in = expires_in
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain, hashed):
        return self.pwd_context.verify(plain, hashed)

    def hash(self, plain):
        return self.pwd_context.hash(plain)

    def token(self, data):
        to_encode = data.copy()
        expires_at = datetime.utcnow() + timedelta(minutes=self.expires_in)
        to_encode.update({"exp": expires_at})
        #
        encoded_jwt = jwt.encode(to_encode, self.key, algorithm=self.algorithm)
        return encoded_jwt

    def payload(self, token):
        try:
            payload = jwt.decode(token, self.key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
