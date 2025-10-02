import hashlib

def compute_file_digest(filepath, algorithm="sha256"):
    hash_func = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()
