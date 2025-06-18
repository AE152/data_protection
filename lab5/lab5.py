import random
import secrets
import hashlib

def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

# def is_prime(number):
#     if number <= 1:
#         return False
#     elif number == 2:
#         return True
#     elif number % 2 == 0:
#         return False
#     else:
#         # Проверяем делители от 3 до квадратного корня из числа (включительно)
#         for i in range(3, int(number**0.5) + 1, 2):
#             if number % i == 0:
#                 return False
#         return True

def is_prime(p):
    if p <= 1:
        return False
    elif p == 2:
        return True
    a = random.randint(2, p - 1)
    # print(p, "-", a)
    if module(a, (p - 1), p) != 1 or gcd(p, a) > 1:
        return False
    return True

#возвращает рандомное простое число
def rand_prime(from_, to):
   while True:
      tmp = random.randint(from_, to)
      if is_prime(tmp):
         return tmp


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



class Server:
    def __init__(self) -> None:
      q = secrets.randbits(1024)
      while not is_prime(q):
         q = secrets.randbits(1024)

      p = secrets.randbits(1024)
      while (not is_prime(p)) or (p == q):
         p = secrets.randbits(1024)
      
      self.N = p * q
      
      Phi = (p - 1) * (q - 1)

      C = rand_prime_not_p(Phi)
      while (C == Phi):
         C = rand_prime_not_p(Phi)
      self.C = C

      D = gcd_modified(C, Phi)[1]
      if D < 0:
         D += Phi
      self.D = D

      self.people = list()
      self.resultBlanks = list()

class Person:
   def __init__(self, passport, vote) -> None:
      self.passport = passport
      self.vote = vote


def sha3(n: int) -> int:
   # Преобразуем число в байты
   data = n.to_bytes((n.bit_length() +7) // 8, byteorder='big')

   # Получаем хэш в виде шестнадцатеричной строки
   hash_result = hashlib.sha3_224(data).hexdigest()

   # Переводим хэш обратно в целое число
   decoded_number = int(hash_result, 16)

   return decoded_number

def voting(Serv : Server, person : Person):
   if person.passport in Serv.people:
      print("Пользователь: " + person.passport + " уже проголосовал")
   else:
      rnd = secrets.randbits(512)
      if (person.vote == "yes"):
         v = 1
      elif (person.vote == "no"):
         v = 0
      n = rnd << 512 | v
      print(n)
      r = rand_prime_not_p(Serv.N)
      h = sha3(n)
      h_ =  (h * pow(r, Serv.D, Serv.N)) % Serv.N
      Serv.people.append(person.passport)
      s_ = module(h_, Serv.C, Serv.N)

      tmp = gcd_modified(r, Serv.N)
      if tmp[0] == 1:
         r_1 = tmp[1]
      else: 
         r_1 = tmp[0]
      if(r_1 < 0):
         r_1 += Serv.N

      s = (s_ * r_1) % Serv.N

      if (module(s, Serv.D, Serv.N) == sha3(n)):
         Serv.resultBlanks.append((s, n))
         print("Голос пользователя: " + person.passport + " принят")

      else:
         print("Голос пользователя: " + person.passport + "отклонен")



Serv = Server()

Alice = Person("12345", "no")
Alex = Person("11111", "no")
Bob = Person("54321", "yes")


voting(Serv, Alice)
voting(Serv, Alex)
voting(Serv, Bob)
voting(Serv, Bob)

res = [0, 0]
for i in Serv.resultBlanks:
   if (i[1] & 1) == 0:
      res[0] += 1
   if (i[1] & 1) == 1:
      res[1] += 1

print("Результаты голосования:\nЗа: " + str(res[1]) + "\nПротив:" + str(res[0]))









