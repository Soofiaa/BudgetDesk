# BudgetDesk

BudgetDesk es una aplicación de escritorio desarrollada en Python para la gestión y análisis de gastos personales mensuales.  
La aplicación permite registrar gastos, organizarlos por categorías, visualizar estadísticas financieras y exportar reportes en Excel mediante una interfaz moderna y fácil de utilizar.

---

# Características Principales

- Registro de gastos personales.
- Gestión de categorías personalizadas.
- Clasificación por método de pago.
- Visualización de gastos en tablas interactivas.
- Resúmenes y gráficos estadísticos.
- Exportación de reportes en Excel.
- Base de datos local SQLite.
- Interfaz moderna desarrollada con CustomTkinter.
- Instalador profesional para Windows.

---

# Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| SQLite | Persistencia de datos |
| Pandas | Manipulación de datos |
| Matplotlib | Generación de gráficos |
| OpenPyXL | Exportación a Excel |
| PyInstaller | Generación de ejecutable |
| Inno Setup | Creación del instalador |

---

# Arquitectura del Proyecto

```plaintext
BudgetDesk/
│
├── main.py
├── database/
│   ├── database.py
│   ├── categories_dao.py
│   └── expenses_dao.py
│
├── models/
│   ├── expense.py
│   └── category.py
│
├── services/
│   ├── expense_service.py
│   └── export_service.py
│
├── ui/
│   ├── app.py
│   ├── add_expense_frame.py
│   ├── expenses_table_frame.py
│   ├── summary_frame.py
│   └── categories_frame.py
│
├── utils/
│   ├── currency_utils.py
│   └── date_utils.py
│
└── assets/

Funcionalidades
Registro de Gastos

Permite registrar:

Monto
Categoría
Fecha
Descripción
Método de pago
Gestión de Categorías

Los usuarios pueden:

Crear categorías
Editar categorías
Eliminar categorías
Visualización de Datos

La aplicación incorpora:

Tabla de gastos
Filtros de búsqueda
Historial de movimientos
Estadísticas y Resúmenes

Incluye gráficos y resúmenes financieros:

Distribución de gastos por categoría
Totales mensuales
Pie charts
Bar charts
Exportación a Excel

Permite exportar reportes .xlsx utilizando:

Pandas
OpenPyXL
Instalación
Requisitos
Python 3.10+
pip
Clonar repositorio
git clone https://github.com/Soofiaa/BudgetDesk.git
cd BudgetDesk
Crear entorno virtual
python -m venv venv
Windows
venv\Scripts\activate
Instalar dependencias
pip install -r requirements.txt
Ejecutar aplicación
python main.py
Generar Ejecutable
pyinstaller main.spec

El ejecutable se generará en:

dist/BudgetDesk/
Generar Instalador

El proyecto utiliza Inno Setup para crear el instalador de Windows.

Archivo utilizado:

installer.iss

Compilar el script generará:

BudgetDesk_Setup.exe
Capturas de Pantalla
Pantalla Principal

Agregar screenshot aquí

Tabla de Gastos

Agregar screenshot aquí

Resumen Estadístico

Agregar screenshot aquí

Estado del Proyecto

Proyecto funcional y en fase de distribución.

Próximas mejoras:

Backups automáticos.
Dashboard avanzado.
Presupuestos mensuales.
Alertas financieras.
Optimización de consultas SQLite.
Objetivo del Proyecto

El objetivo de BudgetDesk es proporcionar una solución simple, rápida y visual para el control financiero personal, utilizando tecnologías modernas del ecosistema Python y buenas prácticas de desarrollo modular.

Autor: Sofía Menzel
GitHub: https://github.com/Soofiaa
LinkedIn: https://www.linkedin.com/in/sofia-menzel-madrid/
