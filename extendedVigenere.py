import vigenere

BYTE_MAX = 256

def extVigenereEnkripsi(src: str, kunci: str, output: str) -> bool :
    try:
        f = open(src, 'rb')
        fileContent = bytearray(f.read())
        kunci = vigenere.getkunci(fileContent, vigenere.clean_text(kunci))

        for idx, plainText in enumerate(fileContent):
            fileContent[idx] = (plainText + ord(kunci[idx])) % BYTE_MAX

        f.close()
        f = open(output, 'wb')
        f.write(fileContent)
        f.close()

        return True
    except Exception as e:
        return False

def extVigenereDekripsi(src: str, kunci: str, output: str) -> str :
    try:
        f = open(src, 'rb')
        fileContent = bytearray(f.read())
        kunci = vigenere.getkunci(fileContent, vigenere.clean_text(kunci))

        for idx, cipherText in enumerate(fileContent):
            fileContent[idx] = (cipherText - ord(kunci[idx])) % BYTE_MAX

        f.close()
        f = open(output, 'wb')
        f.write(fileContent)
        f.close()

        return True
    except:
        return False