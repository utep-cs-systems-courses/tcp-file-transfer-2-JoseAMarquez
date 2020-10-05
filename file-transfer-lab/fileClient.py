#! /usr/bin/env python3

# Echo client program
import socket, sys, re

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

while loop:
    infile = input("What is the name of the file?(Type exit to exit program)")

    if infile == "exit":
        loop = False
        sys.exit(0)



    if exists(infile):
        file = pathlib.Path(infile)
        txt = file.read()

        if len(txt) == 0:
            print("File is empty")
        else:
            framedSend(s,outfile.encode(),debug)
            fileExist = framedReceive(s,debug)
            fileExist= fileExist.decode()
            if fileExist:
                print("File already in Server")
                break
            else:
                try:
                    framedSend(s, txt, debug)
                except:
                    print("Connection lost...")
                    break
                try:
                    serverTxt = framedReceive(s,debug)
                    print("Server says: %s" % serverTxt.decode())
                except:
                    print("Connection lost...")
    else:
        print("File dosent exists")
