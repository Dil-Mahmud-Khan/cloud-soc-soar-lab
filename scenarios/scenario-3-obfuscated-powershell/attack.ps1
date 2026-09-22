# Scenario 3 Attack Simulation: Obfuscated PowerShell Execution
Write-Host "[*] Executing MITRE ATT&CK T1059.001 (Obfuscated PowerShell)..." -ForegroundColor Yellow

$script = "Write-Host 'Adversary Emulation: Simulated Malicious Script Execution'; Start-Sleep -Seconds 2"
$bytes = [System.Text.Encoding]::Unicode.GetBytes($script)
$encoded = [Convert]::ToBase64String($bytes)

Write-Host "[*] Encoded Base64 payload: $encoded" -ForegroundColor Gray
$command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded"

cmd.exe /c $command

Write-Host "[✓] Execution completed. Check LimaCharlie EDR for Obfuscated PowerShell alert." -ForegroundColor Green
