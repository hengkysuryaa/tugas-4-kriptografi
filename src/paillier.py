import secrets, math
from rsa import decrypt
from util import encodeText, isPrime, getInversion

def L(x, n):
    return int((x-1)/n)

def checkKey(p, q):
    return (isPrime(p) and isPrime(q) and (math.gcd(p*q, (p-1)*(q-1)) == 1))

def generateKey(p, q):
    if (isPrime(p) and isPrime(q) and (math.gcd(p*q, (p-1)*(q-1)) == 1)):
        n = p * q
        lamb = math.lcm(p-1, q-1)
        found = False
        while not(found): # mitigasi not invertible
            g = secrets.randbelow(n**2)
            l = L((g**lamb) % (n**2), n)
            miu = getInversion(n, l) 
            if miu != None:
                found = True
        keys = {
            "public" : (g, n),
            "private" : (lamb, miu)
        }
        return keys
    else:
        print("p,q tidak memenuhi syarat")

def getRList(n):
    # Generate bilangan bulat acak r
    list = []
    for i in range(1,n):
        if math.gcd(i,n) == 1:
            list.append(i)
    return list

def encrypt(plainteks, g, n):
    # TODO input teks/angka
    # encode
    enc = encodeText(plainteks)
    #print(enc)
    cipher = ''
    nBlock = len(str(n))
    r = secrets.choice(getRList(n))
    i = 0
    while i < (len(enc) - (len(enc) % nBlock)):
        val = int(enc[i:i+nBlock])
        # cek apakah val >= n
        if val >= n:
            # ciphering 
            val = int(enc[i:i+nBlock-1])
            i -= 1
        i += nBlock
        c = ((g**val) * (r**n)) % (n**2)
        cipher += str(c) + " "
        #print(val, c)

    # sisa angka, jika ada
    if (i < len(enc)):
        c = ((g**val) * (r**n)) % (n**2)
        cipher += str(c) + " "
        #print("sisa", enc[i:], c)
        #print("cipher", cipher)
    return cipher.rstrip()

def decrypt(ciphertext, lamb, miu, n):
    # encode
    #enc = encodeTextPailier(plainteks)
    #print(enc)
    cipher_list = ciphertext.split(" ")
    plain = ''
    for item in cipher_list:
        val = int(item)
        p = (L((val**lamb) % (n**2), n) * miu) % n
        #print(val, p)
        if (p < 10):
            plain += str(p).zfill(2)
        else:
            plain += str(p)

    return plain

if __name__ == "__main__":
    p = 7
    q = 11
    if (checkKey(p, q)):
        keys = generateKey(p, q)
        teks = "akusedangbelajarrajadannaif"
        print(teks)
        enc = encrypt(teks, keys["public"][0], keys["public"][1])
        print(enc)
        dec = decrypt(enc, keys["private"][0], keys["private"][1], keys["public"][1])
        print(encodeText(teks))
        print(dec)
        if (dec == encodeText(teks)):
            print("didekripsi menjadi semula")