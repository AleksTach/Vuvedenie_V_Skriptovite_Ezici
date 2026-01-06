from random import randint

class Player:

  def __init__(self, name, health, energy):
    self.name = name
    self.health = health
    self.energy = energy

  def attack(self):
    if self.energy > 3:
      damage = randint(1, 50)
      print(f"{self.name} attacks and deals {damage} damage!")
      if damage > 25:
        self.energy -= 10
      else:
        self.energy -= 5
      return damage
    else:
      print(f"{self.name} does not have enough energy to attack!")
      return None

  def take_damage(self, damage):

      if self.health < damage:
        self.health = 0 
        print(f"{self.name} has been defeated!")
      else:
        self.health -= damage
        print(f"{self.name} takes {damage} damage, remaining health: {self.health}")

  def heal(self):
      heal_amount = randint(10, 30)
      self.health += heal_amount
      if self.health > 100:
         self.health = 100
         self.energy += 15 
      else:
        if heal_amount > 20:
          self.energy += 5
        else:
           self.energy += 10
      print(f"{self.name} heals for {heal_amount}, new health: {self.health}, new energy: {self.energy}")

  def status(self):
      print(f"Player: {self.name}, Health: {self.health}, Energy: {self.energy}")

def main():
  attack_damage = 0
  player1 = Player("Goblin", 100, 30)
  player2 = Player("Zombi", 100, 10)

  player1.status()
  player2.status()

  print("\n===Battle Start===\n")
  while player1.health > 0 and player2.health > 0:
    attack_damage = player1.attack()
    if attack_damage is None:
      player1.heal()
    else:
      player2.take_damage(attack_damage)
      if player2.health <= 0:
        break

    attack_damage = player2.attack()
    if attack_damage is None:
      player2.heal()
    else:
      player1.take_damage(attack_damage)

  print("\n===Battle End===\n")
  player1.status()
  player2.status()

if __name__ == '__main__':
  main()
    
