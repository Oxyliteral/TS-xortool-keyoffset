# archived, does not work!

import sys
import string

#def xor_bytes(a, b):
#    """XOR two byte arrays."""
#    return bytes(x ^ y for x, y in zip(a, b))

def decode_from_hex(text):
    text = text.decode(encoding='ascii', errors='ignore')
    only_hex_digits = "".join(c for c in text if c in string.hexdigits)
    return bytes.fromhex(only_hex_digits)

def dexor(text, key):
    mod = len(key)
    return bytes(key[index % mod] ^ char for index, char in enumerate(text))

def check_lua_file_integrity(data):
    """Check the integrity of the Lua bytecode file."""
    # Lua 5.1 header format
    if len(data) < 12:
        print('headerlength')
        return False
    
    # Check the header
    if not data.startswith(b'\x1B\x4C\x75\x61'):
        print('header')
        return False
    
    # Check the version and format bytes
    version = data[4]
    format = data[5]
    if version not in [0x51, 0x52, 0x53, 0x54]:  # Allow for Lua 5.1, 5.2, 5.3, 5.4
        print('luaversion')
        return False
    
    # Check the endianness and size size
    endianness = data[6]
    size_size = data[7]
    if endianness not in [0, 1] or size_size not in [1, 2, 4, 8]:
        print('endianness/sizesize')
        return False
    
    # Check the instruction size and number size
    instruction_size = data[8]
    number_size = data[9]
    if instruction_size not in [4, 8] or number_size not in [4, 8]:
        print('instruction/numbersize')
        return False
    
    # Check the integral flag
    integral_flag = data[10]
    if integral_flag not in [0, 1]:
        print('warning: integral flag')
    
    # Check the padding byte
    padding = data[11]
    if padding not in [0, 1]:
        print('padding')
        return False
    
    return True

def decrypt_file_with_key_offset(encrypted_file_path, key, decrypted_base_path, key_base_path, target_plaintext):
    # Read the encrypted file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    key_length = len(key)
    encrypted_length = len(encrypted_data)
    
    # List to store successful offsets and keys
    successful_offsets = []

    print(f'key: {key}')
    print(f'plaintext: {target_plaintext}')
    
    # Iterate through all possible starting positions of the key
    for start_offset in range(key_length):
        # Create the repeated key with the current offset
        #repeated_key = (key[start_offset:] + key[:start_offset]) * (encrypted_length // key_length) + key[start_offset:][:encrypted_length % key_length]
        #repeated_key = (key[start_offset:] + key[:start_offset]) * (encrypted_length // key_length)
        #if len(repeated_key) < encrypted_length:
        #    repeated_key += key[:encrypted_length % key_length]
        
        # XOR the encrypted data with the repeated key to decrypt it
        #decrypted_data = xor_bytes(encrypted_data, repeated_key)
        
        decrypted_data = dexor(decode_from_hex(encrypted_data), key)
        # Check if the decrypted data contains the target plaintext
        if target_plaintext.encode() in decrypted_data:
            
            # Write the decrypted data to a new file
            decrypted_file_path = f"{decrypted_base_path}_offset_{start_offset}.lub"
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            
            # Store the successful offset and key
            successful_offsets.append((start_offset, key[start_offset:] + key[:start_offset]))

             # Write the key to a new file as a byte string
            key_file_path = f"{key_base_path}_offset_{start_offset}.txt"
            with open(key_file_path, 'w') as key_file:
                #key_file.write(f"{successful_offsets}")
                key_file.write(f"Offset: {start_offset}, Key: {key[start_offset:] + key[:start_offset]}\n")
                
            print(f"File decrypted successfully with key offset {start_offset}.")
            print(f"Decrypted file saved to: {decrypted_file_path}")
            print(f"Key saved to: {key_file_path}")

            # Debugging: Check the sizes
            print(f"Encrypted file size: {encrypted_length} bytes")
            print(f"Decrypted file size: {len(decrypted_data)} bytes")

            # Debugging: Check the first 200 bytes of the decrypted data
            print(f"First 200 bytes of decrypted data: {decrypted_data[:200]}")
            # Debugging: Check if the decrypted data looks like a valid Lua file
            if check_lua_file_integrity(decrypted_data):
                print("Decrypted data looks like a valid Lua file.")
            else:
                print("Decrypted data does not look like a valid Lua file.")
    
    if not successful_offsets:
        print("Failed to decrypt the file with the given key and target plaintext.")
    else:
        print(f"Decryption successful for offsets: {successful_offsets}")

# Example usage
encrypted_file_path = 'BattleUI.lub'
key = b'\x06\xd3u\t>\xc6\xa5g9\xbd\xa2L\x07\x04h@\x81\x17\xdb\x19\x1d\xba8\xc1\xea\x1f\xb9!\xae\xccRi\x1b\x98|\x83J\xe0yd.\x03\x86a\x15nb\xd4\x84\xdf\x99t\xe8\xa7\x92=\xd91I\xed\r\xb3\x11\x0b\x0eo\xe4F\xf6\xe1\x91\xa8\x9aO}V\x05[6k\xf4\xc9\x82Y]\xb4\\^4\xa9\x9eH\xbe\xd5\x7fef\xfcUTj\x85l\xe3\x87\xe7p\xd03s\xc8\xdevw\xca\xb7z\xf9\xbfA\xe5\xc0\x80~\xe6{\x8fx\xa6\xef\x88C\xd7\x8d\xac\xc4\xc5\x95\xaa%*\x94\x93\xf8\x96\x1c\x00Z\xafW)P\xcd\xfb5\xd6\xf1\xb0\xa40\xc2\xdaX_\x1e#\x0c\xdcE\x1a\x8b\xb1\xf5S\xa1\xb5\xb6\n\x13 <,\xbc:\xd1\x9d2\xa0\x10\xc3r/\x02&\xec-\xf0\xcb\x90\xb2\xce\xcfq\xe2\x14G\x12\x18\xb8\x8c\x0f"Dm\x9cK\xd87+(`B\x9fNM\'\x89\x16\xab\xeb\xf2\x8a\xd2;\x08\xbb\xdd\xf3Q\xa3\xee\xf7c\xad\xfa\xe9\xff\xfd\xfe\x8e\x9b\x97\x01$?\xc7'
decrypted_base_path = 'decrypted_file'
key_base_path = 'key_file'
target_plaintext_path = "plaintext.txt"

try:
    with open(target_plaintext_path, 'r', encoding='utf-8') as plaintext_file:
        target_plaintext = plaintext_file.read().strip()
except FileNotFoundError:
    print(f"Error: File {plaintext_file_path} not found.")
if len(sys.argv) > 1:
   encrypted_file_path = sys.argv[1] 

decrypt_file_with_key_offset(encrypted_file_path, key, decrypted_base_path, key_base_path, target_plaintext)
print("Enter any key to continue...")
input()
