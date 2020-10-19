#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params,os
from os.path import exists


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from framedSock import framedSend, framedReceive
working = True

while 1:
    sock, addr = lsock.accept()

    if not os.fork():
        print("Connection from", addr)
        while working:
            payloadFileName = framedReceive(sock, debug)
            if not payloadFileName:
                working = False
                break
            payloadFileName = payloadFileName.decode()

            if exists(payloadFileName):
                framedSend(sock, b"True",1)

            else:
                framedSend(sock, b"False",1)
                try:
                    payloadTxt = framedReceive(sock, debug)
                except:
                    print("Connection with ",addr ,"lost ")
                    sys.exit(0)
                try:
                    framedSend(sock,b"Message Completed!",debug)
                except:
                    print("Connection with ",addr ,"lost ")
                    sys.exit(0)
                output = open(payloadFileName, 'a')
                payloadTxt = payloadTxt.decode()
                output.write(payloadTxt)
                output.close()

sock.close()
