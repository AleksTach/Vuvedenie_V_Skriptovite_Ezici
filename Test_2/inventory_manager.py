class InventoryManager:
  inventory = {}
  

  def add_stock(self, quantity, amount):
    if amount <= 0:
      print("ERROR: Invalid input amount")
      return None
    
    if quantity is None:
      print("ERROR: Invalid input quantity")
      return None
      
    if quantity in self.inventory.keys():
      self.inventory[quantity]["available"] += amount
    else:
      self.inventory[quantity] = {"available": amount, "reserved": 0}

    print(f"Added stock --> {quantity}: {amount}")

  
  def remove_stock(self, quantity, amount):
    if amount <= 0:
      print("ERROR: Invalid input amount")
      return None
    
    if quantity is None:
      print("ERROR: Invalid input quantity")
      return None
    
    if quantity in self.inventory.keys():
      if self.inventory[quantity]["available"] >= amount:
        self.inventory[quantity]["available"] -= amount
        print(f"Removed stock --> {quantity}: {amount}")
      else:
        print(f"ERROR: You don't have enough avalaible stock from {self.inventory[quantity]}")
        print(f"Current {quantity} available stock: {self.inventory[quantity]["available"]}")
        return None
    else:
      print(f"ERROR: {quantity} not in inventory")
      return None
      
  
  def reserve_stock(self, quantity, amount):
    if amount <= 0:
      print("ERROR: Invalid input amount")
      return None
    
    if quantity is None:
      print("ERROR: Invalid input quantity")
      return None
    
    if quantity in self.inventory.keys():
      if self.inventory[quantity]["available"] >= amount:
        self.inventory[quantity]["available"] -= amount
        self.inventory[quantity]["reserved"] += amount

        print(f"Reserved stock --> {quantity}: {amount}")
      else:
        print(f"ERROR: You don't have enough avalaible stock from {self.inventory[quantity]}")
        print(f"Current {quantity} available stock: {self.inventory[quantity]["available"]}")
        return None
    else:
      print(f"ERROR: {quantity} not in inventory")
      return None
    
  
  def show_stock(self):
    print("\nCurrent inventory status:")
    for item in self.inventory.keys():
      print(f" {item} - Available: {self.inventory[item]['available']}, Reserved: {self.inventory[item]['reserved']}")

    print("\n")
    

def main():
  acc = InventoryManager()
  acc.add_stock("apple", 50)
  acc.add_stock("banan", 30)
  acc.show_stock()
  acc.remove_stock("apple", 10)
  acc.remove_stock("banan", 20)
  acc.show_stock()
  acc.reserve_stock("banan", 5)
  acc.reserve_stock("apple", 10)
  acc.show_stock()

if __name__ == "__main__":
  main()