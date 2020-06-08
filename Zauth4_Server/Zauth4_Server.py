#!/usr/bin/env python
# Base code taken from: https://pythonspot.com/python-network-sockets-programming-tutorial/ 
print("This server contains code from the following tutorials: ")
print("https://pythonspot.com/python-network-sockets-programming-tutorial/")
print("Please see the tutorial for more information and for great tips")
import time
time.sleep(1)
import os, sys
os.system("clear")
print("[ TCP SERV ] : Zauth4_Server Endpoint")
print("[ TCP SERV ] : Setting up a connection to zauth...")
import zauth_backend
import encryption
import socket
import re
print("[ TCP SERV ] : Connecting to S2A service...")
import Zauth4_S2A as S2A
S2A_Conn=S2A.Wrapper()
from threading import Thread
from socketserver import ThreadingMixIn
import tftpy
print("[ TCP SERV ] : Connecting to RSA handler...")
import rsa2
class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[ TCP SERV + ] : New thread started for "+str(ip)+":"+str(port))
        self.keys=rsa2.newkeys(5120)

    def WrappedSend(self,msg):
        print(msg)
        conn.send(rsa2.encrypt(msg,self.Client_PubKey))
    def run(self):
        try:
  #      if 1==1:
            while True:
                data = conn.recv(5120)
                if not data: break
                #conn.send(data)  # echo
                if "Req_Conn" in data.decode():
                    data=data.decode()
                    dats=re.split(r":",data)
                    print(dats[1])
                    self.Client_PubKey=rsa2.importKey(dats[1])
                    print("[ "+str(self.ip)+" ] : Connection Requested: ")
                    conn.send(self.keys[0].encode())
                else:
                     data=rsa2.decrypt(data,self.keys[1])
                     try:
 #                    if 1==1:
                        if data=="Get_SessionKey":
                            S2A_Conn.gen_session_key(self.ip)
                            self.WrappedSend(S2A_Conn.get_session_key(self.ip))

                        else:
                            dec_data=S2A_Conn.decrypt(data,self.ip)
                            print ("[ "+str(self.ip)+" ] : received data: "+ str(dec_data.decode()))
                            #print(dec_data.decode())
                            if "DEV_INIT" in dec_data.decode():
                                dats=re.split(r":",dec_data.decode())
                                zakey=dats[1] #Application Key
                                deckey=dats[2] # Decryption Key
                                self.zauth=zauth_backend.DevMode(zakey,deckey)
                                self.rtn=self.zauth.TMP_KEY #Return TMP key

                            elif "INIT" in dec_data.decode():
                                dats=re.split(r":",dec_data.decode())
                                zakey=dats[1] #Application Key
                                deckey=dats[2] # Decryption Key
                                self.zauth=zauth_backend.Zauth(zakey,deckey)
                                self.rtn=self.zauth.TMP_KEY #Return TMP key
                            else:
                                try:
#                            if 1==1:

                                    exec("self.rtn=self.zauth."+str(dec_data.decode()),{"self":self})
                                except:
                                    self.rtn=sys.exc_info()
                            encrtn=S2A_Conn.encrypt(self.rtn,self.ip)
                            print("[ "+str(self.ip)+" ] : Sending: "+str(encrtn))
                            self.WrappedSend(encrtn)
                     except:
                            print("Unknown Error: "+str(sys.exc_info()))
                            print("[ "+str(self.ip)+" ] : Session Key was not provided, Connection blocked")

                            conn.send(b'Invalid Key Detected')
                            conn.close()
                            break
        finally:
            print("[ TCP SERV - ] : Thread Ended "+str(self.ip))
TCP_IP = '0.0.0.0'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []
import subprocess as sp
#sp.Popen("python3 Zauth4_TFTP.py",shell=True)
def main_loop():
    global conn
    sp.Popen("python3 Zauth4_TFTP.py",shell=True)
    while True:
        tcpsock.listen(4)
        print ("[ TCP SERV ] : Waiting for incoming connections...")
        (conn, (ip,port)) = tcpsock.accept()
        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)
def reset_loop():
    try:
        main_loop()
    except KeyboardInterrupt:
        print("")
        print("[ TCP SERV ] : Connections Suspended...")
        ques=input("[ TCP SERV ] : Are you sure you would like to close the server? (y/n): ")
        if "y" in ques:
            raise SystemExit()
        else:
            print("[ TCP SERV ] : Restarting Main Loop...")
            reset_loop()
    finally:
        print("[ TCP SERV ] : Closing Connections...")
        tcpsock.close()
reset_loop()
for t in threads:
    t.join()



