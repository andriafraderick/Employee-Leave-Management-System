from passlib.context import CryptContext
from passlib.exc import UnknownHashError

# Set up the password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify a plain password against the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # If the hashed_password is not a valid hash (e.g., plain text), return False
        return False

# Function to hash a plain password before storing
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
