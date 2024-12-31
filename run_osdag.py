# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:51:35 2024

@author: Steve
"""

import subprocess

def run_osdag():
    try:
        subprocess.run(["cmd.exe","/K","run_osdag.bat" ], shell = True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
    
if __name__ == "__main__":
    run_osdag()