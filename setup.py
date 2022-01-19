import getpass
import sys
import telnetlib

def configBordure(id, mdp, ip, connected, pos, nbCoeur, nbPE):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")

    #config interface
    tn.write(b"interface Loopback0\n")
    tn.write(b"ip address "+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+" 255.255.255.255\n")
    tn.write(b"ip ospf 100 area 0\n") 
    tn.write(b"interface GigabitEthernet\n")
    tn.write(b"ip address\n")
    tn.write(b"ip ospf\n")

    #config ospf
    tn.write(b"router ospf 100\n")
    tn.write(b"router-id "+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+"."+str(100+10*(pos+1))+"\n") # @ loopbach
    for i in range(len(connected)):
        tn.write(b"passive-interface GigabitEthernet"+str(3+i))+"/0\n")
        tn.write(b"network 192.168."+str(20*(i+1)))+".0 0.0.0.255 area 0\n")
    tn.write(b"mpls ldp autoconfig\n")

    """
    tn.write(b"passive-interface GigabitEthernet3/0\n")
    tn.write(b"passive-interface GigabitEthernet4/0\n") #?
    tn.write(b"network 192.168.20.0 0.0.0.255 area 0\n") # client
    tn.write(b"network 192.168.40.0 0.0.0.255 area 0\n") # peer
    """

    #config bgp
    tn.write(b"router bgp 100\n")
    tn.write(b"bgp log-neighbor-changes\n")
    for i in range(nbCoeur):
        tn.write(b"neighbor "+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+" remote-as 100\n")
        tn.write(b"neighbor "+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+" update-source Loopback0\n")
        tn.write(b"neighbor "+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+" send-community\n")
    for i in range(nbPE):
        if i != pos:
            tn.write(b"neighbor "+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+" remote-as 100\n") 
            tn.write(b"neighbor "+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+" update-source Loopback0\n")
            tn.write(b"neighbor "+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+" send-community\n")

    for i in range(len(connected)):
        if connected[i][1] == "client":
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 remote-as 1000\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Inbound-Customer in\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Outbound-Customer out\n")
        elif connected[i][1] == "peer":
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 remote-as 10000\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Inbound-Peer in\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Outbound-Peer out\n")
        elif connected[i][1] == "peering":
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 remote-as 10000\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Inbound-Peering in\n")
            tn.write(b"neighbor 192.168."+str(20*(i+1)))+".2 route-map Outbound-Peering out\n")
        else:
            print("ERROR IN ROUTER TYPE CONNECTED")

    tn.write(b"route-map Outbound-Peering permit 10\n")
    tn.write(b"match community Outbound-Peering\n")
    tn.write(b"!\n")
    tn.write(b"route-map Outbound-Peer permit 10\n")
    tn.write(b"match community Outbound-Peer\n")
    tn.write(b"!\n")
    tn.write(b"route-map Outbound-Customer permit 10\n")
    tn.write(b"match community Outbound-Customer\n")
    tn.write(b"!\n")
    tn.write(b"route-map Inbound-Peering permit 10\n")
    tn.write(b"set local-preference 50\n")
    tn.write(b"set community 100:50\n")
    tn.write(b"!\n")
    tn.write(b"route-map Inbound-Peer permit 10\n")
    tn.write(b"set local-preference 100\n")
    tn.write(b"set community 100:100\n")
    tn.write(b"!\n")
    tn.write(b"route-map Inbound-Customer permit 10\n")
    tn.write(b"set local-preference 150\n")
    tn.write(b"set community 100:150\n")

    tn.write(b"ip community-list expanded Outbound-Customer permit 100:150\n")
    tn.write(b"ip community-list expanded Outbound-Customer permit 100:100\n")
    tn.write(b"ip community-list expanded Outbound-Customer permit 100:50\n")
    tn.write(b"!\n")
    tn.write(b"ip community-list expanded Outbound-Peering permit 100:150\n")
    tn.write(b"!\n")
    tn.write(b"ip community-list expanded Outbound-Peer permit 100:150\n")
    tn.write(b"!\n")

    tn.write(b"\n")
    tn.write(b"end\n")

def configCoeur(id, mdp, ip, nbCoeur, pos, nbPE):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")

    tn.write(b"interface Loopback0\n")
    tn.write(b"ip address "+str(10*(pos+1))+"."+str(10*(pos+1))+"."+str(10*(pos+1))+"."+str(10*(pos+1))+" 255.255.255.255\n")
    tn.write(b"ip ospf XXX area X\n") # !!!!!!!!
    tn.write(b"interface GigabitEthernet\n")
    tn.write(b"ip address\n")
    tn.write(b"ip ospf\n")

    #ospf
    tn.write(b"router ospf XXX\n")
    tn.write(b"router-id XX.XX.XX.XX\n")
    tn.write(b"mpls ldp autoconfig\n")

    #bgp
    tn.write(b"router bgp 100\n")
    for i in range(nbCoeur):
        if i != pos:
            tn.write(b"neighbor "+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+" remote-as 100\n")
            tn.write(b"neighbor "+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+"."+str(10*(i+1))+" update-source Loopback0\n")
    for i in range(nbPE):
        tn.write(b"neighbor "+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+" remote-as 100\n")
        tn.write(b"neighbor "+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+"."+str(100+10*(i+1))+" update-source Loopback0\n")

    tn.write(b"\n")
    tn.write(b"end\n")

def configClient(id, mdp, ip, connected):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")

    #bgp
    a = str(100+10*(connected[1]+1))
    tn.write(b"router bgp "+ a +"."+ a +"."+ a +"."+ a +"\n") # @ loopback du routeur de bordure auquel il est connecté, connected donne [id, pos] du routeur de bordure
    tn.write(b"network 10.0.0.0 mask 255.255.255.0\n")
    tn.write(b"neighbor 192.168.20.1 remote-as 100\n") # On met le numero du AS auquel appartient le routeur de bordure


    tn.write(b"\n")
    tn.write(b"end\n")