import re

characters = [chr(97 + i) for i in range (26)]

def process_text(txt: str) -> str:
    res = txt

    #remove spaces
    res.strip()
    res = res.replace(" ","")
    res = res.lower()

    #remove numbers and symbols
    res = ''.join([i for i in res if not i.isdigit()])
    res = re.sub(r'[^\w\s]', '', res)

    return res

def generate_key(txt, key) -> str:
    if(len(key) >= len(txt)):
        return key[:len(key)]
    
    full_key = key
    for i in range(len(txt) - len(key)):
        full_key += key[i % len(key)]
    
    return full_key

def encrypt(txt, key) -> str:
    cipher_text = ""

    for i in range(len(txt)):
        curr_plain_text_num = ord(txt[i]) - ord('a')
        curr_key_text_num = ord(key[i]) - ord('a')
        curr_cipher_text_num = (curr_plain_text_num + curr_key_text_num) % 26

        cipher_text += characters[curr_cipher_text_num]
    return cipher_text

def decrypt(txt, key) -> str:
    plain_text = ""

    for i in range(len(txt)):
        curr_cipher_text_num = ord(txt[i]) - ord('a')
        curr_key_text_num = ord(key[i]) - ord('a')
        curr_plain_text_num = (curr_cipher_text_num - curr_key_text_num) % 26

        plain_text += characters[curr_plain_text_num]
    return plain_text

def vigenere_encrypt(plaintxt, key):
    plaintxt = process_text(plaintxt)
    key = process_text(key)
    full_key = generate_key(plaintxt, key)
    return encrypt(plaintxt, full_key)

def vigenere_decrypt(ciphertxt, key):
    ciphertxt = process_text(ciphertxt)
    key = process_text(key)
    full_key = generate_key(ciphertxt, key)
    return decrypt(ciphertxt, full_key)



    