import json
import getpass
import sys
import telnetlib

import setup as VM

# Opening json
with open('config.json') as json_data:
    data_dict = json.load(json_data)

# Récup data
bordures = list([])
coeurs = list([])
clients = list([])
connected = list([])
connectedList = list([])
D=data_dict["DeviceList"]
for router in D:
    for routerID in router:
        typeRouter=router[routerID]["typeRouter"]
        if typeRouter == "bordure":
            connectedList = list([])
            bordures.append(router)
            for ID in router[routerID]["connected"]:
                for router2 in D:
                    for routerID2 in router2:
                        if ID == routerID2:
                            connectedList.append([ID,router2[ID]["typeRouter"]])
        elif typeRouter == "coeur":
            coeurs.append(router)
        elif typeRouter == "client" or typeRouter == "peer" or typeRouter == "peering" :
            clients.append(router)
        else:
            print ("Type non valide")

# 1ere étape: config des routeurs de coeur
nbCoeur=len(coeurs)
nbPE=len(bordures)
for router in coeurs:
    for routerID in router:
        VM.configCoeur(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"], nbCoeur, coeurs.index(router), nbPE)

for router in bordures:
    for routerID in router:       
        VM.configBordure(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"], connectedList, bordures.index(router), nbCoeur, nbPE)

for router in clients:
    for routerID in router:
        connected = [router[routerID]["connected"][0], bordures.index(router[routerID]["connected"][0])]
        VM.configClient(routerID, router[routerID]["telnetPassword"], router[routerID]["ipAddress"], connected, router[routerID]["typeRouter"])

