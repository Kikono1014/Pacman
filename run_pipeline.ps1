# run_pipeline.ps1
Write-Host "Starting local CI/CD pipeline..."

# Створюємо папку для звітів
New-Item -ItemType Directory -Force -Path reports | Out-Null

# Запуск тестів Pytest
Write-Host "Running Pytest..."
pytest Tests --html=reports/pytest_report.html --self-contained-html
if ($LASTEXITCODE -ne 0) {
    Write-Host "Pytest failed!"
    exit 1
}

# Перевірка стилю коду Flake8
Write-Host "Running Flake8..."
flake8 . --format=html --htmldir=reports/flake8_report
if ($LASTEXITCODE -ne 0) {
    Write-Host "Flake8 failed!"
    exit 1
}

Write-Host "Pipeline completed successfully!"