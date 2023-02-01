import re 

def clean_text(txt):
    txt = txt.upper()
    txt = re.sub(r'\s*\d+\s*', '', txt)
    txt = re.sub(r'[^\w\s]', '', txt)
    txt = txt.replace(' ','')
    return txt

def process_text(txt):
    txt = [txt[i:i+5] for i in range(0, len(txt), 5)]
    txt = ' '.join(txt)
    return txt

def make_matrix(x, y, init):
    return [[init for i in range(x)] for j in range (y)]

def locate_index(c, playfair_matrix):
    loc = list()
    if c == 'J':
        c = 'I'
    for i, j in enumerate(playfair_matrix):
        for k, l in enumerate(j):
            if c == l:
                loc.append(i)
                loc.append(k)
                return loc

def encrypt(txt, playfair_matrix):
    txt = clean_text(txt)
    cipher = ''
    i = 0
    for s in range(0, len(txt)+1, 2):
        if s < len(txt)-1:
            if txt[s] == txt[s+1]:
                txt = txt[:s:1] + 'X' + txt[s+1:]
    if len(txt) % 2 != 0:
        txt = txt[:] + 'X'
    
    while i < len(txt):
        loc = locate_index(txt[i], playfair_matrix)
        loc1 = locate_index(txt[i+1], playfair_matrix)
        if loc[1] == loc1[1]:
            cipher += playfair_matrix[(loc[0] + 1) % 5][loc[1]] + playfair_matrix[(loc1[0] + 1) % 5][loc1[1]]
        elif loc[0] == loc1[0]:
            cipher += playfair_matrix[loc[0]][(loc[1] + 1) % 5] + playfair_matrix[loc1[0]][(loc1[1] + 1) % 5]
        else:
            cipher += playfair_matrix[loc[0]][loc1[1]] + playfair_matrix[loc1[0]][loc[1]]
        i += 2

    cipher = process_text(cipher)
    return cipher

def decrypt(cipher, playfair_matrix):
    cipher = clean_text(cipher)
    plaintxt = ''
    i = 0
    while i < len(cipher):
        loc = locate_index(cipher[i], playfair_matrix)
        loc1 = locate_index(cipher[i+1], playfair_matrix)
        if loc[1] == loc1[1]:
            plaintxt += playfair_matrix[(loc[0] - 1) % 5][loc[1]] + playfair_matrix[(loc[0] - 1) % 5][loc1[1]]
        elif loc[0] == loc1[0]:
            plaintxt += playfair_matrix[loc[0]][(loc[1] - 1) % 5] + playfair_matrix[loc1[0]][(loc1[1] - 1) % 5]
        else:
            plaintxt += playfair_matrix[loc[0]][loc1[1]] + playfair_matrix[loc1[0]][loc[1]]
        i += 2

    plaintxt = process_text(plaintxt)
    return plaintxt

def make_playfair_square(key):
    key = key.upper()
    res = list()
    for c in key:
        if c not in res:
            if c == 'J':
                res.append('I')
            else:
                res.append(c)
    flag = 0

    for i in range(65, 91):
        if chr(i) not in res:
            if i == 73 and chr(74) not in res:
                res.append('I')
                flag = 1
            elif flag == 0 and i == 73 or i == 74:
                pass
            else:
                res.append(chr(i))
    k = 0
    matrix = make_matrix(5, 5, 0)
    for i in range(0, 5):
        for j in range(0, 5):
            matrix[i][j] = res[k]
            k += 1
    return matrix
