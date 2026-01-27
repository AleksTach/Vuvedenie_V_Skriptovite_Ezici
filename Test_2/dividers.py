def deviders(n):
  deviders_list = []
  for num in range(2, n):
    num = int(num)
    if n % num == 0 and num != n:
      deviders_list.append(num)
    
  return deviders_list

def main():
  n = int(input("Enter a number: "))
  print(f"The deviders of {n} are: {deviders(n)}")


if __name__ == "__main__":
    main()