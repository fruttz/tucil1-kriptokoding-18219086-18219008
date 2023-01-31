import vigenere as vc

BYTE_MAX = 256

def extvigenereEnc(src: str, key: str, output: str) -> bool :
    try:
        f = open(src, 'rb')
        fileData = bytearray(f.read())
        key = vc.getKey(fileData, vc.clean_text(key))

        for idx, plainText in enumerate(fileData):
            fileData[idx] = (plainText + ord(key[idx])) % BYTE_MAX

        f.close()
        f = open(output, 'wb')
        f.write(fileData)
        f.close()

        return True
    except Exception as e:
        return False

def extvigenereDec(src: str, key: str, output: str) -> str :
    try:
        f = open(src, 'rb')
        fileData = bytearray(f.read())
        key = vc.getKey(fileData, vc.clean_text(key))

        for idx, cipherText in enumerate(fileData):
            fileData[idx] = (cipherText - ord(key[idx])) % BYTE_MAX

        f.close()
        f = open(output, 'wb')
        f.write(fileData)
        f.close()

        return True
    except:
        return False