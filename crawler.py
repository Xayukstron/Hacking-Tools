#!/usr/bin/env/ python

import requests

def request(url):
    try:
        return requests.get("http://" + url) # returns 200 ok status if the url exists
    except requests.exceptions.ConnctionError: # returns this error if the url does not exist
        pass

target_url = "google.com"

with open("/root/Downloads/subdomains.list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip() # strips(removes the new line character from the end of each line
        test_url = target_url + "/" + word   #word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered URL --> " + test_url)