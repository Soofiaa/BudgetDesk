# BudgetDesk

Aplicación de escritorio en Python para el registro, análisis y control de gastos personales mensuales. Permite clasificar gastos por categoría y método de pago, visualizar resúmenes estadísticos y exportar reportes formateados a Excel.

---

## Características Principales

- Registro de gastos con monto, categoría, fecha, descripción, método de pago y notas.
- Gestión de categorías personalizadas, con protección contra pérdida de datos al eliminar una categoría en uso.
- Filtros de búsqueda por mes, categoría y método de pago.
- Resúmenes y gráficos estadísticos (por categoría, por método de pago, totales mensuales).
- Exportación de reportes a Excel con formato profesional (OpenPyXL).
- Persistencia local en SQLite.
- Interfaz moderna con CustomTkinter.
- Instalador para Windows generado con PyInstaller + Inno Setup.

---

## Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| SQLite | Persistencia de datos |
| Pandas | Manipulación y agregación de datos |
| Matplotlib | Generación de gráficos |
| OpenPyXL | Exportación a Excel |
| pytest | Suite de tests automatizados |
| PyInstaller | Generación de ejecutable |
| Inno Setup | Creación del instalador |

---

## Arquitectura del Proyecto

```plaintext
BudgetDesk/
│
├── main.py
├── build_exe.ps1
├── installer_config.iss
├── requirements.txt
├── requirements-dev.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py
│   ├── categories_dao.py
│   └── expenses_dao.py
│
├── models/
│   ├── __init__.py
│   ├── expense.py
│   └── category.py
│
├── services/
│   ├── __init__.py
│   ├── expense_service.py
│   └── export_service.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── add_expense_frame.py
│   ├── expenses_table_frame.py
│   ├── summary_frame.py
│   ├── categories_frame.py
│   └── styles.py
│
├── utils/
│   ├── __init__.py
│   └── formatting.py
│
└── tests/
    └── test_formatting.py
```

Separación en capas: `database/` (acceso a datos), `models/` (entidades), `services/` (lógica de negocio y agregación), `ui/` (interfaz), `utils/` (funciones auxiliares).

---

## Instalación y Ejecución (desde código fuente)

```bash
git clone https://github.com/Soofiaa/BudgetDesk.git
cd BudgetDesk
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python main.py
```

La base de datos SQLite se crea automáticamente en `~/.budgetdesk/expenses.db` la primera vez que se ejecuta la aplicación.

### Instalador para Windows

También está disponible un instalador `.exe` listo para usar en la sección [Releases](../../releases) del repositorio — no requiere Python instalado.

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/
```

Cobertura actual: parseo de montos en formato chileno (separador de miles y decimales), incluyendo casos límite y de entrada inválida.

---

## Notas de Diseño

Algunas decisiones tomadas deliberadamente durante el desarrollo, pensando en la integridad de los datos del usuario:

- **Las categorías no se pueden eliminar "a ciegas"**: si una categoría tiene gastos asociados, la aplicación exige reasignarlos a otra categoría existente antes de permitir el borrado, evitando registros huérfanos que romperían los resúmenes y filtros.
- **Nombres de categoría insensibles a mayúsculas** al validar duplicados (`"Comida"` y `"comida"` se tratan como la misma categoría), para evitar inconsistencias por error de tipeo del usuario.
- **Separación DAO / servicio / UI**: la lógica de acceso a datos, las reglas de negocio (validación, agregación con Pandas) y la interfaz están desacopladas, lo que facilita testear la lógica sin depender de la UI.

---

## Funcionalidades

**Registro de Gastos** — monto, categoría, fecha, descripción, método de pago y notas opcionales.

**Gestión de Categorías** — creación, listado y eliminación protegida (ver Notas de Diseño).

**Visualización y Filtros** — tabla de gastos con filtros combinables por mes, categoría y método de pago.

**Estadísticas y Resúmenes** — totales mensuales, distribución por categoría y por método de pago, gráficos de torta y de barras.

**Exportación** — reportes a Excel con formato (encabezados, totales, colores alternados por fila).

---

## Autor

Sofía Menzel
GitHub: https://github.com/Soofiaa
LinkedIn: https://www.linkedin.com/in/sofia-menzel-madrid/
