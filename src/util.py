import string

def isPrime(x):
    # Cek apakah sebuah angka bilangan prima
    if x > 1:
        for i in range(2, int(x/2)+1):
            if (x%i) == 0:
                break
        return True

    return False

def getInversion(n, m):
    # cari inversi m (mod n)   
    # for i in range(1,n):
    #     if ((m*i) % n == 1):
    #         return i
    try:
        val = pow(m, -1, n)
        return val
    except:
        return None 

def encodeText(p):
    enc = ''
    for char in p.lower():
        # A=01, B=02, ..., Z = 26
        idx = str(string.ascii_lowercase.rfind(char)+1)
        enc += idx.zfill(2)
    return enc

def encodeTextOneDigit(p):
    enc = ''
    for char in p.lower():
        # A=1, B=2, ..., Z = 26
        idx = str(string.ascii_lowercase.rfind(char)+1)
        enc += idx
    return enc