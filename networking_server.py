# websites and servers - has static IP address
# computer and mobile devices have dynamic IP addresses
# if IP address as street then port number tells house number 
import sys
import socket
import threading

def creating_socket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0" # Ip address of host 
        port = 5000
        s=socket.socket() # creating socket
    except socket.error as msg:
        print("socket creation error: " + str(msg))

def binding_socket():
    try:
        global host
        global port
        global s
        
        print("socket binded to port: ",str(port))
        
        s.bind((host,port)) # binding socket
        
        s.listen(5) # listening for incoming connections , here 5 max number of connections that it can accept
        
        accepting_connections()
    except socket.error as msg:
        print("socket binding error: " + str(msg))
        binding_socket()

def send_message(cli):
    while True:
        cmd=input("enter the command you want to send : ")
        if(cmd=='q'):
            print("Client has disconnected")
            cli.close()
            s.close()
            sys.exit()
            break
        if(len(str(cmd.encode()))!=0):
            cli.send(cmd.encode()) # sending command to client
            client_response=str(cli.recv(1024).decode('utf-8'))
            print(client_response)
                   
def accepting_connections():
    cli, addr = s.accept() # addr[0] is the IP address and addr[1] is the port number
    print("Connected with: ", addr[0], ":", str(addr[1]))
    send_message(cli)
    cli.close()
    
    
if __name__ == "__main__":
    creating_socket()
    binding_socket()