import math, secrets, string
from util import isPrime, getInversion

def getPublicKeyList(n):
    # Generate kandidat public key
    list = []
    for i in range(1,n):
        if math.gcd(i,n) == 1:
            list.append(i)
    return list

def encodeText(p):
    enc = ''
    for char in p.lower():
        idx = str(string.ascii_lowercase.rfind(char))
        enc += idx.zfill(2)
    return enc

def decodeText(c):
    dec = ''
    list = []
    for idx in range(0, len(c), 2):
        list.append(c[idx:idx+2])
    
    for item in list:
        dec += string.ascii_lowercase[int(item)]

    return dec

def generateKey(p, q):
    if (isPrime(p) and isPrime(q)):
        n = p * q
        toisent = (p-1) * (q-1)
        public_keys = getPublicKeyList(toisent)
        e = secrets.choice(public_keys)
        d = getInversion(toisent, e)
        # return e, d, n
        keys = {
            "public" : (e, n),
            "private" : (d, n)
        }
        return keys
    else:
        print("p, q tidak prima")

def encrypt(plaintext, e, n):
    # TODO: apakah 26 alphabet saja, m bebas (?), jika m tidak habis dibagi pesan
    # output angka/teks
    enc = encodeText(plaintext)
    print(enc)
    cipher = ''
    nBlock = len(str(n))-1
    # if (len(enc) % nBlock != 0):
    for i in range(0, len(enc), nBlock):
        #print(i)
        c = (int(enc[i:nBlock+i]) ** e) % n
        print(c, (int(enc[i:nBlock+i])))
        cipher += str(c).zfill(nBlock)
    print(i)
    if (len(enc) % nBlock != 0):
        c = (int(enc[i:]) ** e) % n
        print(enc[i:], c)
        cipher += str(c)
    # else:
    #     print("error")
    return cipher

def decrypt(ciphertext, d, n):
    enc = encodeText(ciphertext)
    # plain = ''
    # nBlock = len(str(n))-1
    # if (len(enc) % nBlock == 0):
    #     for i in range(0, len(enc), nBlock):
    #         #print(i)
    #         c = (int(enc[i:nBlock+i]) ** e) % n
    #         #print(c, (int(enc[i:nBlock+i])))
    #         plain += str(c)
    # else:
    #     print("error")
    # return plain
    
# if (isPrime(2) and isPrime(3)):
#     print("prime")
#print(getPublicKeyList(3220))
print(generateKey(47, 71))
# print(e, d, n)
# print(encodePlaintext("HELOALICE"))
#print(encrypt("HELLOALICE", 79, 3337))
#print(encrypt("HELLOALICE", 1019, 3337))
#print(decodeText("081125").upper())