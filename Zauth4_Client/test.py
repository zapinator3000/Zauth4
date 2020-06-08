#Test for Zauth4
import os
import Zauth4_C2A as C2A
wrap=C2A.Wrapper()
tmp_key=wrap.send_cmd("DEV_INIT:gAAAAABcMQwte8bXXvhECACNIRt2HyE6byKOkj6VRPl0SYDAzfe75pqthR2INeT43h_WB3TLM1xA8_J3WbN3sk-23vwChtI2vRg2DtR66w1LBkd-qNyJT_a92O6pOS7x11pWhLYlK_1c:rmdVHkrUUbiK96gKc14zTm3Et_AJq5YTKIu5jVQYTrk=")
key=str(tmp_key)+"rmdVHkrUUbiK96gKc14zTm3Et_AJq5YTKIu5jVQYTrk="
print(key)
print("Testing Security...")
rtn=wrap.send_cmd("test_security()")
def listify(rtn):
    rtn=rtn.strip("'")
    rtn=rtn.strip("(")
    rtn=rtn.strip(")")
    rtn=rtn.split(",")
    rtn2=[]
    for item in rtn:
        #print(item)
        rtn2.append(item.strip("'").strip(" '"))
    return rtn2
def reconstruct_list(lists,count):
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
rtn=listify(rtn)
print("Internal Call Test: "+str(rtn[0]))
print("External Call Test: "+str(rtn[1]))
wrap.send_special("Zauth_Dev.zauth","Zauth_Dev.zauth")
print("Welcome to the Zauth App development manager")
ques=input("Do you have an account? ")
if "y" in ques or "Y" in ques:
    print("Can I have your information? :")
    username=input("Username: ")
    password=input("Password: ")
    rtn=wrap.send_cmd('login("'+str(username)+'","'+str(password)+'","'+str(key)+'")')
    print(rtn)
wrap.close()
