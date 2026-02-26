import time
import random

def rocketShip():
  countdown = random.randint(5, 20)
  start = input("Press Enter to start the countdown: ")
  if start == "":
    while(countdown > 0):
      print(countdown)
      time.sleep(1)
      countdown -= 1
    print("LAUNCHING!")

if __name__ == "__main__":
  rocketShip()