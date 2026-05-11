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
```

# Funcionalidades:
Registro de Gastos

Permite registrar:
- Monto
- Categoría
- Fecha
- Descripción
- Método de pago
- Gestión de Categorías

Los usuarios pueden:
- Crear categorías
- Editar categorías
- Eliminar categorías
- Visualización de Datos

La aplicación incorpora:
- Tabla de gastos
- Filtros de búsqueda
- Historial de movimientos
- Estadísticas y Resúmenes

Incluye gráficos y resúmenes financieros:
- Distribución de gastos por categoría
- Totales mensuales
- Pie charts
- Bar charts
- Exportación a Excel

Autor: Sofía Menzel
GitHub: https://github.com/Soofiaa
LinkedIn: https://www.linkedin.com/in/sofia-menzel-madrid/
