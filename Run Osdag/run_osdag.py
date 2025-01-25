# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:51:35 2024

@author: Steve
"""
import subprocess


def run_osdag():
    try:
        subprocess.run("call conda activate osdag-env && osdag", check =True, shell = True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    run_osdag()
