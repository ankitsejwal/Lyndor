import os

print(os.getcwd())
f=open('z:/mcwade/bulk.txt')
lineas=f.read().splitlines()
for linea in lineas: 
	print(linea)