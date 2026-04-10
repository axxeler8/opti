import sys
import time
from itertools import product

# ===========================================================================
#  TALLER 1: Lectura y visualización de instancias
# ===========================================================================

def leer_instancia(archivo):
    f = open(archivo, 'r')
    numeros = []
    for linea in f:
        linea = linea.strip()
        if linea != "" and not linea.startswith('#'):
            partes = linea.split()
            for p in partes:
                numeros.append(int(p))
    f.close()
    
    pos = 0
    n = numeros[pos]
    pos += 1
    m = numeros[pos]
    pos += 1

    beneficios = []
    for i in range(n):
        beneficios.append(numeros[pos])
        pos += 1
  
    restricciones = []
    for i in range(m):
        fila = []
        for j in range(n):
            fila.append(numeros[pos])
            pos += 1
        restricciones.append(fila)
  
    capacidades = []
    for i in range(m):
        capacidades.append(numeros[pos])
        pos += 1
   
    instancia = {
        'n': n,
        'm': m,
        'beneficios': beneficios,
        'restricciones': restricciones,
        'capacidades': capacidades,
        'archivo': archivo
    }
    return instancia

def mostrar_instancia(instancia):
    n = instancia['n']
    m = instancia['m']
    print("\n" + "=" * 50)
    print("  INFORMACIÓN DE LA INSTANCIA MKP")
    print("=" * 50)
    print("  Archivo:               ", instancia['archivo'])
    print("  Número de items (n):   ", n)
    print("  Número de restricciones:", m)
    print("  Espacio de búsqueda:    2^" + str(n) + " soluciones")

    print("\n  Beneficios de cada item:")
    print(" ", instancia['beneficios'])

    print("\n  Matriz de restricciones (" + str(m) + " x " + str(n) + "):")
    for i in range(m):
        print("  R" + str(i+1) + " (cap=" + str(instancia['capacidades'][i]) + "):", instancia['restricciones'][i])
    print("=" * 50)


# ===========================================================================
#  TALLER 2: Representación de soluciones y verificación
# ===========================================================================

def leer_solucion(archivo, n):
    f = open(archivo, 'r')
    lineas = []
    for linea in f:
        linea = linea.strip()
        if linea != "" and not linea.startswith('#'):
            lineas.append(linea)
    f.close()
  
    partes = lineas[0].split()
    solucion = []
    for p in partes:
        solucion.append(int(p))
    
    if len(solucion) != n:
        print("Error: La solución no tiene", n, "elementos.")
        sys.exit(1)
    return solucion

def verificar_restricciones(solucion, instancia):
    n = instancia['n']
    m = instancia['m']
    es_valida = True

    for i in range(m):
        consumo = 0
        for j in range(n):
            consumo += instancia['restricciones'][i][j] * solucion[j]
        capacidad = instancia['capacidades'][i]
        if consumo > capacidad:
            es_valida = False

    return es_valida

def imprimir_verificacion(solucion, instancia):
    n = instancia['n']
    m = instancia['m']
    print("\n  Solución:", solucion)
    print("\n  Verificación de restricciones:")

    es_valida = True
   
    for i in range(m):
        consumo = 0
        for j in range(n):
            consumo += instancia['restricciones'][i][j] * solucion[j]
        capacidad = instancia['capacidades'][i]
     
        if consumo <= capacidad:
            estado = "Cumple"
        else:
            estado = "VIOLA"
            es_valida = False
        print("  R" + str(i+1) + " | Consumo: " + str(consumo) + " | Capacidad: " + str(capacidad) + " | Estado: " + estado)

    if es_valida:
        print("  => Solución VÁLIDA")
    else:
        print("  => Solución INVÁLIDA")
    return es_valida


# ===========================================================================
#  TALLER 3: Estrategia de enumeración y función objetivo
# ===========================================================================

def calcular_funcion_objetivo(solucion, instancia):
    n = instancia['n']
    total = 0
    for j in range(n):
        total += instancia['beneficios'][j] * solucion[j]
    return total

def comparar_soluciones(sol1, sol2, instancia):
    valida1 = verificar_restricciones(sol1, instancia)
    valida2 = verificar_restricciones(sol2, instancia)
    fo1 = calcular_funcion_objetivo(sol1, instancia)
    fo2 = calcular_funcion_objetivo(sol2, instancia)

    print("\n" + "=" * 50)
    print("  COMPARACIÓN DE SOLUCIONES")
    print("=" * 50)
    print("  Solución 1:", sol1)
    print("    Válida:", valida1, " |  F.O.:", fo1)
    print("  Solución 2:", sol2)
    print("    Válida:", valida2, " |  F.O.:", fo2)
    print("-" * 50)

    if valida1 and not valida2:
        print("  Resultado: Solución 1 es MEJOR (válida vs inválida)")
    elif not valida1 and valida2:
        print("  Resultado: Solución 2 es MEJOR (válida vs inválida)")
    elif valida1 and valida2:
        if fo1 > fo2:
            print("  Resultado: Solución 1 es MEJOR (mayor F.O.)")
        elif fo2 > fo1:
            print("  Resultado: Solución 2 es MEJOR (mayor F.O.)")
        else:
            print("  Resultado: Ambas soluciones son IGUALES en calidad")
    else:
        print("  Resultado: Ambas soluciones son INVÁLIDAS, no se puede determinar")
    print("=" * 50)


# ===========================================================================
#  TALLER 4: Búsqueda exhaustiva (Fuerza bruta)
# ===========================================================================

def busqueda_exhaustiva(instancia):
    n = instancia['n']
    print("\nEjecutando fuerza bruta para " + str(n) + " items...")

    mejor_solucion = None
    mejor_valor = -1
    soluciones_evaluadas = 0

    tiempo_inicio = time.time()

    for combinacion in product([0, 1], repeat=n):
        solucion = list(combinacion)
        soluciones_evaluadas += 1
        es_valida = verificar_restricciones(solucion, instancia)
        if es_valida:
            valor = calcular_funcion_objetivo(solucion, instancia)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_solucion = list(solucion)

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    print("\n" + "=" * 50)
    print("  RESULTADO ÓPTIMO (Fuerza Bruta)")
    print("=" * 50)
    if mejor_solucion is not None:
        print("  Mejor solución:       ", mejor_solucion)
        print("  Mejor F.O.:           ", mejor_valor)
    else:
        print("  No se encontraron soluciones factibles.")
    print("  Soluciones evaluadas: ", soluciones_evaluadas)
    print("  Tiempo de ejecución:  ", round(tiempo_total, 4), "segundos")
    print("=" * 50)


# ===========================================================================
#  EJECUCIÓN DEL PROGRAMA
# ===========================================================================

if __name__ == "__main__":
    print("-" * 50)
    print("=== MKP SOLVER ===")
    print("-" * 50)

    archivo_instancia = "instancias/mkp_instance.txt"
    archivo_solucion1 = "instancias/solucion_ejemplo.txt"
    archivo_solucion2 = "instancias/solucion_ejemplo2.txt"

    # Leer instancia
    instancia = leer_instancia(archivo_instancia)
    mostrar_instancia(instancia)

    # Leer y verificar solución 1
    solucion1 = leer_solucion(archivo_solucion1, instancia['n'])
    imprimir_verificacion(solucion1, instancia)
    fo1 = calcular_funcion_objetivo(solucion1, instancia)
    print("  Función Objetivo:", fo1)

    # Leer y verificar solución 2
    solucion2 = leer_solucion(archivo_solucion2, instancia['n'])
    imprimir_verificacion(solucion2, instancia)
    fo2 = calcular_funcion_objetivo(solucion2, instancia)
    print("  Función Objetivo:", fo2)

    # Comparar soluciones
    comparar_soluciones(solucion1, solucion2, instancia)

    # Búsqueda exhaustiva
    print("\nIniciando algoritmo de Fuerza Bruta...")
    busqueda_exhaustiva(instancia)
