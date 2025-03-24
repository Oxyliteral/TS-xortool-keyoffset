import sys

def load_file(filename):
    if filename == "-":
        filename = sys.stdin.fileno()
    with open(filename, "rb") as fd:
        return fd.read()

def decode_from_hex(text):
    text = text.decode(encoding='ascii', errors='ignore')
    only_hex_digits = "".join(c for c in text if c in string.hexdigits)
    return bytes.fromhex(only_hex_digits)

def dexor(text, key):
    mod = len(key)
    return bytes(key[index % mod] ^ char for index, char in enumerate(text))
    
def decrypt_file_with_key_offset(encrypted_file_path, key, decrypted_base_path, key_base_path, target_plaintext):
    ciphertext = load_file(encrypted_file_path)
    if len(sys.argv) > 2 and sys.argv[2] == '-h':
        ciphertext = decode_from_hex(ciphertext)
    # List to store successful offsets and keys
    successful_offsets = []

    print(f'key: {key}')
    print(f'plaintext: {target_plaintext}')
    
    key_length = len(key)
    encrypted_length = len(ciphertext)
    
    # Iterate through all possible starting positions of the key
    for start_offset in range(key_length):

        #repeated_key = (key[start_offset:] + key[:start_offset]) * (encrypted_length // key_length) + key[start_offset:][:encrypted_length % key_length]
        repeated_key = (key[start_offset:] + key[:start_offset])
        
        dexored = dexor(ciphertext, repeated_key)
        # Check if the decrypted data contains the target plaintext
        if target_plaintext.encode() in dexored:
            
            # Write the decrypted data to a new file
            decrypted_file_path = f"xortool-keyoffset_{decrypted_base_path}_offset_{start_offset}.out"
            f = open(decrypted_file_path, "wb")
            f.write(dexored)
            f.close()
            
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
    
    if not successful_offsets:
        print("Failed to decrypt the file with the given key and target plaintext.")
    else:
        print(f"Decryption successful for offsets: {successful_offsets}")


key = b'\x06\xd3u\t>\xc6\xa5g9\xbd\xa2L\x07\x04h@\x81\x17\xdb\x19\x1d\xba8\xc1\xea\x1f\xb9!\xae\xccRi\x1b\x98|\x83J\xe0yd.\x03\x86a\x15nb\xd4\x84\xdf\x99t\xe8\xa7\x92=\xd91I\xed\r\xb3\x11\x0b\x0eo\xe4F\xf6\xe1\x91\xa8\x9aO}V\x05[6k\xf4\xc9\x82Y]\xb4\\^4\xa9\x9eH\xbe\xd5\x7fef\xfcUTj\x85l\xe3\x87\xe7p\xd03s\xc8\xdevw\xca\xb7z\xf9\xbfA\xe5\xc0\x80~\xe6{\x8fx\xa6\xef\x88C\xd7\x8d\xac\xc4\xc5\x95\xaa%*\x94\x93\xf8\x96\x1c\x00Z\xafW)P\xcd\xfb5\xd6\xf1\xb0\xa40\xc2\xdaX_\x1e#\x0c\xdcE\x1a\x8b\xb1\xf5S\xa1\xb5\xb6\n\x13 <,\xbc:\xd1\x9d2\xa0\x10\xc3r/\x02&\xec-\xf0\xcb\x90\xb2\xce\xcfq\xe2\x14G\x12\x18\xb8\x8c\x0f"Dm\x9cK\xd87+(`B\x9fNM\'\x89\x16\xab\xeb\xf2\x8a\xd2;\x08\xbb\xdd\xf3Q\xa3\xee\xf7c\xad\xfa\xe9\xff\xfd\xfe\x8e\x9b\x97\x01$?\xc7'

decrypted_base_path = 'decrypted_file'
encrypted_file_path = ''
key_base_path = 'xortool-keyoffset_output_key'
target_plaintext_path = "xortool-keyoffset_plaintext.txt"

try:
    with open(target_plaintext_path, 'r', encoding='utf-8') as plaintext_file:
        target_plaintext = plaintext_file.read().strip()
except FileNotFoundError:
    print(f"Error: File {target_plaintext_path} not found.")
    input()
if len(sys.argv) > 1:
   encrypted_file_path = sys.argv[1]

decrypt_file_with_key_offset(encrypted_file_path, key, decrypted_base_path, key_base_path, target_plaintext)
print("Enter any key to close...")
input()
