param(
  [int]$time = 40
)
Write-Host "Running AFTER..." -ForegroundColor Yellow
promptproof attack --config configs\demo_after.yaml --time $time --verbose
$after = (Get-ChildItem logs\run_*.jsonl | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
promptproof report --logs $after --out reports\after.html
Write-Host "after.html -> reports\after.html" -ForegroundColor Green
