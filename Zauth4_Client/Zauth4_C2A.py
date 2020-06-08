import os,time
from cryptography.fernet import Fernet
import zauth4_client as z4c
version="0.1"
name="Zauth4 Client-2-Application Wrapper"
description="This module is a wrapper to sit between the client and the application."
print(str(name)+" is loaded")
class Wrapper:
        def __init__(self):
                print(str(name)+" ...Instance Created")
                print("Getting key...")
                key=self.send_cmd("Req_Conn","non-encrypted")
                self.set_session_key(key)
                self.cipher_suite= Fernet(key)
        def decrypt(self,data):
                try:
                        plain_text=self.cipher_suite.decrypt(data.encode())
                except:
                        plain_text=self.cipher_suite.decrypt(data)
                return plain_text
        def encrypt(self,data):
                try:
                        encrypt_text=self.cipher_suite.encrypt(data.encode())
                except:
                        encrypt_text=self.cipher_suite.encrypt(data)
                return encrypt_text
        def get_session_key(self):
                return self.Session_Key
        def set_session_key(self,key):
                self.Session_Key=key
        def send_cmd(self,cmd,mode="encrypted"):
                if mode=="encrypted":
                        cmd=self.encrypt(cmd)
                
                rtn=z4c.send(cmd)
                #print(rtn)
                if mode=="encrypted":
                        return self.decrypt(rtn).decode()
                else:
                        return rtn
        def close(self):
                print("Closing connection...")
                z4c.close()
        def send_special(self,filename,path):
                print("Sending Special File")
                z4c.upload_special(filename,path)
