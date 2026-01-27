def is_power_of_three(n):
    if n < 1:
        return False
    
    for pow in range(0, n):
        if 3 ** pow == n:
            return True
        if 3 ** pow > n:
            return False 
        
def main():
  n = int(input("Enter a number: "))
  
  if is_power_of_three(n):
      print(f"{n} is a power of three.")
  else:
      print(f"{n} is not a power of three.")    

if __name__ == "__main__":
    main()