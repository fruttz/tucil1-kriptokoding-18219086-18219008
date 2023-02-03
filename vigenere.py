import re

#vignere cipher std: 26 alfabet
alf = [chr(97 + i) for i in range(26)]

def enkripsiVigenere(plain_text: str, kunci: str) -> str:
    cipher_text = ""

    for i in range(len(plain_text)):
        curr_plain_text_num = ord(plain_text[i]) - ord('a')
        curr_kunci_text_num = ord(kunci[i]) - ord('a')
        curr_cipher_text_num = (curr_plain_text_num + curr_kunci_text_num) % 26

        cipher_text += alf[curr_cipher_text_num]
    return cipher_text

def dekripsiVigenere(cipher_text: str, kunci: str) -> str:
    plain_text = ""

    for i in range(len(cipher_text)):
        curr_cipher_text_num = ord(cipher_text[i]) - ord('a')
        curr_kunci_text_num = ord(kunci[i]) - ord('a')
        curr_plain_text_num = (curr_cipher_text_num - curr_kunci_text_num) % 26

        plain_text += alf[curr_plain_text_num]
    return plain_text

def vigenerestdEnkripsi(plain_text: str, kunci: str):
    plain_text = clean_text(plain_text)
    kunci = clean_text(kunci)
    full_kunci = getkunci(plain_text, kunci)
    return enkripsiVigenere(plain_text, full_kunci)

def vigenerestdDekripsi(cipher_text: str, kunci: str):
    cipher_text = clean_text(cipher_text)
    kunci = clean_text(kunci)
    full_kunci = getkunci(cipher_text, kunci)
    return dekripsiVigenere(cipher_text, full_kunci)

def clean_text(plainText: str) -> str:
    hasil = plainText

    #merge text
    hasil.strip()
    hasil = hasil.replace(" ", "")
    hasil = hasil.lower()

    #remove angka
    hasil = ''.join([i for i in hasil if not i.isdigit()])

    #remove tanda
    hasil = re.sub(r'[^\w\s]', '', hasil)

    return hasil

def getkunci(plain_text: str, kunci: str) -> str:
    if(len(kunci) >= len(plain_text)):
        return kunci[:len(kunci)]

    full_kunci: str = kunci
    for i in range(len(plain_text) - len(kunci)):
        full_kunci += kunci[i % len(kunci)]

    return full_kunci
