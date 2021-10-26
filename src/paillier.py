import secrets, math
from util import isPrime, getInversion

def L(x, n):
    return int((x-1)/n)

def generateKey(p, q):
    if (isPrime(p) and isPrime(q) and math.gcd(p*q, (p-1)*(q-1))):
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

print(generateKey(7, 11))