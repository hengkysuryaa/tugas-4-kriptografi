import secrets

def add(p1, p2, p):
    #print(p2[0] - p1[0])
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
        for i in range(k-2):
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
    x = secrets.choice(range(1,p))
    ktable = getkTable(2, 1, 5, 0, 1)
    q = ktable[x-1]
    return {
        "public" : q,
        "private" : x
    }

def encodeKolbitz(plain, a, b, p, k):
    charlist = '0123456789abcdefghijklmnopqrstuvwxyz'
    found = False
    i = 1
    m = charlist.find(plain)
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

def encrypt(plainteks, basePoint, publicKey, a, b, p, k):
    cipher = []
    kTable = getkTable(a, b, p, basePoint[0], basePoint[1])
    for char in plainteks:
        pm = encodeKolbitz(char, a, b, p, k)
        print(pm)
        k_enc = secrets.choice(range(1,p))
        #print(k_enc)
        item1 = kTable[k_enc-1]
        item2 = add(pm, mult(publicKey, k_enc, a, p), p)
        cipher.append((item1, item2))
    return cipher

def decrypt(ciphertext, privateKey, a, p):
    for c in ciphertext:
        x = mult(c[0], privateKey, a , p)
        #print(x[1])
        x = (x[0], -x[1]%p)
        pm = add(c[0], x, p)
        print(pm)

if __name__ == "__main__":
    eg = generateElipticGroup(2, 1, 5)
    #kt = getkTable(2, 1, 5, 0, 1)
    alicekey = generateKey(2, 1, 5, eg[0][0], eg[0][1])
    bobkey = generateKey(2, 1, 5, eg[0][0], eg[0][1])
    #print(encodeKolbitz('b', -1, 188, 751, 20))
    #print(add((8,8), (5,9), 11))
    #print(mult((5,9), 3, 1, 11))
    #print(encrypt('b', eg[0], key["public"], 2, 1, 5, 3))
    enc = encrypt('b', eg[0], bobkey["public"], 2, 1, 5, 3)
    #decrypt(enc, bobkey["private"], 2, 5)
    
