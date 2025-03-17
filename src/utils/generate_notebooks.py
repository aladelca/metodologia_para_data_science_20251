"""Functions to generate educational Jupyter notebooks."""

from pathlib import Path
from typing import Dict

from utils.notebook_generator import Cells, code_cell, create_notebook, markdown_cell


def generate_basic_concepts() -> Cells:
    """Generate notebook about basic Python concepts."""
    cells = [
        markdown_cell(
            """# Conceptos Básicos de Python

Este notebook introduce los conceptos fundamentales de Python que necesitarás para el
análisis de datos y machine learning.

## Contenido
1. Variables y Tipos de Datos
2. Operadores
3. Entrada/Salida Básica
4. Comentarios y Documentación"""
        ),
        markdown_cell(
            """## 1. Variables y Tipos de Datos

Python es un lenguaje de tipado dinámico, lo que significa que no necesitas declarar el
tipo de una variable explícitamente."""
        ),
        code_cell(
            """# Tipos numéricos
entero = 42
flotante = 3.14159
complejo = 3 + 4j

print(f"entero: {entero} (tipo: {type(entero)})")
print(f"flotante: {flotante} (tipo: {type(flotante)})")
print(f"complejo: {complejo} (tipo: {type(complejo)})")"""
        ),
        code_cell(
            """# Cadenas de texto
nombre = "Ada Lovelace"
descripcion = '''Primera programadora:
Escribió el primer algoritmo para ser
procesado por una máquina.'''

print(f"nombre: {nombre}")
print(f"descripción:\\n{descripcion}")"""
        ),
        code_cell(
            """# Booleanos
verdadero = True
falso = False

print(f"verdadero: {verdadero}")
print(f"falso: {falso}")"""
        ),
        markdown_cell(
            """## 2. Operadores

Python proporciona varios tipos de operadores para trabajar con variables."""
        ),
        code_cell(
            """# Operadores aritméticos
a = 10
b = 3

print(f"Suma: {a + b}")
print(f"Resta: {a - b}")
print(f"Multiplicación: {a * b}")
print(f"División: {a / b}")
print(f"División entera: {a // b}")
print(f"Módulo: {a % b}")
print(f"Potencia: {a ** b}")"""
        ),
        code_cell(
            """# Operadores de comparación
x = 5
y = 10

print(f"x = {x}, y = {y}")
print(f"x < y: {x < y}")
print(f"x > y: {x > y}")
print(f"x <= y: {x <= y}")
print(f"x >= y: {x >= y}")
print(f"x == y: {x == y}")
print(f"x != y: {x != y}")"""
        ),
        markdown_cell(
            """## 3. Entrada/Salida Básica

Python proporciona funciones integradas para la entrada y salida de datos."""
        ),
        code_cell(
            """# Función print() para salida
nombre = "Juan"
edad = 25
# Diferentes formas de usar print()
print("Hola Mundo")
print("Nombre:", nombre)
print(f"Edad: {edad}")  # f-strings (recomendado)
print("Mi nombre es {0} y tengo {1} años".format(nombre, edad))"""
        ),
        markdown_cell(
            """La función `input()` se usa para obtener entrada del usuario:
```python
nombre = input("Ingresa tu nombre: ")
edad = int(input("Ingresa tu edad: "))
```

**Nota**: En Jupyter, es mejor usar variables predefinidas para los ejemplos."""
        ),
        markdown_cell(
            """## 4. Comentarios y Documentación

Los comentarios son fundamentales para hacer el código más comprensible."""
        ),
        code_cell(
            """# Esto es un comentario de una línea

'''
Esto es un comentario
de múltiples líneas
usando comillas simples
'''

\"\"\"
También puedes usar
comillas dobles para
comentarios multilínea
\"\"\"

def suma(a, b):
    \"\"\"
    Suma dos números y retorna el resultado.

    Args:
        a (int): Primer número
        b (int): Segundo número

    Returns:
        int: La suma de a y b
    \"\"\"
    return a + b

# Ejemplo de uso de la función documentada
resultado = suma(5, 3)
print(f"5 + 3 = {resultado}")

# Ver la documentación
help(suma)"""
        ),
    ]

    return cells


def generate_control_structures() -> Cells:
    """Generate notebook about control structures."""
    cells = [
        markdown_cell(
            """# Estructuras de Control en Python

Este notebook cubre las estructuras de control fundamentales en Python.

## Contenido
1. Condicionales (if, elif, else)
2. Bucles (for, while)
3. Control de Bucles (break, continue)
4. Manejo de Excepciones (try/except)"""
        ),
        markdown_cell(
            """## 1. Condicionales

Las estructuras condicionales permiten ejecutar diferentes bloques de código según se
cumplan ciertas condiciones."""
        ),
        code_cell(
            """# Ejemplo básico de if
edad = 18

if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")

# Ejemplo con elif
nota = 85

if nota >= 90:
    print("A - Excelente")
elif nota >= 80:
    print("B - Bueno")
elif nota >= 70:
    print("C - Regular")
else:
    print("D - Necesita mejorar")"""
        ),
        markdown_cell(
            """## 2. Bucles

Python proporciona dos tipos principales de bucles: `for` y `while`."""
        ),
        code_cell(
            """# Bucle for con range
print("Contando del 1 al 5:")
for i in range(1, 6):
    print(i)

# Bucle for con lista
frutas = ["manzana", "banana", "naranja"]
print("\\nLista de frutas:")
for fruta in frutas:
    print(fruta)

# Bucle while
print("\\nCuenta regresiva:")
contador = 5
while contador > 0:
    print(contador)
    contador -= 1
print("¡Despegue!")"""
        ),
        markdown_cell(
            """## 3. Control de Bucles

Las declaraciones `break` y `continue` permiten un control más fino sobre los bucles."""
        ),
        code_cell(
            """# Ejemplo de break
print("Buscando el primer número par:")
for num in range(1, 10, 2):  # Números impares
    if num * 2 > 10:
        break
    print(f"{num} * 2 = {num * 2}")
print("Bucle terminado\\n")

# Ejemplo de continue
print("Números del 1 al 5, saltando el 3:")
for i in range(1, 6):
    if i == 3:
        continue
    print(i)"""
        ),
        markdown_cell(
            """## 4. Manejo de Excepciones

El manejo de excepciones permite manejar errores de forma elegante."""
        ),
        code_cell(
            """# Ejemplo básico de try/except
def dividir(a, b):
    try:
        resultado = a / b
        print(f"{a} / {b} = {resultado}")
    except ZeroDivisionError:
        print("¡Error! No se puede dividir por cero")
    except TypeError:
        print("¡Error! Los argumentos deben ser números")
    finally:
        print("Operación completada")

# Probando la función
print("Caso 1: División normal")
dividir(10, 2)

print("\\nCaso 2: División por cero")
dividir(10, 0)

print("\\nCaso 3: Tipo de dato incorrecto")
dividir(10, "2"))"""
        ),
    ]

    return cells


def generate_functions() -> Cells:
    """Generate notebook about functions."""
    cells = [
        markdown_cell(
            """# Funciones en Python

Este notebook explora el uso de funciones en Python, una herramienta fundamental para la
organización y reutilización de código.

## Contenido
1. Definición y Llamada de Funciones
2. Argumentos y Parámetros
3. Retorno de Valores
4. Funciones Lambda
5. Decoradores"""
        ),
        markdown_cell(
            """## 1. Definición y Llamada de Funciones

Las funciones se definen usando la palabra clave `def`."""
        ),
        code_cell(
            """# Función básica
def saludar():
    print("¡Hola, mundo!")

# Llamada a la función
saludar()

# Función con documentación
def saludar_persona(nombre):
    \"\"\"
    Saluda a una persona por su nombre.

    Args:
        nombre (str): Nombre de la persona a saludar
    \"\"\"
    print(f"¡Hola, {nombre}!")

saludar_persona("Ana")"""
        ),
        markdown_cell(
            """## 2. Argumentos y Parámetros

Python ofrece varias formas de pasar argumentos a las funciones."""
        ),
        code_cell(
            """# Parámetros posicionales y con valores por defecto
def describir_persona(nombre, edad=25, ciudad="desconocida"):
    print(f"{nombre} tiene {edad} años y vive en {ciudad}")

describir_persona("Juan")
describir_persona("María", 30)
describir_persona("Pedro", ciudad="Madrid")

# Args y kwargs
def info_contacto(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

info_contacto("Juan", "Pedro", email="juan@mail.com", tel="123456789")"""
        ),
        markdown_cell(
            """## 3. Retorno de Valores

Las funciones pueden retornar uno o múltiples valores."""
        ),
        code_cell(
            """# Retorno simple
def cuadrado(x):
    return x ** 2

# Retorno múltiple
def estadisticas(numeros):
    return min(numeros), max(numeros), sum(numeros)/len(numeros)

# Uso de las funciones
print(f"El cuadrado de 5 es {cuadrado(5)}")

nums = [1, 2, 3, 4, 5]
minimo, maximo, promedio = estadisticas(nums)
print(f"Mínimo: {minimo}, Máximo: {maximo}, Promedio: {promedio:.2f}")"""
        ),
        markdown_cell(
            """## 4. Funciones Lambda

Las funciones lambda son funciones anónimas de una sola línea."""
        ),
        code_cell(
            """# Función lambda básica
cubo = lambda x: x ** 3

# Uso con map
numeros = [1, 2, 3, 4, 5]
cubos = list(map(lambda x: x ** 3, numeros))

print(f"Números: {numeros}")
print(f"Cubos: {cubos}")

# Uso con filter
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(f"Números pares: {pares}")"""
        ),
        markdown_cell(
            """## 5. Decoradores

Los decoradores son funciones que modifican el comportamiento de otras funciones."""
        ),
        code_cell(
            """def mi_decorador(func):
    def wrapper():
        print("Antes de la función")
        func()
        print("Después de la función")
    return wrapper

@mi_decorador
def saludar():
    print("¡Hola!")

# Llamada a la función decorada
saludar()

# Decorador con argumentos
def repetir(veces):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(3)
def mensaje(texto):
    print(texto)

mensaje("¡Hola!")"""
        ),
    ]

    return cells


def generate_classes() -> Cells:
    """Generate notebook about classes and OOP."""
    cells = [
        markdown_cell(
            """# Clases y Programación Orientada a Objetos en Python

Este notebook explora los conceptos fundamentales de la Programación Orientada a Objetos
(POO) en Python.

## Contenido
1. Definición de Clases
2. Herencia
3. Encapsulación
4. Polimorfismo
5. Métodos Especiales"""
        ),
        markdown_cell(
            """## 1. Definición de Clases

Una clase es una plantilla para crear objetos que encapsulan datos y comportamiento."""
        ),
        code_cell(
            """class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def presentarse(self):
        return f"Hola, soy {self.nombre} y tengo {self.edad} años"

# Crear instancias de la clase
persona1 = Persona("Ana", 25)
persona2 = Persona("Juan", 30)

print(persona1.presentarse())
print(persona2.presentarse())"""
        ),
        markdown_cell(
            """## 2. Herencia

La herencia permite crear nuevas clases basadas en clases existentes."""
        ),
        code_cell(
            """class Empleado(Persona):
    def __init__(self, nombre, edad, salario):
        super().__init__(nombre, edad)
        self.salario = salario

    def presentarse(self):
        return f"{super().presentarse()} y gano {self.salario}€"

# Crear una instancia de Empleado
empleado = Empleado("Carlos", 35, 30000)
print(empleado.presentarse())"""
        ),
        markdown_cell(
            """## 3. Encapsulación

La encapsulación permite ocultar los detalles internos de una clase."""
        ),
        code_cell(
            """class CuentaBancaria:
    def __init__(self, saldo_inicial):
        self.__saldo = saldo_inicial  # Atributo privado

    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
            return True
        return False

    def retirar(self, cantidad):
        if 0 < cantidad <= self.__saldo:
            self.__saldo -= cantidad
            return True
        return False

    def obtener_saldo(self):
        return self.__saldo

# Usar la cuenta bancaria
cuenta = CuentaBancaria(1000)
print(f"Saldo inicial: {cuenta.obtener_saldo()}€")

cuenta.depositar(500)
print(f"Después de depositar 500€: {cuenta.obtener_saldo()}€")

cuenta.retirar(200)
print(f"Después de retirar 200€: {cuenta.obtener_saldo()}€")"""
        ),
        markdown_cell(
            """## 4. Polimorfismo

El polimorfismo permite que objetos de diferentes clases respondan al mismo método."""
        ),
        code_cell(
            """class Animal:
    def hacer_sonido(self):
        pass

class Perro(Animal):
    def hacer_sonido(self):
        return "¡Guau!"

class Gato(Animal):
    def hacer_sonido(self):
        return "¡Miau!"

# Función que trabaja con cualquier Animal
def escuchar_animal(animal):
    print(f"El animal dice: {animal.hacer_sonido()}")

# Crear instancias y usar polimorfismo
perro = Perro()
gato = Gato()

escuchar_animal(perro)
escuchar_animal(gato)"""
        ),
        markdown_cell(
            """## 5. Métodos Especiales

Los métodos especiales (también conocidos como métodos mágicos) definen el "
comportamiento de los objetos en diferentes situaciones."""
        ),
        code_cell(
            """class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, otro):
        return Vector(self.x + otro.x, self.y + otro.y)

    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

# Usar los métodos especiales
v1 = Vector(2, 3)
v2 = Vector(3, 4)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"Longitud de v1: {len(v1)}")
print(f"¿v1 == v2? {v1 == v2}")"""
        ),
    ]

    return cells


def generate_error_handling() -> Cells:
    """Generate notebook about error handling."""
    cells = [
        markdown_cell(
            """# Manejo de Errores en Python

Este notebook explora las técnicas de manejo de errores y excepciones en Python.

## Contenido
1. Tipos de Errores Comunes
2. Try/Except
3. Raise
4. Finally y Else
5. Creación de Excepciones Personalizadas"""
        ),
        markdown_cell(
            """## 1. Tipos de Errores Comunes

Python tiene varios tipos de errores incorporados."""
        ),
        code_cell(
            """# TypeError
try:
    resultado = "2" + 2
except TypeError as e:
    print(f"TypeError: {e}")

# ZeroDivisionError
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"ZeroDivisionError: {e}")

# IndexError
try:
    lista = [1, 2, 3]
    elemento = lista[5]
except IndexError as e:
    print(f"IndexError: {e}")

# KeyError
try:
    diccionario = {"a": 1, "b": 2}
    valor = diccionario["c"]
except KeyError as e:
    print(f"KeyError: {e}")"""
        ),
        markdown_cell(
            """## 2. Try/Except

El bloque try/except es la base del manejo de errores."""
        ),
        code_cell(
            """def dividir_numeros(a, b):
    try:
        resultado = a / b
        return resultado
    except ZeroDivisionError:
        return "No se puede dividir por cero"
    except TypeError:
        return "Ambos valores deben ser números"

# Probar la función
print(dividir_numeros(10, 2))
print(dividir_numeros(10, 0))
print(dividir_numeros(10, "2"))

# Capturar múltiples excepciones
def procesar_dato(dato):
    try:
        num = float(dato)
        resultado = 10 / num
        return resultado
    except (ValueError, ZeroDivisionError) as e:
        return f"Error: {type(e).__name__} - {str(e)}"

print(procesar_dato("abc"))
print(procesar_dato("0"))"""
        ),
        markdown_cell(
            """## 3. Raise

`raise` permite lanzar excepciones manualmente."""
        ),
        code_cell(
            """def validar_edad(edad):
    if not isinstance(edad, int):
        raise TypeError("La edad debe ser un número entero")
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    if edad > 150:
        raise ValueError("Edad no válida")
    return "Edad válida"

# Probar la función
try:
    print(validar_edad(25))
    print(validar_edad(-5))
except ValueError as e:
    print(f"Error de validación: {e}")"""
        ),
        markdown_cell(
            """## 4. Finally y Else

`finally` se ejecuta siempre, mientras que `else` solo si no hay excepciones."""
        ),
        code_cell(
            """def procesar_archivo(nombre):
    try:
        f = open(nombre, 'r')
    except FileNotFoundError:
        print("El archivo no existe")
    else:
        print("Archivo abierto exitosamente")
        f.close()
    finally:
        print("Proceso terminado")

# Probar con un archivo que no existe
procesar_archivo("archivo_inexistente.txt")

# Ejemplo con else
def convertir_a_entero(texto):
    try:
        numero = int(texto)
    except ValueError:
        print("No se pudo convertir a entero")
    else:
        print("Conversión exitosa")
        return numero
    finally:
        print("Proceso de conversión terminado")

print(convertir_a_entero("123"))
print(convertir_a_entero("abc"))"""
        ),
        markdown_cell(
            """## 5. Creación de Excepciones Personalizadas

Podemos crear nuestras propias clases de excepciones."""
        ),
        code_cell(
            """class SaldoInsuficienteError(Exception):
    \"\"\"Excepción lanzada cuando no hay suficiente saldo.\"\"\"
    def __init__(self, saldo, cantidad):
        self.saldo = saldo
        self.cantidad = cantidad
        self.mensaje = (
            f"No hay suficiente saldo. "
            f"Saldo: {saldo}€, Cantidad solicitada: {cantidad}€"
        )
        super().__init__(self.mensaje)

class CuentaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def retirar(self, cantidad):
        if cantidad > self.saldo:
            raise SaldoInsuficienteError(self.saldo, cantidad)
        self.saldo -= cantidad
        return f"Retiro exitoso. Nuevo saldo: {self.saldo}€"

# Probar la excepción personalizada
cuenta = CuentaBancaria(100)

try:
    print(cuenta.retirar(50))
    print(cuenta.retirar(100))
except SaldoInsuficienteError as e:
    print(f"Error: {e}")"""
        ),
    ]

    return cells


def generate_code_standards() -> Cells:
    """Generate notebook about Python code standards."""
    cells: Cells = []

    # Introduction
    cells.append(
        markdown_cell(
            """# Estándares de Código en Python

Este notebook explora las mejores prácticas y estándares para escribir código Python
de alta calidad."""
        )
    )

    # PEP 8 section
    cells.append(
        markdown_cell(
            """## 1. PEP 8 - Guía de Estilo

La guía de estilo oficial para código Python."""
        )
    )

    # Code examples
    cells.append(
        code_cell(
            """# Ejemplos de nombres
nombre_usuario = "Juan"  # snake_case para variables
MAX_INTENTOS = 3  # UPPER_CASE para constantes

class UsuarioRegistrado:  # PascalCase para clases
    def __init__(self):
        self._saldo = 0  # underscore para privados"""
        )
    )

    # Type hints section
    cells.append(
        markdown_cell(
            """## 2. Type Hints

Las anotaciones de tipo mejoran la robustez del código."""
        )
    )

    cells.append(
        code_cell(
            """from typing import List, Dict, Optional

def procesar_datos(valores: List[float]) -> Dict[str, float]:
    return {"media": sum(valores) / len(valores)}"""
        )
    )

    # Testing section
    cells.append(
        markdown_cell(
            """## 3. Testing

El testing es fundamental para la calidad del código."""
        )
    )

    cells.append(
        code_cell(
            """import pytest

def test_suma():
    assert 1 + 1 == 2"""
        )
    )

    # SOLID principles
    cells.append(
        markdown_cell(
            """## 4. Principios SOLID

Principios fundamentales para código mantenible."""
        )
    )

    cells.append(
        code_cell(
            """from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangulo(Figura):
    def area(self) -> float:
        return self.base * self.altura"""
        )
    )

    return cells


def main() -> None:
    """Generate all notebooks."""
    notebooks: Dict[str, Cells] = {
        "01_conceptos_basicos.ipynb": generate_basic_concepts(),
        "02_estructuras_control.ipynb": generate_control_structures(),
        "03_funciones.ipynb": generate_functions(),
        "04_clases.ipynb": generate_classes(),
        "05_manejo_errores.ipynb": generate_error_handling(),
        "06_estandares_codigo.ipynb": generate_code_standards(),
    }

    base_path = Path(__file__).parent.parent / "notebooks" / "learning_path"
    base_path.mkdir(parents=True, exist_ok=True)

    for filename, cells in notebooks.items():
        output_path = base_path / filename
        create_notebook(cells, output_path)
        print(f"Created notebook: {output_path}")


if __name__ == "__main__":
    main()
