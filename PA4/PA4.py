from Crypto.Cipher import DES3
from Crypto.Util.strxor import strxor
from time import time
import struct
from math import sqrt

def lcg(X_0,length_lcg):
  a = 101427
  c = 321
  m = 2 ** 16
  lcg_rand_no_list = [X_0]
  X_prev = X_0
  for i in range(length_lcg):
    X = (a * X_prev + c) % m
    lcg_rand_no_list.append(X)
    X_prev = X
  return lcg_rand_no_list

def ansi_x9_17(V, key, limit):
  des3 = DES3.new(key, DES3.MODE_ECB)
  rand_no_list =[]
  for i in range(limit):
    EDT = des3.encrypt(hex(int(time()*10**6))[-8:].encode("utf8"))
    R = des3.encrypt(strxor(V, EDT))
    V = des3.encrypt(strxor(R, EDT))
    rand_no_list.append(int(struct.unpack('L', R)[0])) #64 bit output
  return rand_no_list

def chi_squared_test(observed,length,m):
  new_observed = [i/m for i in observed] # normalize random nos to get the random nos generated between [0,1]
  expected = length/m
  chi_sq_value = 0
  for observed_val in new_observed:
    chi_sq_value += ( pow((expected - observed_val), 2)/expected )
  result = "Failed to reject null hypothesis => PRNG is Random"
  alpha = 0.05
  crit_value = 10233.7489
  if chi_sq_value > crit_value:
      result = "Null hypothesis rejected => PRNG is not random enough"

  print("Alpha = ",alpha)
  print("Chi Square value = ",chi_sq_value)
  print("Critical Value = ",crit_value)
  print("Result = " ,result)

def kolmogorov_smirnov_test(random_no_list,n,m):
  new_random_no_list = [i/m for i in random_no_list] # normalize random nos to get the random nos generated between [0,1]
  new_random_no_list.sort()
  D_plus =[]
  D_minus =[]

  # Calculate max(i/N-Ri)
  for i in range(1, n + 1):
    x = i / n - new_random_no_list[i-1]
    D_plus.append(x)
  
  # Calculate max(Ri-((i-1)/N))
  for i in range(1, n + 1):
    y =(i-1)/n
    y =new_random_no_list[i-1]-y
    D_minus.append(y)
  
  # Calculate max(D+, D-)
  D = max(sqrt(n) * max(D_plus), sqrt(n) * max(D_minus))
  #significance test
  alpha_level = 0.05
  critical_value = 1.36/sqrt(n)
  result = "Failed to reject null hypothesis => PRNG is Random"
  if D > critical_value:
        result = "Null hypothesis rejected => PRNG is not random enough"
  print("Alpha = ",alpha_level)
  print("D_statistic = " ,D)
  print("Critical value = ",critical_value)
  print("Result = ",result)



# Driver Code

# Getting random nos from LCG PRNG
X_0 = 1
length_lcg = 10000
m = 2 ** 16
lcg_rand_no_list= lcg(X_0, length_lcg)
print("Random numbers genereated from LCG :\n",lcg_rand_no_list)

# Getting random nos from ANSI PRNG
seed = 109827492
key = 598982742938470
length_ansi = 10000
seed = hex(seed)[2:18].zfill(8).encode("utf8")
key = hex(key)[2:18].zfill(16)
ansi_rand_no_list = ansi_x9_17(seed, key, length_ansi)
chi_ansi_rand_no_list = [int((i/2**64)*m) for i in ansi_rand_no_list]
print("Random numbers genereated from ANSI :\n",ansi_rand_no_list)

# Running the Chi Squared test
print("\n\nRunning the Chi Squared test on:" )
print("\n1. LCG:")
chi_squared_test(lcg_rand_no_list,length_lcg,m-1)
print("\n2. ANSI: ")
chi_sq_value = chi_squared_test(chi_ansi_rand_no_list,length_ansi,2**64)

# Running the Kolmogorov Smirnov test
print("\n\nRunning the Kolmogorov Smirnov test on:" )
print("\n1. LCG: ")
kolmogorov_smirnov_test(lcg_rand_no_list,length_lcg,m)
print('\n2. ANSI: ')
kolmogorov_smirnov_test(ansi_rand_no_list,length_ansi,2**64)