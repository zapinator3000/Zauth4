#!/usr/bin/python
##2019 Zackery Painter
# Do not attempt to modify this software in any way
# Attempting to do so may cause incompatability in the software
# It is not recommended to add any code in this software
####
# Inspection code is modified and originally from https://stackoverflow.com/questions/2654113/how-to-get-the-callers-method-name-in-the-called-method
import os
import time
from cryptography.fernet import Fernet
import mysql.connector
import datetime
import urllib3.request
import inspect
First=True
try:##Connect to the server
        cnx = mysql.connector.connect(user='default', password='P@sSWORD',
             host="192.168.1.26",
             database="zauth")
        print("[ BACKEND ] : Connected!")
 
except:
#        os.system("tput setaf 1")
        input("[ BACKEND ] : ERROR: Connection Failed")
#        os.system("tput setaf 7")
        quit()
try:

        urllib.request.urlretrieve ("http://zzmines.ddns.net/zauth/encryption.pyc","encryption.pyc")
        
except:
        print("[ BACKEND ] : WARNING: Unable to get new encryption system! You may experience compatability issues!")
import encryption as ec
# This class contains everything for internal use only.
class __Internal:
    def __init__(self):
        # Check to make sure the call is being made internally
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        self.NOVER=False
        if not "zauth_backend.py" in  calframe[1][1]:
                print("[ BACKEND ] : Authorization Error: This function is for module internal use only, but you attempted to import it externally")
                raise PermissionError("You do not have permission to use this section")
                
        #print(calframe)
##        print('caller name:', calframe[1][1])
        if Zauth.DEBUG==True:
                print("Internal Library loaded")
        
    def lookup(self, types,query,key):
        # Check to make sure the call is being made internally
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        self.NOVER=False
        if not "zauth_backend.py" in  calframe[1][1]:
                print("[ BACKEND ] : Authorization Error: This function is for module internal use only, but you attempted to import it externally")
                raise PermissionError("You do not have permission to use this section")
          
        x=0

#        app=Zauth.keyhandle(key)
        if Zauth.DEBUG==True:
            print("[ BACKEND ] : Looking up: "+str(query)+" by: "+str(types))
        if types=="username":
            get=("SELECT * FROM userdb;")
            cursor=cnx.cursor()
            cursor.execute(get)
            for dat in cursor:
                username=ec.decrypt(dat[0],Zauth.decryption_key)
                if str(username)==str(query):
                    x=x+1
                    if Zauth.DEBUG==True:
                        print("[ BACKEND ] : Gathering information...")
                    password=ec.decrypt(dat[1],Zauth.decryption_key)
                    Firstname=ec.decrypt(dat[2],Zauth.decryption_key)
                    Lastname=ec.decrypt(dat[3],Zauth.decryption_key)
                    email=ec.decrypt(dat[4],Zauth.decryption_key)
                    try:
                        apps=ec.decrypt(dat[5],Zauth.decryption_key)
                    except:
                        if Zauth.DEBUG==True:
                            print("[ BACKEND ] : No apps")
                        apps="None"

                ##Wait for system to complete query to prevent errors
            cursor.close()
            #Zauth.log(app," Looked up username by username search:"+username)
            if x>0:                
                    return [username,password,Firstname,Lastname,email,apps]
            else:
                    #Zauth.log(app," Username lookup failed!")
                    raise NameError("Username not found")
        if types=="username_enc":
            get=("SELECT * FROM userdb;")
            cursor=cnx.cursor()
            cursor.execute(get)
            for dat in cursor:
                username=ec.decrypt(dat[0],Zauth.decryption_key)
                if username==query:
                    x=x+1
                    if Zauth.DEBUG==True:
                        print("[ BACKEND ] : Gathering information...")
                    password=dat[1]
                    Firstname=dat[2]
                    Lastname=dat[3]
                    email=dat[4]
                    enc_user=dat[0]
                    try:
                        apps=dat[5]
                    except:
                        if Zauth.DEBUG==True:
                            print("[ BACKEND ] : No apps")
                        apps="None"
            cursor.close()

            #self.log(app," Looked up username by encrypted username search")
            if x>0:                
                    return [enc_user,password,Firstname,Lastname,email,apps]
            else:
                    #self.log(app," Username_enc lookup failed!")    
                    raise NameError("Username not found")
    def test(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if not "zauth_backend.py" in  calframe[1][1]:
                return "Fail"
        else:
                return "Pass"
class Zauth:
    DEBUG=False
    NOVER=False
    decryption_key=None
    def __init__(self,key,dec_key):
        self.DEBUG=False

        if self.DEBUG==True:
                print("[ BACKEND ] : Key exchange in process...")
        Zauth.decryption_key=ec.decrypt(key,dec_key)
        if self.DEBUG==True:
                print("[ BACKEND ] : Decryption key decrypted and loaded...")
                print("[ BACKEND ] : Generating Temp security key...")
        Zauth.TMP_KEY = Fernet.generate_key()

    def test_security(self):
        test1=SecureUse.test()
        # This function shouldn't be able to create an instance of the external class
        test2="Fail"
        try:
                test2 = __Internal()
                
                #print("External Call Test: Fail")
        except:
                test2="Pass"
                #print("External Call Test: Pass")
        return test1,test2
    def checklog(self,key,searchfor,query):

        app=self.keyhandle(key)
        sel=("SELECT * FROM logs")
        cursor=cnx.cursor()
        cursor.execute(sel)
        for data in cursor:
                if searchfor=="App":
                        if data[0].lower()==query.lower():
                                print(data[0]+": "+data[1]+" | "+data[2])
                elif searchfor=="Tag":
                        if query.lower() in data[1].lower():
                                print(data[0]+": "+data[1]+" | "+data[2])
                elif searchfor=="Date":
                        if query.lower() in data[2].lower():
                                print(data[0]+": "+data[1]+" | "+data[2])
 
                else:                                
                        print(data[0]+": "+data[1]+" | "+data[2])

        cursor.close()
        if searchfor=="App":
                 self.log(app," Read log check for App name")
        elif searchfor=="Tag":
                 self.log(app," Read log check for Tag in string")
        elif searchfor=="Date":
                 self.log(app," Read log check for date")
        else:                                
                self.log(app," Read full log check")
    def log(self,app,item):
        timestamp=datetime.datetime.now().strftime('%m-%d-%Y %H:%M')
        if self.DEBUG==True:
           print("[ BACKEND ] : Logging: "+app+" doing: "+str(item)+" at the time: "+timestamp)
        upld= ("INSERT INTO logs "
            "(app, action, timestamp)"
            "VALUES (%(app)s, %(action)s, %(timestamp)s)")
        upld_dat = {
                'app':app,
                'action':item,
                'timestamp':timestamp
                 }
        cursor = cnx.cursor()
        cursor.execute(upld,upld_dat)
        cnx.commit()
        cursor.close()
    def generate_api_code(key):
        SecureUse.NOVER=True
        ##            init("gAAAAABcMPsujFYOJDSJyFDZydhAd8yWZAC22RPTq3QwdJ641isVPJ6gYQkvmjVNSrjAzYlyGazc_2baBrqAkzdHUlVaVSzN0J8vxVWAoun-SkE_SBcQHFIvPfMECfk0yiSPLUiissq8","RDe-pJ0TzhvM1tBurDMO51hYNi87rnsxKoVaaHrZidU=")#This is the skeleton Key that contains the real encryption key.
        app=self.keyhandle(Zauth.TMP_KEY+Zauth.key)
        ##            print(app)
        key=key.replace(TMP_KEY,"")
        if Zauth.DEBUG==True:
                print("[ BACKEND ] : Generating API system key: ")
        tmp=ec.encrypt(Zauth.decryption_key,str(Zauth.key))
        open(str(app)+"_key.txt","a").write("\nAPI KEY:\n"+tmp)
        if Zauth.DEBUG==True:
                print("[ BACKEND ] : Done")
        log(app," Generated new API key")
        SecureUse.NOVER=False 
    def generate_special(self,key,app):
        import random
        self.keyhandle(key)
        selected = random.randint(1, 10)
       # print(selected)
        tmp=[]
        prev_rand=0
        x=0
        rand=0
        while x<10:
                x=x+1
                #print(str(selected)+":"+str(x))
                for i in range(4):
                        rand = random.randint(1, 200000)
                        prev_rand=prev_rand+rand
                final=ec.encrypt(str(prev_rand),self.decryption_key)
                if int(x)==int(selected):
                        #print("Adding encrypted app dat")
                        rtn=ec.encrypt(str(app),self.decryption_key)
                        tmp.append(rtn)
                else:
                        tmp.append(final)
        for item in tmp:
                print("[ BACKEND ] : Generated: "+str(item))
        for item in tmp:
                print("[ BACKEND ] : Decrypted: "+ec.decrypt(item,self.decryption_key))

        executable= ("INSERT INTO authorizations "
        "(app, line, code)"
        "VALUES (%(app)s, %(line)s, %(code)s)")
        dat = {
         'app':str(ec.encrypt(app,self.decryption_key)),
         'line':str(ec.encrypt(str(selected),self.decryption_key)),
         'code':rtn
          }
        cursor = cnx.cursor()
        cursor.execute(executable,dat)
        cnx.commit()
        cursor.close()
        print("[ BACKEND ] : System has generated the application information")
        open("magic/"+app+".zauth","w+").write("")
        for item in tmp:
                open(app.decode()+".zauth","a").write(item+"\n")
        print("[ BACKEND ] : Special file has been generated: "+str(app+".zauth"))
        self.log(app,"New Special file was generated!")
    def keycheck(self,key):##Basic Keycheck script with external processing required
        x=0
        Fail=False
        global First
        if self.DEBUG==True:
            print("[ BACKEND ] : Checking application key...")
        get=("SELECT * FROM keytable")
        cursor=cnx.cursor()
        cursor.execute(get)
        for item in cursor:
            complete_key=str(Zauth.TMP_KEY)+str(item[0])
#            print(complete_key)
            if complete_key==key:
                    x=x+1
                    data=item
            if item[0]==key:
                    Fail=True

        if x==1:
            #print("Key registry found")
            if data[3]=="Disabled":
                return "Failed_Disabled"
            else:
                if First==False:
                        if complete_key==prev_key:
                                self.log(data[1]," Validated through Keycheck!")
                                return [data[1],data[2]]
                        else:
                                return "Failed_REALKEY_CHANGED"
                else:
                        First=True
                        self.log(data[1]," Validated through Keycheck!")
                        if self.NOVER==False:
                               # hashcheck(key)
                               pass
                        else:
                               print("[ BACKEND ] : WARNING: HASH CHECKING IS DISABLED!")
                        return [data[1],data[2]]
        elif x >1:
            #print("Possible key attack...")
            self.log(data[1]," Has attempted a key attack!")
            return "Failed_keyattack"
        elif Fail==True:
            self.log("UNKNOWN"," Has failed to present TMP_KEY")
            return "Failed_TMP_KEY_CHECK"
        else:
            #print("Key not found")
            self.log("System"," Application produced invalid key!")
            return "Failed_Key_not_found"
    def genkey(self,app,desc,username):## Generate key for an application development use. Key must present this key when an app connects
       if Zauth.DEBUG==True:
           print("[ BACKEND ] : Creating Key...")
       key = Fernet.generate_key()
       if Zauth.DEBUG==True:
           print("[ BACKEND ] : Uploading key...")
       upld= ("INSERT INTO keytable "
            "(keycode, app, description, status, username)"
            "VALUES (%(keycode)s, %(app)s, %(description)s, %(status)s,%(username)s)")
       upld_dat = {
                'keycode':key,
                'app':app,
               'description':desc,
               'status':"Active",
                'username':username
                }
       cursor = cnx.cursor()
       cursor.execute(upld,upld_dat)
       cnx.commit()
       cursor.close()
       if Zauth.DEBUG==True:
           print("[ BACKEND ] : Key: "+str(key)+" for application "+str(app)+" uploaded")
           print("[ BACKEND ] : Locally saving key...")
       open(str(app)+"_key.txt","w+").write(key)
    def special_handle(self,app):
        if self.DEBUG==True:
                print("[ BACKEND ] : Gathering Special file information...")
        if os.path.exists("magic/"+app+".zauth")==True:
                import linecache
                sel=("SELECT * FROM authorizations")
                cursor=cnx.cursor()
                cursor.execute(sel)
                num=0
                #print(str(app))
                for item in cursor:
                        #print(self.decryption_key)
                        #input("press enter")
                        #print(str(ec.decrypt(item[0],self.decryption_key)))
                        try:
                                if str(ec.decrypt(item[0],self.decryption_key))==str(app):
                                        time.sleep(1)
                                        dat=item
                                        num=num+1
                        except:
                                print("[ BACKEND ] : WARN: Encryption module returned invalid result, Trying to continue...")
                                self.log(app, "WARN: Encryption module returned invalid result")

                if num==0:
                        raise SystemError("No special file is on server")
                if num>1:
                        raise SystemError("Application has multiple registrations on the server!")
                        self.log(app," Application has given multiple registrations!")
                line=int(ec.decrypt(dat[1],self.decryption_key))
                code=dat[2]
                recovered_code=linecache.getline("magic/"+app+".zauth",line)
                cursor.close()
                try:
                    #    print(recovered_code)
                        
                        #input("press enter")
                        if ec.decrypt(recovered_code,self.decryption_key)==ec.decrypt(code,self.decryption_key):
                                self.log(app," code matches application code in special file..")
                                if ec.decrypt(recovered_code,self.decryption_key)==app:
                                        self.log(app," Code is accepted by system!")
                                        if Zauth.DEBUG==True:
                                                print("[ BACKEND ] : The magic file is correct!")
                                else:
                                        self.log(app," Code does not match application information")
                                        raise SystemError("The given applicatoin information is incorrect")
                        else:
                                print("[ BACKEND ] : "+str(code))
                                print("[ BACKEND ] : "+str(recovered_code))
                                self.log(app," File is incorrect")
                                print("[ BACKEND ] : That is not the correct file")
                                raise SystemError("An invalid Special File has been presented")
                except:
                        self.log(app, " Code is either corrupted, invalid, or a magic file attack was attempted")
                        print("[ BACKEND ] : An invalid magic file was given, the system will now abort")
                        input(" Press enter")
                        raise SystemError("Invalid Magic File")
        else:
                self.log(app," Application has not presented a valid special file: No such file or directory")
                raise SystemError("Application has not presented a valid special file: No such file or directory")

    def keyhandle(self,key):   ###Optional "All in one" Handler for functions and applications
        rtn=self.keycheck(key)
        if rtn=="Failed_keyattack":
            print("[ BACKEND ] : The application is using a key used by multiple apps, the app can not be determined")
            print("[ BACKEND ] : Not cotinuing")
        
            raise SystemError("Keyattack detected")
        elif rtn=="Failed_Key_not_found":
            print("[ BACKEND ] : Invalid key given: Key not present on server ")
            raise KeyError("Invalid key given")
        elif rtn=="Failed_Disabled":
            print("[ BACKEND ] : This key is disabled")
            raise SystemError("Key is disabled on system")
        elif rtn=="Failed_TMP_KEY_CHECK":
            print("[ BACKEND ] : The application has not presented a TMP KEY")
            raise KeyError("The application has not presented a valid TMP KEY")
        elif rtn=="Failed_REALKEY_CHANGED":
            print("[ BACKEND ] : Warning! The application key has been changed since the start of the application, access has been denied")
            self.log("System"," KEYFRAUD DETECTED! ACCESS WAS DENIED TO THE APPLICATION")
            raise KeyError("The Application Key has been changed since the initial request. The key may be comprimised")
        else:
            #print(rtn[0])
            self.special_handle(rtn[0])
            try:
                test=rtn[0]
                if self.DEBUG==True:
                    print("[ BACKEND ] : Valid key given!")
                return rtn[0]
            except:
                print("[ BACKEND ] : Invalid returned format")
                raise TypeError("Unrecognized format returned from key check")
    def KeyLookup(self,key,lookupKey):##Basic Keytable lookup service
        x=0
        app=self.keycheck(key)
        lookupKey=lookupKey.replace(str(self.TMP_KEY),"")
        #print(lookupKey)
        if self.DEBUG==True:
            print("[ BACKEND ] : Checking application key...")
        get=("SELECT * FROM keytable")
        cursor=cnx.cursor()
        cursor.execute(get)
        item=[]
        for data in cursor:
            if lookupKey =="":
                    item.append(data)
            else:
                    #print(data)
                    if lookupKey in data[1] or lookupKey in data[0]:
                            item.append(data)
        self.log(app[0]," Looked up information in KeyTable.")
        return [item]
    def add_client(self,username,key):
        app=self.keyhandle(key)
        from uuid import getnode as get_mac
        import platform
        import sys
        import geocoder
        from requests import get
        mac=get_mac()
        sel=("SELECT * FROM clients WHERE ID='"+str(mac)+"'")
        cursor=cnx.cursor()
        cursor.execute(sel)
        x=0
        for item in cursor:
                x=x+1
        if x==0:
                IP = get('https://api.ipify.org').text
                Location=geocoder.freegeoip(str(IP))
                try:
                        Location=Location.city+", "+Location.country
                except:
                        print("[ BACKEND ] : Unable to get location!")
                        print("[ BACKEND ] : Setting location as: Unknown")
                        Location="Unknown"
                #print(Location)
                upld= ("INSERT INTO clients "
                    "(Name, Location, OS, ID)"
                    "VALUES (%(Name)s, %(Location)s, %(OS)s, %(ID)s)")
                upld_dat = {
                'Name':platform.uname()[1],
                'Location':Location,
                'OS':platform.platform(),
                'ID':mac
                }
                cursor = cnx.cursor()
                cursor.execute(upld,upld_dat)
                cnx.commit()
                cursor.close()
                self.log(app," Added client to tracking database with the ID: "+str(mac))
        else:
                self.log(app," Ignoring request to add an existing client to the tracking database with ID: "+str(mac))
    def view_clients(self,key):
        app=self.keyhandle(key)
        self.log(app," Searched for clients registered")
        sel=("SELECT * FROM clients")
        cursor=cnx.cursor()
        cursor.execute(sel)
        dats=[]
        for data in cursor:
                dats.append(data)
        cursor.close()
        return dats
    def view_logins(self,key,username):
        app=self.keyhandle(key)
        self.log(app," Looked up login history for user: "+username)
        sel=("SELECT * FROM logins")
        cursor=cnx.cursor()
        cursor.execute(sel)
        usernames=[]
        timestamps=[]
        IDs=[]
        apps=[]
        for data in cursor:
                if ec.decrypt(data[0],self.decryption_key)==username:
                        usernames.append(username)
                        timestamps.append(data[1])
                        IDs.append(data[2])
                        apps.append(data[3])
        cursor.close()
        translated=[]
        for item in IDs:
                sels=("SELECT * FROM clients WHERE ID='"+item+"'")
                cursor=cnx.cursor()
                cursor.execute(sels)
                for dat in cursor:
                        tmp=dat[0]
                translated.append(tmp)
        complete=[usernames,timestamps,translated,apps]
        cursor.close()
        return complete
    def login(self,username,password,key): ##More advanced Login system for external processing
        import datetime
        from uuid import getnode as get_mac
        times=datetime.datetime.today().strftime("%H:%m/%m-%d-%Y")
        app=self.keyhandle(key)#Two time key check
        rtn=SecureUse.lookup("username",username,key)
        rtn_enc=SecureUse.lookup("username_enc",username,key)
        self.log(app," Requested for advanced login system")
        #print(rtn[5])
        mac=get_mac()
        if app in rtn[5]:
                if password==rtn[1]:
                    print("[ BACKEND ] : Logged in")
                    self.add_client(rtn_enc[0],key)
                    upld= ("INSERT INTO logins "
                    "(username, timestamp, ID, app)"
                    "VALUES (%(username)s, %(timestamp)s, %(ID)s, %(app)s)")
                    upld_dat = {
                        'username':rtn_enc[0],
                        'timestamp':times,
                        'ID':mac,
                        'app':app
                        }
                    cursor = cnx.cursor()
                    cursor.execute(upld,upld_dat)
                    cnx.commit()
                    cursor.close()                     
                    return "Success"
                else:
                    print("[ BACKEND ] : Unable to login")
                    return "Failed"
        else:
                print("[ BACKEND ] : An app is attempting to access unathorized data!")
                self.log(app," Requested unauthorized data!")
                return "Unauthorized"


    def addapp(self,key,username):## Add an app to the allowed apps
        app=self.keyhandle(key)#Run self.keycheck
        rtn=SecureUse.lookup("username",username,key)
        rtn_ec=SecureUse.lookup("username_enc",username,key)
        username=rtn_ec[0]
        password=rtn_ec[1]
        Firstname=rtn_ec[2]
        Lastname=rtn_ec[3]
        email=rtn_ec[4]
        apps=rtn[5]+","+app
        apps=ec.encrypt(apps,self.decryption_key)
        dels=("DELETE FROM userdb WHERE username='"+str(username)+"'")
        cursor=cnx.cursor()
        cursor.execute(dels)
        cnx.commit()
        cursor.close()
        time.sleep(1)
        upld= ("INSERT INTO userdb "
            "(username, password, Firstname, Lastname, email, apps)"
            "VALUES (%(username)s, %(password)s, %(Firstname)s, %(Lastname)s, %(email)s, %(apps)s)")
        upld_dat = {
                'username':username,
                'password':password,
                'Firstname':Firstname,
                'Lastname':Lastname,
                'email':email,
                'apps':apps
                }
        cursor = cnx.cursor()
        cursor.execute(upld,upld_dat)
        cnx.commit()
        cursor.close()    
        self.log(app," Added app to account: "+str(rtn[0]))
    def delapp(self,key,username):#Delete all apps registered with the user
        app=self.keyhandle(key)#Run self.keycheck
        rtn=SecureUse.lookup("username",username,key)
        rtn_ec=SecureUse.lookup("username_enc",username,key)
        apps=""
        apps=ec.encrypt(apps,self.decryption_key)
#    print(rtn_ec[0])
        test=("SELECT * FROM userdb WHERE username='"+rtn_ec[0]+"'")
        cursor=cnx.cursor()
        cursor.execute(test)
        x=0
        for item in cursor:
                x=x+1
        if x==0:
                print("[ BACKEND ] : There are no users with that name")
                return "ERROR"
        dat=(apps,rtn_ec[0])
        addapp= ("""
               UPDATE userdb
               SET apps=%s
               WHERE username=%s
                """)
        cursor=cnx.cursor()
        cursor.execute(addapp,dat)
        cnx.commit()
        cursor.close()
        self.log(app," Deleted apps on account: "+str(username))

class DevMode(Zauth):
    def __init__(self,key,dec_key):
            print("[ BACKEND ] : Entering Developer mode")
            super().__init__(key,dec_key)
    def Enable_Nover(self):
            Zauth.NOVER=True
    def Disable_Nover(self):
            Zauth.NOVER=False
    def Enable_DEBUG(self):
            Zauth.DEBUG=True
            print("[ BACKEND ] : Debug Enabled")

SecureUse=__Internal()

