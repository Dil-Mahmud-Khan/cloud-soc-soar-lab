<#
================================================================================
  Automated Endpoint Live Triage Collector
  Author: Dil Mahmud Khan
  Standard: RFC 3227 Volatile Evidence Acquisition
================================================================================
#>

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$triageDir = "C:\LabAttacks\Triage_$timestamp"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  🔬 Live Forensic Triage Collection Initialized" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[*] Target Directory: $triageDir" -ForegroundColor Gray

New-Item -ItemType Directory -Path $triageDir -Force | Out-Null

# 1. System Metadata & Network Sockets
Write-Host "[1/6] Capturing Active Network Sockets & DNS Cache..." -ForegroundColor Yellow
netstat -ano > "$triageDir\network_sockets.txt"
Get-DnsClientCache | Select-Object Entry, RecordName, Data | Out-File "$triageDir\dns_cache.txt"

# 2. Process List & Command Lines
Write-Host "[2/6] Capturing Process Memory & Parent-Child Trees..." -ForegroundColor Yellow
Get-CimInstance Win32_Process | Select-Object ProcessId, ParentProcessId, Name, CommandLine, CreationDate | Export-Csv -Path "$triageDir\process_list.csv" -NoTypeInformation

# 3. Logged-in Users & Active Sessions
Write-Host "[3/6] Capturing Active User Sessions & Privileges..." -ForegroundColor Yellow
query user > "$triageDir\active_sessions.txt" 2>$null
whoami /priv > "$triageDir\analyst_privileges.txt"

# 4. Persistence Mechanisms (Registry Run Keys)
Write-Host "[4/6] Auditing Persistence Locations (Registry Run Keys)..." -ForegroundColor Yellow
$runKeys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
)
foreach ($key in $runKeys) {
    if (Test-Path $key) {
        Get-ItemProperty -Path $key | Out-File -FilePath "$triageDir\registry_persistence.txt" -Append
    }
}

# 5. Scheduled Tasks
Write-Host "[5/6] Exporting Active Scheduled Tasks..." -ForegroundColor Yellow
Get-ScheduledTask | Where-Object { $_.State -ne "Disabled" } | Select-Object TaskName, TaskPath, State | Export-Csv -Path "$triageDir\scheduled_tasks.csv" -NoTypeInformation

# 6. Temp Executables & Staged Payloads
Write-Host "[6/6] Scanning Staging Directories (Temp Folders)..." -ForegroundColor Yellow
Get-ChildItem -Path "C:\Windows\Temp", "C:\Users\*\AppData\Local\Temp" -Include *.exe, *.bat, *.ps1, *.tmp, *.dmp -Recurse -ErrorAction SilentlyContinue | Select-Object FullName, Length, CreationTime, LastWriteTime | Export-Csv -Path "$triageDir\temp_executables.csv" -NoTypeInformation

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  [✓] Triage Collection Complete! Saved to: $triageDir" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
