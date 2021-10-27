import math, secrets, string
from util import isPrime, getInversion, encodeText

def getPublicKeyList(n):
    # Generate kandidat public key
    list = []
    for i in range(1,n):
        if math.gcd(i,n) == 1:
            list.append(i)
    return list

def decodeText(c):
    dec = ''
    list = []
    for idx in range(0, len(c), 2):
        list.append(c[idx:idx+2])
    
    for item in list:
        dec += string.ascii_lowercase[(int(item)-1)%26]

    return dec

def generateKey(p, q):
    if (isPrime(p) and isPrime(q)):
        n = p * q
        toisent = (p-1) * (q-1)
        public_keys = getPublicKeyList(toisent)
        e = secrets.choice(public_keys)
        d = getInversion(toisent, e)
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
    cipher = ''
    nBlock = len(str(n))
    i = 0
    while i < (len(enc) - (len(enc) % nBlock)):
        val = int(enc[i:i+nBlock])
        # cek apakah val >= n-1
        if val >= n-1:
            # ciphering 
            val = int(enc[i:i+nBlock-1])
            i -= 1
        i += nBlock
        c = (val ** e) % n
        cipher += str(c).zfill(nBlock)
        #print(val, c)

    # sisa angka, jika ada
    if (i < len(enc)):
        c = (int(enc[i:]) ** e) % n
        cipher += str(c).zfill(nBlock)
        #print("sisa", enc[i:], c)
        #print("cipher", cipher)
    return cipher

def decrypt(ciphertext, d, n):
    dec = ciphertext
    plain = ''
    nBlock = len(str(n))
    i = 0
    while i < (len(dec) - (len(dec) % nBlock)):
        val = int(dec[i:i+nBlock])
        # cek apakah val >= n-1
        if val >= n-1:
            # ciphering 
            val = int(dec[i:i+nBlock-1])
            i -= 1
        i += nBlock
        p = (val ** d) % n
        if (len(str(p))%2 != 0):
            plain += str(p).zfill(len(str(p))+1)
        else:
            plain += str(p)
        #print(val, c)

    # sisa angka, jika ada
    if (i < len(dec)):
        p = (int(dec[i:]) ** d) % n
        if (len(str(p))%2 != 0):
            plain += str(p).zfill(len(str(p))+1)
        else:
            plain += str(p)
        #print("sisa", enc[i:], c)
    return plain
    
if __name__ == "__main__":
    teks = "helloalicenicetomeetyou"
    keys = generateKey(83, 101)
    
    cipher_num = encrypt(teks, keys["public"][0], keys["public"][1])
    #print("cipher", decodeText(cipher_num))
    
    dec = decrypt(cipher_num, keys["private"][0], keys["private"][1])
    print("hasil dekripsi", decodeText(dec))
    
    if (teks == decodeText(dec)):
        print("didekripsi menjadi semula")
    
    #encoded = encodeText(teks)
    # if (isPrime(2) and isPrime(3)):
    #     print("prime")
    #print(getPublicKeyList(77))
    #print(generateKey(47, 71))
    # print(e, d, n)
    # print(encodePlaintext("HELOALICE"))
    #print(encrypt("HELLOALICE", 1019, 3337))
    #print(decodeText("081125").upper())