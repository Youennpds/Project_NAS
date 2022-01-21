import getpass
import sys
import telnetlib

nbCoeurCoPE=2
nbCoCoeur=3

def configBordure(id, mdp, ip, connected, pos, nbCoeur, nbPE):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")

    tn.write(b"conf t\n")
    #config interface
    tn.write(b"interface Loopback0\n")
    a=str(100+10*(pos+1)).encode("ascii")
    tn.write(b"ip address "+a+b"."+a+b"."+a+b"."+a+b" 255.255.255.255\n")
    tn.write(b"ip ospf 100 area 0\n")

    for i in range(len(connected)+nbCoeurCoPE):
        tn.write(b"interface GigabitEthernet" + str(2+i).encode("ascii") + b"/0\n")
        if i < len(connected):
            tn.write(b"ip address 192.168."+str(10*(i+1)+20*pos).encode("ascii")+ b".1 255.255.255.0\n")
        else:
            tn.write(b"ip address 192.168."+str((i-1+2*pos)).encode("ascii")+ b".1 255.255.255.0\n")
        #tn.write(b"ip ospf 100 area 0\n")
        tn.write(b"no shutdown\n")

    #config ospf
    tn.write(b"router ospf 100\n")
    tn.write(b"router-id "+a+b"."+a+b"."+a+b"."+a+b"\n") # @ loopback
    for i in range(len(connected)):
        tn.write(b"passive-interface GigabitEthernet"+str(2+i).encode("ascii")+b"/0\n")
        tn.write(b"network 192.168."+str(10*(i+1)+20*pos).encode("ascii")+b".0 0.0.0.255 area 0\n")
    tn.write(b"mpls ldp autoconfig\n")

    #config bgp
    tn.write(b"router bgp 100\n")
    tn.write(b"bgp log-neighbor-changes\n")
    for i in range(nbCoeur):
        a=str(10*(i+1)).encode("ascii")
        tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" remote-as 100\n")
        tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" update-source Loopback0\n")
        tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" send-community\n")
    for i in range(nbPE):
        if i != pos:
            a=str(100+10*(i+1)).encode("ascii")
            tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" remote-as 100\n")
            tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" update-source Loopback0\n")
            tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" send-community\n")

    for i in range(len(connected)):
        a=str(10*(i+1)+20*pos).encode("ascii")
        if connected[i][1] == "client":
            tn.write(b"neighbor 192.168."+a+b".2 remote-as 1000\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Inbound-Customer in\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Outbound-Customer out\n")
        elif connected[i][1] == "peer":
            tn.write(b"neighbor 192.168."+a+b".2 remote-as 10000\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Inbound-Peer in\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Outbound-Peer out\n")
        elif connected[i][1] == "peering":
            tn.write(b"neighbor 192.168."+a+b".2 remote-as 100000\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Inbound-Peering in\n")
            tn.write(b"neighbor 192.168."+a+b".2 route-map Outbound-Peering out\n")
        else:
            print("ERROR IN ROUTER TYPE CONNECTED")

    tn.write(b"route-map Outbound-Peering permit 10\n")
    tn.write(b"match community Outbound-Peering\n")
    tn.write(b"route-map Outbound-Peer permit 10\n")
    tn.write(b"match community Outbound-Peer\n")
    tn.write(b"route-map Outbound-Customer permit 10\n")
    tn.write(b"match community Outbound-Customer\n")
    tn.write(b"route-map Inbound-Peering permit 10\n")
    tn.write(b"set local-preference 50\n")
    tn.write(b"set community 100:50\n")
    tn.write(b"route-map Inbound-Peer permit 10\n")
    tn.write(b"set local-preference 100\n")
    tn.write(b"set community 100:100\n")
    tn.write(b"route-map Inbound-Customer permit 10\n")
    tn.write(b"set local-preference 150\n")
    tn.write(b"set community 100:150\n")
    tn.write(b"exit\n")
    tn.write(b"ip community-list expanded Outbound-Customer permit 100:50\n")
    tn.write(b"ip community-list expanded Outbound-Customer permit 100:100\n")
    tn.write(b"ip community-list expanded Outbound-Customer permit 100:150\n")
    tn.write(b"ip community-list expanded Outbound-Peering permit 100:150\n")
    tn.write(b"ip community-list expanded Outbound-Peer permit 100:150\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode("ascii"))

def configCoeur(id, mdp, ip, nbCoeur, pos, nbPE, incr):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")

    tn.write(b"conf t\n")
    tn.write(b"interface Loopback0\n")
    a=str(10*(pos+1)).encode("ascii")
    tn.write(b"ip address "+a+b"."+a+b"."+a+b"."+a+b" 255.255.255.255\n")
    tn.write(b"ip ospf 100 area 0\n")

    for i in range(nbCoCoeur):
        tn.write(b"interface GigabitEthernet"+str(2+i).encode("ascii")+b"/0\n")
        tn.write(b"ip address 192.168."+str(incr).encode("ascii")+b"."+str(incr).encode("ascii")+b" 255.255.255.0\n")
        #tn.write(b"ip ospf 100 area 0\n")
        tn.write(b"no shutdown\n")
        incr+=1
        tn.write(b"exit\n")

    #ospf
    tn.write(b"router ospf 100\n")
    tn.write(b"router-id "+a+b"."+a+b"."+a+b"."+a+b"\n") # @loopback pour ospf
    tn.write(b"mpls ldp autoconfig\n")
    tn.write(b"exit\n")

    #bgp
    tn.write(b"router bgp 100\n")
    for i in range(nbCoeur):
        if i != pos:
            a=str(10*(i+1)).encode("ascii")
            tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" remote-as 100\n")
            tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" update-source Loopback0\n")
    for i in range(nbPE):
        a=str(100+10*(i+1)).encode("ascii")
        tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" remote-as 100\n")
        tn.write(b"neighbor "+a+b"."+a+b"."+a+b"."+a+b" update-source Loopback0\n")

    tn.write(b"\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode("ascii"))
    return(incr)

def configClient(id, mdp, ip, connected, type, posInConnectedListPE):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(id.encode("ascii") + b"\n")
    tn.read_until(b"Password:")
    tn.write(mdp.encode("ascii") + b"\n")

    tn.write(b"enable\n")
    tn.write(b"cisco\n")
    tn.write(b"conf t\n")
    tn.write(b"interface GigabitEthernet2/0\n")
    tn.write(b"ip address 192.168."+str(10*(posInConnectedListPE+1)+20*connected[1]).encode("ascii")+ b".2 255.255.255.0\n")
    tn.write(b"no shutdown\n")
    tn.write(b"exit\n")

    # bgp
    a = str(100+10*(connected[1]+1)).encode("ascii")
    tn.write(b"router bgp 100\n") # @ loopback du routeur de bordure auquel il est connecté, connected donne [id, pos] du routeur de bordure
    #tn.write(b"network 10.0.0.0 mask 255.255.255.0\n") #on en a besoin pour ping d'un endroit different et verif que tout marche
    if type == "client":
        a=1000
    elif type == "peer":
        a=10000
    elif type == "peering":
        a=100000
    else:
        print("Problème type client\n")

    tn.write(b"neighbor 192.168."+str(10*(posInConnectedListPE+1)+20*connected[1]).encode("ascii")+ b".1 remote-as "+str(a).encode("ascii")+b"\n") # SELON TYPE CLIENT

    tn.write(b"\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    print(tn.read_all().decode("ascii"))
