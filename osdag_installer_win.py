# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:57:06 2024

@author: Steve
"""
#%%
import os
import subprocess
import requests
import time

def install_miniconda():
    upf = os.environ.get('USERPROFILE')
    if os.path.exists(r"C:\miniconda3") == False and os.path.exists(f"{upf}\\miniconda3") == False:
        # os.path.exists(r"C:\miniconda3") == False - checks if miniconda3 is not installed system wide for all users in C drive 
        installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        installer_name = "Miniconda3-latest-Windows-x86_64.exe"
    

    
        print("Downloading the latest Miniconda installer...")
        response = requests.get(installer_url, stream=True)
        with open(installer_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)
            print("Download completed.")        
    
        print("Installing Miniconda...")   
        subprocess.run(["start", "/wait", "Miniconda3-latest-Windows-x86_64.exe", "/InstallationType=JustMe", "/RegisterPython=0", "/AddToPath=1", "/S"], shell=True)
        print("Miniconda Installed Successfully")
    else:
        print("Miniconda is already installed.")


'''
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
'''
def create_conda_env():
    """Creates the Conda environment and installs Osdag in the same shell."""
    upf = os.environ.get("USERPROFILE")
    conda_bat = os.path.join(upf, "miniconda3", "condabin", "conda.bat")

    # Check if conda.bat exists
    if not os.path.exists(conda_bat):
        raise FileNotFoundError(f"Conda was not found at {conda_bat}. Ensure Miniconda is installed.")

    print("Creating Conda environment and installing Osdag...")
    
    success = False
    attempt = 1

    while not success and attempt<=10:
        try:
            print(f"Attempt {attempt}: Running Conda command to install Osdag...")
            
            # Run the Conda command in the same shell
            subprocess.run(
                f'"{conda_bat}" activate && conda create -n osdag-env osdag::osdag -c conda-forge -y',
                check=True,
                shell=True,
            )
            print("Osdag was installed successfully.")
            success = True  # Exit the loop if the command succeeds
            
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt} failed. Retrying... Error: {e}")
            attempt += 1
            time.sleep(10)  # Wait 10 seconds before retrying
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
            break  # Exit the loop if Conda is not installed and cannot proceed

    if attempt == 10 and not success:
        print("Failed to install Osdag after multiple attempts. Please check your network or Conda setup.")


def main():
    try:
        install_miniconda()
        #install_tinytex()
        create_conda_env() 
        print("Installation completed successfully. Ready to use.")
    except Exception as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
#makes sure code runs directly from this script and not some external func
    main()
