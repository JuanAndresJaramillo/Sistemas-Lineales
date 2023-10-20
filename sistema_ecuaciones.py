

import numpy as np  # Importa la biblioteca NumPy

class SistemasLineales:
    """
    Clase que nos permite trabajar con sistemas matriciales para darle solución a estos
    """

    # Método constructor
    def __init__(self, nombre_archivo):
        """
        Inicializa una instancia de la clase y recibe el nombre del archivo como parámetro.
        """
        self.nombre_archivo = nombre_archivo
        try:
            archivo = open(self.nombre_archivo, 'r')  # Abre el archivo en modo lectura.
            self.datos = archivo.read().split()  # Lee el contenido del archivo y lo divide en una lista.
        except FileNotFoundError:
            print('\n', '---'*15)
            print('El archivo no se ha encontrado')  # Mensaje de error si el archivo no se encuentra.
            print('---'*15, '\n')

    @property
    def mostrar_menu(self):
        """
        Propiedad que muestra un menú en la consola con los sistemas de ecuaciones disponibles en el archivo.
        """
        datos = self.datos
        indice_mostrar = 1
        indice = 0
        print('\n', '**'*10, 'Sistemas de Ecuaciones', '**'*10)
        for string in datos:
            if indice % 2 == 0:
                print(f'\n{indice_mostrar}.', end=" ")
            print(f'{string[0]} = [ {string[2:].replace(",", " ")} ]', end="  ")
            if indice % 2 != 0:
                indice_mostrar += 1
            indice += 1
        print('\n5. Salir\n')

    def extraer_vector(self, opc):
        """
        Extrae un vector a partir de los datos del archivo, dado un índice opc.
        """
        string = self.datos[2*opc - 1][2:].split(',')  # Divide y separa los elementos del vector.
        vector = []
        for element in string:
            num = int(element)  # Convierte cada elemento a entero.
            vector.append(num)
        return np.array(vector)  # Devuelve el vector como un array NumPy.

    def extraer_matriz(self, opc, vector_b):
        """
        Extrae una matriz a partir de los datos del archivo, dado un índice opc, y utiliza el vector_b para determinar su tamaño.
        """
        string = self.datos[2*opc - 2][2:].split(',')  # Divide y separa los elementos de la matriz.
        matriz = []
        for element in string:
            num = int(element)  # Convierte cada elemento a entero.
            matriz.append(num)
        matriz_numpy = np.array(matriz)
        matriz_ordenada = matriz_numpy.reshape((matriz_numpy.size // vector_b.size, vector_b.size))  # Reorganiza los datos en una matriz.
        return matriz_ordenada

    @staticmethod
    def mostrar_sistema(matriz, vector):
        """
        Muestra un sistema de ecuaciones en la consola utilizando la matriz y el vector recibidos como entrada.
        """
        i = 0
        for vectors in matriz:
            i += 1
            j = 0
            print(f'\n', end="")
            for elements in vectors:
                j += 1
                if (vector.size - 1) >= j:
                    print(f'{elements}*X{j} +', end=" ")  # Muestra la ecuación del sistema.
                else:
                    print(f'{elements}*X{j} = {vector[i-1]}')  # Muestra la ecuación final del sistema.

    @staticmethod
    def ingresar_opcion(mensaje):
        """
        Permite al usuario ingresar una opción de menú y valida que sea un número entre 1 y 5.
        """
        while True:
            try:
                opc = int(input(mensaje))  # Solicita al usuario que ingrese una opción.
                if opc > 5 or opc < 1:
                    raise TypeError('\nDigite una opción válida\n')  # Muestra un mensaje de error si la opción no es válida.
            except TypeError as mens:
                print(mens)
            except ValueError:
                print('\nSeleccione un número\n')  # Muestra un mensaje de error si no se ingresa un número.
            else:
                return opc

    @staticmethod
    def solucionar_sistema(matriz, vector):
        """
        Resuelve el sistema de ecuaciones lineales utilizando la función np.linalg.solve de NumPy.
        Muestra la solución en la consola y maneja casos en los que el sistema no tiene solución o tiene infinitas soluciones.
        """
        try:
            sol = np.linalg.solve(matriz, vector)  # Resuelve el sistema de ecuaciones.
            i = 0
            print('\n**************')
            for element in sol:
                i += 1
                print(f'X{i} = {round(element, 3)}')  # Muestra la solución con formato.
            print('**************\n')
        except np.linalg.LinAlgError:
            matriz_aumentada = np.column_stack((matriz, vector))
            rango_mat = np.linalg.matrix_rank(matriz)
            rango_mataumen = np.linalg.matrix_rank(matriz_aumentada)
            if rango_mat == rango_mataumen:
                print('\nEl sistema tiene infinitas soluciones\n')  # Muestra un mensaje si el sistema tiene infinitas soluciones.
            else:
                print('\nEl sistema no tiene solución\n')  # Muestra un mensaje si el sistema no tiene solución.

if __name__ == '__main__':
    arch = SistemasLineales('matrices.txt')  # Crea una instancia de la clase SistemasLineales con un archivo dado.
    while True:
        arch.mostrar_menu  # Muestra el menú en la consola.
        opcion = arch.ingresar_opcion('Seleccione el sistema lineal a resolver ')
        if opcion == 5:
            break  # Sale del bucle si se selecciona la opción 5 (Salir).
        else:
            vector = arch.extraer_vector(opcion)
            matriz = arch.extraer_matriz(opcion, vector)
            arch.mostrar_sistema(matriz, vector)  # Muestra el sistema de ecuaciones.
            arch.solucionar_sistema(matriz, vector)  # Resuelve el sistema y muestra la solución o un mensaje de error