from cryptography.fernet import Fernet
import mysql.connector
import os
import random
###Encryption layer for the Game Console
print("[ ENCRYPTION ] : Encryption layer for the Zauth system has been loaded")
#key="I8sMQvPAFHA3VHFn0i-lOLSF5SZKusCRWxXaWs14eX4="
#key2="deA6J0ynM309jkn4o4nYyGhecnqRaQBL4IjOxXRF1tM="
def encrypt(ins,key):
    print("[ ENCRYPTION ] : Encrypting using key: "+str(key))
    cipher_suite= Fernet(key)

    #print("encrypting:"+str(ins))
    rand=random.randint(0,1)
#    print(rand)
    if rand==1:
        cipher_text=cipher_suite.encrypt(ins.encode())
        try:
            cipher_text2=cipher_suite.encrypt(cipher_text.encode())
        except:
            cipher_text2=cipher_suite.encrypt(cipher_text)
    else:
        cipher_text=cipher_suite.encrypt(ins.encode())

    return cipher_text
def decrypt(ins,key):
    cipher_suite= Fernet(key)
    x=1
    #print('Decrypting:'+str(ins))
    plain_text = cipher_suite.decrypt(ins.encode())

    try:
        x=x+1
        #print("Attempting decrypt"+str(x))
        plain_text=cipher_suite.decrypt(plain_text.encode())
    except:
        try:
        #print("Attempting decrypt"+str(x))
            plain_text=cipher_suite.decrypt(plain_text)
        except:
            pass
    try:
        return plain_text.decode()
    except:
        return plain_text
