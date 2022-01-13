from tkinter import * 
import time

# Encrypting using arithmetic expression (subtracting the current alphabet POSITION from the last alphabet ASCII VALUE)
def encrypt():               
	pt = e1.get()
	ct = []
	for char in pt:
		if char == " ":							# for space character
			ct.append(" ")
		if ord(char)>=97:					# for small alphabets (a,b,c,....)
			ct.append(chr(122 - (ord(char) - 97)))
		elif ord(char)>=65: 				# for capital alphabets (A,B,C....)
			ct.append(chr(90 - (ord(char) - 65)))	
	ct = "".join(ct)	
	e2.delete(0, END)
	time.sleep(0.5)
	e2.insert(0, ct)
  
# Decrypting using arithmetic expression (subtracting the current alphabet POSITION from the last alphabet ASCII VALUE)
def decrypt():            
	ct = e2.get()
	pt = []
	for char in ct:
		if char == " ":							# for space character
			pt.append(" ")
		if ord(char)>=97:						# for small alphabets (a,b,c,....)
			pt.append(chr(122 - (ord(char) - 97)))
		elif ord(char)>=65:						# for capital alphabets (A,B,C....)
			pt.append(chr(90 - (ord(char) - 65)))
	pt = "".join(pt)	
	e1.delete(0, END)
	time.sleep(0.5)
	e1.insert(0, pt)
      
# Driver code
root = Tk()
root.title("Network Security PA0")
root.configure(background='#CBFFCB')
root.geometry("700x300")

l0 = Label(root, text ="Network Security (PA-0)",pady=10, font=('Arial', 13), background='#CBFFCB')               
l0.grid(row = 0, column = 2)
l1 = Label(root, text ="PLAINTEXT :",pady=10, background='#CBFFCB')               
l1.grid(row = 1, column = 1)
l2 = Label(root, text ="CIPHERTEXT :",pady=10, background='#CBFFCB')
l2.grid(row = 1, column = 3)

e1 = Entry(root)
e1.grid(row = 2, column = 1, padx=5,pady=10, ipadx = 50,ipady=50)
e2 = Entry(root)
e2.grid(row = 2, column = 3, padx=5,pady=10, ipadx = 50,ipady=50)

b1 = Button(root, text = "Encipher", bg ="pink", fg ="blue", command = encrypt)
b1.grid(row = 3, column = 1)
b2 = Button(root, text = "Decipher", bg ="pink", fg ="blue", command = decrypt)
b2.grid(row = 3, column = 3)
  
root.mainloop()