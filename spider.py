#!/usr/bin/env/ python

import requests
import re
import urlparse

target_url = "https://google.com"
target_links = []

def extract_links_from(url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content) #response.content will return the html code used for the webpage

def crawl(url):
    href_links = extract_links_from(target_url)
    for link in href_links:
        link = urlparse.urljoin(target_url, link) # will convert the relative links to full links

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links: # this check will just eliminate all the links to website other than the target website.
            target_links.append(link)
            print(link)
            crawl(link)

crawl(target_url)