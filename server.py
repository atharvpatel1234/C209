# ------- Bolierplate Code Start -----


import socket
from  threading import Thread
import time

IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}
BUFFER_SIZE=4096


def acceptConnections():
    global SERVER
    global clients
    
    while True:
        client, addr = SERVER.accept()
        print(client, addr)
        client_name=client.recv(4096).decode().lower()
        clients[client_name]={
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096,


        }

        print(f"connection established with {client_name}:{addr}")
        thread=Thread(target=handleClient,args=(client,client_name,))
        print("HEllo")
        thread.start()

def handleClient(client,client_name):
    global clients
    global BUFFER_SIZE
    global SERVER
    
    print("checking")
    #Sending welcome Message
    banner1="Welcome, Your Now Connected To Server!! \n Click on Rfresh TO seeAll availabe Users.\n Select the User and click on Connect To start Chatting"
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE=clients[client_name]["file_size"]
            chunk=client.recv(BUFFER_SIZE)
            message=chunk.decode().strip().lower()
            if message:
                handleMessages(client,message,client_name)
            else:
                removeClient(client_name)
        except:
            pass

def handleMessages(client,message,client_name):
    if message=='show_list':
        handleShowList(client)


def removeClient():
    print("Remove Client")

def handleShowList(client):
    global clients
    counter=0

    for c in clients:
        counter+=1
        client_address=clients[c]["address"][0]
        connected_with=clients[c]["connected_with"]
        message=""
        if connected_with:
            message=f"{counter},{c},{client_address},connected With {connected_with},Tiul,\n "
        else:
            message=f"{counter},{c},{client_address},Available,Tiul \n"    
        client.send(message.encode())
        time.sleep(1)

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()




# ------ Bolierplate Code End -----------
