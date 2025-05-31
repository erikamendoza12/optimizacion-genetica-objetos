import random
import matplotlib.pyplot as plt
from itertools import combinations

def generar_objetos(datos_objetos):
    objetos = []
    for datos in datos_objetos:
        nombre = datos[0]
        peso = datos[1]
        importancia = datos[2]
        codigo = datos[3]
        objetos.append((nombre, peso, importancia, codigo))
    return objetos


def generar_combinaciones(objetos, N):
    combinaciones = []
    for _ in range(N):
        combinacion = []
        peso_total = 0
        while peso_total <= 10:
            objeto = random.choice(objetos)
            if peso_total + objeto[1] <= 10:
                combinacion.append(objeto)
                peso_total += objeto[1]
            else:
                break
        combinaciones.append(combinacion)
    return combinaciones


def seleccionar_objetos(combinaciones, mejores_FA, lista1_anterior, lista2_anterior):
    mejores_objetos = []
    lista1 = None
    lista2 = None
    
    if not mejores_FA:
        for combo in combinaciones:
            peso_total = sum(obj[1] for obj in combo)
            fa = sum(obj[2] for obj in combo) - (peso_total * 0.5)
            if fa > 0:
                # Agregar la combinación junto con su FA a la lista de mejores objetos
                mejores_objetos.append((combo, fa))

        # Ordenar las combinaciones por su valor de FA en orden descendente
        mejores_objetos.sort(key=lambda x: x[1], reverse=True)

        # Seleccionar las dos primeras combinaciones con mayor FA
        lista1 = mejores_objetos[0][0]
        lista2 = mejores_objetos[1][0]
    
    if mejores_FA:
        for combo in combinaciones:
            peso_total = sum(obj[1] for obj in combo)
            fa = sum(obj[2] for obj in combo) - (peso_total * 0.5)
            if fa > 0:
                # Agregar la combinación junto con su FA a la lista de mejores objetos
                mejores_objetos.append((combo, fa))

        # Ordenar las combinaciones por su valor de FA en orden descendente
        mejores_objetos.sort(key=lambda x: x[1], reverse=True)

        FA_compro = mejores_objetos[0][1]

        if FA_compro >= max(mejores_FA):
            lista1 = mejores_objetos[0][0]
            lista2 = mejores_objetos[1][0]
        else:
            # Si el mayor FA de esta generación es menor que el de la anterior,
            # se mantienen las listas de la iteración anterior
            lista1 = lista1_anterior
            lista2 = lista2_anterior

    return lista1, lista2






def cruza_objetos(lista1, lista2):
    # Calcular la cantidad de objetos a seleccionar de cada lista
    num_objetos = len(lista1)
    mitad = num_objetos // 2
    
    # Seleccionar el 50% de los objetos de la primer lista
    hijos1 = lista1[:mitad]
    # Seleccionar el 50% de los objetos de la segunda lista
    hijos2 = lista2[:mitad]
    
    # Agregar el otro 50% de los objetos de la segunda lista a los hijos de la primer lista
    hijos1.extend(lista2[mitad:])
    # Agregar el otro 50% de los objetos de la primer lista a los hijos de la segunda lista
    hijos2.extend(lista1[mitad:])
    
    # Mezclar los objetos en los hijos
    random.shuffle(hijos1)
    random.shuffle(hijos2)
    
    return hijos1, hijos2




def mutar_objetos(hijos1, hijos2, Pm):
    objetos_mutados_1 = []
    objetos_mutados_2 = []
    
    for objeto in hijos1:
        # Aplicar mutación con probabilidad Pm
        if random.random() < Pm:
            nuevo_codigo = objeto[3]  # Usar el nuevo código generado en la función de cruce
            # Cambiar el primer número del código
            nuevo_codigo = nuevo_codigo[:1] + ('1' if nuevo_codigo[1] == '0' else '0') + nuevo_codigo[2:]
            nuevo_peso = objeto[1] 
            nuevo_valor = objeto[2] 
            
            # Agregar el objeto mutado a la lista de objetos mutados
            objetos_mutados_1.append((objeto[0], nuevo_peso, nuevo_valor, nuevo_codigo))
        else:
            # Si no se muta, agregar el objeto original a la lista de objetos mutados
            objetos_mutados_1.append(objeto)

    for objeto in hijos2:
        # Aplicar mutación con probabilidad Pm
        if random.random() < Pm:
            nuevo_codigo = objeto[3]  # Usar el nuevo código generado en la función de cruce
            # Cambiar el primer número del código
            nuevo_codigo = nuevo_codigo[:1] + ('1' if nuevo_codigo[1] == '0' else '0') + nuevo_codigo[2:]
            nuevo_peso = objeto[1] 
            nuevo_valor = objeto[2]  
            
            # Agregar el objeto mutado a la lista de objetos mutados
            objetos_mutados_2.append((objeto[0], nuevo_peso, nuevo_valor, nuevo_codigo))
        else:
            # Si no se muta, agregar el objeto original a la lista de objetos mutados
            objetos_mutados_2.append(objeto)
    
    
    return objetos_mutados_1, objetos_mutados_2




def seleccionar_elitismo(objetos_mutados_1, objetos_mutados_2, mejores_FA):
    # Calcular el valor total y el peso total para la lista 1
    valor_total_1 = sum(objeto[2] for objeto in objetos_mutados_1)
    peso_total_1 = sum(objeto[1] for objeto in objetos_mutados_1)
    # Calcular el valor total y el peso total para la lista 2
    valor_total_2 = sum(objeto[2] for objeto in objetos_mutados_2)
    peso_total_2 = sum(objeto[1] for objeto in objetos_mutados_2)
    
    # Calcular el FA para la lista 1 y 2
    fa_1 = valor_total_1 - (peso_total_1 * 0.5)
    fa_2 = valor_total_2 - (peso_total_2 * 0.5)
    
    nueva_generacion = objetos
    
    # Comparar los factores de aptitud y guardar el mejor
    if fa_1 > fa_2:
        mejores_FA.append(fa_1)
        nueva_generacion.extend(objetos_mutados_1)
        print(objetos_mutados_1)
        print("Valor total:", valor_total_1)
        print("Peso total:", peso_total_1)
    else:
        mejores_FA.append(fa_2)
        nueva_generacion.extend(objetos_mutados_2)
        print(objetos_mutados_2)
        print("Valor total:", valor_total_2)
        print("Peso total:", peso_total_2)
    
    
    return nueva_generacion, mejores_FA



# Valores de N y Pm a probar
valores_N = [10, 100, 1000]
valores_Pm = [0.1, 0.01, 0.001]

# Pm con su grado de mutación correspondiente
grado_mutacion = [0.1, 0.01, 0.001]

# Datos de los objetos
datos_objetos = [
    ("Botella de agua", 1, 10, "000011"),
    ("Comida enlatada", 2, 15, "001010"),
    ("Botiquín de primeros auxilios", 1.5, 20, "010001"),
    ("Linterna", 0.5, 12, "100110"),
    ("Baterías", 0.3, 6, "111000"),
    ("Tienda de campaña", 3, 25, "101010"),
    ("Pala", 2.5, 10, "011001"),
    ("Fósforos", 0.05, 4, "110011"),
    ("Cuchillo", 1, 14, "010101"),
    ("Manta térmica", 0.8, 18, "001100"),
    ("Cuerda", 1.2, 7, "100001"),
    ("Mapa", 0.1, 7, "011110"),
    ("Saco de dormir", 1.5, 25, "101100"),
    ("Repelente de insectos", 0.2, 8, "110000"),
    ("Kit de herramientas", 2.0, 20, "001111"),
    ("Medicina", 0.5, 35, "111100"),
    ("Machete", 1.8, 14, "010010"),
    ("Radio de comunicación", 0.8, 20, "100000"),
    ("Paquete de semillas", 0.2, 10, "011000"),
    ("Lámpara solar portátil", 0.6, 18, "000101")
]

for N in valores_N:
    for Pm in valores_Pm:

        # Número de generaciones
        G = 10

        # Listas para almacenar los valores de FA del mejor objeto en cada generación
        mejores_FA = []

        # Generar objetos iniciales
        objetos = generar_objetos(datos_objetos)
        
        # Variables para mantener un seguimiento de las listas seleccionadas en la iteración anterior
        lista1_anterior = None
        lista2_anterior = None
        
        for generacion in range(G):
            
            combinaciones = generar_combinaciones(objetos, N)
    
            lista1, lista2 = seleccionar_objetos(combinaciones, mejores_FA, lista1_anterior, lista2_anterior)
            
            # Cruzar objetos seleccionados
            hijos1, hijos2 = cruza_objetos(lista1, lista2)

            # Mutar objetos cruzados
            objetos_mutados_1, objetos_mutados_2 = mutar_objetos(hijos1, hijos2, Pm)

            # Aplicar elitismo para agregar el mejor objeto a la lista principal
            objetos, mejores_FA = seleccionar_elitismo(objetos_mutados_1, objetos_mutados_2, mejores_FA)

            # Actualizar las listas seleccionadas para la próxima iteración
            lista1_anterior = lista1
            lista2_anterior = lista2

        G = len(mejores_FA)

        # Graficar los valores de FA del mejor objeto por generación
        plt.plot(range(1, G+1), mejores_FA, marker='o')
        plt.title(f'Evolución de la función de aptitud del mejor objeto (N={N}, Pm={Pm})')
        plt.xlabel('Generación')
        plt.ylabel('Valor de la función de aptitud (FA)')
        plt.grid(True)

        # Agregar los valores correspondientes encima de los puntos
        for i, valor in enumerate(mejores_FA):
            plt.text(i+1, valor, str(valor), ha='center', va='bottom')

        plt.show()

        
