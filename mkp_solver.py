import sys
import time

# ===========================================================================
#  TALLER 1: Lectura y visualización de instancias
# ===========================================================================

def leer_instancia(archivo):
    with open(archivo, 'r') as f:
        numeros = []
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith('#'):
                numeros.extend(linea.split())
    
    numeros = list(map(int, numeros))
    pos = 0
    
    n = numeros[pos]; pos += 1
    m = numeros[pos]; pos += 1
    
    beneficios = numeros[pos:pos + n]; pos += n
    
    restricciones = []
    for i in range(m):
        fila = numeros[pos:pos + n]; pos += n
        restricciones.append(fila)
    
    capacidades = numeros[pos:pos + m]
    
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
    print(f"  Archivo:                  {instancia['archivo']}")
    print(f"  Número de items (n):      {n}")
    print(f"  Número de restricciones:  {m}")
    print(f"  Espacio de búsqueda:      2^{n} soluciones")
    
    print("\n  Beneficios de cada item:")
    print("  " + " ".join(f"{b:>4}" for b in instancia['beneficios']))
    
    print(f"\n  Matriz de restricciones ({m} x {n}):")
    for i in range(m):
        print(f"  R{i+1} (cap={instancia['capacidades'][i]:>3}): ", end="")
        print(" ".join(f"{r:>4}" for r in instancia['restricciones'][i]))
    print("=" * 50)


# ===========================================================================
#  TALLER 2: Representación de soluciones y verificación
# ===========================================================================

def leer_solucion(archivo, n):
    with open(archivo, 'r') as f:
        lineas = []
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith('#'):
                lineas.append(linea)
    
    solucion = list(map(int, lineas[0].split()))
    if len(solucion) != n:
        raise ValueError(f"La solución no tiene {n} elementos.")
    return solucion

def verificar_restricciones(solucion, instancia):
    n = instancia['n']
    m = instancia['m']
    es_valida = True
    detalles = []
    
    for i in range(m):
        consumo = sum(instancia['restricciones'][i][j] * solucion[j] for j in range(n))
        capacidad = instancia['capacidades'][i]
        cumple = consumo <= capacidad
        if not cumple:
            es_valida = False
        detalles.append({
            'restriccion': i + 1, 'consumo': consumo,
            'capacidad': capacidad, 'cumple': cumple, 'holgura': capacidad - consumo
        })
    return es_valida, detalles

def imprimir_verificacion(solucion, instancia):
    es_valida, detalles = verificar_restricciones(solucion, instancia)
    print("\n  Solución:", solucion)
    print("\n  Verificación de restricciones:")
    for d in detalles:
        estado = "Cumple" if d['cumple'] else "VIOLA"
        print(f"  R{d['restriccion']} | Consumo: {d['consumo']} | Capacidad: {d['capacidad']} | Estado: {estado}")
    return es_valida


# ===========================================================================
#  TALLER 3: Estrategia de enumeración y función objetivo
# ===========================================================================

def calcular_funcion_objetivo(solucion, instancia):
    return sum(instancia['beneficios'][j] * solucion[j] for j in range(instancia['n']))

def comparar_soluciones(sol1, sol2, instancia):
    valida1, _ = verificar_restricciones(sol1, instancia)
    valida2, _ = verificar_restricciones(sol2, instancia)
    fo1 = calcular_funcion_objetivo(sol1, instancia)
    fo2 = calcular_funcion_objetivo(sol2, instancia)

    print("\n" + "=" * 50)
    print("  COMPARACIÓN DE SOLUCIONES")
    print("=" * 50)
    print(f"  Solución 1: {sol1}")
    print(f"    Válida: {'Sí' if valida1 else 'No'}  |  F.O.: {fo1}")
    print(f"  Solución 2: {sol2}")
    print(f"    Válida: {'Sí' if valida2 else 'No'}  |  F.O.: {fo2}")
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

def generar_solucion_desde_entero(numero, n):  
    return [(numero >> j) & 1 for j in range(n - 1, -1, -1)]


# ===========================================================================
#  TALLER 4: Búsqueda exhaustiva (Fuerza bruta)
# ===========================================================================

def busqueda_exhaustiva(instancia):
    n = instancia['n']
    total_soluciones = 2 ** n
    print(f"\nEjecutando fuerza bruta para {n} items ({total_soluciones} posibles)...")
    
    mejor_solucion = None
    mejor_valor = -1
    soluciones_evaluadas = 0
    
    tiempo_inicio = time.time()
    
    for i in range(total_soluciones):
        solucion = generar_solucion_desde_entero(i, n)
        soluciones_evaluadas += 1
        es_valida, _ = verificar_restricciones(solucion, instancia)
        if es_valida:
            valor = calcular_funcion_objetivo(solucion, instancia)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_solucion = solucion[:]
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
                
    print("\n" + "=" * 50)
    print("  RESULTADO ÓPTIMO (Fuerza Bruta)")
    print("=" * 50)
    if mejor_solucion:
        print(f"  Mejor vector solución:    {mejor_solucion}")
        print(f"  Mejor Función Objetivo:   {mejor_valor}")
    else:
        print("  No se encontraron soluciones factibles.")
    print(f"  Soluciones evaluadas:     {soluciones_evaluadas}")
    print(f"  Tiempo de ejecución:      {tiempo_total:.6f} segundos")
    print("=" * 50)


# ===========================================================================
#  EJECUCIÓN DEL PROGRAMA
# ===========================================================================

if __name__ == "__main__":
    print("-" * 50)
    print("=== MKP SOLVER ===")
    print("-" * 50)
    
    # --- Rutas de archivos ---
    archivo_instancia = "instancias/mkp_instance.txt"
    archivo_solucion1 = "instancias/solucion_ejemplo.txt"
    archivo_solucion2 = "instancias/solucion_ejemplo2.txt"
    
    # --- Lectura de instancia ---
    try:
        instancia = leer_instancia(archivo_instancia)
        mostrar_instancia(instancia)
    except Exception as e:
        print(f"Error cargando la instancia: {e}")
        sys.exit(1)
        
    # --- Lectura y verificación de solución 1 ---
    try:
        solucion1 = leer_solucion(archivo_solucion1, instancia['n'])
        imprimir_verificacion(solucion1, instancia)
        valor_fo1 = calcular_funcion_objetivo(solucion1, instancia)
        print(f"  Función Objetivo de esta solución: {valor_fo1}")
    except Exception as e:
        print(f"Error cargando la solución 1: {e}")
        solucion1 = None
    
    # --- Lectura y verificación de solución 2 ---
    try:
        solucion2 = leer_solucion(archivo_solucion2, instancia['n'])
        imprimir_verificacion(solucion2, instancia)
        valor_fo2 = calcular_funcion_objetivo(solucion2, instancia)
        print(f"  Función Objetivo de esta solución: {valor_fo2}")
    except Exception as e:
        print(f"Error cargando la solución 2: {e}")
        solucion2 = None
    
    # --- Comparación de soluciones ---
    if solucion1 and solucion2:
        comparar_soluciones(solucion1, solucion2, instancia)
    
    # --- Búsqueda exhaustiva ---
    print("\nIniciando algoritmo de Fuerza Bruta...")
    busqueda_exhaustiva(instancia)

