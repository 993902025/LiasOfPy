# -*- coding: utf-8 -*

import sys
import threading
import time
import socket


class sock:
    s = socket.socket()
    def __init__(self, ip, port):
        try:
            self.s.connect((ip, port))
        except Exception as e:
            print ("err1 init sock:%s:" % e)
            sys.exit()
        try:
            self.mc = msgcenter() 
        except Exception as e:
            print ("err11 init msgcenter:%s:" % e)
            sys.exit()
        try:            
            t = threading.Thread( target=self.recvmsg)
            t.start()
            t.join()
        except Exception as e:
            print ("err2:%s:" % e)
            sys.exit(2)
    
    def recvmsg(self):
        try:
            #lock_1 = threading.Rlock()
            while 1:
                buff = self.s.recv(1024)
                if len(buff) > 0:
                    #lock_1.acquire()
                    self.mc.imsg(buff)                    
                    #lock_1.release()
                #else:
                    #sleep(1)
        except Exception as e:
            if type(e) == NameError:
                raise NameError("xxxxxxxxxx")
                exit()
            else:
                print ("err recvmsg:%s, %s:" % (type(e), str(e)))

    def sendmsg(self,msg):
        if len(msg) > 0:
            try:
                bmsg = msg.encode("utf-8")
                self.s.send(bmsg)
                return 0
            except Exception as e:
                print ("err sendmsg:%s:" % e)
                sys.exit()
        else:
            #print ("no msg for send")
            return -1

    def close(self):
        try:
            self.s.close()
            return 0
        except Exception as e:
            print ("err sendmsg:%s:" % e)
            sys.exit()

class msgcenter:
    msglist = []
    def __init__(self):
        pass
    
    def imsg(self,msg):
        self.msglist.append(msg)

    def omsg(self):
        if len(self.msglist) > 0:
            msg = self.msglist[0]
            del self.msglist[0]
            return msg
        else:
            return -2
            print("no msg")

def main(ip = '127.0.0.1', port = 7277):
    ip = ip
    port = port
    cs = sock(ip, port)
    sendstr = "ttttt"
    while 1:
        #sendstr = input("input str:\n")
        if sendstr == "q":
            print ("stop...")
            cs.close()
            sys.exit(0)
        else:
            cs.sendmsg(sendstr)
            sendstr = ""
            getstr = cs.mc.omsg()
            if getstr != -2:
                print (getstr.decode())
    pass
    
if __name__ == '__main__':
    print ("start")
    main('127.0.0.1', 7777)
    exit(1)
