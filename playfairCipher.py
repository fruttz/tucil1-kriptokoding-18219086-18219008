import re

def textCleaning(text):
    text = text.upper()
    text = re.sub(r'\s*\d+\s*', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace(' ', '')
    return text

def postProcess(text):
    text = [text[i:i+5] for i in range(0, len(text), 5)]
    text = ' '.join(text)
    return text

def matriks(x, y, initial):
    return [[initial for i in range(x)] for j in range(y)]

def locateIndex(c, matriksPlayfair):  # get location of each character
    loc = list()
    if c == 'J':
        c = 'I'
    for i, j in enumerate(matriksPlayfair):
        for k, l in enumerate(j):
            if c == l:
                loc.append(i)
                loc.append(k)
                return loc

def encrypt(text, matriksPlayfair):
    text = textCleaning(text)
    cipher = ''
    i = 0
    for s in range(0, len(text)+1, 2):
        if s < len(text)-1:
            if text[s] == text[s+1]:
                text = text[:s+1]+'X'+text[s+1:]
    if len(text) % 2 != 0:
        text = text[:]+'X'

    while i < len(text):
        loc = list()
        loc = locateIndex(text[i], matriksPlayfair)
        loc1 = list()
        loc1 = locateIndex(text[i+1], matriksPlayfair)
        if loc[1] == loc1[1]:
            cipher += matriksPlayfair[(loc[0]+1)%5][loc[1]] + matriksPlayfair[(loc1[0]+1)%5][loc1[1]]
        elif loc[0] == loc1[0]:
            cipher += matriksPlayfair[loc[0]][(loc[1]+1) % 5] + matriksPlayfair[loc1[0]][(loc1[1]+1) % 5]
        else:
            cipher += matriksPlayfair[loc[0]][loc1[1]] + matriksPlayfair[loc1[0]][loc[1]]
        i = i+2

    cipher = postProcess(cipher)
    return cipher


def decrypt(cipher, matriksPlayfair):  # decryption
    cipher = textCleaning(cipher)
    plainText = ''
    i = 0
    while i < len(cipher):
        loc = list()
        loc = locateIndex(cipher[i], matriksPlayfair)
        loc1 = list()
        loc1 = locateIndex(cipher[i+1], matriksPlayfair)
        if loc[1] == loc1[1]:
            plainText += matriksPlayfair[(loc[0]-1) % 5][loc[1]] + matriksPlayfair[(loc1[0]-1) % 5][loc1[1]]
        elif loc[0] == loc1[0]:
            plainText += matriksPlayfair[loc[0]][(loc[1]-1) % 5] + matriksPlayfair[loc1[0]][(loc1[1]-1) % 5]
        else:
            plainText += matriksPlayfair[loc[0]][loc1[1]] + matriksPlayfair[loc1[0]][loc[1]]
        i = i+2

    plainText = postProcess(plainText)
    return plainText


def createPlayfairSquare(key):
    key = key.upper()
    result = list()

    for c in key:  # storing key
        if c not in result:
            if c == 'J':  # replacing j with i
                result.append('I')
            else:
                result.append(c)
    flag = 0

    for i in range(65, 91):  # storing other character
        if chr(i) not in result:
            if i == 73 and chr(74) not in result:
                result.append("I")
                flag = 1
            elif flag == 0 and i == 73 or i == 74:
                pass
            else:
                result.append(chr(i))
    k = 0
    thisMatrix = matriks(5, 5, 0)  # initialize matrix
    for i in range(0, 5):  # making matrix
        for j in range(0, 5):
            thisMatrix[i][j] = result[k]
            k += 1
    return thisMatrix

def main():
    while(1):
        choice=int(input("\n 1.Encryption \n 2.Decryption: \n 3.EXIT \n"))
        key=input("Enter key : ")
        key = textCleaning(key)

        PS = createPlayfairSquare(key)
        if choice==1:
            plainText = input("Enter Plaintext : ")
            plainText = textCleaning(plainText)
            print(encrypt(plainText, PS))
        elif choice==2:
            cipher = input('Enter cipher : ')
            cipher = textCleaning(cipher)
            print(decrypt(cipher,PS))
        elif choice==3:
            exit()
        else:
            print("Choose correct choice")
    return 0

if __name__ == '__main__':
    main()