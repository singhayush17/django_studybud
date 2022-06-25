from itertools import groupby

from collections import OrderedDict

import math
from collections import Counter
import os
import sys
from io import BytesIO, IOBase
def main():
    pass
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):

        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)

class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

if __name__ == "__main__":
    main()




'''kk
l=[ [0]*m for i in range(n)]'''

'''GROUP BY
res=[i[0] for i in groupby(l)]'''


def find_gcd(l):
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a
    n =1
    f = l[0]
    while n != len(l):
        f = gcd(f,l[n])
        if  f == 1:
            return 1
        else:
            n = n + 1
    return f


def lcm(a,b):
    return (a // math.gcd(a,b))* b


def isPrime(n):
    if(n<2): return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True


'''Remove dupl w order
res = list(OrderedDict.fromkeys(l))'''

def decimalToBinary(n):
    return bin(n).replace("0b", "")


def binaryToDecimal(n):
    n=str(n)
    return int(n,2)


import bisect
#a=bisect.bisect_left(l,b)


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]



