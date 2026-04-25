Set-Location "c:\Users\umerm\Desktop\carpool-app"

$pythonExe = "c:\Users\umerm\Desktop\carpool-app\.venv\Scripts\python.exe"

function Get-PhoneDemoIp {
    param(
        [string]$OverrideIp
    )

    if ($OverrideIp) {
        return $OverrideIp.Trim()
    }

    $candidateAliases = @(
        "Wi-?Fi",
        "Wireless",
        "Ethernet",
        "Local Area Connection"
    )

    foreach ($aliasPattern in $candidateAliases) {
        $preferred = Get-NetIPAddress -AddressFamily IPv4 |
            Where-Object {
                $_.IPAddress -notlike "169.254*" -and
                $_.IPAddress -ne "127.0.0.1" -and
                $_.PrefixOrigin -ne "WellKnown" -and
                $_.InterfaceAlias -match $aliasPattern -and
                $_.InterfaceAlias -notmatch "vEthernet|Virtual|Loopback|Bluetooth|WSL|VPN|TAP|Hamachi|VirtualBox|Hyper-V" -and
                $_.IPAddress -notmatch "^192\.168\.56\."
            } |
            Select-Object -First 1 -ExpandProperty IPAddress

        if ($preferred) {
            return $preferred
        }
    }

    $fallback = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object {
            $_.IPAddress -notlike "169.254*" -and
            $_.IPAddress -ne "127.0.0.1" -and
            $_.InterfaceAlias -notmatch "vEthernet|Loopback|Bluetooth|WSL|VPN|TAP|Hamachi|VirtualBox|Hyper-V"
        } |
        Select-Object -First 1 -ExpandProperty IPAddress

    return $fallback
}

$ip = Get-PhoneDemoIp -OverrideIp $env:PHONE_DEMO_IP

if (-not $ip) {
    Write-Host "Could not auto-detect a real LAN IP. Set PHONE_DEMO_IP manually, then rerun." -ForegroundColor Yellow
    $ip = "127.0.0.1"
}

$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost,$ip"

Write-Host "" 
Write-Host "Phone demo server starting..." -ForegroundColor Cyan
Write-Host "Open on laptop: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Open on phone:  http://$ip`:8000/" -ForegroundColor Green
Write-Host "If this IP looks wrong, run: `$env:PHONE_DEMO_IP='YOUR_WIFI_IP'" -ForegroundColor DarkYellow
Write-Host "" 

& $pythonExe manage.py runserver 0.0.0.0:8000
