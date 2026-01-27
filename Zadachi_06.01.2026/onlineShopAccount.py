import json

class OnlineShopAccount:
  username = ""
  balance = 0
  items = {}

  def __init__(self, username, balance):
    self.username = username
    self.balance = balance
    self.items = {}

  def add_funds(self, amount):
    if amount <= 0:
      return print("ERROR: Invalid input amount!")
    self.balance += amount
    print(f"Deposited: {amount} --> New Balance: {self.balance}")

  def buy_item(self, item_name, item_price):
    if item_name is None or not isinstance(item_name, str):
      print("ERROR: Invalid item name!")
      return None
    if item_price <= 0:
      print("ERROR: Invalid item name")
      return None

    if self.balance >= item_price:
      self.balance -= item_price
      if item_name not in self.items.keys():
        self.items[item_name] = item_price
      else:
        print(f"Already existing item in {self.username}'s inventory(...)")
        return None
      
      print(f"New Item bought --> {item_name}: {item_price}")
      print(f"Current Balance: {self.balance}")
    else:
      print("ERROR: You don't have enough balance to afford this item!")
      print(f"Current Balance: {self.balance}")
      return None
    
  def refund(self, item_name):
    if item_name is None or not isinstance(item_name, str):
      print("ERROR: Invalid item name!")
      return None
     
    if item_name not in self.items.keys():
       print(f"ERROR: {item_name} is not in {self.username}'s inventory")
       return None
     
    self.balance += self.items[item_name]
    print(f"Item refunded --> {item_name}: {self.items[item_name]}")
    print(f"Current Balance: {self.balance}")
    self.items.pop(item_name)
  
  def show_user_details(self, file_path):
    user_details = {
      "username": self.username,
      "balance": self.balance,
      "items": self.items
    }

    with open(file_path, "w", encoding="utf-8") as f:
      json.dump(user_details, f, ensure_ascii=False, indent=4)



def main():
  acc = OnlineShopAccount("test", 100)
  acc.buy_item("Item_1", 10)
  acc.buy_item("Item_2", 20)
  acc.buy_item("Item_3", 60)
  acc.buy_item("Test", 20)
  acc.refund("Item_1")
  acc.buy_item("Test", 20)
  acc.show_user_details("user_details.json")


if __name__ == "__main__":
 main()
