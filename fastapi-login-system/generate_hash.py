from auth.password_utils import get_password_hash

hashed = get_password_hash("securepassword17")  # Replace with your password
print(hashed)
