@echo off
call .\.venv\Scripts\activate
promptproof init
promptproof attack --config configs\sample_target.yaml --time 60
for /f "delims=" %%F in ('dir /b /o-d logs\run_*.jsonl') do set LATEST=logs\%%F& goto :gotone
:gotone
promptproof mitigate --log %LATEST% --config configs\sample_target.yaml
promptproof report --out reports\report.html
echo Done. Open reports\report.html
