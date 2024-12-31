# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:57:06 2024

@author: Steve
"""

import os
import subprocess
import requests

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
        
        
def install_tinytex():
    try:
        subprocess.run('TinyTex\install-bin-windows.bat', check = True, shell = True )
        print('TinyTex Installed Succesfully, Now installing required additional packages...')
    except subprocess.calledProcessError as e:
        print(f"An error occurred while installing TinyTex- {e}")
        
    try:
        subprocess.run(['tlmgr','install','lastpage','parskip','needspace','fancyhdr','colortbl','multirow'], check = True)
        print("Required Packages Installed Successfully")
    except subprocess.calledProcessError as e:
        print(f"An error occurred while installing additional packages of TinyTex: {e}")
        

def create_conda_env():
    print("Creating Conda environment...")
    try:
        subprocess.run(["conda", "create", "-n", "osdag-env", "osdag::osdag", "-c", "conda-forge"], shell=True)
        print("Osdag was installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Encountered an error while creating conda env or installing osdag: {e}")
        


def main():
    try:
        install_miniconda()
        install_tinytex()
        create_conda_env() 
        print("Installation completed successfully.")
    except Exception as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
#makes sure code runs directly from this script and not some external func
    main()
