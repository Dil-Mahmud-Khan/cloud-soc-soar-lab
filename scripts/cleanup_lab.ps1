# ====================================================================
#  Lab Artifact Cleanup Script
#  Author: Dil Mahmud Khan
#  Removes temporary files generated during adversary emulation
# ====================================================================

$labPath = "C:\LabAttacks"

Write-Host "[*] Cleaning up temporary attack files in $labPath..." -ForegroundColor Yellow

$filesToRemove = @(
    "$labPath\payload_certutil.tmp",
    "$labPath\lsass_simulated.dmp",
    "$labPath\certutil.txt"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "    [✓] Deleted: $file" -ForegroundColor Green
    }
}

Write-Host "[*] Cleanup finished." -ForegroundColor Cyan
