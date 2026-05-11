# Script de construcción para BudgetDesk
# Este script usa PyInstaller para generar el ejecutable.

$VENV_BIN = ".venv\Scripts"
$PYTHON = "$VENV_BIN\python.exe"
$PYINSTALLER = "$VENV_BIN\pyinstaller.exe"

if (-not (Test-Path $PYTHON)) {
    Write-Error "No se encontró el entorno virtual en .venv. Por favor, créalo primero."
    exit 1
}

# Obtener la ruta de customtkinter dinámicamente
$CTK_PATH = & $PYTHON -c "import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))"

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host "Iniciando construcción de BudgetDesk..." -ForegroundColor Cyan
Write-Host "Ruta de CustomTkinter: $CTK_PATH"
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

# Ejecutar PyInstaller
# --noconsole: No abre ventana de comandos (app GUI)
# --onedir: Crea una carpeta con dependencias (mejor para instaladores)
# --add-data: Incluye los archivos de tema y recursos de customtkinter
& $PYINSTALLER --noconsole `
    --onedir `
    --name "BudgetDesk" `
    --add-data "${CTK_PATH};customtkinter" `
    --clean `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[ÉXITO] Construcción finalizada correctamente." -ForegroundColor Green
    Write-Host "Los archivos se encuentran en: dist/BudgetDesk" -ForegroundColor Green
    Write-Host "Ejecuta 'dist/BudgetDesk/BudgetDesk.exe' para probar."
} else {
    Write-Host "`n[ERROR] Falló la construcción." -ForegroundColor Red
}
