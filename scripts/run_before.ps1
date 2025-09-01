param(
  [int]$time = 40
)
Write-Host "Running BEFORE..." -ForegroundColor Yellow
promptproof attack --config configs\demo_before.yaml --time $time --verbose
$before = (Get-ChildItem logs\run_*.jsonl | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
promptproof report --logs $before --out reports\before.html
Write-Host "before.html -> reports\before.html" -ForegroundColor Green
