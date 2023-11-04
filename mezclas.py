from itertools import permutations


def mezclar_filas(array):
    row_permutations = list(permutations(array))
    matrices_permutadas = []

    for permuted_rows in row_permutations:
        matrices_permutadas.append(list(permuted_rows))

    return matrices_permutadas


# print(mezclar_filas([
#     [0, 5, 6],
#     [1, 0, 5],
#     [7, 4, 3]
# ]))
