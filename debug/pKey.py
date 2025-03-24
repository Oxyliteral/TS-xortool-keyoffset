def xor_bytes(a, b):
    """XOR two byte arrays."""
    return bytes(x ^ y for x, y in zip(a, b))

def find_xor_key(encrypted_file_path, decrypted_file_path, key_length=256):
    # Read the encrypted and decrypted files
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    with open(decrypted_file_path, 'rb') as decrypted_file:
        decrypted_data = decrypted_file.read()
    
    # Ensure both files are of the same length
    if len(encrypted_data) != len(decrypted_data):
        raise ValueError("The encrypted and decrypted files must be of the same length.")
    
    # XOR the encrypted and decrypted data to find the key
    key = xor_bytes(encrypted_data[:key_length], decrypted_data[:key_length])
    
    return key

# Example usage
encrypted_file_path = 'newera_system.lub'
decrypted_file_path = '000.out'

key = find_xor_key(encrypted_file_path, decrypted_file_path, key_length=256)

# Print the key
print("XOR Key:", key)
