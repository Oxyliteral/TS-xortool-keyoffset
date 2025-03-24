def xor_bytes(a, b):
    """XOR two byte arrays."""
    return bytes(x ^ y for x, y in zip(a, b))

def decrypt_file(encrypted_file_path, key, decrypted_file_path):
    # Read the encrypted file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    # Ensure the key is repeated to match the length of the encrypted data
    key_length = len(key)
    repeated_key = (key * (len(encrypted_data) // key_length)) + key[:len(encrypted_data) % key_length]
    
    # XOR the encrypted data with the repeated key to decrypt it
    decrypted_data = xor_bytes(encrypted_data, repeated_key)
    
    # Write the decrypted data to the new file
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

# Example usage
encrypted_file_path = 'newera_script_common.lub'
key = b'\x06\xd3u\t>\xc6\xa5g9\xbd\xa2L\x07\x04h@\x81\x17\xdb\x19\x1d\xba8\xc1\xea\x1f\xb9!\xae\xccRi\x1b\x98|\x83J\xe0yd.\x03\x86a\x15nb\xd4\x84\xdf\x99t\xe8\xa7\x92=\xd91I\xed\r\xb3\x11\x0b\x0eo\xe4F\xf6\xe1\x91\xa8\x9aO}V\x05[6k\xf4\xc9\x82Y]\xb4\\^4\xa9\x9eH\xbe\xd5\x7fef\xfcUTj\x85l\xe3\x87\xe7p\xd03s\xc8\xdevw\xca\xb7z\xf9\xbfA\xe5\xc0\x80~\xe6{\x8fx\xa6\xef\x88C\xd7\x8d\xac\xc4\xc5\x95\xaa%*\x94\x93\xf8\x96\x1c\x00Z\xafW)P\xcd\xfb5\xd6\xf1\xb0\xa40\xc2\xdaX_\x1e#\x0c\xdcE\x1a\x8b\xb1\xf5S\xa1\xb5\xb6\n\x13 <,\xbc:\xd1\x9d2\xa0\x10\xc3r/\x02&\xec-\xf0\xcb\x90\xb2\xce\xcfq\xe2\x14G\x12\x18\xb8\x8c\x0f"Dm\x9cK\xd87+(`B\x9fNM\'\x89\x16\xab\xeb\xf2\x8a\xd2;\x08\xbb\xdd\xf3Q\xa3\xee\xf7c\xad\xfa\xe9\xff\xfd\xfe\x8e\x9b\x97\x01$?\xc7'  # Replace with your 256-byte key
decrypted_file_path = 'decrypted_file.bin'

decrypt_file(encrypted_file_path, key, decrypted_file_path)

print("File decrypted successfully.")
