# Validaciones del Proyecto

Este documento describe todas las validaciones implementadas en el proyecto y cómo asegurarse de que pasen correctamente.

## Pre-commit Hooks

Los pre-commit hooks son validaciones que se ejecutan automáticamente antes de cada commit. Para instalarlos:

```bash
pip install pre-commit
pre-commit install
```

### Lista de Validaciones

1. **Formateo de Código**
   - `trim trailing whitespace`: Elimina espacios en blanco al final de las líneas
   - `fix end of files`: Asegura que los archivos terminen con una nueva línea
   - `black`: Formatea el código Python según el estándar de Black
   - `isort`: Ordena las importaciones automáticamente

2. **Verificación de Sintaxis y Estilo**
   - `check python ast`: Verifica la sintaxis de Python
   - `check yaml`: Valida archivos YAML
   - `check json`: Valida archivos JSON
   - `flake8`: Verifica el estilo del código con varios plugins:
     - `flake8-builtins`: Evita sobrescribir nombres builtin
     - `flake8-pytest-style`: Verifica el estilo de los tests
     - `flake8-variables-names`: Verifica nombres de variables
     - `flake8-simplify`: Sugiere simplificaciones de código

3. **Seguridad**
   - `check for merge conflicts`: Detecta conflictos de merge no resueltos
   - `detect private key`: Previene commits de claves privadas
   - `bandit`: Análisis de seguridad del código Python

4. **Documentación**
   - `check docstring is first`: Verifica que los docstrings estén al inicio
   - `interrogate`: Verifica cobertura de docstrings (mínimo 95%)

5. **Tipado**
   - `mypy`: Verifica anotaciones de tipos

6. **Complejidad**
   - `complexity-check`: Verifica la complejidad del código usando `xenon`

### Cómo Pasar las Validaciones

1. **Formateo de Código**
   ```bash
   # Formatear código automáticamente
   black .
   isort .
   ```

2. **Docstrings**
   - Usar el estilo Google para docstrings
   - Incluir secciones: Args, Returns, Raises (cuando aplique)
   - Ejemplo:
   ```python
   def function(arg1: str, arg2: int) -> bool:
       """Descripción de la función.

       Args:
           arg1: Descripción del primer argumento
           arg2: Descripción del segundo argumento

       Returns:
           Descripción del valor retornado

       Raises:
           ValueError: Descripción de cuándo se lanza
       """
   ```

3. **Anotaciones de Tipos**
   - Agregar tipos a todos los argumentos de funciones
   - Agregar tipos de retorno
   - Usar tipos del módulo `typing` para casos complejos
   ```python
   from typing import List, Dict, Optional

   def process_data(items: List[str]) -> Dict[str, int]:
       ...
   ```

4. **Tests**
   - Nombrar tests con prefijo `test_`
   - Incluir docstring explicativo
   - Usar fixtures de pytest cuando sea posible
   - Asegurar cobertura mínima del 80%

## Validación de la Estructura del Proyecto

El proyecto requiere la siguiente estructura de directorios:
```
.
├── data/
│   ├── raw/
│   ├── processed/
│   └── interim/
├── models/
├── notebooks/
├── src/
├── utils/
└── visualization/
```

## Validación de Dependencias

1. Asegurar que todas las dependencias estén en `requirements.txt`
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar Todas las Validaciones

```bash
# Ejecutar pre-commit en todos los archivos
pre-commit run --all-files

# Ejecutar tests con cobertura
pytest --cov=src

# Ejecutar validación del pipeline
python -m src.utils.validate_pipeline
```

## Solución de Problemas Comunes

1. **Error de docstring faltante**
   - Agregar docstring al inicio del módulo/clase/función
   - Asegurar que siga el formato Google

2. **Error de tipo**
   - Agregar anotaciones de tipo faltantes
   - Verificar que los tipos sean correctos
   - Usar `Optional` para valores que pueden ser None

3. **Error de complejidad**
   - Dividir funciones largas en funciones más pequeñas
   - Reducir niveles de anidamiento
   - Simplificar lógica compleja

4. **Error de estilo**
   - Ejecutar `black` y `isort`
   - Seguir recomendaciones de `flake8`
   - Mantener líneas cortas (máximo 88 caracteres)
