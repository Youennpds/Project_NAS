
import getpass
import sys
import telnetlib

HOST = "192.168.122.71"
user = raw_input("Enter your telnet username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until("Username: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

# ********** CONFIUGURATION DES ROUTEURS DE BORDURES PE1 ET PE2 **************

# Configuration des interfaces

tn.write("configure terminal\n")
tn.write("interface Loopback0\n") 
tn.write("ip address X.X.X.X 255.255.255.255\n")  #a completer avec la bonne adresse
tn.write("ip ospf XXX area X\n")                #a completer avec la bonne adresse
tn.write("exit\n")
tn.write("interface GigabitEthernet\n")   
tn.write("ip address\n")            #a completer avec la bonne adresse
tn.write("ip ospf\n")               #a completer avec la bonne adresse
tn.write("exit\n")

#Configuration de OSPF
tn.write("router ospf XXX\n")     #a completer
tn.write("router-id XX.XX.XX.XX\n")
tn.write("passive-interface GigabitEthernet3/0\n")
tn.write("passive-interface GigabitEthernet4/0\n")
tn.write("network 192.168.20.0 0.0.0.255 area 0\n")
tn.write("network 192.168.40.0 0.0.0.255 area 0\n")
tn.write("mpls ldp autoconfig\n")
tn.write("exit\n")

#Les interfaces qui quittent le routeur de bordure pour aller vers les clients doivent être en OSPF passif

# Configuration de BGP
tn.write("router bgp XXX\n")  #a completer
tn.write("neighbor 10.10.10.10 remote-as 100\n")
tn.write("neighbor 10.10.10.10 update-source Loopback0\n")
tn.write("neighbor 20.20.20.20 remote-as 100\n")
tn.write("neighbor 20.20.20.20 update-source Loopback0\n")
tn.write("neighbor 30.30.30.30 remote-as 100\n")
tn.write("neighbor 30.30.30.30 update-source Loopback0\n")
tn.write("neighbor 40.40.40.40 remote-as 100\n")
tn.write("neighbor 40.40.40.40 update-source Loopback0\n")
tn.write("neighbor 120.120.120.120 remote-as 100\n")
tn.write("neighbor 120.120.120.120 update-source Loopback0\n")
tn.write("neighbor 192.168.20.2 remote-as 1000\n")
tn.write("neighbor 192.168.20.2 send-community\n")
tn.write("neighbor 192.168.20.2 route-map customer-in in\n")
tn.write("neighbor 192.168.20.2 route-map customer-out out\n")
tn.write("neighbor 192.168.40.2 remote-as 10000\n")
tn.write("neighbor 192.168.40.2 send-community\n")
tn.write("neighbor 192.168.40.2 route-map peer-in in\n")
tn.write("neighbor 192.168.40.2 route-map peer-out out\n")

# Configuration du trafic In/Out(Bound)
    #Creation des routes maps
    tn.write("route-map XXX\n")  # a completer
    tn.write("set local-preference 150 | set community 100:150\n") #pour les clients
    tn.write("set local-preference 100 | set community 100:100\n") #pour les peer
    tn.write("set local-preference 50  | set community 100:50\n") #pour les peering
    tn.write("end\n")


#****************CONFIGURATION DES ROUTERS DE COEURS***************************

#Configuration des interfaces
tn.write("configure terminal\n")
tn.write("interface Loopback0\n") 
tn.write("ip address X.X.X.X 255.255.255.255\n")  #a completer avec la bonne adresse
tn.write("ip ospf XXX area X\n")                #a completer avec la bonne adresse
tn.write("exit\n")
tn.write("interface GigabitEthernet\n")   
tn.write("ip address\n")            #a completer avec la bonne adresse
tn.write("ip ospf\n")          1
     #a completer avec la bonne adresse
tn.write("exit\n")

#Configuration de OSPF
tn.write("router ospf XXX\n")     #a completer
tn.write("router-id XX.XX.XX.XX\n")
tn.write("mpls ldp autoconfig\n")

#Configuration de BGP
tn.write("router bgp 100\n") 
tn.write("neighbor 20.20.20.20 remote-as 100\n")
tn.write("neighbor 20.20.20.20 update-source Loopback0\n")
tn.write("neighbor 30.30.30.30 remote-as 100\n")
tn.write("neighbor 30.30.30.30 update-source Loopback0\n")
tn.write("neighbor 40.40.40.40 remote-as 100\n")
tn.write("neighbor 40.40.40.40 update-source Loopback0\n")
tn.write("neighbor 110.110.110.110 remote-as 100\n")
tn.write("neighbor 110.110.110.110 update-source Loopback0\n")
tn.write("neighbor 120.120.120.120 remote-as 100\n")
tn.write("neighbor 120.120.120.120 update-source Loopback0\n")

#*********** CONFIGURATION DES ROUTEURS CLIENTS : TYPE CE************

#Configuration des interfaces


#Configuration de BGP
tn.write("router bgp XXXX\n")
tn.write("network 10.0.0.0 mask 255.255.255.0\n")
tn.write("neighbor 192.168.20.1 remote-as XXX\n")  #On met le numero du AS auquel appartient le routeur de bordure

print tn.read_all()