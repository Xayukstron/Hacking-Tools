#!/usr/bin/env python

import scapy.all as scapy
import argparse

def parse_ip_range():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="Enter the IP range you want to be scanned here.")
    ip_range = parser.parse_args()
    return ip_range.ip

def scan(ip):
    arp_request = scapy.ARP(pdst=ip) # Creats an ARP packet and assigns the required ip to be searched in the network to the packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Creates an ether frame and sets the destination mac to the boradcast mac
    arp_request_boradcast = broadcast/arp_request # Appends both the packets into a single packet
    answered_list = scapy.srp(arp_request_boradcast, timeout=1, verbose=False)[0] #answered_list, unanswered_list = scapy.srp(arp_request_boradcast, timeout=1)
    # scapy.sr will send and receive packets(.sr) but we have to use .srp to be able to implement the ethernet part of the packet
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n---------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

ip_range = parse_ip_range()
scan_result = scan(ip_range)
print_result(scan_result)