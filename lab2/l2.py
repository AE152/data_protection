import random
from math import sqrt, ceil

#проверяет простое чило или нет
def is_prime(a):
   if (a <= 1):
      return False
   count_division = 1
   for i in range(2, a // 2 + 1):
      if (a % i == 0):
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
def generate_prime_not_p(p):
   while (True):
      Cb = rand_prime(0,p)
      if (Cb != p):
         break
   return Cb


def shamir(m):
   print("шифр Шамира :")
   p = rand_prime(100, 10 ** 4)
   Ca = generate_prime_not_p(p - 1)
   tmp = gcd_modified(p - 1, Ca)
   Da = tmp[2]
   if Da < 0:
      Da += p - 1
   Cb = generate_prime_not_p(p - 1)
   tmp = gcd_modified(p - 1, Cb)
   Db = tmp[2]
   if Db < 0:
      Db += p - 1

   encoding_res = list()
   for m_i in m:
      x1 = module(m_i,Ca,p)
      x2 = module(x1, Cb ,p)
      encoding_res.append(x2)

   #print("результат кодирования = ",encoding_res)

   with open('out.txt', 'wt') as out_file:
        out_file.write(str(encoding_res))

   decoding_res = list()
   for tmp in encoding_res:
      x3 = module(tmp , Da, p)
      x4 = module(x3,Db,p)
      decoding_res.append(x4)
   #print("результат декодирования = ", bytes(decoding_res))


   with open('out.jpeg', 'wb') as out_file:
        out_file.write(bytes(decoding_res))


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

# шифр Эль-Гамаля
def ElGamal(m):
   print("шифр Эль-Гамаля :")

   tmp = rand_p_q_g()
   p = tmp[0]
   g = tmp[2]

   A_ci = rand_prime(0, p - 1)
   A_di = module(g,A_ci,p)

   B_ci = rand_prime(0, p - 1)
   r = module(g,B_ci,p)

   encoding_res = list() 
   for m_i in m:
      b = m_i*module(A_di,B_ci,p) % p
      encoding_res.append(b)
   #print("результат кодирования = ",encoding_res)

   with open('out.txt', 'wt') as out_file:
        out_file.write(str(encoding_res))

   decoding_res = list()
   for e in encoding_res:
      m1 = e * module( r,(p - 1 - A_ci), p) % p
      decoding_res.append(m1)
   #print("результат декодирования = ", bytes(decoding_res))
   # with open('out.txt', 'wb') as out_file:
   #      out_file.write(bytes(decoding_res))
   with open('out.jpeg', 'wb') as out_file:
        out_file.write(bytes(decoding_res))
   


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


# шифр RSA
def RSA(m):
   print("шифр RSA :")

   P = rand_prime(0, 10 ** 4)
   Q = rand_prime(0, 10 ** 4)
   N = P * Q
   Phi = (P - 1) * (Q - 1)
   d = generate_prime_not_p(Phi)
   c = gcd_modified(d, Phi)[1]
   if c < 0:
      c += Phi
   encoding_res = list()
   for m_i in m:
      e = module(m_i, d, N)
      encoding_res.append(e)
   #print("результат кодирования = ",encoding_res)
   with open('out.txt', 'wt') as out_file:
        out_file.write(str(encoding_res))

   decoding_res = list()
   for tmp in encoding_res:
      m1 = module(tmp, c, N)
      decoding_res.append(m1)
   #print("результат декодирования = ", bytes(decoding_res))
   with open('out.jpeg', 'wb') as out_file:
        out_file.write(bytes(decoding_res))


# шифр Вернама
def vernam(m):
   print("шифр Вернама :")
   codes = list()
   for _ in range(len(m)):
      codes.append(random.randint(0, 255))
   
   encoding_res = list()
   for i in range(len(m)):
      encoding_res.append(m[i] ^ codes[i])
   #print("результат кодирования = ",encoding_res)
   with open('out.txt', 'wt') as out_file:
        out_file.write(str(encoding_res))

   decoding_res = list()
   for i in range(len(m)):
      decoding_res.append(encoding_res[i] ^ codes[i])
   #print("результат декодирования = ",bytes(decoding_res))
   with open('out.jpeg', 'wb') as out_file:
        out_file.write(bytes(decoding_res))


if __name__ == '__main__':

   with open('orig.jpeg', 'rb') as origin_file:
      m = bytes(origin_file.read())
   #print(m)

   #shamir(m)

   #ElGamal(m)
   
   #RSA(m)

   vernam(m)
   
   
   
