from mezclas import mezclar_filas
import numpy as np
from itertools import permutations
import pprint as pr

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
        pr.pprint(L)
        pr.pprint(U)

        # messagebox.showinfo('cambios filas', CAMBIOFILAS[i] )
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
                    else:
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
                "soluciones": x
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

