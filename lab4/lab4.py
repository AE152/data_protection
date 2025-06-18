import random

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


count_players = 7

value = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suit = ['♠', '♣', '♥', '♦']
all_cards = list()
for tmp_suit in suit:
    for tmp_value in value:
        all_cards.append((tmp_suit, tmp_value))

num_cards = list(range(2, 54))

q = rand_prime(10**6, 10**9)
while True:
    p = q * 2 + 1
    if is_prime(p):
        break
    q = rand_prime(10**6, 10**9)

c_i = list()
d_i = list()
for _ in range(0, count_players):
    tmp_c = rand_prime_not_p(p-1)
    tmp_d = gcd_modified(tmp_c, p-1)[1]
    if tmp_d < 0:
        tmp_d += (p - 1)
    c_i.append(tmp_c)
    d_i.append(tmp_d)

#Шифрование колоды
for i in range(0, count_players):
    for k in range(0, len(num_cards)):
        num_cards[k] = module(num_cards[k], c_i[i], p)
    random.shuffle(num_cards)

#Раздача карт
players = list()
for i in range(0, count_players):
    tmp_list = list()

    for j in range(0, 2):
        card = num_cards[j]
        num_cards.remove(card)
        tmp_list.append(card)
    players.append(tmp_list)

on_table = list()
for i in range(0, 5):
    on_table.append(num_cards[i])
    num_cards.remove(num_cards[i])

#Расшифровка карт игроков
for i in range(0, count_players):
    #сначала расшифровывают все игроки а потом хозяин карт
    for k in range(0, count_players):
        if i == k:
            continue
        for j in range(0, 2):
            players[i][j] =  module(players[i][j], d_i[k], p) 

    for j in range(0, 2):
        players[i][j] =  all_cards[module(players[i][j], d_i[i], p) - 2]

#Расшифровка карт на столе
for i in range(0, count_players):
    for k in range(0, 5):
        on_table[k] = module(on_table[k], d_i[i], p) 

print("Карты на столе:")        
for k in range(0, 5):
    on_table[k] = all_cards[on_table[k] - 2]
    print(on_table[k][1]+ on_table[k][0] + " ", end=" ")
print()

print("Карты игроков:")
for i in range(0, count_players):
    print("Игрок " + str(i+1) + ": ", end=" ")
    for j in range(0,2):
        print(players[i][j][1]+ players[i][j][0] + " ", end=" ")
    print()

