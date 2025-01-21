@echo off

where /q powershell || echo PowerShell not found && exit /b

rem Switch to a temporary directory
cd /d "%TMP%" || cd /d "%TEMP%" || (echo Unable to access temporary directories && exit /b)

rem Clean up any leftover TinyTeX directories
for /d %%G in ("TinyTeX*") do rd /s /q "%%~G"

if not defined TINYTEX_INSTALLER set TINYTEX_INSTALLER=TinyTeX-1

rem Determine installation directory
if not defined TINYTEX_DIR (
  set TINYTEX_DIR=%APPDATA%
  powershell -Command "if ($Env:APPDATA -match '^[!-~]+$') {exit 0} else {exit 1}" || set TINYTEX_DIR=%ProgramData%
)

set BUNDLE_EXT=zip
if "%TINYTEX_INSTALLER%" == "TinyTeX-2" set BUNDLE_EXT=exe

rem Construct the download URL
if not defined TINYTEX_VERSION (
  set TINYTEX_URL=https://github.com/rstudio/tinytex-releases/releases/download/daily/%TINYTEX_INSTALLER%.%BUNDLE_EXT%
) else (
  set TINYTEX_URL=https://github.com/rstudio/tinytex-releases/releases/download/v%TINYTEX_VERSION%/%TINYTEX_INSTALLER%-v%TINYTEX_VERSION%.%BUNDLE_EXT%
)

set DOWNLOADED_FILE=install.%BUNDLE_EXT%

rem Method 1: System.Net.WebClient
echo Download %BUNDLE_EXT% file... Method 1: System.Net.WebClient
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile($Env:TINYTEX_URL, $Env:DOWNLOADED_FILE)"
if not errorlevel 1 goto unzip

rem Method 2: Invoke-WebRequest
echo Download %BUNDLE_EXT% file... Method 2: Invoke-WebRequest
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest $Env:TINYTEX_URL -OutFile $Env:DOWNLOADED_FILE"
if not errorlevel 1 goto unzip

rem Method 3: System.Net.Http.HttpClient
echo Download %BUNDLE_EXT% file... Method 3: System.Net.Http.HttpClient
powershell -Command "& { try { Add-Type -A 'System.Net.Http'; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $response = (New-Object System.Net.Http.HttpClient).GetAsync($Env:TINYTEX_URL); $response.Wait(); $outputFileStream = [System.IO.FileStream]::new($Env:DOWNLOADED_FILE, [System.IO.FileMode]::Create, [System.IO.FileAccess::Write]); $response.Result.Content.CopyToAsync($outputFileStream).Wait(); $outputFileStream.Close()} catch {throw $_} }"
if errorlevel 1 (echo Failed to download TinyTeX && exit /b %ERRORLEVEL%)

:unzip
rem Unzip or execute the downloaded file
echo Unbundle TinyTeX
if %BUNDLE_EXT% == exe (
  CALL %DOWNLOADED_FILE% -y
) ELSE (
  powershell -Command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::ExtractToDirectory($Env:DOWNLOADED_FILE, '.'); }"
)
del %DOWNLOADED_FILE%

rem Move TinyTeX to the final directory
rd /s /q "%TINYTEX_DIR%\TinyTeX"
move /y TinyTeX "%TINYTEX_DIR%"

rem Add tlmgr to PATH and configure
echo Adding tlmgr to PATH
cd /d "%TINYTEX_DIR%\TinyTeX\bin\win*"
call tlmgr path add
if /i not "%CI%"=="true" call tlmgr option repository ctan
call tlmgr postaction install script xetex

exit /b %ERRORLEVEL%
