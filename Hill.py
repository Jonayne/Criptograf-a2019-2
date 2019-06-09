'''
Proyecto - Cifrado Hill
Integrantes:
 - Suárez López Jonathan
 - Vargas Alba Alfonso
'''
import math

def cifra(txt_plano, clave):	
	'''
	Función cifra que a partir del texto plano y su palabra clave genera los diagramas del mensaje y su criptograma.	
	'''
	
	# Damos valores numéricos a la clave y el mensaje.
	clave_n = [diccionario.index(letra) for letra in clave if letra in diccionario]
	txt_plano_n = [diccionario.index(letra) for letra in txt_plano if letra in diccionario]
	
	tam_matriz = math.sqrt(len(clave_n))

	# Revisamos si es un entero.
	if tam_matriz % 1 != 0:
		print("¡Clave no válida! No se puede generar matriz de nxn.")
		exit(-1)

	# Damos la llave y la determinante de su matriz.
	llave = genera_llave(clave_n, tam_matriz)
	determinante_matriz = dame_determinante(llave)

	if not(dame_inversa(determinante_matriz)):
		print("¡La matriz generada por la llave no es invertible! Por lo tanto, no se puede cifrar.")
		exit(-1)

	diagramas = genera_diagramas(txt_plano_n, tam_matriz)
	print("Matriz de cifrado: ", end='')
	print(llave)
	criptograma = genera_criptogramas(diagramas, llave)

	return [criptograma, llave]

def mcd(a, b):
	'''	
	Función mcd que da el maximo común divisor de números a, b.	
	'''
	resto = 0
	while(b > 0):
		resto = b
		b = a % b
		a = resto
	return a

def dame_inversa(det):
	'''
	Función dame_inversa que asegura que la matriz asociada a la determinante sea invertible y da el inverso de su determinante.
	'''
	if(mcd(det, 27) == 1):
		inv = 0
		for i in range(27):
			inv_tmp = (det*i) % 27
			if inv_tmp == 1:
				inv = i
	else:
		return False

	return inv

def genera_criptogramas(diagramas, clave):
	'''
	Función que genera los criptogramas a partir de la palabra clave y los diagramas del mensaje.
	'''
	criptogramas = []
	for diagrama in diagramas:
		criptogramas.append(multiplica_matrices(clave, diagrama))

	return criptogramas

def multiplica_matrices(a, b):
	'''
	Función para multiplicar matrices con los valores correspondientes al modulo 27.
	'''
	criptograma = []
	for i in range(len(a)):
		criptograma.append([0]*len(b[0]))

	for i in range(len(a)):
		for j in range(len(b[0])):
			for k in range(len(b)):
				criptograma[i][j] += a[i][k] * b[k][j]
	# Aplicamos el módulo correspondiente.
	for i in range(len(a)):
		for j in range(len(b[0])):
			criptograma[i][j] = criptograma[i][j] % 27

	return criptograma

def genera_llave(clave_n, tam):
	'''
	Función para generar la  matriz de la clave. 
	'''
	llave = []
	contador = 1
	conj = []
	
	for num in clave_n:
		conj.append(num)
		if contador % tam == 0:
			llave.append(conj.copy())
			conj = []
		contador+=1
	return llave

def genera_diagramas(txt_n, tam):
	'''
	Función para generar los diagramas del texto plano.
	'''
	diagramas = []
	contador = 1
	diag = []
	
	for num in txt_n:
		diag.append([num])
		if contador % tam == 0:
			diagramas.append(diag.copy())
			diag = []
		contador+=1
	return diagramas

def traduce_a_palabras(criptograma):
	'''
	Función para pasar los índices a letras del criptograma a partir del diccionario.
	'''
	texto = ""
	for lista in criptograma:
		for num in lista:
			texto+=diccionario[num[0]]
	return texto

def matriz_traspuesta(m):
	'''
	Función que pasa una matriz a su traspuesta (de filas pasa a columnas).
	'''	
	return [list(i) for i in zip(*m)]

def dame_menor_matriz(m,i,j):
	'''
	Función que da la matriz de menores valores.
	'''
	return [renglon[:j] + renglon[j+1:] for renglon in (m[:i]+m[i+1:])]

def dame_determinante(m):
	'''
	Función que da la determinante de una matriz.
	'''
	#Caso de 2x2.
	if len(m) == 2:
		return m[0][0]*m[1][1]-m[0][1]*m[1][0]

	determinante = 0
	for c in range(len(m)):
		determinante += ((-1)**c)*m[0][c]*dame_determinante(dame_menor_matriz(m,0,c))
	return determinante

def dame_matriz_inversa(m):
	'''
	Función que da la matriz inversa.
	'''
	# (Ya que buscamos una matriz inversa modular, es necesario sacar la inversa del determinante)
	# y en vez de dividir sobre éste, multiplicaremos.
	determinante = dame_inversa(dame_determinante(m))

	#Caso de 2x2.
	if len(m) == 2:
		return [[m[1][1]*determinante, -1*m[0][1]*determinante],
				[-1*m[1][0]*determinante, m[0][0]*determinante]]

	#Buscamos la matriz de cofactores.
	cofactors = []
	for r in range(len(m)):
		renglon_cofct = []
		for c in range(len(m)):
			menor = dame_menor_matriz(m,r,c)
			renglon_cofct.append(((-1)**(r+c)) * dame_determinante(menor))
		cofactors.append(renglon_cofct)
	# Le sacamos la traspuesta (i.e, la matriz de adjuntos.)
	cofactors = matriz_traspuesta(cofactors)
	for r in range(len(cofactors)):
		for c in range(len(cofactors)):
			cofactors[r][c] = (cofactors[r][c]*determinante) % 27
	return cofactors

def descrifra(criptograma, llave):
	'''
	Función que descifra un mensaje dado el criptograma y la llave de cifrado.
	'''
	descrifrada = []

	llave_inversa = dame_matriz_inversa(llave)
	print("Matriz de descifrado: ", end='')
	print(llave_inversa)
	for ci in criptograma:
		descrifrada.append(multiplica_matrices(llave_inversa, ci))
	return descrifrada

if __name__ == '__main__':

	print("Proyecto - Cifrado Hill \nIntegrantes: \nSuárez López Jonathan \nVargas Alba Alfonso \n\n")

	diccionario = ["A", "B", "C", "D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

	txt_a_cifrar = "SI TUVIERA QUE ELEGIR ENTRE UN MAL MAYOR O UN MAL MENOR, PREFERIRIA NO ELEGIR NINGUNO."
	print("TEXTO ORIGINAL: \n" + txt_a_cifrar)

	txt_conocido = "ENTRE UN MA"
	print("Texto conocido: \n" + txt_conocido)
	criptograma = cifra(txt_a_cifrar, txt_conocido)


	txt_cifrado = traduce_a_palabras(criptograma[0])
	print("TEXTO CIFRADO: \n" + txt_cifrado)

	txt_descrifrado_n = descrifra(criptograma[0], criptograma[1])
	txt_descrifrado = traduce_a_palabras(txt_descrifrado_n)
	print("TEXTO DESCRIFRADO: \n" + txt_descrifrado)
	
