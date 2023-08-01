#/usr/bin/env python

import subprocess
import optparse
import re


def getCurrentMac(interface):
    consoleOutput = subprocess.check_output(["ifconfig",interface])
    currentMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",consoleOutput)
    print("current Mac ->"+ str(currentMac.group(0)))
    subprocess.call(["ifconfig",interface])

def get_Arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Named the mac_Address")
    parse.add_option("-m", "--mac", dest="new_mac", help="enter the new mac address")
    (options, arguments) = parse.parse_args()
    if not options.interface:
        parse.error("Please specific the Interface or use help section for more info")
    elif not options.new_mac:
        parse.error("Please specify the new mac address or use help section for more info")
    else:
        return options

def changeMac(interface,new_mac):
    print("[+] your mac change seccessfully" + interface + " new mac " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



options = get_Arguments();
getCurrentMac(options.interface)
changeMac(options.interface,options.new_mac)







