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
    if not os.path.exists("C:\\Miniconda3") or not os.path.exists("%USERPROFILE%\Miniconda3"):
        installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        installer_name = "Miniconda3-latest-Windows-x86_64.exe"
    
    # Check if the installer is already downloaded
        if not os.path.exists(installer_name):
            print("Downloading the latest Miniconda installer...")
            response = requests.get(installer_url, stream=True)
            with open(installer_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
                        print("Download completed.")
        else:
            print("Installer already exists. Skipping download.")
        
            print("Miniconda not found. Installing Miniconda...")
            subprocess.run(["start", "/wait", "Miniconda3-latest-Windows-x86_64.exe", "/InstallationType=JustMe", "/RegisterPython=0", "/AddToPath=1", "/S"], shell=True)
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
