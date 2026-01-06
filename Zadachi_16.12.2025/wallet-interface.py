class Wallet:

  def __init__(self, wallet_holder, balance, currency):
    self.wallet_holder = wallet_holder
    self.balance = balance
    self.currency = currency

  @staticmethod
  def convert_currency(amount, from_currency, to_currency):
      EXCHANGE_RATES = {
        'EUR': 1.00000,
        'USD': 1.17000,
        'BGN': 1.95583
      }
      if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return None

      eur_amount = amount / EXCHANGE_RATES[from_currency]
      final_amount = eur_amount * EXCHANGE_RATES[to_currency]
      return round(final_amount, 2)
    
  def deposit(self, amount, currency):
    if currency == self.currency:
      exchange_amount = amount
    else:
      exchange_amount = Wallet.convert_currency(amount, currency, self.currency)

    if exchange_amount > 0:
      self.balance += exchange_amount
      return print(f"Deposited: {amount} {currency} -> New Balance: {self.balance} {self.currency}")
    else:
      return print("Invalid deposit amount")
    
  def withdraw(self, amount, currency):
    if currency == self.currency:
      exchange_amount = amount
    else:
      exchange_amount = Wallet.convert_currency(amount, currency, self.currency)

    if self.balance >= exchange_amount:
      self.balance -= exchange_amount
      return print(f"Withdrawed: {amount} {currency} -> New Balance: {self.balance} {self.currency}")
    elif self.balance < exchange_amount:
      return print("Not enough funds in the wallet")
    else:
      return print("Invalid withdraw amount")
    
  def show_current_balance(self):
    print("======================================")
    print("           WALLET INTERFACE           ")
    print("======================================")
    print(f"Wallet holder: {self.wallet_holder}  ")
    print("--------------------------------------")
    print(f"Current Wallet Balance: {self.balance} {self.currency}")
    print("======================================")


def main():
  Account1 = Wallet("Aleksandar", 100000, "BGN")
  Account2 = Wallet("Ivan", 200, "USD")

  Account1.deposit(100, "EUR")
  Account1.withdraw(195.58, "BGN")
  Account1.show_current_balance()

if __name__ == "__main__":
  main()