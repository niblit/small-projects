import concurrent.futures
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
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
animales4 = list(combinations(animales, 4))

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
    with ProcessPoolExecutor() as ppe:
        results = [ppe.submit(process, a4) for a4 in animales4]

        for result in concurrent.futures.as_completed(results):
            print(result.result())


def process(cuatro_animales):
    vocablos = []

    for vocablo in obtener_vocablo(cuatro_animales):
        if revisar_vocablo(vocablo):
            vocablos.append(vocablo)

    resultados = elegir_vocablos(vocablos)

    mensaje = ""

    mensaje += "\n" + f"Para los cuatro animales: {' '.join(cuatro_animales)}"
    if len(resultados) == 0:
        mensaje += "\n" + "No se encontró ningún vocablo"
    elif len(resultados) == 1:
        mensaje += "\n" + f"El mejor vocablo es: {resultados}"
    else:
        mensaje += "\n" + f"Los mejores vocablos son:\n {' - '.join(resultados)}"

    return mensaje


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
    menores_promedios = [("", 100)]
    mayores_dsm = [("", 0)]
    for vocablo in lista_vocablos:
        puntos = []
        for letra in vocablo:
            puntos.append(letras_valores[letra])
        puntos.sort()
        promedio = sum(puntos) / len(puntos)
        if promedio < menores_promedios[0][1]:
            menores_promedios = [(vocablo, promedio)]
        elif promedio == menores_promedios[0][1]:
            menores_promedios.append((vocablo, promedio))

        des_std_mues = (sum((x - promedio)**2 for x in puntos)) / (len(puntos) - 1)**0.5
        if des_std_mues > mayores_dsm[0][1]:
            mayores_dsm = [(vocablo, des_std_mues)]
        elif des_std_mues == mayores_dsm[0][1]:
            mayores_dsm.append((vocablo, des_std_mues))

    resultados = []

    for a in menores_promedios:
        resultados.append(a[0])
    for a in mayores_dsm:
        resultados.append(a[0])

    resultados = list(set(resultados))
    return resultados


if __name__ == '__main__':
    main()
