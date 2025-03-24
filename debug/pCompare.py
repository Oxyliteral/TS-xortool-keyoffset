def are_bytes_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        byte_number = 0
        byte1 = f1.read(1)
        byte2 = f2.read(1)

        while byte1 or byte2:
            if byte1 != byte2:
                if not byte1:
                    print(f"File 1 ended at byte {byte_number + 1}, but File 2 has additional data:")
                    print(f"File 2: {byte2[0]} (0x{byte2[0]:02x})")
                elif not byte2:
                    print(f"File 2 ended at byte {byte_number + 1}, but File 1 has additional data:")
                    print(f"File 1: {byte1[0]} (0x{byte1[0]:02x})")
                else:
                    print(f"Files differ at byte {byte_number + 1}:")
                    print(f"File 1: {byte1[0]} (0x{byte1[0]:02x})")
                    print(f"File 2: {byte2[0]} (0x{byte2[0]:02x})")
                return False

            byte1 = f1.read(1)
            byte2 = f2.read(1)
            byte_number += 1

    return True
def main():
    file1 = 'xortool-keyoffset_decrypted_file_offset_209.out'
    file2 = '000.out'
    if are_bytes_equal(file1, file2):
        print(f"Files {file1} and {file2} are equal.")
    else:
        print(f"Files {file1} and {file2} are different.")

if __name__ == "__main__":
    main()
