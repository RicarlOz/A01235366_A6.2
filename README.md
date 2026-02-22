# Tarea 6.2 – Ejercicio de programación 3 y pruebas de unidad  
**Materia:** Pruebas de software y aseguramiento de la calidad  
**Autor:** Ricardo Gómez  

---

## 📌 Descripción general

Este repositorio contiene la solución a la **Tarea 6.2**, cuyo objetivo principal es implementar un sistema de reservaciones en Python aplicando principios de diseño orientado a objetos, pruebas unitarias y aseguramiento de calidad mediante herramientas de análisis estático.

La actividad incluye:

- Implementación de un sistema con las abstracciones:
  - Hotel
  - Customer
  - Reservation
- Persistencia de datos utilizando archivos JSON
- Manejo de errores sin interrumpir ejecución
- Pruebas unitarias completas utilizando `unittest`
- Cobertura de código superior al 85%
- Cumplimiento del estándar de codificación **PEP 8**
- Uso de herramientas de análisis estático:
  - `flake8`
  - `pylint`
- Control de versiones en Git con commits estructurados siguiendo Conventional Commits

## 📂 Estructura del repositorio

```
├── src/
│ ├── models.py
│ ├── services.py
│ ├── storage.py
│ └── program.py
├── tests/
│ ├── test_services.py
│ └── test_storage.py
├── data/
│ ├── hotels.json
│ ├── customers.json
│ └── reservations.json
├── results/
│ ├── unittest.txt
│ ├── coverage.txt
│ ├── flake8.txt
│ └── pylint.txt
└── README.md
```


### Descripción de carpetas

- **src/**  
  Contiene la implementación del sistema:
  - `models.py`: Definición de entidades usando `@dataclass`
  - `services.py`: Lógica de negocio
  - `storage.py`: Persistencia en archivos JSON y manejo resiliente de errores
  - `program.py`: Interfaz de línea de comandos (CLI)

- **tests/**  
  Contiene los casos de prueba unitarios:
  - Pruebas de flujo normal
  - Pruebas negativas
  - Manejo de errores en archivos
  - Validación de persistencia

- **data/**  
  Archivos JSON utilizados para almacenamiento persistente.

- **results/**  
  Evidencia de ejecución:
  - Resultados de pruebas unitarias
  - Reporte de cobertura
  - Resultados de análisis estático


## 🏗 Sistema implementado

### 🔹 Hotel

Permite:
- Crear hotel
- Modificar información
- Eliminar hotel
- Consultar información
- Reservar habitaciones
- Cancelar reservaciones


### 🔹 Customer

Permite:
- Crear cliente
- Modificar información
- Eliminar cliente
- Consultar información


### 🔹 Reservation

Permite:
- Crear reservación asociando Hotel y Customer
- Cancelar reservación


## 💾 Persistencia y manejo de errores

El sistema utiliza archivos JSON para almacenar información.

Se implementa manejo de errores para:

- Archivo inexistente
- JSON mal formado
- Estructura incorrecta del archivo
- Datos inválidos
- Errores de lectura/escritura

En todos los casos:
- Se imprime un mensaje de error en consola
- La ejecución continúa sin interrumpirse


## 🧪 Pruebas unitarias

Las pruebas fueron implementadas utilizando el módulo estándar `unittest`.

Incluyen:

- Casos de prueba funcionales
- Casos negativos (≥ 5 requeridos)
- Validación de errores de archivo
- Validación de límites (hotel lleno)
- Cancelación de reservaciones inexistentes

### Ejecutar pruebas

```
python -m unittest -v
```

## 📊 Cobertura de código

La cobertura fue medida utilizando la herramienta coverage.


```
coverage run -m unittest -v
coverage report -m
```

### Resultados finales
- Cobertura total: 95%
- Todas las clases superan el 85% requerido

🧹 Análisis estático

### Flake8

```
flake8 src tests
```

Resultado: Sin errores.

### Pylint

```
pylint src tests
```

Resultado: 10.00 / 10

## ▶️ Ejecución del programa (CLI)

El sistema incluye una interfaz básica por consola para demostración:

```
python -m src.program
```

Permite crear hoteles, clientes y reservaciones desde línea de comandos.

## 🛠 Tecnologías utilizadas
- Python 3
- unittest
- coverage
- flake8
- pylint
- JSON
- Git
- Conventional Commits