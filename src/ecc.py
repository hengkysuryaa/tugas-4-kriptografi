import secrets, math
import string

def add(p1, p2, p):
    if (p2[0] - p1[0] == 0):
        return p1
    #print(p2[1] - p1[1], p2[0] - p1[0])
    m = ((p2[1] - p1[1]) * pow((p2[0] - p1[0]), -1, p)) % p
    xr = ((m**2) - p1[0] - p2[0]) % p
    yr = (m*(p1[0] - xr) - p1[1]) % p
    return (xr, yr)

def mult(point, k, a ,p):
    # Cari 2P
    if (k>1):
        x = point[0]
        y = point[1]
        m = ((3*(x**2) + a) * pow(2*y, -1, p)) % p
        xr = ((m**2) - 2*x) % p
        yr = (m*(x-xr) - y) % p
        point2 = (xr, yr)
        for i in range(3, k+1):
            point2 = add(point, point2, p)
        return point2
    else:
        return point

def generateElipticGroup(a, b, p):
    list = []
    for i in range(p):
        y_squared = ((i**3) + a*i + b) % p
        for j in range(p):
            if ((j**2)%p) == y_squared:
                list.append((i,j))

    return list

def getkTable(a, b, p, x, y):
    eg = generateElipticGroup(a, b, p)
    list = [(x,y)]
    m = ((3*(x**2) + a) * pow(2*y, -1, p)) % p
    xr = ((m**2) - 2*x) % p
    yr = (m*(x-xr) - y) % p
    list.append((xr, yr))
    for i in range(2, len(eg)):
        # print(list)
        # print(list[i-1][1] - list[0][1])
        m = ((list[i-1][1] - list[0][1]) * pow((list[i-1][0] - list[0][0]), -1, p)) % p
        xr = ((m**2) - list[0][0] - list[i-1][0]) % p
        yr = (m*(list[0][0] - xr) - list[0][1]) % p
        list.append((xr, yr))
    
    return list

def generateKey(a, b, p, x, y):
    try:
        privateKey = secrets.choice(range(1,p))
        # q = ktable[privateKey]
        q = mult((x,y), privateKey, a, p)
    except:
        return None
    
    return {
        "public" : q,
        "private" : privateKey
    }

def encodeKolbitz(plain, a, b, p, k):
    charlist = 'abcdefghijklmnopqrstuvwxyz'
    found = False
    i = 1
    m = charlist.find(plain)
    print(m)
    while not(found):
        x = m*k + i
        y_squared = ((x**3) + a*x + b) % p
        y = -999
        for j in range(p):
            if ((j**2)%p) == y_squared:
                y = j
                found = True
                break
        i += 1

    return (x, y)

def decodeKobiltz(code, k):
    charlist = 'abcdefghijklmnopqrstuvwxyz'
    plain = ''
    for item in code:
        #print(item)
        m = charlist[math.floor((item[0]-1)/k)]
        plain += m
    return plain

def encodeECC(char):
    idx = string.ascii_lowercase.rfind(char)
    idx = str(idx).zfill(2)
    return (int(idx[0]), int(idx[1]))

def decodeECC(point):
    idx = int(str(point[0]) + str(point[1]))
    char = string.ascii_lowercase[idx]
    return char

def encrypt(plainteks, basePoint, publicKey, a, b, p, k):
    cipher = []
    #print(kTable)
    for char in plainteks:
        #print(char)
        #pm = encodeKolbitz(char, a, b, p, k)
        pm = encodeECC(char)
        #pm = (10,10)
        #print(pm)
        k_enc = secrets.choice(range(1,p))
        #print(k_enc)
        #item1 = kTable[k_enc]
        item1 = mult(basePoint, k_enc, a, p)
        #print(item1)
        item2 = add(pm, mult(publicKey, k_enc, a, p), p)
        # print(pm)
        # print("kbB", mult(publicKey, k_enc, a, p))
        #print(item2)
        #item2 = (3,2)
        cipher.append((item1, item2))
    return cipher

def decrypt(ciphertext, privateKey, a, p, k):
    plain = ''
    for c in ciphertext:
        x = mult(c[0], privateKey, a , p)
        x = (x[0], -x[1])
        #print("x", x)
        pm = add(c[1], x, p)
        #print("pm", pm)
        #print("bkB", x)
        print(pm)
        plain += decodeECC(pm)
    return plain
    # plain = decodeKobiltz(plain, k)
    # return plain

if __name__ == "__main__":
    eg = generateElipticGroup(1, 6, 47)
    #kt = getkTable(2, 1, 5, 0, 1)
    #alicekey = generateKey(2, 1, 5, eg[0][0], eg[0][1])
    # bobkey = generateKey(1, 6, 47, eg[3][0], eg[3][1])
    # print(bobkey)
    #print(bobkey)
    #print(encodeKolbitz('b', -1, 188, 751, 20))
    #print("add:", add((35,4), (8,3), 11))
    #print(mult((5,9), 3, 1, 11))
    #print(encrypt('b', eg[0], key["public"], 2, 1, 5, 3))
    teks = 'hello'
    enc = encrypt(teks, eg[3], (2, 4), 1, 6, 47, 3)
    #print(enc)
    dec = decrypt(enc, 11, 1, 47, 3)
    print(dec)
    if (dec == teks):
        print("didekripsi menjadi semula")
    #print(mult((8,3),3,1,11))