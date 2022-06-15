#!/usr/bin/env python

# This code will throw error if specified interface isn't available

import subprocess
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", dest="interface", help="Interface Name")
parser.add_argument("-m", "--mac", dest="mac", help="New MAC address")
args = parser.parse_args()

interface = args.interface
mac = args.mac

if not interface:
    parser.error("[-] Interface name is required, use -h for more info")
elif not mac:
    default = "00:11:22:33:44:55"
    que = str(input(("[!] MAC address is not specified, would you like to use the default one? [Y/n]")))
    if que == "Y" or que == "y":
        mac = "00:11:22:33:44:55"
    else:
        parser.error("[-] MAC address is required, use --help for more info")

def mac_checker():
    ifconfig = subprocess.check_output(["ifconfig", interface])
    check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
    if not check:
        print("[-] Unable to find current MAC address")
    else:
        return check.group(0)

current_mac = str(mac_checker())

if len(current_mac) < 6:
    exit()
else:
    print(f"[+] Your current MAC address is {current_mac}")

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", mac])
subprocess.call(["ifconfig", interface, "up"])

current_mac = str(mac_checker())

if current_mac == mac:
    print(f"[+] MAC address has been successfully changed to {current_mac}")
else:
    print("MAC address could not be changed, check the entered MAC address")
