import time

for i in range(0,100):
	i+=1
	print("\r{0}".format('Descargando...' + str(i) + '%'), end='')
	time.sleep(1)