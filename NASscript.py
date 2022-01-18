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
