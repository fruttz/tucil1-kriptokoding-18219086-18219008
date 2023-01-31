import vigenereCypher as vig

FILESIZE_MAX = 256

def extended_vigenere_encrypt(path: str, key: str, output: str) -> bool:
    try:
        f = open(path, 'rb')
        data = bytearray(f.read())
        key = vig.generate_key(data, vig.process_text(key))
        for idx, plaintxt in enumerate(data):
            data[idx] = (plaintxt + ord(key[idx])) % FILESIZE_MAX
        f.close()
        f = open(output, 'wb')
        f.write(data)
        f.close()
        return True
    except Exception as e:
        return False

def extended_vigenere_decrypt(path: str, key: str, output: str) -> bool:
    try:
        f = open(path, 'rb')
        data = bytearray(f.read())
        key = vig.generate_key(data, vig.process_text(key))
        for idx, ciphertxt in enumerate(data):
            data[idx] = (ciphertxt - ord(key[idx])) % FILESIZE_MAX
        f.close()
        f.open(output, 'wb')
        f.write(data)
        f.close()
        return True
    except Exception as e:
        return False

