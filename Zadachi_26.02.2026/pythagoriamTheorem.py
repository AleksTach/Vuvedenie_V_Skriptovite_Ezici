import random
import math

def pyTh():
  side1 = random.randint(1, 20)
  side2 = random.randint(1, 20)
  hip = math.sqrt(math.pow(side1, 2) + math.pow(side2, 2))
  print(side1)
  print(side2)
  print(round(hip , 2))

if __name__ == '__main__':
  pyTh()