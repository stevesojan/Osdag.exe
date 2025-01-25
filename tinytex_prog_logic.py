# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 16:23:46 2025

@author: Steve
"""
import os
import subprocess
def install_tinytex():
    """Installs TinyTeX and configures it, with fallback download methods."""
    try:
        print("Installing TinyTeX...")

        # Step 1: Define Environment Variables
        tinytex_url = "https://github.com/rstudio/tinytex-releases/releases/download/daily/TinyTeX-1.zip"
        temp_dir = os.getenv("TEMP")
        tinytex_dir = os.getenv("APPDATA", "Roaming")
        downloaded_file = os.path.join(temp_dir, "install.zip")

        # Step 2: Clean up Temporary Files
        print("Cleaning up any leftover TinyTeX directories...")
        tinytex_pattern = os.path.join(tinytex_dir, "TinyTeX*")
        subprocess.run(f'del /f /s /q "{tinytex_pattern}" & rmdir /s /q "{tinytex_dir}\\TinyTeX"', shell=True,
                       check=False)

        # Step 3: Download TinyTeX with Multiple Methods
        success = False
        print("Downloading TinyTeX...")

        # Method 1: System.Net.WebClient
        print("Method 1: Using System.Net.WebClient...")
        print(
            "Do not panic if you see text in red, or if the shell looks stuck, the installer is working, please wait ;)")
        download_command = f'powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile(\'{tinytex_url}\', \'{downloaded_file}\')"'
        if subprocess.run(download_command, shell=True).returncode == 0:
            success = True

        # Method 2: Invoke-WebRequest
        if not success:
            print("Method 1 failed. Trying Method 2: Invoke-WebRequest...")
            download_command = f'powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest \'{tinytex_url}\' -OutFile \'{downloaded_file}\'"'
            if subprocess.run(download_command, shell=True).returncode == 0:
                success = True

        # Method 3: System.Net.Http.HttpClient
        if not success:
            print("Method 2 failed. Trying Method 3: System.Net.Http.HttpClient...")
            download_command = f'powershell -Command "& {{ try {{ Add-Type -A \'System.Net.Http\'; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $response = (New-Object System.Net.Http.HttpClient).GetAsync(\'{tinytex_url}\'); $response.Wait(); $outputFileStream = [System.IO.FileStream]::new(\'{downloaded_file}\', [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write); $response.Result.Content.CopyToAsync($outputFileStream).Wait(); $outputFileStream.Close() }} catch {{ throw $_ }} }}"'
            if subprocess.run(download_command, shell=True).returncode == 0:
                success = True

        # Exit if all download methods fail
        if not success:
            print("All download methods failed. Unable to download TinyTeX.")
            return

        # Step 4: Unzip the File
        print("Unzipping TinyTeX...")
        unzip_command = f'powershell -Command "& {{ Add-Type -A \'System.IO.Compression.FileSystem\'; [System.IO.Compression.ZipFile]::ExtractToDirectory(\'{downloaded_file}\', \'{temp_dir}\'); }}"'
        subprocess.run(unzip_command, shell=True, check=True)
        os.remove(downloaded_file)

        # Step 5: Move TinyTeX to Target Directory
        print(f"Moving TinyTeX to {tinytex_dir}...")
        tinytex_path = os.path.join(tinytex_dir, "TinyTeX")
        subprocess.run(f'move /y "{os.path.join(temp_dir, "TinyTeX")}" "{tinytex_path}"', shell=True, check=True)

        # Step 6: Configure tlmgr
        print("Configuring TinyTeX...")
        tlmgr_path = os.path.join(tinytex_path, "bin", "windows", "tlmgr")
        subprocess.run(f'"{tlmgr_path}" path add', shell=True, check=True)
        subprocess.run(f'"{tlmgr_path}" option repository ctan', shell=True, check=True)
        subprocess.run(f'"{tlmgr_path}" postaction install script xetex', shell=True, check=True)

        print("TinyTeX installed and configured successfully.")
        print("Now Installing additional required packages...")
        subprocess.run(
            [f'{tlmgr_path}', 'install', 'lastpage', 'parskip', 'needspace', 'fancyhdr', 'colortbl', 'multirow'],
            check=True, shell=True)
        print("Required Packages Installed Successfully")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during TinyTeX installation: {e}")
        
        
install_tinytex()