import random
import statistics
import numpy as np
import matplotlib.pyplot as plt
from Crypto.Cipher import DES

sysrandom = random.SystemRandom()

randArray = []  #Initialize a random list to get the 5 flipped plaintexts/keys 

#function to get the hamming distance between two bit strings
def getHammingDistance(bits0,bits1):
    return bin(bits0 ^ bits1).count("1")

#function to flip the bits on a bit string with a given hamming distance
def bit_flip_with_n_hamDist(bits0, n):
  nos = random.sample(range(0, 64), n)
  list1 = ["1" if i in nos else "0" for i in range(64) ]
  new = "".join(list1)
  bits1 = bits0 ^ int(new,2)
  return bits1

def diff_plaintext():
  #constant key
  key = '01234567' 
  des = DES.new(key, DES.MODE_ECB)  
  #Getting the original random 64 bit plaintext
  org_pt = sysrandom.getrandbits(64)
  org_ct = des.encrypt(org_pt.to_bytes(8,'little'))
  round_change_bits = {0:0, 1:1, 2:5, 3:10, 4:25, 5:50}
  data= []

  for round in round_change_bits:
    randArray = []
    #Generating 5 plaintexts which differ only by value of dictionary bits for each round
    for i in range(5):
        randArray.append(bit_flip_with_n_hamDist(org_pt,round_change_bits[round]))
    
    hamming_d = []
    for i in randArray:
      ciphertext2 = des.encrypt(i.to_bytes(8,'little'))
      d = getHammingDistance(int.from_bytes(org_ct,'little'),int.from_bytes(ciphertext2,'little'))    
      hamming_d.append(d)

    data_1 = np.array(hamming_d)
    data.append(data_1)

  # Creating plot
  fig = plt.figure(figsize =(10, 8))
  plt.title("Different Plaintexts, Constant Key")
  plt.ylabel('No of bits that differ in corresponding ciphertexts')
  plt.xlabel('No of bits that differ in the 5 Plaintexts')
  bp = plt.boxplot(data)
  plt.xticks(range(1,7), round_change_bits.values())
  
  # show plot
  plt.show()

def diff_key(): 
  #constant plaintext  
  pt = '12345678'
  #Getting the original random 64 bit key
  org_key = sysrandom.getrandbits(64)
  org_des = DES.new(org_key.to_bytes(8,'little'), DES.MODE_ECB)    
  org_ct = org_des.encrypt(pt)
  round_change_bits = {0:0, 1:1, 2:5, 3:10, 4:25, 5:50}
  data= []

  for round in round_change_bits:
    randArray = []
    #Generating 5 keys which differ only value of dictionary bits for each round
    for i in range(5):
        randArray.append(bit_flip_with_n_hamDist(org_key,round_change_bits[round]))
    
    hamming_d = []
    for i in randArray:
      des2 = DES.new(i.to_bytes(8,'little'), DES.MODE_ECB)
      ciphertext2 = des2.encrypt(pt)
      d = getHammingDistance(int.from_bytes(org_ct,'little'),int.from_bytes(ciphertext2,'little'))    
      hamming_d.append(d)

    data_1 = np.array(hamming_d)
    data.append(data_1)

  # Creating plot
  fig = plt.figure(figsize =(10, 8))
  plt.title("Different Keys, Constant Plaintext")
  plt.ylabel('No of bits that differ in the corresponding ciphertexts')
  plt.xlabel('No of bits that differ in the 5 keys')
  bp = plt.boxplot(data)
  plt.xticks(range(1,7), round_change_bits.values())
  
  # show plot
  plt.show()

#Driver code
diff_plaintext()
diff_key()
