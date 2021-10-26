import secrets

def generateKey(p):
    # g < p
    g = secrets.randbelow(p)
    # 1 <= x <= p-2
    x = secrets.choice(range(1,p-1))
    y = (g ** x) % p
    keys = {
        "public" : (y, g, p),
        "private" : (x, p)
    }
    return keys

print(generateKey(2357)) 