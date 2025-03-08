import secrets

# Generate a secure random API key
api_key = secrets.token_hex(32)  # 64-character hex string (high security)
print("Your secure API key:", api_key)
