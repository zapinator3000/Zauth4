#!/usr/bin/env python
print("This client contains code from the following tutorials: ")
print("https://pythonspot.com/python-network-sockets-programming-tutorial/")
print("Please see the tutorial for more information and for great tips")
import socket


TCP_IP = '192.168.1.26'
TCP_PORT = 5005
TFTP_PORT = 5000
BUFFER_SIZE = 64000
MESSAGE = "Req_Conn"
print("Connecting to TFTP server...")
print("Done...Connecting to TCP Server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Done...")
def rec():
    data = s.recv(BUFFER_SIZE)
    return data
def send(data):
    try:
        s.send(data.encode())
    except:
        s.send(data)
    rtn=rec()
    return rtn.decode()
def close():
    print("Connection Closed...")
    s.close()
def upload_special(file,path):
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((TCP_IP, TFTP_PORT))
    f=str(file)+":"+open(path,"r").read()
    s2.send(f.encode())
    rtn=s2.recv(BUFFER_SIZE)
    if not rtn.decode()=="Success":
        print(rtn.decode())
        raise SystemError("The Following Error was reported: "+str(rtn.decode))
    print("Uploaded...")
