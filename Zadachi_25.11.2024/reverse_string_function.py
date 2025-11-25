def reverse_plain_func(str):
  strlen = len(str) # Syzdavam promenliva za duljinata na spisuka
  for ch in range(int(strlen) // 2): # Cikyl, koito obhozhda samo do sredata na spisuka, zashoto shte razmenqme po edin element s negoviq simetri4en
    sym = str[ch]  # Zapazvame stoinostta na tekushtiya element v promenliva sym
    str[ch] = str[int(strlen) - int(ch) - 1]  # Razmenqme tekushtiya element s negoviq simetri4en
    str[int(strlen) - int(ch) - 1] = sym  # Razmenqme simetri4niq element s zapazena stoinost 
  return str # Vrushtame oburnatiq spisuk

def reverse_rekurs_func(str):
  if len(str) == 0: # Proverqva dali spisuka e prazen
    return [] # Ako e prazen, vrushta prazen spisuk
  else:
    return [str[-1]] + reverse_rekurs_func(str[:-1]) # Vryshta posledniq element + rekursivno izvikvane na funkciqta s ostatyka na spisuka bez posledniq element


str = ['9', '8', '7', '6', '5', '4', '4', '3', '2', '1', '0']

reverse_plain = reverse_plain_func(str.copy())
print(f"The string is: {str}")
print(f"The plain reversed version of string is:  {reverse_plain}")

reverse_rekurs = reverse_rekurs_func(str.copy())
print(f"The recursed version of the string is: {reverse_rekurs}")