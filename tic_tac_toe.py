import copy
import os

class Nodo:
	
	def __init__(self,tablero,padre):
		self.tablero = tablero
		self.padre = padre
		self.hijos=[]
		if self.padre == "":
			self.costo = 0	
		else:
			self.costo = self.calcularcosto()		
			
	def agregarhijo(self,tablero):
		self.hijos.append(Nodo(tablero,self))
	
	def tiro(self):
		coords = [item for item in range(len(self.tablero)) if self.tablero[item] == " "] #Coordenadas de los posibles lugares a tirar
		cola = []
		ct = 0 #Cuenta los hijos agregados
		for coord in coords:
			t = copy.copy(self.tablero) 	#Obtiene t el valor del tablero actual 			
			t[coord] = 'O'					#Tira 
			self.agregarhijo(t)				#Agrega el nuevo tablero como hijo	
			cola.append(self.hijos[ct])   
			ct = ct + 1
		
		cola = (sorted(cola, key=lambda Nodo: Nodo.costo, reverse =True))
		return cola[0]	
	
	def calcularcosto(self):
		costo= 0
		lineas = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [2,4,6] ] #Lineas con las posiciones de casillas
		posibles = [ [0,3,6] , [0,4] , [0,5,7] , [3,1] , [4,1,6,7] , [5,1] , [3,2,7] , [4,2] , [5,2,6] ] #lineas de cada posicion 
						
		for coord in range(9):			#Ver en donde difieren
			if self.tablero[coord] != self.padre.tablero[coord]:
				break
		
		for i in range(len(posibles[coord])): #Cuantas lineas sean posibles en la posicion actual 
			lineacoord = lineas[posibles[coord][i]] #Me da el vector de 3x1 con la coordenada de la linea a evaluar
			linea=[]
			for x in lineacoord:
				linea.append(self.padre.tablero[x]) #Llena al vector linea con la linea real del padre
			if ('X' in linea)==False: #Si hay ya un tiro del enemigo
				costo = costo + 1 		#Costo por linea posible 
				ct = 0 #cuenta nuestros tiros
				for y in linea: 
					if y=='O':
						ct = ct+1
				if ct==1:
					costo = costo + 1   #Costo por tiro propio en la linea
				if ct==2:
					costo = costo + 100 #Se tiene que tirar ahi para ganar
			if ('X' in linea)==True:  #Si hay ya un tiro enemigo en la linea
				if ('O' in linea) == False :
					costo = costo + 2     	#Costo por bloquear al enemigo en esa linea sin que haya un tiro nuestro en la misma
				ct1=0 #cuenta los tiros del enemigo en la linea
				for y in linea:		
					if y=='X':			#Para determinar si es necesario tirar ahi porque el enemigo ya va a ganar
						ct1  = ct1+1
				if ct1==2:
					costo = costo + 50 #Se tiene que tirar ahi para bloquear al enemigo
			
		tablerot=copy.copy(self.tablero)
		if tiroprox(tablerot)==True: #Calcula los dos proximos tiros, si gracias al tiro actual el enemigo nos hace un "jaque" en su prox movimiento, entonces esta posicion tiene costo 0
			costo=0								
		return costo	
	
def tiroprox(tablerot):
	coords = [item for item in range(len(tablerot)) if tablerot[item] == " "] #Coordenadas de los posibles lugares a tirar
	lineas = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [2,4,6] ]
 	hijos=[]
 	costo=[]
 							
	for coord in coords: #Calcula el mejor tiro que el enemigo puede realizar 
		t=copy.copy(tablerot)
		t[coord]='X'
		hijos.append(t)
		costo.append(calcularcosto(t,tablerot))
	
	if len(costo)>0: #Solo en realidad hubieran posibilidades donde tirar
		
		a=max(costo)
		b=costo.index(a)
	
		ct=0
		t=copy.copy(hijos[b])
	
		for linea in lineas: #Checa si el enemigo esta a punto de ganar, asi calculamos que si tiene dos lineas con esa oportunidad, ya nos hizo un "jaque"
			if (t[linea[0]] == "X" and t[linea[1]]=="X" and t[linea[2]]==" "):
				ct=ct+1
			if (t[linea[0]] == "X" and t[linea[1]]==" " and t[linea[2]]=="X"):
				ct=ct+1
			if (t[linea[0]] == " " and t[linea[1]]=="X" and t[linea[2]]=="X"):
				ct=ct+1
	
		if ct>=2:
			return True
	
	return False	
						
def calcularcosto(tablerot,tablerot2): #Calcula el costo para realizar el mejor tiro del enemigo en la suposicion futura
	costo= 0
	lineas = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [2,4,6] ] #Lineas con las posiciones de casillas
	posibles = [ [0,3,6] , [0,4] , [0,5,7] , [3,1] , [4,1,6,7] , [5,1] , [3,2,7] , [4,2] , [5,2,6] ] #lineas de cada posicion 
						
	for coord in range(9):			#Ver en donde difieren
		if tablerot[coord] != tablerot2[coord]:
			break
	
	for i in range(len(posibles[coord])): #Cuantas lineas sean posibles en la posicion actual 
		lineacoord = lineas[ posibles[coord][i] ] #Me da el vector de 3x1 con la coordenada de la linea a evaluar
		linea=[]
		for x in lineacoord:
			linea.append(tablerot2[x]) #Llena al vector linea con la linea real del padre
		if ('O' in linea)==False: #Si hay ya un tiro del enemigo
			costo = costo + 1 		#Costo por linea posible 
			ct = 0 #cuenta nuestros tiros
			for y in linea: 
				if y=='X':
					ct = ct+1
			if ct==1:
				costo = costo + 1   #Costo por tiro propio en la linea
			if ct==2:
				costo = costo + 100 #Se tiene que tirar ahi para ganar
		if ('O' in linea)==True:  #Si hay ya un tiro enemigo en la linea
			if ('X' in linea) == False :
				costo = costo + 2     	#Costo por bloquear al enemigo en esa linea sin que haya un tiro nuestro en la misma
			ct1=0 #cuenta los tiros del enemigo en la linea
			for y in linea:
				if y=='O':
					ct1  = ct1+1
			if ct1==2:
				costo = costo + 50 #Se tiene que tirar ahi para bloquear al enemigo				
	
	return costo	
					
def imprimirtablero(tablero):
	print tablero[0:3]
	print ""
	print tablero[3:6]
	print ""
	print tablero[6:9]
	print ""

def ganador(tablero):
	lineas = [ [0,1,2] , [3,4,5] , [6,7,8] , [0,3,6] , [1,4,7] , [2,5,8] , [0,4,8] , [2,4,6] ] #Lineas con las posiciones de casillas
	
	for linea in lineas:
			if tablero[linea[0]] == "O" and tablero[linea[1]] ==  "O" and tablero[linea[2]] == "O":
				return 1
			if tablero[linea[0]] == "X" and tablero[linea[1]] ==  "X" and tablero[linea[2]] == "X":
				return 2
	return 0
	
def imprimirganador(tablero):
	if ganador(tablero)==2:
		print "Gana Humano"
	if ganador(tablero)==1:
		print "Gana CPU"	
	if ganador(tablero)==0:
		print "Empate"
			
def main():
	while True:
		tablero = [" "," "," "," "," "," "," "," "," "] #Empieza CPU
		ct=0
		jugadas = []
		while True: #Mientras haya casillas desocupadas y nadie haya ganado
			if (" " in tablero)==True:
				os.system("clear")
				jugadas.append(Nodo(tablero,""))
				tablero = copy.copy(jugadas[ct].tiro().tablero)
				ct = ct+1
				imprimirtablero(tablero)
			else:
				break	
			print ""
			if ganador(tablero)!=0: #Si alguien ya gano
				break
			if (" " in tablero)==True:
				while True:
					pos = int(raw_input("Posicion a tirar: "))
					if tablero[pos-1]==" ":
						break
					else:
						print "Casilla ya ocupada, intentar de nuevo"	
				tablero[pos-1] = 'X'
			else:
				break
			print ""
			if ganador(tablero)!=0: #Si alguien ya gano
				break
		imprimirganador(tablero)
		raw_input("Termino el juego")	
		os.system("clear") #Linux/OSX
		#os.system("cls")   #Windows		
	
		tablero = [" "," "," "," "," "," "," "," "," "] #Empieza humano
		ct = 0
		jugadas = []
		imprimirtablero(tablero)
		print ""
		while True: #Mientas haya casillas desocupadas
			if (" " in tablero)==True:
				while True:
					pos = int(raw_input("Posicion a tirar: "))
					if tablero[pos-1]==" ":
						break
					else:
						print "Casilla ya ocupada, intentar de nuevo"
				tablero[pos-1] = 'X'	
			else:
				break
			if ganador(tablero)!=0:
				break
			if (" " in tablero)==True:
				os.system("clear")
				jugadas.append(Nodo(tablero,""))
				tablero = copy.copy(jugadas[ct].tiro().tablero)
				ct = ct+1
				imprimirtablero(tablero)
			else:
				break
			if ganador(tablero)!=0:
				break	
		os.system("clear")
		imprimirtablero(tablero)
		imprimirganador(tablero)
		raw_input("Termino el juego")
		os.system("clear")			
main()
