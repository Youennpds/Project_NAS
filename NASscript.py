import json
import getpass
import sys
import telnetlib

# Opening json
with open('config.json') as json_data:
    data_dict = json.load(json_data)

# Récup data
for router in data_dict["DeviceList"]:  
    for routerID in router:
        
        host=router[routerID]["ipAddress"]
        user=routerID
        password=router[routerID]["telnetPassword"]
        typeRouter=router[routerID]["typeRouter"]
        print("Data récupérée : ",host,user,password,typeRouter)

        # Début telnet avec data récupérées
        tn = telnetlib.Telnet(host)

        tn.read_until(b"Username:")
        tn.write(user.encode("ascii") + b"\n")
        if password:
            tn.read_until(b"Password:")
            tn.write(password.encode("ascii")+b"\n")
            tn.write(b"en \n")
            tn.write(b"cisco\n")

            if typeRouter == "bordure":
                print('oui')
            elif typeRouter == "coeur":
                print('oui')
            elif typeRouter == "client":
                print("oui")
            else:
                print ("non")
                
            
            print(tn.read_all().decode("ascii"))
            print ("Configuration terminée \n")
            
"""
import json
import getpass
import sys
import telnetlib

import setup.py as VM

# Opening json
with open('config.json') as json_data:
    data_dict = json.load(json_data)

# Récup data
bordures = list([])
coeurs = list([])
clients = list([])
for router in data_dict["DeviceList"]:
    for routerID in router:
        typeRouter=router[routerID]["typeRouter"]
        if typeRouter == "bordure":
            bordures.append(router)
        elif typeRouter == "coeur":
            coeurs.append(router)
        elif typeRouter == "client":
            clients.append(router)
        else:
            print ("non")

for router in coeurs:
    for routerID in router:
        VM.configCoeur(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"])

for router in bordures:
    for routerID in router:
        VM.configBordure(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"])

for router in clients:
    for routerID in router:
        VM.configClient(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"])
"""
