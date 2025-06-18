import random
from math import sqrt, ceil
import os
import shutil
import hashlib
from colorama import Fore, init
from math import sqrt

def is_prime(number):
    if number <= 1:
        return False
    elif number == 2:
        return True
    elif number % 2 == 0:
        return False
    else:
        # Проверяем делители от 3 до квадратного корня из числа (включительно)
        for i in range(3, int(number**0.5) + 1, 2):
            if number % i == 0:
                return False
        return True

#возвращает рандомное простое число
def rand_prime(from_, to):
   while True:
      tmp = random.randint(from_, to)
      if is_prime(tmp):
         return tmp
      
#обобщенный алгоритм Евклида
def evkl_gcd(a, b):
   if (a<b):
      print("Bad imput data!")
      return -1
   
   U = [a, 1, 0]
   V = [b, 0, 1]
   while (V[0] != 0):
      q = U[0] // V[0]
      T = [U[0] % V[0], U[1] - q * V[1], U[2] - q * V[2]]
      U = V
      V = T
   return U


# Обобщённый Алгоритм Евклида, для нахождения наибольшего общего делителя и двух неизвестных уравнения
def gcd_modified(a, b):
   U = (a, 1, 0)
   V = (b, 0, 1)
   while (V[0] != 0):
      q = U[0] // V[0]
      T = (U[0] % V[0], U[1] - q * V[1], U[2] - q * V[2])
      U = V
      V = T
   return U
   
# генерируем взаимно-простое число
def rand_prime_not_p(p):
   while (True):
      Cb = rand_prime(0,p)
      if (Cb != p):
         break
   return Cb

# читаем побайтово файлы
def read_file(filename: str, ext: str) -> bytearray:
    with open(filename + '.' + ext, 'rb') as origin_file:
        return bytearray(origin_file.read())

#быстрое возведение в степень по модулю
def module(a, x, p):
   y = 1
   s = a

   while x > 0:
      if (x % 2 == 1):
         y = (y * s) % p
      s = (s * s) % p
      x = x//2

   return y

def rand_p_q_g():
   while True:
      q = rand_prime(100, 10**4)
      p = 2 * q + 1
      if is_prime(p):
         break
   while True:
      g = rand_prime(1, p - 1)
      if module(g,q, p) != 1:
         return [p, q, g]


#x - секретное
#y - публичное
#r s - для проверки подписи
def ElGamal_signature(m):
    tmp = rand_p_q_g()
    p = tmp[0]
    g = tmp[2]
    x = rand_prime(1, p - 1)
    y = module(g, x, p)
    k = rand_prime_not_p(p - 1)
    r = module(g, k, p)

    h = hashlib.md5(m).hexdigest()

    # числовое представление хэш функции 
    h_b = ""
    for tmp_h in h:
       h_b += str(module(g, int(tmp_h, 16), p))
    print(f'hash h_b {h_b}')

    u = []
    for h_tmp in h:
       u.append((int(h_tmp, 16) - x * r) % (p - 1))
    s = []
    for u_tmp in u:
       s.append((gcd_modified(k, p - 1)[1] * u_tmp) % (p - 1))

    with open('elgamal.txt', 'w') as f:
        f.write(str(s))

    #Проверка подписи
    res = ""
    for tmp_s in s:
       res += str(module(y, r, p) * module(r, tmp_s, p) % p)
    print(f'hash check: {res}')

    if res == h_b:
       print("signature is correct")
    else:
       print("signature is not correct")


# N d - публичные
# c - секретное
def RSA_signature(m):
   P = rand_prime(0, 10 ** 2)
   Q = rand_prime(0, 10 ** 2)
   N = P * Q
   Phi = (P - 1) * (Q - 1)
   d = rand_prime_not_p(Phi)
   c = gcd_modified(d, Phi)[1]
   if c < 0:
      c += Phi

   # Хэш функция подписанного сообщения
   h = hashlib.md5(m).hexdigest()
   print(f'hash: {h}')
   # числовое представление хэш функции 
   h_b = ""
   for tmp_h in h:
      h_b += str(int(tmp_h, 16))
   print(f'hash h_b {h_b}')
    
   s = []
   for tmp_h in h:
      s.append(module(int(tmp_h, 16), c, N))

   with open('rsa.txt', 'w') as f:
      f.write(str(s))

   #Проверка подписи
   res = ""
   for tmp_s in s:
      res += str(module(tmp_s, d, N))
   print(f'hash check: {res}')

   if res == h_b:
      print("signature is correct")
   else:
      print("signature is not correct")

import secrets

#x - секретный
#y, r, q - публичное
def GOST_sign(m: bytearray):
   q = secrets.randbits(16)
   while not is_prime(q):
      q = secrets.randbits(16)

   b = secrets.randbits(31)
   while not is_prime(q * b + 1):
      b = secrets.randbits(31)
   p = q * b + 1

   g = random.randint(1, p - 1)
   a = module(g, b, p)
   while not a > 1:
      g = random.randint(1, p - 1)
      a = module(g, b, p)

   x = random.randint(1, q-1)

   y = module(a, x, p)

   h = hashlib.md5(m).hexdigest()
   print(f'hash: {h}')
   h = int(h, 16)

   r = 0
   s = 0
   while s == 0:
      while r == 0:
         k = random.randint(1, q-1)
         r = module(a, k, p) % q
      s = (k * h + x * r) % q

   with open("gost.txt", 'w') as f:
      f.write(str(s))

   #Проверка подписи
   h_1 = gcd_modified(h, q)[1]
   if h_1 < 1:
      h_1 += q


   u1 = (s * h_1) % q
   u2 = (-r * h_1) % q
   v = ((module(a, u1, p) * module(y, u2, p)) % p) % q

   if v == r:
      print("signature is correct")
   else:
      print("signature is not correct")



if __name__ == '__main__':

   m = read_file("input", "txt")

   print(m)

   print()
   ElGamal_signature(m)

   print()
   RSA_signature(m)
   
   print()
   GOST_sign(m)










   #проверяет простое чило или нет
# def is_prime(a):
#    if (a <= 1):
#       return False
#    count_division = 1
#    for i in range(2, int(sqrt(a)) + 1):
#       if (a % i == 0):
#          count_division += 1
#    if count_division >= 2:
#       return False
#    else:
#       return True
   
# def is_prime2(p):
#     if p <= 1:
#         return False
#     elif p == 2:
#         return True
#     a = random.randint(2, p - 1)
#     # print(p, "-", a)
#     if module(a, (p - 1), p) != 1 or gcd(p, a) > 1:
#         return False
#     return True

# def is_prime3(num):
#     prime = num > 1 and (num % 2 != 0 or num == 2) and (num % 3 != 0 or num == 3)
#     i = 5
#     d = 2

#     while prime and i * i <= num:
#         prime = num % i != 0
#         i += d
#         d = 6 - d # чередование прироста 2 и 4: 5 + 2, 7 + 4, 11 + 2, и т.д.
#     return prime