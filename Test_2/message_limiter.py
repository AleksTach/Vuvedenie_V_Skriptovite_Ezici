class MessageLimiter:
  limit = 10

  def add_limit(self, amount):
    if amount <= 0:
      print("ERROR: Invalid input amount")
      return None
    
    self.limit += amount
    print(f"Message limit increased with: {amount}")

  
  def send_message(self):
    if self.limit < 0:
      print("ERROR: Message is critical low, can't send message")
      return None
    
    self.limit -= 1
    print(f"Message successfuly send --> decreasing message limit with 1")


  
  def block_messages(self, amount):
      if amount <= 0:
        print("ERROR: Invalid input amount")
        return None
      
      if self.limit >= amount:
        self.limit -= amount
        print(f"Decreasing message limit with: {amount}")
      else:
        self.limit = 0
        print("Blocking messages(...)")
        print("Increase message limit to send messages")
      

  
  def show_limit(self):
    if self.limit > 0:
      print(f"\nCurrent Message Limit: {self.limit}\n")
    else:
      print("Out of available messages\n")

def main():
  test = MessageLimiter()
  test.show_limit()
  test.add_limit(1)
  test.send_message()
  test.send_message()
  test.show_limit()
  test.block_messages(9)
  test.show_limit()
  test.add_limit(3)
  test.show_limit()

if __name__ == "__main__":
  main()