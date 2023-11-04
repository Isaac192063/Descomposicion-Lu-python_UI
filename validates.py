def validators(array, numCuadrado, n):
# validamos espacios en balncos y letras ingresadso en vez de numeros
    i = 0
    for f in range(numCuadrado):
        for c in range(n):
            value = array[f"value{i}"].get().strip()
            if value == "" or not (value.lstrip('-').isdigit() or (value[0] == '-' and value[1:].isdigit())):
                return False
            i += 1
    return True

# validar los sistemas de ecuacione singresadis

