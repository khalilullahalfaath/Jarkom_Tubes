from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink, Link, Intf
from mininet.log import setLogLevel,info
from datetime import datetime
from mininet.node import CPULimitedHost
from subprocess import Popen, PIPE
 
import os
import time
 
if '__main__'==__name__:
	os.system("mn -c")
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s"%(key, value), shell=True, stdout=PIPE,stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)
 
	# Konfigurasi host
	hostA      = net.addHost("hostA")
	hostB      = net.addHost("hostB")
 
	# Konfigurasi router
	router1    = net.addHost("router1")
	router2    = net.addHost("router2")
	router3    = net.addHost("router3")
	router4    = net.addHost("router4")
 
	# Konfigurasi bandwidth dan buffer size
	# Ubah nilai buffer size jadi 20,40,60,100
	bw1 = {"bw": 1, "max_queue_size" : 100}
	bw2 = {"bw": 0.5, "max_queue_size" : 100}
 
	# Konfigurasi link
	net.addLink(hostA, router1,intfName1 = 'hostA-eth0',intfName2='router1-eth0', cls=TCLink, **bw1)
	net.addLink(hostA, router2,intfName1 = 'hostA-eth1',intfName2='router2-eth0', cls=TCLink, **bw1)
 
	net.addLink(hostB, router3,intfName1 = 'hostB-eth0',intfName2='router3-eth0', cls=TCLink, **bw1)
	net.addLink(hostB, router4,intfName1 = 'hostB-eth1',intfName2='router4-eth0', cls=TCLink, **bw1)
 
	net.addLink(router1, router4, intfName1 = 'router1-eth2',intfName2='router4-eth1', cls=TCLink, **bw1)
	net.addLink(router2, router3, intfName1 = 'router2-eth1',intfName2='router3-eth2', cls=TCLink, **bw1)
 
	net.addLink(router2, router4, intfName1 = 'router2-eth2',intfName2='router4-eth2', cls=TCLink, **bw2)
	net.addLink(router1, router3, intfName1 = 'router1-eth1',intfName2='router3-eth1',cls=TCLink, **bw2)
 		
	# bangun topology
	net.build()

	# mengaktifkan router
	router1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	router2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	router3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	router4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
 
	# Inisialisasi IP pada host A
	hostA.cmd("ifconfig hostA-eth0 0")
	hostA.cmd("ifconfig hostA-eth1 0")
	hostA.cmd("ifconfig hostA-eth0 192.150.0.1 netmask 255.255.255.252")
	hostA.cmd("ifconfig hostA-eth1 192.150.0.5 netmask 255.255.255.252")
	
	# Inisialisasi IP pada host B
	hostB.cmd("ifconfig hostB-eth0 0")
	hostB.cmd("ifconfig hostB-eth1 0")
	hostB.cmd("ifconfig hostB-eth0 192.150.0.9 netmask 255.255.255.252")
	hostB.cmd("ifconfig hostB-eth1 192.150.0.13 netmask 255.255.255.252")
	
	#Memasukkan IP router pada router 1
	router1.cmd("ifconfig router1-eth0 0")
	router1.cmd("ifconfig router1-eth1 0")	
	router1.cmd("ifconfig router1-eth2 0")
	router1.cmd("ifconfig router1-eth0 192.150.0.2 netmask 255.255.255.252")
	router1.cmd("ifconfig router1-eth1 192.150.0.17 netmask 255.255.255.252")
	router1.cmd("ifconfig router1-eth2 192.150.0.29 netmask 255.255.255.252")
		
	#Memasukkan IP router pada router 2
	router2.cmd("ifconfig router2-eth0 0")
	router2.cmd("ifconfig router2-eth1 0")	
	router2.cmd("ifconfig router2-eth2 0")
	router2.cmd("ifconfig router2-eth0 192.150.0.6 netmask 255.255.255.252")
	router2.cmd("ifconfig router2-eth1 192.150.0.25 netmask 255.255.255.252")
	router2.cmd("ifconfig router2-eth2 192.150.0.21 netmask 255.255.255.252")
		
	#Memasukkan IP router pada router 3
	router3.cmd("ifconfig router3-eth0 0")
	router3.cmd("ifconfig router3-eth1 0")	
	router3.cmd("ifconfig router3-eth2 0")
	router3.cmd("ifconfig router3-eth0 192.150.0.10 netmask 255.255.255.252")
	router3.cmd("ifconfig router3-eth1 192.150.0.18 netmask 255.255.255.252")
	router3.cmd("ifconfig router3-eth2 192.150.0.26 netmask 255.255.255.252")
	
	#Memasukkan IP router pada router 4
	router4.cmd("ifconfig router4-eth0 0")
	router4.cmd("ifconfig router4-eth1 0")	
	router4.cmd("ifconfig router4-eth2 0")
	router4.cmd("ifconfig router4-eth0 192.150.0.14 netmask 255.255.255.252")
	router4.cmd("ifconfig router4-eth1 192.150.0.30 netmask 255.255.255.252")
	router4.cmd("ifconfig router4-eth2 192.150.0.22 netmask 255.255.255.252")

	# routing tetangga hostA
	hostA.cmd("ip rule add from 192.150.0.1 table 1") #intf -eth0
	hostA.cmd("ip rule add from 192.150.0.5 table 2") #intf -eth1
	hostA.cmd("ip route add 192.150.0.0/30 dev hostA-eth0 scope link table 1")
	hostA.cmd("ip route add default via 192.150.0.2 dev hostA-eth0 table 1")
	hostA.cmd("ip route add 192.150.0.4/30 dev hostA-eth1 scope link table 2")
	hostA.cmd("ip route add default via 192.150.0.6 dev hostA-eth1 table 2")
	hostA.cmd("ip route add default scope global nexthop via 192.150.0.2 dev hostA-eth0")	
	
	# routing tetangga hostB
	hostB.cmd("ip rule add from 192.150.0.9 table 1") #intf -eth0
	hostB.cmd("ip rule add from 192.150.0.13 table 2") #intf -eth1
	hostB.cmd("ip route add 192.150.0.8/30 dev hostB-eth0 scope link table 1")
	hostB.cmd("ip route add default via 192.150.0.10 dev hostB-eth0 table 1")
	hostB.cmd("ip route add 192.150.0.12/30 dev hostB-eth1 scope link table 2")
	hostB.cmd("ip route add default via 192.150.0.14 dev hostB-eth1 table 2")
	hostB.cmd("ip route add default scope global nexthop via 192.150.0.10 dev hostB-eth0")
	
	# routing tetangga router1
	router1.cmd("ip rule add from 192.150.0.2 table 1") #intf -eth0
	router1.cmd("ip rule add from 192.150.0.17 table 2") #intf -eth1
	router1.cmd("ip rule add from 192.150.0.29 table 3") #intf -eth2
	router1.cmd("ip route add 192.150.0.0/30 dev router1-eth0 scope link table 1")
	router1.cmd("ip route add default via 192.150.0.1 dev router1-eth0 table 1")
	router1.cmd("ip route add 192.150.0.16/30 dev router1-eth1 scope link table 2")
	router1.cmd("ip route add default via 192.150.0.18 dev router1-eth1 table 2")
	router1.cmd("ip route add 192.150.0.28/30 dev router1-eth2 scope link table 3")
	router1.cmd("ip route add default via 192.150.0.30 dev router1-eth2 table 3")
	router1.cmd("ip route add default scope global nexthop via 192.150.0.1 dev router1-eth0")

	# routing tetangga router2
	router2.cmd("ip rule add from 192.150.0.6 table 1") #intf -eth0
	router2.cmd("ip rule add from 192.150.0.25 table 2") #intf -eth1
	router2.cmd("ip rule add from 192.150.0.21 table 3") #intf -eth2
	router2.cmd("ip route add 192.150.0.4/30 dev router2-eth0 scope link table 1")
	router2.cmd("ip route add default via 192.150.0.5 dev router2-eth0 table 1")
	router2.cmd("ip route add 192.150.0.24/30 dev router2-eth1 scope link table 2")
	router2.cmd("ip route add default via 192.150.0.26 dev router2-eth1 table 2")
	router2.cmd("ip route add 192.150.0.20/30 dev router2-eth2 scope link table 3")
	router2.cmd("ip route add default via 192.150.0.22 dev router2-eth2 table 3")
	router2.cmd("ip route add default scope global nexthop via 192.150.0.5 dev router2-eth0")
	
	# routing tetangga router3
	router3.cmd("ip rule add from 192.150.0.10 table 1") #intf -eth0
	router3.cmd("ip rule add from 192.150.0.18 table 2") #intf -eth1
	router3.cmd("ip rule add from 192.150.0.26 table 3") #intf -eth2
	router3.cmd("ip route add 192.150.0.8/30 dev router3-eth0 scope link table 1")
	router3.cmd("ip route add default via 192.150.0.9 dev router3-eth0 table 1")
	router3.cmd("ip route add 192.150.0.16/30 dev router3-eth1 scope link table 2")
	router3.cmd("ip route add default via 192.150.0.17 dev router3-eth1 table 2")
	router3.cmd("ip route add 192.150.0.24/30 dev router3-eth2 scope link table 3")
	router3.cmd("ip route add default via 192.150.0.25 dev router3-eth2 table 3")
	router3.cmd("ip route add default scope global nexthop via 192.150.0.9 dev router3-eth0")

	# routing tetangga router4
	router4.cmd("ip rule add from 192.150.0.14 table 1") #intf -eth0
	router4.cmd("ip rule add from 192.150.0.30 table 2") #intf -eth1
	router4.cmd("ip rule add from 192.150.0.22 table 3") #intf -eth2
	router4.cmd("ip route add 192.150.0.12/30 dev router4-eth0 scope link table 1")
	router4.cmd("ip route add default via 192.150.0.13 dev router4-eth0 table 1")
	router4.cmd("ip route add 192.150.0.28/30 dev router4-eth1 scope link table 2")
	router4.cmd("ip route add default via 192.150.0.29 dev router4-eth1 table 2")
	router4.cmd("ip route add 192.150.0.20/30 dev router4-eth2 scope link table 3")
	router4.cmd("ip route add default via 192.150.0.21 dev router4-eth2 table 3")
	router4.cmd("ip route add default scope global nexthop via 192.150.0.13 dev router4-eth0")

	# routing router1
	router1.cmd("route add -net 192.150.0.8/30 gw 192.150.0.18")
	router1.cmd("route add -net 192.150.0.12/30 gw 192.150.0.30")
	router1.cmd("route add -net 192.150.0.20/30 gw 192.150.0.30")
	router1.cmd("route add -net 192.150.0.4/30 gw 192.150.0.1")
	router1.cmd("route add -net 192.150.0.24/30 gw 192.150.0.18")
	
	# routing router2
	router2.cmd("route add -net 192.150.0.0/30 gw 192.150.0.5")
	router2.cmd("route add -net 192.150.0.16/30 gw 192.150.0.26")
	router2.cmd("route add -net 192.150.0.8/30 gw 192.150.0.26")
	router2.cmd("route add -net 192.150.0.12/30 gw 192.150.0.22")
	router2.cmd("route add -net 192.150.0.28/30 gw 192.150.0.22")

	# routing router3
	router3.cmd("route add -net 192.150.0.4/30 gw 192.150.0.25")
	router3.cmd("route add -net 192.150.0.0/30 gw 192.150.0.17")
	router3.cmd("route add -net 192.150.0.20/30 gw 192.150.0.25")
	router3.cmd("route add -net 192.150.0.12/30 gw 192.150.0.9")
	router3.cmd("route add -net 192.150.0.28/30 gw 192.150.0.17")

	# routing router4
	router4.cmd("route add -net 192.150.0.0/30 gw 192.150.0.29")
	router4.cmd("route add -net 192.150.0.4/30 gw 192.150.0.21")
	router4.cmd("route add -net 192.150.0.8/30 gw 192.150.0.13")
	router4.cmd("route add -net 192.150.0.16/30 gw 192.150.0.29")
	router4.cmd("route add -net 192.150.0.24/30 gw 192.150.0.21")
	
	#############################################################
	##############################CLO3###########################	
	#############################################################
	
	# Membuat server
	# hostB.cmd("iperf -s &")

	# Membuat file wireshark
	# hostB.cmd("tcpdump -w 1301204376jarkomyes.pcap &")
	
	# Membuat client
	# hostA.cmd("iperf -c 192.150.0.9 -t 100 &")
	# time.sleep(10)
	# hostA.cmd("iperf -c 192.150.0.9")


	#############################################################
	##############################CLO4###########################
	#############################################################
	
	# Menjalankan background traffic 
	hostB.cmd("iperf -s &")
	hostA.cmd("iperf -t 60 -c 192.150.0.9")
	
	CLI(net)
net.stop()







		
		
		
		
		
