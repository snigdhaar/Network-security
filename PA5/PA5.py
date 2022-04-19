from Crypto.Util.number import inverse
import sympy
import random

def encrypt(m,public_key_list):
  p = public_key_list[0]
  g = public_key_list[1]
  h = public_key_list[2]
  
  k = random.randint( 1, p - 1 )  # Choose a random integer k
  c1 = pow(g,k,p)
  K = pow(h, k, p)    # Compute one-time key K
  c2 = (K * m ) % p
  return c1,c2

def decrypt(c1,c2,private_key_list):
  p = private_key_list[0]
  x = private_key_list[2]
  
  K = pow(c1,x,p)  # recover one-time key K
  dm = (c2 * inverse(K,p)) % p
  return dm

def find_primitive_root( p ):
		if p == 2:
				return 1
		p1 = 2
		p2 = (p-1) // p1
		while(True):
				g = random.randint( 2, p-1 )
				if not (pow( g, (p-1)//p1, p ) == 1):
						if not pow( g, (p-1)//p2, p ) == 1:
								return g

def generate_keys(m):
		p = sympy.randprime(m*2, m*4)
		g = find_primitive_root(p)
		g = pow( g, 2, p ) #computes base^exp mod modulus
		x = random.randint( 1, (p - 1) // 2 )
		h = pow( g, x, p ) #computes base^exp mod modulus

		publicKey = [p, g, h]
		privateKey = [p, g, x] # here p, g are also included in the private key since they are globally known

		return {'privatekey': privateKey, 'publickey': publicKey}


input_message = input("Enter the message Bob wants to send to Alice: ")
inputbytes = str.encode(input_message)
m = int(inputbytes.hex(), 16)
print("MESSAGE as an int (M) : {}".format(m))
print("______________________________________________________________")

print("\nKey generation by Alice:\n")
key_dict = generate_keys(m)
print("Public key of Alice [q, alpha, Ya]: (Known to both Bob and Alice)")
print("Prime number (q)      : {}".format(key_dict['publickey'][0]))
print("Primitive root of P (alpha)         : {}".format(key_dict['publickey'][1]))
print("Shared secret (Ya)     : {}".format(key_dict['publickey'][2]))

print("\nPrivate key of Alice : (known only to Alice)")
print("Private key of Alice (Xa) : {}".format(key_dict['privatekey'][2]))
print("______________________________________________________________")

print("\nEncryption by Bob with Alice’s Public Key: ")
c1, c2 = encrypt(m,key_dict['publickey'])
print("Encrypted Message (C1): {}".format(c1))
print("Encrypted Message (C2): {}".format(c2))
print("______________________________________________________________")

print("\nDecryption by Alice with Alice’s Private Key: ")
dm = decrypt(c1,c2, key_dict['privatekey'])
print("Decrypted Integer     : {}".format(dm))
x = format(dm, 'x')
print("Decrypted Hex         : {}".format(x))
message = bytes.fromhex(x).decode("utf-8")
print("Decrypted Message     : {}".format(message))
print("______________________________________________________________")