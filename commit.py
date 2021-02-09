#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 10:45:10 2021

@author: raghhav
"""

import subprocess as cmd

res = input("Do you wish to add all files?([y]/n)\n")
if res.startswith('n'):
    file = input("Enter file name\n")
    cp = cmd.run(f"git add '{file}'",check=True, shell=True)
else:
    cp = cmd.run("git add .", check=True, shell=True)
#print(cp)

response = input("Do you want to use the default message for this commit?([y]/n)\n")
message = "Updating the repository"

if response.startswith('n'):
    message = input("What message you want?\n")

cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True)
cp = cmd.run("git push origin main", check=True, shell=True)
