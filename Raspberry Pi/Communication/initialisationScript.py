from pexpect import pxssh
import os
import threading

def ev3_15():
    s = pxssh.pxssh()
    if not s.login ('10.42.0.180', 'robot', 'maker'):
        print ("SSH session failed on login.")
        print (str(s))
    else:
        print ("SSH session login successful")
        s.sendline ('nohup python3 subscriber15.py &')
        print('EV3_15 Ready for work')
        s.logout()
        
    #s.logout()
def ev3_35():
    s = pxssh.pxssh()
    if not s.login ('10.42.0.54', 'robot', 'maker'):
        print ("SSH session failed on login.")
        print (str(s))
    else:
        print ("SSH session login successful")
        s.sendline ('nohup python3 subscriber35.py &')
        print('EV3_35 Ready for work')
        s.logout()

def f():      
    t1 = threading.Thread(target = ev3_15)
    t2 = threading.Thread(target = ev3_35)
    t1.start()
    t2.start()

if __name__ == "__main__":
    f()
