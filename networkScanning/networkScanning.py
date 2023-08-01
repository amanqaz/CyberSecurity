#!/usr/bin/env python
import optparse

import scapy.all as scapy


def getArguments():

    parser = optparse.OptionParser()
    parser.add_option("--ip","--IP" ,dest = "ipaddress",help = "Please read documentation scapy")
    (options,arguments) = parser.parse_args()
    print(options.ipaddress)
    if not options.ipaddress:
        parser.error("Please specify ip address or try to help by using help command")
    else:
        return options;

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadCast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff");

    arp_broadCast = broadCast/arp_request
    client_list=[]
    answered = scapy.srp(arp_broadCast,timeout = 1,verbose = False)[0]
    for element in answered:
        client_disc = {"ip" : element[1].psrc , "mac" : element[1].hwsrc }
        client_list.append(client_disc)
    return client_list




def print_result(client_list):
    print("IP Address \t\t\t MacAddress")
    for client in client_list:
        print(client["ip"]+"\t\t"+client["mac"])







options = getArguments()

result_scanning = scan(options.ipaddress)
print_result(result_scanning)