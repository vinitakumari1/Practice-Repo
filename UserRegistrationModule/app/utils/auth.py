from passlib.context import CryptContext  # #This initializes a CryptContext with bcrypt as the hashing algorithm.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # "deprecated='auto'" allows automatic migration if you later change the hashing scheme.
                                                 

def hash_password(password: str): # Takes a plain password and returns a bcrypt hashed version.
    return pwd_context.hash(password) #Use this when storing passwords in a database.

def verify_password(plain_password, hashed_password): # Checks whether a plain password matches the stored hashed password.
    return pwd_context.verify(plain_password, hashed_password) # Returns True if they match, False otherwise.




