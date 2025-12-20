class Library_Account:

  def __init__(self, username):
    self.username = username
    self.books = []
    self.inventory = 0

  def borrow_book(self, book):
    if book in self.books:
      return print(f"You already have {book} in your inventory.")
    elif self.inventory <= 3:
      self.inventory += 1
      self.books.append(book)
      return print(f"Borrowed {book} from the library.")
    else:
      return print("You have exceeded the limit of borrowed books from the library.")
    
  def return_book(self, book):
    if book not in self.books:
      return print(f"You can't return {book}, because you haven't taken it yet.")
    else:
      self.inventory -= 1
      self.books.remove(book)
      return print(f"Returned {book} to the library.")
    
  def list_books(self):
    print("======================================")
    print("            LIBRARY ACCOUNT           ")
    print("======================================")
    print(f"Username: {self.username}            ")
    print("--------------------------------------")
    print("Borrowed books form the library       ")
    for num in range(len(self.books)):
      print(f"{num+1}) {self.books[num]}")
    print("======================================")

def main():
  Account = Library_Account("Sa6ko")
  Account.borrow_book("Sveti Pesho")
  Account.borrow_book("Patlaci i Trynaci")
  Account.list_books()
  Account.return_book("Sveti Pesho")
  Account.list_books()

if __name__ == "__main__":
  main()