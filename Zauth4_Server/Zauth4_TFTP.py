import socket

print("[ TFTP SERVER ] : Starting Server...")
#!/usr/bin/env python
 
import socket, sys, os, re
from threading import Thread
from socketserver import ThreadingMixIn

class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[ TFTP SERVER + ] New thread started for "+ip+":"+str(port))


    def run(self):
        try:
            while True:
                data = conn.recv(2048)
                if not data: break
#                print ("received data:", data)
                dats=re.split(r":",data.decode())
                filename=dats[0]
                filedat=dats[1]
                print("[ TFTP SERVER ] Writing File: "+str(filename))
                open("magic/"+str(filename),"w+").write(str(filedat))
                print("[ TFTP SERVER ] > > > >Done")
                break
            conn.send(b'Success')
        except:
            print("[ TFTP SERVER "+str(self.ip)+" ] Something happened")
            conn.send(str(sys.exc_info()).encode())
        finally:
            print ("[ TFTP SERVER - ] Thread Ended "+ip+":"+str(port))

TCP_IP = '0.0.0.0'
TCP_PORT = 5000
BUFFER_SIZE = 64000  # Normally 1024, but we want fast response


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []
try:
    while True:
        tcpsock.listen(4)
        print ("[ TFTP SERVER ] : Waiting for incoming connections...")
        (conn, (ip,port)) = tcpsock.accept()
        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)
except:
    print("[ TFTP SERVER ] : Something went Wrong")
finally:
    print("[ TFTP SERVER ] : Closed TFTP server")
    tcpsock.close()
for t in threads:
    t.join()
