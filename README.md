# Metodología para Data Science: Optimización de Estrategias de Inversiónnnn

Este repositorio contiene el código y recursos para el curso de Metodología para Data Science, enfocado en el desarrollo de estrategias óptimas de inversión para fondos provenientes de AFP utilizando técnicas de Machine Learning y optimización.

## Caso de Uso: Optimización de Portafolio de Inversión-

El proyecto se centra en desarrollar una estrategia de inversión óptima para fondos retirados de AFP, utilizando:

- Análisis de datos históricos de diferentes instrumentos financieros
- Algoritmos de Machine Learning para predicción de rendimientos
- Técnicas de optimización para la construcción de portafolios
- Evaluación de riesgo y retorno esperado
- Backtesting de estrategias

### Parámetros del Caso de Uso

- **Presupuesto**: 1,000,000 de soles peruanos
- **Horizonte de inversión**: 10 años
- **Opciones de inversión a evaluar**:
  1. Mantener los fondos en la AFP
  2. Invertir en bonos del tesoro
  3. Comprar propiedades y cobrar alquiler
  4. Invertir todo en el índice S&P 500 (ETF SPY)
  5. Diversificar en 100 acciones diferentes
  6. Invertir en oro

### Objetivos

1. Analizar el comportamiento histórico de las seis opciones de inversión
2. Desarrollar modelos predictivos para estimar rendimientos futuros en el horizonte de 10 años
3. Implementar algoritmos de optimización de portafolio considerando el presupuesto disponible
4. Evaluar y comparar las diferentes estrategias de inversión
5. Generar recomendaciones basadas en el perfil de riesgo del inversionista y el horizonte temporal definido

## Estructura del Repositorio

```
.
├── .github/            # Configuraciones de GitHub (workflows, settings)
├── src/               # Código fuente del proyecto
│   ├── data/          # Datos históricos de mercados financieros
│   ├── notebooks/     # Jupyter notebooks para análisis y backtesting
│   ├── models/        # Modelos de ML y optimización
│   ├── tests/         # Tests unitarios e integración
│   │   ├── unit/     # Tests unitarios
│   │   └── integration/ # Tests de integración
│   ├── utils/         # Funciones de utilidad
│   └── visualization/ # Visualizaciones y dashboards financieros
├── .gitignore        # Archivos y directorios ignorados por git
├── requirements.txt   # Dependencias del proyecto
└── README.md         # Este archivo
```

## Configuración del Entorno

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/aladelca/metodologia_para_data_science_20251.git
   cd metodologia_para_data_science_20251
   ```

2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar pre-commit hooks (IMPORTANTE):
   ```bash
   # Instalar pre-commit
   pip install pre-commit

   # Instalar los hooks en el repositorio
   pre-commit install

   # Verificar la instalación
   pre-commit --version

   # (Opcional) Ejecutar los hooks manualmente
   pre-commit run --all-files
   ```

   Los hooks se ejecutarán automáticamente en cada commit e incluyen:
   - Formateo de código (Black)
   - Verificación de estilo (Flake8)
   - Ordenamiento de imports (isort)
   - Verificación de tipos (mypy)
   - Ejecución de tests (pytest)
   - Verificación de dependencias

## Flujo de Trabajo con Git

1. Crear una nueva rama para tu trabajo:
   ```bash
   git checkout -b feature/[tus-iniciales]/[descripcion]
   ```

2. Realizar cambios y commits:
   ```bash
   git add .
   git commit -m "Descripción detallada de los cambios"
   ```

3. Subir cambios y crear Pull Request:
   ```bash
   git push origin feature/[tus-iniciales]/[descripcion]
   ```

4. Esperar la revisión del instructor (@aladelca)

## Metodología de Desarrollo (CRISP-DM)

1. **Comprensión del Negocio**
   - Definición de objetivos de inversión para el monto de 1,000,000 de soles
   - Identificación de restricciones legales y fiscales en Perú para cada opción
   - Definición del perfil de riesgo para un horizonte de 10 años
   - Establecimiento de métricas de éxito y rendimiento esperado
   - Planificación del proyecto

2. **Comprensión de los Datos**
   - Recopilación de datos históricos para cada opción de inversión:
     * Rendimiento histórico de fondos AFP
     * Rendimiento de bonos del tesoro peruano e internacional
     * Datos del mercado inmobiliario y retornos por alquiler
     * Rendimiento histórico del S&P 500
     * Datos de las 100 acciones a considerar en la diversificación
     * Comportamiento histórico del oro
   - Verificación de calidad de datos y tratamiento de series temporales
   - Identificación de fuentes adicionales de información macroeconómica

3. **Preparación de los Datos**
   - Limpieza y tratamiento de datos faltantes
   - Ajuste por inflación y tipo de cambio (USD/PEN)
   - Cálculo de indicadores financieros relevantes para cada clase de activo
   - Feature engineering para análisis técnico y fundamental
   - Normalización y transformación de variables
   - Preparación de conjuntos de entrenamiento y validación con series temporales

4. **Modelado**
   - Desarrollo de modelos predictivos para cada alternativa:
     * Predicción de rendimientos en AFPs
     * Proyección de tasas de interés para bonos
     * Modelos de valoración inmobiliaria y retornos por alquiler
     * Predicción de rendimientos para S&P 500
     * Modelos para la selección de las 100 acciones
     * Proyección del precio del oro
   - Implementación de algoritmos de optimización:
     * Comparación directa de alternativas
     * Optimización con restricciones de riesgo
     * Modelos de asignación de activos
   - Validación cruzada y ajuste de hiperparámetros

5. **Evaluación**
   - Backtesting de estrategias con datos históricos
   - Simulación de escenarios para el horizonte de 10 años
   - Análisis de robustez ante diferentes condiciones macroeconómicas
   - Evaluación de costos de transacción, impuestos y comisiones
   - Análisis de liquidez y accesibilidad de cada opción
   - Validación con expertos financieros

6. **Implementación**
   - Documentación detallada de la estrategia recomendada
   - Plan de implementación para el inversionista
   - Guía de monitoreo y ajustes para el horizonte de 10 años
   - Procedimientos de rebalanceo y toma de decisiones
   - Recomendaciones específicas para el contexto peruano

## Entregables por Fase

### 1. Comprensión del Negocio
- Documento de objetivos y restricciones específicas para inversión de 1,000,000 de soles
- Perfil de riesgo y expectativas para el horizonte de 10 años
- Plan de proyecto y definición de KPIs
- Análisis preliminar de las seis alternativas de inversión

### 2. Comprensión de los Datos
- Informe de calidad de datos históricos para cada alternativa de inversión
- Catálogo de fuentes de datos para AFP, bonos, propiedades, S&P 500, acciones diversificadas y oro
- Análisis exploratorio inicial con foco en rendimiento histórico a 10 años

### 3. Preparación de los Datos
- Pipeline de procesamiento de datos para las seis opciones de inversión
- Documentación de features generados relevantes para cada clase de activo
- Ajuste de datos por inflación y tipo de cambio (soles peruanos)
- Conjuntos de datos procesados para modelado

### 4. Modelado
- Notebooks con implementación de modelos predictivos para cada alternativa
- Modelos de optimización considerando el monto de 1,000,000 de soles
- Simulación de escenarios para el horizonte de 10 años
- Documentación de parámetros y decisiones
- Resultados de validación comparativos

### 5. Evaluación
- Reportes de rendimiento proyectado a 10 años
- Análisis de riesgo ajustado al horizonte temporal
- Comparativas con benchmarks para cada clase de activo
- Evaluación de costos de transacción e impuestos aplicables en Perú

### 6. Implementación
- Recomendación final entre las seis opciones evaluadas
- Código documentado para replicar el análisis
- Manual de usuario para implementación práctica de la estrategia
- Guía de rebalanceo para el horizonte de 10 años

## Convenciones de Código y Calidad

### Pre-commit Hooks

El proyecto utiliza pre-commit hooks para asegurar la calidad del código. Para configurar:

```bash
pip install pre-commit
pre-commit install
```

Los hooks incluyen:
- Black (formateo de código)
- Flake8 (linting)
- isort (ordenamiento de imports)
- mypy (verificación de tipos)
- pytest (pruebas unitarias)
- Verificación de dependencias

### Requerimientos de Calidad

1. **Estilo de Código**
   - Seguir PEP 8
   - Usar Black para formateo automático
   - Documentar con docstrings estilo NumPy
   - Máxima longitud de línea: 88 caracteres

2. **Testing**
   - Cada feature debe incluir tests unitarios
   - Cobertura mínima requerida: 80%
   - Los tests se ejecutan automáticamente en cada commit

3. **Documentación**
   - Docstrings obligatorios para funciones y clases
   - README actualizado para nuevas funcionalidades
   - Comentarios claros en código complejo

4. **Control de Calidad**
   - Los pre-commit hooks deben pasar antes de cada commit
   - Las Pull Requests deben pasar todas las validaciones
   - El pipeline de validación debe ejecutarse exitosamente

### Pipeline de Validación

El pipeline de validación (`src/utils/validate_pipeline.py`) verifica:
1. Estructura correcta del proyecto
2. Disponibilidad de datos necesarios
3. Dependencias requeridas
4. Calidad del código
5. Cobertura de tests

### Testing

El proyecto sigue una estructura de testing organizada:

1. **Tests Unitarios** (`src/tests/unit/`)
   - Pruebas de componentes individuales
   - Validación de funciones específicas
   - Cobertura de casos edge

2. **Tests de Integración** (`src/tests/integration/`)
   - Pruebas de flujos completos
   - Validación de interacción entre componentes
   - Escenarios de uso real

3. **Ejecución de Tests**
   ```bash
   # Ejecutar todos los tests
   pytest

   # Ejecutar tests con reporte de cobertura
   pytest --cov=src

   # Ejecutar tests específicos
   pytest src/tests/unit/  # Solo tests unitarios
   pytest src/tests/integration/  # Solo tests de integración
   ```

4. **Requerimientos de Testing**
   - Cobertura mínima: 80%
   - Tests obligatorios para cada feature nueva
   - Documentación de casos de prueba
   - Fixtures compartidos en `conftest.py`

## Contacto

Para dudas o consultas, contactar al instructor:
- GitHub: [@aladelca](https://github.com/aladelca)

## Documentación

- [Guía de Validaciones](VALIDATIONS.md): Documentación detallada sobre las validaciones del proyecto y cómo pasarlas.
