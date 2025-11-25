def fibonachi_plain_function(num): 
  if num < 3: # Proverqva dali poziciqta e po-malka ot 3, zashtoto purvite dve pozicii sa 1
    return 1 # Vryshta 1 za purvite dve pozicii
  a = 1 # Purvi chisloto na fibonachi
  b = 1 # Vtoro chisloto na fibonachi
  for _ in range(3, num + 1): # Cikyl ot 3 do num, za da izchisli chisloto na fibonachi na poziciq num
    a, b = b, a + b # Presmqtame a i b
  return b # Vrushtame syotvetnoto chuislo na fibunachi


def fibonachi_recurs_function(num):
  if num < 3: # Proverqva dali poziciqta e po-malka ot 3, zashtoto purvite dve pozicii sa 1
    return 1 # Vryshta 1 za purvite dve pozicii
  else:
    return fibonachi_recurs_function(num - 1) + fibonachi_recurs_function(num - 2) # Rekursivno izvikvane na funkciqta za predishnite dve pozicii i subira na rezultatat
  
  
num = 9
fibonachi_plain = fibonachi_plain_function(num)
print(f"The plain Fibonacci number at position {num} is: {fibonachi_plain}")

fibonachi_recurs = fibonachi_recurs_function(num)
print(f"The recursive Fibonacci number at position {num} is: {fibonachi_recurs}")