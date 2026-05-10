# Instrucciones del proyecto - BudgetDesk

## Idioma
- TODO debe estar en español:
  - interfaz,
  - textos,
  - mensajes,
  - botones,
  - labels,
  - explicaciones,
  - documentación,
  - comentarios,
  - nombres visibles para el usuario.
- El código puede mantener nombres técnicos en inglés cuando sea estándar de programación.
- Explica errores y soluciones en español claro.

## Objetivo del proyecto
BudgetDesk es una aplicación de escritorio para controlar gastos personales mensuales desde el PC.

La aplicación debe permitir:
- registrar gastos,
- categorizarlos,
- clasificarlos por método de pago,
- visualizar resúmenes,
- generar estadísticas,
- exportar información.

La prioridad es:
- simplicidad,
- claridad,
- rapidez,
- facilidad de uso,
- estabilidad.

## Tecnologías permitidas
Usar únicamente:
- Python
- CustomTkinter
- SQLite
- Pandas
- Matplotlib
- OpenPyXL

No usar:
- Electron
- React
- frameworks web
- servidores innecesarios
- Docker
- APIs externas innecesarias

## Arquitectura
Mantener estructura modular y limpia.

Separar:
- interfaz,
- lógica,
- base de datos,
- gráficos,
- exportación,
- utilidades.

Evitar archivos gigantes.

## Estructura recomendada
- main.py
- database/
- models/
- services/
- ui/
- charts/
- exports/
- utils/

## Funcionalidades MVP
### Registro de gastos
Cada gasto debe incluir:
- monto,
- descripción,
- fecha,
- categoría,
- método de pago,
- notas opcionales.

### Métodos de pago
Usar:
- débito,
- transferencia,
- crédito.

### Categorías iniciales
- comida,
- transporte,
- mascotas,
- salud,
- cuentas,
- compras,
- ocio,
- educación,
- otros.

### Funciones principales
- agregar gasto,
- editar gasto,
- eliminar gasto,
- filtrar gastos,
- resumen mensual,
- total mensual,
- total por categoría,
- total por método de pago,
- gráficos básicos,
- exportar a Excel.

## Base de datos
Usar SQLite local.

No usar bases de datos remotas.

Evitar pérdida de datos.

Antes de modificar tablas:
- explicar cambios,
- indicar impacto,
- evitar romper compatibilidad.

## Interfaz
La interfaz debe ser:
- limpia,
- moderna,
- simple,
- rápida,
- intuitiva.

Usar:
- CustomTkinter
- modo oscuro elegante
- diseño ordenado

Evitar:
- interfaces recargadas,
- exceso de colores,
- ventanas innecesarias.

## Gráficos
Usar Matplotlib.

Mostrar:
- gastos por categoría,
- gastos por método de pago,
- evolución mensual.

Mantener gráficos simples y claros.

## Exportación
Permitir exportar:
- Excel,
- CSV.

Usar OpenPyXL para Excel.

## Seguridad y estabilidad
- Nunca borrar archivos sin confirmación.
- Nunca sobrescribir datos automáticamente.
- Nunca modificar múltiples archivos innecesariamente.
- No agregar dependencias sin explicar:
  - para qué sirven,
  - por qué son necesarias.
- No refactorizar todo el proyecto sin autorización.

## Flujo obligatorio antes de modificar código
Antes de hacer cambios:
1. Explicar el plan.
2. Indicar archivos a modificar.
3. Explicar impacto esperado.

Después de hacer cambios:
1. Explicar qué se modificó.
2. Mostrar archivos modificados.
3. Explicar cómo probar.
4. Informar riesgos o pendientes.

## Git
- No hacer commits automáticos.
- No hacer push automático.
- No modificar historial Git.
- Recomendar commits claros.

## Calidad del código
- Código limpio.
- Fácil de mantener.
- Funciones pequeñas.
- Evitar duplicación.
- Evitar complejidad innecesaria.
- Priorizar claridad sobre sofisticación.

## Manejo de errores
Cuando ocurra un error:
1. Explicar causa probable.
2. Explicar solución mínima.
3. Evitar cambios innecesarios.
4. No inventar soluciones.

## Comportamiento esperado del agente IA
- Actuar como desarrollador senior mentor.
- Explicar decisiones técnicas.
- Priorizar estabilidad.
- Priorizar mantenibilidad.
- Priorizar experiencia de usuario.
- No asumir cosas no verificadas.
- No ejecutar acciones destructivas.

## Formato de respuesta esperado
Después de cada tarea responder:

### Cambios realizados
- ...

### Archivos modificados
- ...

### Cómo probar
- ...

### Riesgos o pendientes
- ...