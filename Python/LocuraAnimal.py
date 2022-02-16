from itertools import combinations
from pprint import pprint

"""
EJERCICIO
Con la “tabla de poder” analizado, del conjunto de 4 animales seleccionados, el 
equipo deberá generar un vocablo de 13 letras, bajo las siguientes condiciones 
• De cada animal mínimo se deberán tomar tres letras distintas
• Una misma letra no deberá aparecer más de dos veces en el vocablo final
• Pueden aparecer máximo dos modas en el vocablo final (puntos)
• La mediana deberá ser forzosamente un número impar en el vocablo final (puntos)
• El promedio de puntos deberá ser el menor posible
• La desviación estándar muestral la mayor posible


Por Salvador Bravo Garnica
"""

animales = [
    "cocodrilo",
    "avestruz",
    "murcielago",
    "ornitorrinco",
    "rinoceronte",
    "guacamaya",
    "suricato",
    "jilguero",
    "barracuda",
    "salamandra",
    "albatro",
    "chinchilla",
    "capibara",
    "hormiga",
    "hipopotamo",
    "libelula",
    "luciernaga",
    "tiburon",
    "zarigueya",
    "perezoso",
    "mantarraya",
    "zorrillo",
    "zorrillo",
    "armadillo",
    "elefante",
    "quetzal",
    "antilope",
    "leopardo"
]

# sobreescribe aquí animales para solo calcular ciertas combinaciones, mira el ejemplo
animales4 = [
    ("tiburon", "zorrillo", "mandril", "albatro"),
    ("quetzal", "albatro", "mandril", "murcielago"),
    ("tiburon", "albatro", "ornitorrinco", "hormiga"),
    ("ornitorrinco", "zarigueya", "barracuda", "elefante"),
    ("tiburon", "albatro", "murcielago", "jilguero"),

]

# o puedes generar todas las posibilidades
# animales4 = list(combinations(animales, 4))

letras_valores = {
    "a": 10,
    "b": 4,
    "c": 6,
    "d": 8,
    "e": 13,
    "f": 1,
    "g": 5,
    "h": 11,
    "i": 7,
    "j": 8,
    "k": 12,
    "l": 2,
    "m": 3,
    "n": 3,
    "o": 2,
    "p": 12,
    "q": 8,
    "r": 7,
    "s": 11,
    "t": 5,
    "u": 1,
    "v": 13,
    "w": 8,
    "x": 6,
    "y": 4,
    "z": 10
}


def main():
    for animales4_elemento in animales4:
        vocablos = []

        for vocablo in obtener_vocablo(animales4_elemento):
            if revisar_vocablo(vocablo):
                vocablos.append(vocablo)

        resultados = elegir_vocablos(vocablos)

        print(f"Para los cuatro animales: {' '.join(animales4_elemento)}")
        if len(resultados) == 0:
            print("\tNo se encontró ningún vocablo")
        elif len(resultados) == 1:
            print(f"\tEl mejor vocablo es: {resultados}")
        else:
            print(f"\tLos mejores vocablos son:")
            pprint(resultados)


def obtener_vocablo(lista_animales):
    lista_filtrada = [list(set(animal)) for animal in lista_animales]
    for de_quien_se_escogen_4 in range(3):
        if len(lista_filtrada[de_quien_se_escogen_4]) < 4:
            continue

        for primera in combinations(lista_filtrada[0], 4 if de_quien_se_escogen_4 == 0 else 3):
            for segunda in combinations(lista_filtrada[1], 4 if de_quien_se_escogen_4 == 1 else 3):
                for tercera in combinations(lista_filtrada[2], 4 if de_quien_se_escogen_4 == 2 else 3):
                    vocablo = primera + segunda + tercera
                    yield "".join(vocablo)


def revisar_vocablo(vocablo):
    frecuencia = {}
    for letra in vocablo:
        frecuencia.setdefault(letra, 0)
        frecuencia[letra] += 1

    # Una misma letra no deberá aparecer más de dos veces en el vocablo final
    if any(valor > 2 for valor in frecuencia.values()):
        return False

    frecuencia_puntos = {}
    for letra in vocablo:
        puntos = letras_valores[letra]
        frecuencia_puntos.setdefault(puntos, 0)
        frecuencia_puntos[puntos] += 1

    # Pueden aparecer máximo dos modas en el vocablo final (puntos)
    modas = [(0, "")]
    for llave, valor in frecuencia_puntos.items():
        if valor > modas[0][0]:
            modas = [(valor, llave)]
        elif valor == modas[0][0]:
            modas.append((valor, llave))
    if len(modas) > 2:
        return False

    # La mediana deberá ser forzosamente un número impar en el vocablo final (puntos)
    lista_puntos = []
    for llave, valor in frecuencia_puntos.items():
        for _ in range(valor):
            lista_puntos.append(llave)
    lista_puntos.sort()

    len_lista = len(lista_puntos)
    if len_lista % 2 == 0:
        mediana = (lista_puntos[len_lista // 2] + lista_puntos[(len_lista // 2) + 1]) / 2
    else:
        mediana = lista_puntos[(len_lista // 2) + 1]

    if mediana % 2 == 0:
        return False

    return True


def elegir_vocablos(lista_vocablos):
    menores_promedios = [("", 100, 0)]
    mayores_dsm = [("", 0, 100)]

    for vocablo in lista_vocablos:
        puntos = []
        for letra in vocablo:
            puntos.append(letras_valores[letra])
        puntos.sort()

        promedio = sum(puntos) / len(puntos)
        des_std_mues = (sum((x - promedio)**2 for x in puntos) / (len(puntos) - 1))**0.5

        if promedio < menores_promedios[0][1]:
            menores_promedios = [(vocablo, promedio, des_std_mues)]
        elif promedio == menores_promedios[0][1]:
            menores_promedios.append((vocablo, promedio, des_std_mues))

        if des_std_mues > mayores_dsm[0][1]:
            mayores_dsm = [(vocablo, des_std_mues, promedio)]
        elif des_std_mues == mayores_dsm[0][1]:
            mayores_dsm.append((vocablo, des_std_mues, promedio))

    menores_promedios_mayores_dsm = [("", 100, 0)]
    for elemento in menores_promedios:
        if elemento[2] > menores_promedios_mayores_dsm[0][2]:
            menores_promedios_mayores_dsm = [elemento]
        elif elemento[2] == menores_promedios_mayores_dsm[0][2]:
            menores_promedios_mayores_dsm.append(elemento)

    mayores_dsm_menores_promedios = [("", 0, 100)]
    for elemento in mayores_dsm:
        if elemento[2] < mayores_dsm_menores_promedios[0][2]:
            mayores_dsm_menores_promedios = [elemento]
        elif elemento[2] == mayores_dsm_menores_promedios[0][2]:
            mayores_dsm_menores_promedios.append(elemento)

    resultados = []

    for a in menores_promedios_mayores_dsm:
        resultados.append(a[0] + f" promedio {a[1]:.2f}" + f" dsm {a[2]:.2f}")
    for a in mayores_dsm_menores_promedios:
        resultados.append(a[0] + f" promedio {a[2]:.2f}" + f" dsm {a[1]:.2f}")

    resultados = list(set(resultados))
    return resultados


if __name__ == '__main__':
    main()
