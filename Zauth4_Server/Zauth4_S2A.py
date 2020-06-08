import os,time
from cryptography.fernet import Fernet
version="0.1"
name="Zauth4 Server-2-Application Wrapper"
description="This module is a wrapper to sit between the server and the application."
print("[ S2A ] : "+str(name)+" is loaded")
ips={}
class Wrapper:
	def __init__(self):
		print("[ S2A ] : "+str(name)+" ...Instance Created")
	def gen_session_key(self,ip):
		print("[ S2A ] : Generating Session Key:")
		self.Session_Key = Fernet.generate_key()
		ips[ip]=self.Session_Key
		return self.Session_Key
	def decrypt(self,data,ip):
		self.cipher_suite= Fernet(ips[ip])
		try:
			plain_text=self.cipher_suite.decrypt(data.encode())
		except:
			plain_text=self.cipher_suite.decrypt(data)
		return plain_text
	def encrypt(self,data,ip):
		self.cipher_suite= Fernet(ips[ip])
		try:
			encrypt_text=self.cipher_suite.encrypt(str(data).encode())
		except:
			encrypt_text=self.cipher_suite.encrypt(data)
		return encrypt_text
	def get_session_key(self,ip):
		return ips[ip]

