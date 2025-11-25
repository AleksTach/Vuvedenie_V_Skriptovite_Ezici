def sum_plain_func(list):
  sum = 0  # Syzdavam sumata
  for num in range(len(list)): #Cikula obhozhda spisuka s chisla
    sum += list[num] # Vseki put kum sumata se pribavq syotvetniq element ot spisuka
  return sum #Funkciqta vrushta sumata na elementite v spisuka

def sum_rekurs_func(list):
  if len(list) == 0: # Proverq dali spisuka e prazen
    return 0 # Ako e prazen, vrushta 0
  else:
    return list[0] + sum_rekurs_func(list[1:]) # Vryshta purviq element + rekursivno izvikvane na funkciqta s ostatyka na spisuka


list = [1, 2, 3, 4, 5, 6]
sum_plain = sum_plain_func(list)
print(f"The plain sum of the numbers in the list is: {sum_plain}")

sum_rekurs = sum_rekurs_func(list)
print(f"The rekursive sum of the numbers in the list is: {sum_rekurs}")
