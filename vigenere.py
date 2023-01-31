import re

#vignere cipher std: 26 alfabet
alf = [chr(97 + i) for i in range(26)]

def clean_text(pt: str) -> str:
    result = pt

    #merge text
    result.strip()
    result = result.replace(" ", "")
    result = result.lower()

    #remove angka
    result = ''.join([i for i in result if not i.isdigit()])

    #remove tanda
    result = re.sub(r'[^\w\s]', '', result)

    return result

def getKey(plain_text: str, key: str) -> str:
    if(len(key) >= len(plain_text)):
        return key[:len(key)]

    full_key: str = key
    for i in range(len(plain_text) - len(key)):
        full_key += key[i % len(key)]

    return full_key

def vigenereEnc(plain_text: str, key: str) -> str:
    cipher_text = ""

    for i in range(len(plain_text)):
        curr_plain_text_num = ord(plain_text[i]) - ord('a')
        curr_key_text_num = ord(key[i]) - ord('a')
        curr_cipher_text_num = (curr_plain_text_num + curr_key_text_num) % 26

        cipher_text += alf[curr_cipher_text_num]
    return cipher_text

def vigenereDec(cipher_text: str, key: str) -> str:
    plain_text = ""

    for i in range(len(cipher_text)):
        curr_cipher_text_num = ord(cipher_text[i]) - ord('a')
        curr_key_text_num = ord(key[i]) - ord('a')
        curr_plain_text_num = (curr_cipher_text_num - curr_key_text_num) % 26

        plain_text += alf[curr_plain_text_num]
    return plain_text

def vigenerestdEnc(plain_text: str, key: str):
    plain_text = clean_text(plain_text)
    key = clean_text(key)
    full_key = getKey(plain_text, key)
    return vigenereEnc(plain_text, full_key)

def vigenerestdDec(cipher_text: str, key: str):
    cipher_text = clean_text(cipher_text)
    key = clean_text(key)
    full_key = getKey(cipher_text, key)
    return vigenereDec(cipher_text, full_key)