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