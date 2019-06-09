from random import randrange, getrandbits

def cifra(llave_publica, m):
	'''
	Función que se encarga de cifrar el mensaje m a partir de la llave pública.
	m : Mensaje a cifrar.
	llave_publica: Dulpa que contiene la llave pública que se usara para cifrar.
	'''
	n = llave_publica[0]
	e = llave_publica[1]

	m_num = [abecedario.index(letra) for letra in m if letra in abecedario]
	print("El valor numérico del mensaje es: ",end='')
	print(m_num)
	m_cif = []
	for num in m_num:
		# A cada valor del msg hacemos (numˆe) % n.
		m_cif.append(pow(num, e, n))

	return m_cif

def descifra(n, d, m_cif):
	'''
	Funciín para descifrar un mensaje a partir de la llave privada y n.
	'''
	m_desc = []
	for num in m_cif:
		# (numˆd) % n.
		m_desc.append(pow(num, d, n))

	return m_desc

def genera_llaves():
	'''
	Genera las llaves pública y privada. Es decir, (n,e) y d.
	'''
	p = genera_primo()
	q = genera_primo()
	while q == p:
		q = genera_primo()

	n = p*q
	phi = (p-1)*(q-1)

	e = 2
	while e < phi:
		if(mcd(e, phi) == 1):
			break
		else:
			e+=1

	public_key = (n, e)

	d = modulo_inverso(e, phi)

	return (public_key, d)

def mcd(x, y):
	'''
	Función para obtener el mcd entre x e y.
	'''	
	if x < 0:
		x *= -1

	if y < 0:
		y *= -1

	if x < y:
		x, y = y, x

	while x % y != 0:
		x = x % y
		if x < y:
			x, y = y, x
	return y

def modulo_inverso(a, m):
	'''
	Regresa (si existe) el inverso modular de a módulo m.
	'''
	for i in range(1,m):
		if (m*i + 1) % a == 0:
			return (m*i + 1) // a
	return None

def es_primo(n, k=128):
	""" Revisa si un número es un primo.
		n : número a testear.
		k : número de pruebas a realizar.
	"""
	# Si n no es par (descartando a 2).
	if n == 2 or n == 3:
		return True
	if n <= 1 or n % 2 == 0:
		return False
	# buscamos a r y a s.
	s = 0
	r = n - 1
	while r & 1 == 0:
		s += 1
		r //= 2
	# hacemos k tests.
	for _ in range(k):
		a = randrange(2, n - 1)
		x = pow(a, r, n)
		if x != 1 and x != n - 1:
			j = 1
			while j < s and x != n - 1:
				x = pow(x, 2, n)
				if x == 1:
					return False
				j += 1
			if x != n - 1:
				return False
	return True

def genera_candidato_primo(tam):
	""" Generamos un entero impar aleatoriamente.
		tam : tamaño en bits del número a generar.
	"""
	p = getrandbits(tam)
	p |= (1 << tam - 1) | 1
	return p

def genera_primo(tam=350):
	""" Genera un primo y lo devuelve.
		tam : tamaño en bits del primo a generar.
	"""
	p = 4
	# Generaremos tantos números hasta que alguno pase el test de primalidad.
	while not es_primo(p, 128):
		p = genera_candidato_primo(tam)
	return p


if __name__ == '__main__':

	'''
	Proyecto 2: RSA, Criptografía y Seguridad.
	Integrantes:
	- Jonathan Suárez López.
	- Alfonso Vargas Alba.
	'''

	abecedario = ["A", "B", "C", "D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

	llaves = genera_llaves()
	print("La llave pública es ",end='')
	print(llaves[0], end=' ')
	print("y la privada es " + str(llaves[1]) + "\n")

	msg = "ESTE ES UN MENSAJE DE PRUEBA PARA DETERMINAR SI FUNCIONA LA PROGRAMACION DE RSA JIJI."
	print("El mensaje a enviar es: " + msg + "\n")

	msg_cifrado_n = cifra(llaves[0], msg)
	print("El valor numérico del mensaje cifrado es: ", end='')
	print(msg_cifrado_n)
	print("")

	msg_descifrado_n = descifra(llaves[0][0], llaves[1], msg_cifrado_n)
	print("El valor numérico del mensaje descifrado es: ",end='')
	print(msg_descifrado_n)
	print("El mensaje descifrado es: ", end='')
	print([abecedario[indice] for indice in msg_descifrado_n])
	