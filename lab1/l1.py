import random
from math import ceil, sqrt

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

#обобщенный алгоритм Евклида
def general_gcd(a, b):
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

#проверяет простое чило или нет
def is_prime(a):
   if (a <= 1):
      return False
   count_division = 1
   for i in range(2, a // 2 + 1):
      if (a % 2 == 0):
         count_division += 1
   if count_division >= 2:
      return False
   else:
      return True

#возвращает рандомное простое число
def rand_prime(from_, to):
   while True:
      tmp = random.randint(from_, to)
      if is_prime(tmp):
         return tmp


def rand_p_q_g():
   while True:
      q = rand_prime(2, 10**9)
      p = 2 * q + 1
      if is_prime(p):
         break
   while True:
      g = rand_prime(1, p - 1)
      if (module(g, q, p) != 1):
         return [p, q, g]

def diffie_hellman():
   tmp = rand_p_q_g()
   p = tmp[0]
   q = tmp[1]
   g = tmp[2]
   Xa = random.randint(100, 10**9)
   Xb = random.randint(100, 10**9)
   Ya = module(g, Xa, p)
   Yb = module(g, Xb, p)
   Zab = module(Yb, Xa, p)
   Zba = module(Ya, Xb, p)
   print("Параметры: p = ", p, "q = ", q, "g = ", g,
         "\nСекретные ключи: Xa = ", Xa, "Xb = ", Xb, 
         "\nОткрытые ключи: Ya = ", Ya, "Yb = ", Yb,
         "\n Zab = ", Zab, "Zba = ", Zba)

# Шаг младенца, шаг великана  y = a^x mod p 
def mladen_velik(y, a, p):
   m = k = ceil(sqrt(p))
   a_j_y = []
   a_im = []

   for j in range(0, m):
      i = j + 1
      a_j_y.append((a**j * y) % p)
      a_im.append((a**(i*m)) % p) 
   for i in range(0, m):
      if a_im[i] in a_j_y:
         j = a_j_y.index(a_im[i])
         i+=1
         break
   return(i*m-j)%p
   

print(module(13,5,11))

print(general_gcd(28,19))

diffie_hellman()

print(mladen_velik(10, 13, 11))

















#алгоритм Евклида
def gcd(a, b):
   if (a<b):
      print("Bad imput data!")
      return -1
   
   while(b != 0):
      r = a % b
      a = b
      b = r
      
   return a

print(gcd(130, 32))
print(general_gcd(130, 32))