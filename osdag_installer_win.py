# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:57:06 2024

@author: Steve
"""

import os
import subprocess
import sys
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

def create_conda_env():
    print("Creating Conda environment...")
    subprocess.run(["conda", "create", "-n", "osdag_env", "python=3.8", "-y"], shell=True)
    subprocess.run(["conda", "activate", "osdag_env"], shell=True)

def install_dependencies():
    print("Installing Python dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True)

def main():
    try:
        install_miniconda()
        create_conda_env()
        install_dependencies()
        print("Installation completed successfully.")
    except Exception as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
    main()
