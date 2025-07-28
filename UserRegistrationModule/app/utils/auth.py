from passlib.context import CryptContext  # #This initializes a CryptContext with bcrypt as the hashing algorithm.
from datetime import datetime, timedelta
from passlib.context import CryptContext  #This initializes a CryptContext with bcrypt as the hashing algorithm.
import jwt
from fastapi import HTTPException, status

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # "deprecated='auto'" allows automatic migration if you later change the hashing scheme.

# JWT Configuration
SECRET_KEY = "YOUR_SECRET_KEY"  # change this to a strong random value
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


                                                 

def hash_password(password: str): # Takes a plain password and returns a bcrypt hashed version.
    return pwd_context.hash(password) #Use this when storing passwords in a database.

def verify_password(plain_password, hashed_password): # Checks whether a plain password matches the stored hashed password.
    return pwd_context.verify(plain_password, hashed_password) # Returns True if they match, False otherwise.




def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")