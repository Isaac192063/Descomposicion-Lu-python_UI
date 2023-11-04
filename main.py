import tkinter.font as font
from tkinter import  Tk, Button, Entry, Label, ttk, PhotoImage, messagebox
from tkinter import  Scrollbar,Frame, Canvas
from tkinter import  *
from itertools import permutations
import numpy as np

# mostrar el paso a paso
# mostrar las 4 cifras sin que el contenido se desborde
# mostrar las zetas

def mezclar_filas(array):
# calculamos todas las combinaciones del array y las devolvemso en una lista de python
    row_permutations = list(permutations(array)) 
    matrices_permutadas = []

    for permuted_rows in row_permutations:
        matrices_permutadas.append(list(permuted_rows))

    return matrices_permutadas

def verificarDescomponerLu(arrayTrabajar):
	# aca verificmaos todas las combinaciones posibles y si una se puede descomponer devuleve los valores de L y U
    CAMBIOFILAS = {
        0: "no se intercambiaron las filas ",
        1: "se intercambiaron la fila 2 y 3",
        2: "se intercambiaron la fila 1 y 2",
        3: "se intercambio la fila 1 por la 2, la 2 por la 3 y la 3 por la 1",
        4: "se intercambio la fila 1 por la 3, la 2 por la 1 y la 3 por la 2",
        5: "se intercambio la fila 1 y 3",
    }
    array = mezclar_filas(arrayTrabajar)
    i = 0
    lon = len(array)-1
    data = descomponerLu(array[i])

    while not data and i < lon:
        i += 1
        data = descomponerLu(array[i])

    if data:
        L = data["L"]
        U = data["U"]

        return {"L": L, "U": U}
    else:
        return False
 


def descomponerLu(arrayTrabajar):

    try:
    # Definir la matriz 3x3 de ejemplo
        A = np.array(arrayTrabajar)

        # Inicializar las matrices L y U
        L = np.zeros((3, 3))
        U = np.zeros((3, 3))

        # Implementar el algoritmo de descomposición LU
        for i in range(3):
            # Calcular la matriz U
            for k in range(i, 3):
                suma = 0
                for j in range(i):
                    suma += float(L[i][j] * U[j][k])
                U[i][k] = float(A[i][k] - suma)

            # Calcular la matriz L
            for k in range(i, 3):
                if i == k:
                    L[i][i] = 1
                else:
                    suma = 0
                    if U[i][i] == 0:
                        return False
                    for j in range(i):
                        suma += float(L[k][j] * U[j][i])
                    L[k][i] = float((A[k][i] - suma) / U[i][i])
        return {
            "L": L,
            "U": U
        }
    except:
        return False
 



def resolverSistema(terminos, cohefientes):
    data = verificarDescomponerLu(terminos)
    L, U = data["L"], data["U"]

    valido = True
    solution_error = False

    i = 0
    for l, u in zip(L, U):
        if any(l) == 0 or any(u) == 0: # valdamos los 0 ingresados en las matrices L y U
            valido = False
            break
        i += 1

    if valido:
        b = np.array(cohefientes)

        try:
            # Resuelve Ly = b usando sustitución hacia adelante
            y = np.linalg.solve(L, b)

            # Resuelve Ux = y usando sustitución hacia atrás
            x = np.linalg.solve(U, y)
            return {
                "descomposicon": {
                    "L": L,
                    "U": U
                },
                "soluciones": x,
				"zetas": y
            }
        except np.linalg.LinAlgError:
            solution_error = True

#  validamos que la fial no se todos ceros en la matriz y en lso cohefientes 
# y devolvemso una clave que pueda interpretar la funcion que al emplee
    if not valido or solution_error:
        print(i)
        try:
            b = np.array(cohefientes)
            y = np.linalg.solve(L, b)
            print(y)
            if y[i] == 0:
                return{
                    "soluciones":np.array([-1])
                }
            else:
                return{
                    "soluciones":np.array([-2])
                }
        except:
            return{
                "soluciones":np.array([-2])
            }





class Ventana(Frame):
	def __init__(self, master, *args):
		super().__init__( master,*args)
# definifimos los contenedores para el programa en que en este caso serian los frames, pero los mas generales, como el inicio y el menu
		self.menu = True
		self.color = True
		self.fuentePropia = font.Font(family="roman", size=130, weight="normal")
		self.numAprox = 4
		self.showInfoDescomposicion = ''
		self.showInfoResolucion = ''

		self.frame_inicio = Frame(self.master, bg='black', width=50, height=45)
		self.frame_inicio.grid_propagate(0)
		self.frame_inicio.grid(column=0, row = 0, sticky='nsew')
		self.frame_menu = Frame(self.master, bg='black', width = 65)
		self.frame_menu.grid_propagate(0)
		self.frame_menu.grid(column=0, row = 1, sticky='nsew')
		self.frame_top = Frame(self.master, bg='black', height = 50)
		self.frame_top.grid(column = 1, row = 0, sticky='nsew')
		self.frame_principal = Frame(self.master, bg='black')
		self.frame_principal.grid(column=1, row=1, sticky='nsew')
		self.master.columnconfigure(1, weight=1)
		self.master.rowconfigure(1, weight=1)
		self.frame_principal.columnconfigure(0, weight=1)
		self.frame_principal.rowconfigure(0, weight=1)
		self.widgets()		

# este progarama tiene una navegacion por rutas los que hace que tengamos que definir una funcion por cada ruta ya que hace modificamos su valor y cambiamos de contenedor,
# además de que definimos algunas configuraciones especidfimaos para el tamaño de la grilla en cada seccion

	def pantalla_inicial(self):
		self.paginas.select([self.frame_inicio])
		
	def pantalla_calcularLu(self):
		self.paginas.select([self.descomponerLU])
		self.descomponerLU.columnconfigure(0, weight=1)

	def pantalla_resolverSistema(self):
		self.paginas.select([self.frameResolverSistem])
		self.frameResolverSistem.columnconfigure(0, weight=1)
		self.frameResolverSistem.columnconfigure(1, weight=1)

	def pantalla_ajustes(self):
		self.paginas.select([self.frame_configuracion])

	def pantalla_manual(self):
		self.paginas.select([self.frame_manualUsuario])

# aca tenemos un menu lateral que basiamente establece el tamaño por defector WITDH y luego con un for la vamos sumando la tamaño del grama econ lo cual podemos visualizar
# el contenido completo que incluye el nombre de cada ruta
	def menu_lateral(self):
		WIDTH = 250
		ti = 20
		if self.menu :
			for i in range(65,WIDTH,ti):				
				self.frame_menu.config(width= i)
				self.frame_inicio.config(width= i)
				self.frame_menu.update()
				clik_inicio = self.bt_cerrar.grid_forget()
				if clik_inicio is None:		
					self.bt_inicio.grid(column=0, row=0, padx =5, pady=10)
					self.bt_inicio.grid_propagate(0)
					self.bt_inicio.config(width=i)
					self.pantalla_inicial()
			self.menu = False
		else:
			for i in range(WIDTH,65,-ti):
				self.frame_menu.config(width=  i)
				self.frame_inicio.config(width= i)
				self.frame_menu.update()
				clik_inicio = self.bt_inicio.grid_forget()
				if clik_inicio is   None:
					self.frame_menu.grid_propagate(0)		
					self.bt_cerrar.grid(column=0, row=0, padx =5, pady=10)
					self.bt_cerrar.grid_propagate(0)
					self.bt_cerrar.config(width=i)
					self.pantalla_inicial()
			self.menu = True

# esta es una funcionalidad "extra que parcticamente cabia de color entre oscuro y claro para mejor el gusto dle usuario"
	def cambiar_color(self):
		if self.color == True:
			self.bt_color['image'] = self.dia
			self.titulo.config(fg='deep sky blue')
			self.frame_configuracion.config(bg= '#202020')
			self.text_ajustes.config(bg='#202020')
			self.bt_color.config(bg='black',activebackground='black')
			self.frame_inicio.config(bg='#202020')
			self.descomponerLU.config(bg='#202020')
			self.frameResolverSistem.config(bg='#202020')
			self.color = False	
		else:
			self.bt_color['image'] = self.noche
			self.titulo.config(fg='DarkOrchid1')
			self.frame_configuracion.config(bg= 'white')
			self.text_ajustes.config(bg='white')
			self.bt_color.config(bg='white',activebackground='white')
			self.frame_inicio.config(bg='#fff')
			self.descomponerLU.config(bg='#fff')
			self.frameResolverSistem.config(bg='#fff')	
			self.color = True

	def showPass(self, L, U):
		nuevaVentana = Toplevel(self.master)
	
		dataL=['L₂₁','L₃₁','L₃₂']
		filaL = [
			"primera columna de L", 
			"segunda columna de L"
		]
		filaU = [
			"Calculo de la primera fila de U",
			"Calculo de la segunda fila de U",
			"Calculo de la tercera fila de U"
		]
		dataU = ['u₁₁' ,'u₁₂','u₁₃', 'u₂₂', 'u₂₃','u₃₃']
		text = ''
		aux, aux1 = 0,0

		for c in range(3):
			if c <2:
				text+=filaL[c-1]+'\n'
			for f in range(3):
				if L[f][c]!=0 and L[f][c]!=1:
					text+=dataL[aux]+'='+str(L[f][c])+'\n'
					aux+=1

		text2 = ''
		for j,filas in enumerate(U):
			text2+=filaU[j]+'\n'
			for i,value in enumerate(filas):
				if value!=0:
					text2+=dataU[aux1]+'='+str(value)+'\n'
					aux1+=1



		label = Label(nuevaVentana, text=text, font=('Arial', 20, "normal")).pack()
		dataU = []
		
		
		label = Label(nuevaVentana, text=text2, font=('Arial', 20, "normal")).pack()
		# label = Label(nuevaVentana, text='Calculo de la segunda fila de U').pack()
		# label = Label(nuevaVentana, text='Calculo de la tercera fila de U').pack()


	def calcularLU(self):

		numCuadrado = 3
		
		i = 0
		arrayGlobal = []
		for f in range(numCuadrado):
			arrayTem = []
			for c in range(numCuadrado):
				arrayTem.append(float(self.dataINputs[f"value{i}"].get()))
				i+=1
			arrayGlobal.append(arrayTem)
		# extrameos los valores de lso inuts a tarvés de un arreglo ya se lo enviamos a la funcion en una lista

		dataLu = verificarDescomponerLu(arrayGlobal) 
		# creacion  de los resultados 

		if dataLu: #verificamos la solucion de dataLu. 

			self.frame_sol_LU = Frame(self.descomponerLU)
			self.frame_sol_LU.grid(row=3, column=0, sticky='nsew')

			L = dataLu["L"]
			U = dataLu["U"]
			print(L)
			print(U)

			################# SOLUCION DESCOMPONER LU ####################
			# "coloreamos los datos en pantalla"
			Label(self.frame_sol_LU, text='L =', font=("Calibri Light", 60, "normal"), bg='#fff').grid(row=0,column=0, rowspan=4)
			Label(self.frame_sol_LU, text='[', font=self.fuentePropia, bg='#fff').grid(row=0,column=1, rowspan=4)
			for f in range(len(L)):
				for c in range(2,len(L[0])+2):
					print(L[f][c-2])
					# en la opcion de formatear es ña cantidad de digitos de comoa flotante
					Label(self.frame_sol_LU, bg='#fff', text=self.formatear_numero(L[f][c-2], int(self.numAprox)), font=("Arial", 25, "normal")).grid(row=f, column=c, ipadx=10, ipady=10)
			
			Label(self.frame_sol_LU, text=']', font=self.fuentePropia, bg='#fff').grid(row=0,column=5, rowspan=4)
			Label(self.frame_sol_LU, text='U = ', font=("Calibri Light", 60, "normal"), bg='#fff').grid(row=0,column=6, rowspan=4)
			Label(self.frame_sol_LU, text='[', font=self.fuentePropia, bg='#fff').grid(row=0,column=7, rowspan=4)

			for f in range(len(U)):
				for c in range(8,len(U[0])+8):
					print(U[f][c-8])
					Label(self.frame_sol_LU, bg='#fff',text=self.formatear_numero(U[f][c-8], int(self.numAprox)),  font=("Arial", 25, "normal")).grid(row=f, column=c,  ipadx=10, ipady=10)

			Label(self.frame_sol_LU, text=']', font=self.fuentePropia, bg='#fff').grid(row=0,column=11, rowspan=4)
			Button(self.frame_sol_LU, text='ver paso a paso', bg='#fff', command=lambda:self.showPass(L,U)).grid(row=4,column=0, rowspan=4)

		else: 
			messagebox.showerror("Error", "la matriz ingresada no tiene descomposicion LU")

	def resolverSistem(self):
		NUM_CUADRADO = 4
		i = 0
		M = []
		# repetimso el proceos anterior pero ahora lo divimso en dos lostas que son las de coheficientes y terminso independientes del sistema de ecuaciones
		cohefientVariable = []
		for f in range(NUM_CUADRADO-1):
			arrayTem = []
			for c in range(1,NUM_CUADRADO+1):
				if c % NUM_CUADRADO == 0:
					cohefientVariable.append(float(self.inputValues[i].get()))
				else:
					arrayTem.append(float(self.inputValues[i].get()))
				i+=1
			M.append(arrayTem)
		
		# creacion de los resultados

		
		data = resolverSistema(M,cohefientVariable)
		# debiso en que un sistema de ecuaicones podemos obtener variso resultados, solucion unica, infinta y no tern solucion
		# pues validamos cada uno de los casos
		# y pintamos cada uno de los datos en patalla
		val = data["soluciones"]
		if np.array_equal(val, [-1]):
			messagebox.showerror("Error", "El sistema tiene soluciones infinitas.")
		elif np.array_equal(val, [-2]):
			messagebox.showerror("Error", "El sistema no tiene solucion")
		else:
			descomposicion, soluciones = data["descomposicon"], data["soluciones"]
			l,u = descomposicion["L"], descomposicion["U"]
			z = data['zetas']

			self.frame_solLU = Frame(self.frameResolverSistem, bg='#fff')
			self.frame_solLU.grid(row=3, column=0)

			Label(self.frame_solLU, text='L =', font=("Calibri Light", 60, "normal"), bg='#fff').grid(row=0,column=0, rowspan=4)
			Label(self.frame_solLU, text='[', font=self.fuentePropia, bg='#fff').grid(row=0,column=1, rowspan=4)
			for f in range(len(l)):
				for c in range(2,len(l[0])+2):
					print(l[f][c-2])
					Label(self.frame_solLU, bg='#fff', text=self.formatear_numero(l[f][c-2], int(self.numAprox)), font=("Arial", 25, "normal")).grid(row=f, column=c,  ipadx=10, ipady=10)
			
			Label(self.frame_solLU, text=']', font=self.fuentePropia, bg='#fff').grid(row=0,column=5, rowspan=4)
			Label(self.frame_solLU, text='U = ', font=("Calibri Light", 60, "normal"), bg='#fff').grid(row=0,column=6, rowspan=4)
			Label(self.frame_solLU, text='[', font=self.fuentePropia, bg='#fff').grid(row=0,column=7, rowspan=4)

			for f in range(len(u)):
				for c in range(8,len(u[0])+8):
					print(u[f][c-8])
					Label(self.frame_solLU, bg='#fff',text=self.formatear_numero(u[f][c-8], int(self.numAprox)),  font=("Arial", 25, "normal")).grid(row=f, column=c,  ipadx=10, ipady=10)

			Label(self.frame_solLU, text=']', font=self.fuentePropia, bg='#fff').grid(row=0,column=11, rowspan=4)

			self.sol = Frame(self.frameResolverSistem)
			self.sol.grid(row=4, column=0)
			text = ["x", "y","z"]
			for i in range(3):
				Label(self.sol, text=text[i] +': '+ self.formatear_numero(soluciones[i], int(self.numAprox)), font=("Arial", 25, "normal"), bg='#fff').grid(row=0,column=i,  ipadx=10, ipady=10)

	# esta funcion es para mostrara los elementos en patalla de la seccionde calcular sistemas de ecuaciones
	def init_function2(self):
		numCuadrado = 3
		i= 0
		VALUE_PADDING = 15
		self.inputValues = {}
		letraCoheficiente = ["x", "y", "z", "="]
		LIMIT = numCuadrado+numCuadrado+2+1

		Label(self.resolveSistem, text='{', font=("Calibri Light", 145, "normal"), bg='#fff').grid(row=0,column=0, rowspan=4)
		for f in range(1,numCuadrado+1):
			j = 0
			for c in range(1,LIMIT): #alternamos y juagamos con los indices para que queden bien colocados en la grilla
				if c == LIMIT-1: # 
					input = Entry(self.resolveSistem,width=2, highlightthickness=1, font=("Arial", 25))
					input.grid(row=f,column=c,  )
					self.inputValues[i] = input
					i+=1
				elif c == LIMIT-2:
					coheficiente = Label(self.resolveSistem, text=letraCoheficiente[j],font=("Arial", 25), bg='#fff')
					coheficiente.grid(row=f, column=c,padx=(0,VALUE_PADDING))
					j+=1
				elif (c-1)%2== 0:
					input = Entry(self.resolveSistem,width=2, highlightthickness=1, font=("Arial", 25))
					input.grid(row=f,column=c,  )
					self.inputValues[i] = input
					i+=1
				else:
					coheficiente = Label(self.resolveSistem, text=letraCoheficiente[j],font=("Arial", 25), bg='#fff')
					coheficiente.grid(row=f, column=c,padx=(0,VALUE_PADDING))
					j+=1

		self.btn_calcular = Button(self.frameResolverSistem,text='calcular', command=self.resolverSistem)
		self.btn_calcular.grid(row=2, column=0, ipadx=5, ipady=5)

# en esta funcion se definein todos los componenetes de las secciones que el susario al ejecutrar va a ver en pantalla
	def widgets(self):
		# iconos para el menu
		self.imagen_inicio = PhotoImage(file ='imgs/inicio.png')
		self.imagen_menu = PhotoImage(file ='imgs/menu.png')
		self.imagen_descomponer = PhotoImage(file ='imgs/descomponer.png')
		self.imagen_res_sistem = PhotoImage(file ='imgs/sistema2.png')
		self.imagen_ajustes = PhotoImage(file ='imgs/configuracion.png')
		self.imagen_manual = PhotoImage(file ='imgs/escribir.png')

		self.dia = PhotoImage(file ='imgs/dia.png')
		self.noche= PhotoImage(file ='imgs/noche.png')
		self.bt_inicio = Button(self.frame_inicio, image= self.imagen_inicio, bg='black',activebackground='black', bd=0, command = self.menu_lateral)
		self.bt_inicio.grid(column=0, row=0, padx=(5,0), pady=10)
		self.bt_cerrar = Button(self.frame_inicio, image= self.imagen_menu, bg='black',activebackground='black', bd=0, command = self.menu_lateral)
		self.bt_cerrar.grid(column=0, row=0, padx=5, pady=10)	

		#BOTONES Y ETIQUETAS DEL MENU LATERAL 
		Button(self.frame_menu, image= self.imagen_descomponer, bg='black', activebackground='black', bd=0, command = self.pantalla_calcularLu).grid(column=0, row=1, pady=20,padx=10)
		Button(self.frame_menu, image= self.imagen_res_sistem, bg='black',activebackground='black', bd=0, command =self.pantalla_resolverSistema ).grid(column=0, row=2, pady=20,padx=10)
		Button(self.frame_menu, image= self.imagen_manual, bg= 'black',activebackground='black', bd=0, command = self.pantalla_manual).grid(column=0, row=3, pady=20,padx=10)
		Button(self.frame_menu, image= self.imagen_ajustes, bg= 'black',activebackground='black', bd=0, command = self.pantalla_ajustes).grid(column=0, row=4, pady=20,padx=10)
		Label(self.frame_menu, text= 'Descomponer LU', bg= 'black', fg= 'DarkOrchid1', font= ('Lucida Sans', 12, 'bold')).grid(column=1, row=1, pady=20, padx=2)
		Label(self.frame_menu, text= 'Resolver sistema', bg= 'black', fg= 'DarkOrchid1', font= ('Lucida Sans', 12, 'bold')).grid(column=1, row=2, pady=20, padx=2)
		Label(self.frame_menu, text= 'manual', bg= 'black', fg= 'DarkOrchid1', font= ('Lucida Sans', 12, 'bold')).grid(column=1, row=3, pady=20, padx=2)
		Label(self.frame_menu, text= 'Ajustes', bg= 'black', fg= 'DarkOrchid1', font= ('Lucida Sans', 12, 'bold')).grid(column=1, row=4, pady=20, padx=2)

        	#############################  CREAR  PAGINAS  ##############################
		estilo_paginas = ttk.Style()
		estilo_paginas.configure("TNotebook", background='black', foreground='black', padding=0, borderwidth=0)
		estilo_paginas.theme_use('default')
		estilo_paginas.configure("TNotebook", background='black', borderwidth=0)
		estilo_paginas.configure("TNotebook.Tab", background="black", borderwidth=0)
		estilo_paginas.map("TNotebook", background=[("selected", 'black')])
		estilo_paginas.map("TNotebook.Tab", background=[("selected", 'black')], foreground=[("selected", 'black')]);

		#CREACCION DE LAS PAGINAS 
		self.paginas = ttk.Notebook(self.frame_principal , style= 'TNotebook') #, style = 'TNotebook'
		self.paginas.grid(column=0,row=0, sticky='nsew')
		self.frame_inicio = Frame(self.paginas, bg='DarkOrchid1')
		self.descomponerLU = Frame(self.paginas, bg='white')
		self.frameResolverSistem = Frame(self.paginas, bg='white')
		self.frame_configuracion = Frame(self.paginas, bg='white')
		self.frame_manualUsuario = Frame(self.paginas, bg='white')
		self.paginas.add(self.frame_inicio)
		self.paginas.add(self.descomponerLU)
		self.paginas.add(self.frameResolverSistem)
		self.paginas.add(self.frame_configuracion)
		self.paginas.add(self.frame_manualUsuario)

		##############################         PAGINAS       #############################################

		######################## FRAME TITULO #################
		self.titulo = Label(self.frame_top,text= 'calculadora Matrices LU', bg='black', fg= 'DarkOrchid1', font= ('Imprint MT Shadow', 15, 'bold'))
		self.titulo.pack(expand=1)

		######################## VENTANA PRINCIPAL #################
		Label(self.frame_inicio, text= 'Inicio', bg='DarkOrchid1', fg= 'white', font= ('Freehand521 BT', 20, 'bold')).pack(expand=1)
		Button(self.frame_inicio, text='descomponer matriz LU 3x3', command=self.pantalla_calcularLu).pack(expand=1, ipadx=
        5, ipady=5)
		Button(self.frame_inicio, text='Resolver sistemas 3x3', command=self.pantalla_resolverSistema).pack(expand=1, ipadx=
        5, ipady=5)

		######################## DESCOMPONER LU #################

		Label(self.descomponerLU, text= 'descomponer LU', bg='white', fg= 'DarkOrchid1', font=('Kaufmann BT',24,'bold')).grid(columnspan=2, column=0,row=0, pady=5)
		self.frameContLU = Frame(self.descomponerLU, bg='#fff')
		self.descomponerLU.grid_rowconfigure(2, weight=0)
		self.frameContLU.grid(row=1,column=0)
		numCuadrado = 3
		self.dataINputs = {}
		i= 0
		Label(self.frameContLU, text='[', font=self.fuentePropia, bg='#fff').grid(row=0,column=0, rowspan=4)
		for f in range(1,numCuadrado+1):
			for c in range(1,numCuadrado+1):
				input = Entry(self.frameContLU, width=2, highlightthickness=1, font=("Arial", 30))
				input.grid(row=f,column=c, padx=5, pady=5)
				self.dataINputs[f"value{i}"] = input
				i+=1
		Label(self.frameContLU, text=']', font=self.fuentePropia, bg='#fff').grid(row=0,column=numCuadrado+1, rowspan=4)
		Button(self.descomponerLU, text='Calcular lu', command=self.calcularLU).grid(row=2, column=0, ipadx=5,ipady=5)
	

		######################## RESOOLVER SISTEMAS DE ECUACIONES #################
		Label(self.frameResolverSistem, text = 'resolver sistemas de ecuaciones',fg='purple', bg ='white', font=('Kaufmann BT',24,'bold')).grid(columnspan=2, column=0,row=0, pady=5)
		self.resolveSistem = Frame(self.frameResolverSistem, bg='#fff', width=40, height=40)
		self.resolveSistem.grid(row=1,column=0)
		self.init_function2()
	
		######################## MANUAL DE USUARIO #################
		TEXT = """
		instrucciones de Uso:

			Descomposición LU 3x3: 

			1. Accede a la sección 'Descomposición LU 3x3' en la calculadora. 
			2. Ingresa los valores de la matriz 3x3 en el formato adecuado. 
			3. Presiona el botón 'Calcular' para obtener las matrices L y U resultantes. 
			4. Verifica los resultados en la pantalla de la calculadora. 
			5. Resolver Sistema de Ecuaciones: 

			Resolver sistemas de ecuaciones 3x3: 

			1. Accede a la sección 'Resolver Sistema de Ecuaciones'. 
			2. Ingresa los términos y coeficientes del sistema de ecuaciones. 
			3. Presiona el botón 'Calcular' para obtener las soluciones del sistema de ecuaciones. 
			4. Revisa las soluciones en la pantalla de la calculadora. 
			
			IMPORTANTE : 
			Asegúrate de ingresar los valores de la matriz y del sistema de ecuaciones correctamente  
			para obtener resultados precisos. 
			Si encuentras algún problema o error, verifica la entrada de los datos y vuelve a intentarlo. 
			Si no estás familiarizado con el método de descomposición LU, te recomendamos leer la sección  
			de ayuda o buscar información adicional en línea. 
			
			Información Adicional: 
			La calculadora está diseñada para proporcionar resultados precisos, pero ten en cuenta que puede  
			haber limitaciones en la precisión o el rango de valores debido a las restricciones del método de  
			descomposición LU 
		"""
		ventana.bind_all("<MouseWheel>", self.on_mousewheel)

		scrollbar = Scrollbar(self.frame_manualUsuario, orient=VERTICAL)
		scrollbar.pack(side=RIGHT, fill=Y) # definismo un scroll para que pueda ser scrolleable 

		self.canvas = Canvas(self.frame_manualUsuario, yscrollcommand=scrollbar.set, bg='#ffffff')
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

		scrollbar.config(command=self.canvas.yview)
		interior_frame = Frame(self.canvas, bg='#ffffff')
		interior_frame_id = self.canvas.create_window(0, 0, window=interior_frame, anchor=NW)

		a = Label(interior_frame, bg = '#fff', text='MANUAL DE USUARIO ', font=("Arial", 25, "bold"))
		label = Label(interior_frame, bg='#ffffff', text=TEXT, font=("Arial", 15, "normal"), justify="left", wraplength=1700)
		a.pack()
		label.pack()

		interior_frame.bind("<Configure>", self.configure_interior_frame)
		ventana.bind_all("<MouseWheel>", self.on_mousewheel)


		######################## AJUSTES #################
		self.text_ajustes = Label(self.frame_configuracion, text = 'Configuracion',fg='purple', bg ='white', font=('Kaufmann BT',28,'bold'))
		self.text_ajustes.pack()
		self.bt_color = Button(self.frame_configuracion, image = self.noche , command= self.cambiar_color, bg = 'white', bd=0, activebackground='white')
		self.bt_color.pack()
		self.frameAprox = Frame(self.frame_configuracion)
		self.frameAprox.pack()
		# en esta seccion podemos modificar el numero de digitos de como flotante
		Label(self.frameAprox, text='limite de aproximacion').grid(row=0, column=0, padx=5, pady=5)
		value = Entry(self.frameAprox, width=10, font=("Arial", 25, "normal"))
		value.grid(row=0, column=1, padx=5, pady=5)
		Button(self.frameAprox, text='guardar los cambios', command=lambda: self.cambiar(value)).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#  esta funcion modifica la longitus de numero de coma floatnte
	def cambiar(self, value):
		self.numAprox = value.get()
		messagebox.showinfo("Actualizacion",self.numAprox )
	def formatear_numero(self,numero, cifras):
		if isinstance(numero, int) or numero.is_integer():
			return f"{int(numero):d}.".ljust(len(str(int(numero))) + cifras+1, '0')
		else:
			return f"{numero:.{cifras}f}"

# estas dos funciones son oara controlar el scroll
	def on_mousewheel(self,event):
		self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def configure_interior_frame(self,event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# se utiliza para verificar si el script actual se está ejecutando como un programa principal.
if __name__ == "__main__":
	ventana = Tk()
	
	ventana.title('matriz LU')

	ancho_pantalla = ventana.winfo_screenwidth()-10
	alto_pantalla = ventana.winfo_screenheight()

	# Configurar el tamaño de la ventana
	ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")
	app = Ventana(ventana)
	app.mainloop()
