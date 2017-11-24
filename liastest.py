#! /usr/bin/python
#! python3
# -*- coding: utf-8 -*-

import os
import sys
import math 
import socket
import random
import datetime
import ctypes
import platform
import threading
import socket_thread 


system = platform.system()

agentid = 33010010
gamename = "B001"
drawno = 2017024
key = "111111"


#@0233|1|1|0|005905|BET|330106|$...$|47A27919D2F664703A3179701E1A3653

def FormBetString(comball, speball,mul=1):
    if len(comball) < 12:
        print ("comball error")
        exit()
    if len(comball) % 2 != 0:
        print ("comball error")
        exit()
    if len(speball) < 2:
        print ("speball error")
        exit()
    if len(speball) % 2 != 0:
        print ("speball error")
        exit()
    comballcount = len(comball) / 2
    speballcount = len(speball) / 2    
    betstrdic = { 'playtype':1, 'count':1, 'betdetail':'' }
    #sigle
    if comballcount == 6 and speballcount == 1:
        betstrdic['playtype'] = 1
    #double
    elif comballcount == 6 and speballcount > 1:
        betstrdic['playtype'] = 2       
    betcount =  math.factorial(comballcount) / ( math.factorial(comballcount-6) * math.factorial(6) )* speballcount
    print ("betcount:\t%-10s" % str(betcount))
    betstrdic['betdetail'] = str(mul).zfill(3) + "%02d" % comballcount + str(comball) +  "%02d" % speballcount + str(speball)
    print ("betdetail:\t%-10s" % betstrdic['betdetail'])
    return (betstrdic)

def FormTicketString(comball, speball,mul=1):
    t = 0
    ticketid = str(agentid) + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "%06d" % t
    t += 1
    betdetail = FormBetString(comball, speball,mul)
    playtype = betdetail['playtype']
    money = "%.2f"% (betdetail['count'] * mul * 2)
    print ("betmoney:\t%s"%money)
    betdetail = betdetail['betdetail']
    name = " "
    phonenumber = " "
    idnumber = " "
    cardnumber = " "
    reserve1 = " "
    reserve2 = " "
    reserve3 = " "
    outstr = ticketid + "$" + str(playtype) + "$" + str(money) + "$" + betdetail + "$" + name + "$" + phonenumber + "$" + idnumber + "$" + cardnumber + "$" + reserve1 + "$" + reserve2 + "$" + reserve3
    print ("ticketstr:\t%-10s" % outstr)
    return outstr

#Form The Send Msg String 
def FormSendMessage(commid, msgbody, key = key):
    reqtype = "1"
    reqid = "1"
    endflag = "0"
    seqid = "012345"
    commandid = commid.upper()
    msghead = reqtype + "|" + reqid + "|" + endflag + "|" + seqid + "|" + commandid + "|" + str(agentid) + "|" 
    msgstr = msghead + msgbody 
    md5 = WebMD5String32(msgstr + key)
    msgbody = WebEncodeString(msgbody)
    msgstr = msghead + "|" + msgbody + "|" + md5
    packetlen = len(msgstr)
    msgstr = "@" + "%04d"%packetlen + "|" + msgstr
    print ("msgstr:\t\t%-10s" % msgstr)
    return msgstr
    
def WebEncodeString(instr):
    filepath = ( sys.path[0] )
    if system == "Windows":
        websec = ctypes.WinDLL(filepath + "\BzWebSec.dll")
    elif system == "Linux":
        websec = ctypes.cdll.LoadLibrary(filepath + '/libbzwebsec.so')
    str1 = ctypes.c_char_p(instr.encode())
    bufflen = ( (len(instr) + 7) / 8 * 16 ) + 1
    try:
        result = ctypes.create_string_buffer( round(bufflen) )
    except TypeError:
        result = create_string_buffer( bufflen )
    r = websec.WebEncodeString(str1, key, ctypes.byref(result) )
    if r == 0:
        outstr = result.value.decode()
        print ( "----->Encodeing----->")    #( "\n%s\n-->Encodeing-->\n%s" % (instr,outstr))
        return outstr
    if r == -1:
        print ("Encode Error!!!")
        return r
    return r

def WebMD5String32(instr):
    filepath = ( sys.path[0] )
    if system == "Windows":
        websec = ctypes.WinDLL(filepath + "\BzWebSec.dll")
    elif system == "Linux":
        websec = ctypes.cdll.LoadLibrary(filepath + '/libbzwebsec.so')
    str1 = ctypes.c_char_p(instr.encode())
    bufflen = 32 + 1
    try:
        result = ctypes.create_string_buffer( round(bufflen) )
    except TypeError:
        result = create_string_buffer( bufflen )
    r = websec.WebMD5String32(str1, ctypes.byref(result) )
    if r == 0:
        outstr = result.value.decode()
        print ( "----->MD5_32_ing----->")    #( "\n%s\n-->MD5_32_ing-->\n%s" % (instr,outstr))
        return outstr
    if r == -1:
        print ("MD5 Error!!!")
        return r
    return r

#这个跟上面的加密可以弄个类一起
def WebCalculateMAC(istr):
    filepath = ( sys.path[0] )
    if system == "Windows":
        websec = ctypes.WinDLL(filepath + "\BzWebSec.dll")
    elif system == "Linux":
        websec = ctypes.cdll.LoadLibrary(filepath + '/libbzwebsec.so')
    str1 = ctypes.c_char_p(instr.encode())
    bufflen = ( (len(instr) + 7) / 8 * 16 ) + 1
    try:
        result = ctypes.create_string_buffer( round(bufflen) )
    except TypeError:
        result = create_string_buffer( bufflen )
    r = websec.WebCalculateMAC(str1, ctypes.byref(result) )
    if r == 0:
        outstr = result.value.decode()
        print ( "----->MACing----->")   #( "\n%s\n-->Encodeing-->\n%s" % (instr,outstr))
        return outstr
    if r == -1:
        print ("Encode Error!!!")
        return r
    return r


class SockClass:
    def __init__(self,ip,port):
        try:
            s = socket()
        except Exception as e:
            print ('Create socket failed. %s, %s' % (type(e), str(e)))
            exit(1)
        try:
            self.ip = ip
            self.prot = port
            con = s.connect((ip,port))
        except Exception as e:
            print ('Socket Connect Error. %s,%s' % (type(e), str(e)))
            exit(1)
        try:
            readtd = threading.Thread(target=readmsg)
        except Exception as e:
            print ('Thread Create Error. %s,%s' % (type(e), str(e)))
            exit(1)
        
    def readmsg():
        print ("Start Recvieve")
        while 1:
            try:
                msgbuff = s.recv()
                domessage(msgbuff)
            except Exception as e:
                print ('Socket Recvieve Error. %s,%s' % (type(e), str(e)))
                exit(1)

    def domessage(msgbuff):
        mc.get(msgbuff)
        print
        pass

    def sendmsg(sendstr):
        try:
            s.send(sendstr)
        except Exception as e:
            print ('Socket Send Error. %s,%s' % (type(e), str(e)))
            exit(1)


class Msgcenter:
    def __init__(self):
        msgbuff = []

    def add(msg):
        msgbuff.append(msg)

    def show():
        msg = msgbuff[0]
        del msgbuff[0]
        return msg

     
                   
def bet(comball, speball, mul = 1):
    commid = 'bet'.upper(   )    
    ticketstr = FormTicketString(comball, speball, mul)               #
    msgstr = FormSendMessage(commid, ticketstr, key)
    cs.sendmsg(msgstr)
    getstr = cs.mc.omsg()
    if getstr != -2:
        print (getstr.decode())
    pass

def onnet():
    ip = "10.1.1.151"
    port = 9901
    try:
        cs = socket_thread.sock(ip, port)
    except Exception as e:
        print ('test test Error. %s,%s' % (type(e), str(e)))
        exit(1)
    #sc.sendmsg("@0061|1|1|0|021158|GETTIME|330106||47D8F64C84FC2C6A97721079D04EB207")
    #ticketstr = ""               
    msgstr = FormSendMessage("gettime", "330106")  
    print (msgstr)
    sendstr = msgstr
    if sendstr == None:
        print ("stop...")
        cs.close()
        sys.exit(0)
    else:
        cs.sendmsg(sendstr)
        sendstr = None
    pass     
    while 1:        
        getstr = cs.mc.omsg()
        if getstr != -2:
            print (getstr.decode())
            pass
        
    cs.close()
    
def test():
    global cs
    b1 = "010203040506"
    b2 = "07"   
    ip = "10.1.1.151"
    port = 9901
    try:
        cs = socket_thread.sock(ip, port)
    except Exception as e:
        print ('test test Error. %s,%s' % (type(e), str(e)))
        exit(1)
    bet(b1, b2) 
    pass

def t():
    while 1:
        print ("1")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ("help")
        exit(0)
    elif len(sys.argv) > 1:
        if sys.argv[1][0] == "-":
            switch = sys.argv[1][1:].upper()
        else:
            print ("Para is error!")
            exit(1)
    #elif len(sys.argv) == 2:
        if switch == "H":
            print ("help")
            exit(0)
        elif switch == "T":
            print ("For Testing...")
            test()
        elif switch == "BET" or switch == "B":
            try:
                comball = sys.argv[2]
            except IndexError:
                comball = input("Please Input Commond Bet Number Like \'010203040506\' Next Line:\n")
            try:
                speball = sys.argv[3]
            except IndexError:
                speball = input("Please Input Speball Bet Number Like \'0102\' After Next Line:\n")
            mul = 1
            bet(comball, speball)
            exit(0)
        else:
            print ("abalblablabla")
    elif len( sys.argv ) < 3:
        print ("Need Input Special Bet Balls!")
        exit()
    else:
        print ("Input Error!")


