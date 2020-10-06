#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from os.path import exists
from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)
loop = True

while 1:
    inFile = input("What is the name of the file?(Type exit to exit program)")
    if inFile == "exit":
        sys.exit(0)
    if exists(inFile):
        file = open(inFile, mode = "r", encoding="utf-8")
        txt = file.read()
        if len(txt) == 0:
            print("File is empty")
        else:
            framedSend(s,inFile.encode(),debug)
            try:
                fileExist = framedReceive(s,debug)
                fileExist = fileExist.decode()
            except:
                print('error while recieving')

            if fileExist == True:
                print("File already in Server")
            else:
                print("Sending message")
                framedSend(s, txt.encode(),debug)
                try:
                    serverAns = framedReceive(s,debug);
                    serverAns = serverAns.decode()
                    print(serverAns)
                except:
                    print('error while recieving ans')
    else:
        print("File dosent exists")


s.shutdown(socket.SHUT_WR)

while 1:
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")
s.close()
