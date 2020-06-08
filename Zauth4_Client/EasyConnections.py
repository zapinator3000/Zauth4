#Test for Zauth4
import os
import Zauth4_C2A as C2A
wrap=C2A.Wrapper()
class Tools:
    def __init__(self):
        print("Tools loaded")
    def listify(self,rtn):
        rtn=rtn.strip("'")
        rtn=rtn.strip("(")
        rtn=rtn.strip(")")
        rtn=rtn.split(",")
        rtn2=[]
        for item in rtn:
            #print(item)
            rtn2.append(item.strip("'").strip(" '"))
        return rtn2
    def reconstruct_list(self,lists,count):
        x=0
        out=[]
        big_out=[]
        for thing in lists:
            thing=listify(thing)
            if x==count:
                x=1
                big_out.append(out)
                out=[]
            else:
                x=x+1
                out.append(thing[0])
        #print(big_out)
        return big_out
class Connections:
    def __init__(self):
        self.key="Default"
        self.tmp_key="Default"
        self.app_key="Default"
    def init_debug(self,zakey,deckey):
        self.tmp_key=wrap.send_cmd("DEV_INIT:"+str(zakey)+":"+str(deckey))
        self.key=str(self.tmp_key)+self.app_key
    def init_normal(self,zakey,deckey):
        self.tmp_key=wrap.send_cmd("INIT:"+str(zakey)+":"+str(deckey))
        self.key=str(self.tmp_key)+self.app_key
    def test_system(self):
        tool=Tools()
        rtn=wrap.send_cmd("test_security()")
        rtn=tool.listify(rtn)
        print("Internal Call Test: "+str(rtn[0]))
        print("External Call Test: "+str(rtn[1]))
    def send_special(self,filename,content):
        wrap.send_special(filename,content)
    def login_wrapper(self,appname):
        print("Welcome to "+str(appname))
        ques=input("Do you have a zauth account? ")
        if "y" in ques or "Y" in ques:
            print("Can I have your information? :")
            username=input("Username: ")
            password=input("Password: ")
            print("Logging in...")
            rtn=wrap.send_cmd('login("'+str(username)+'","'+str(password)+'","'+str(self.key)+'")')
            if not rtn == "Success":
                if "Username not found" in rtn:
                    print("Username was not found in our system...")
                    self.login_wrapper(appname)
                elif "Failed" in rtn:
                    print("Password was incorrect, please try again...")
                    self.login_wrapper(appname)
            else:
                print("Log-in Success!")
    def close(self):
        wrap.close()
