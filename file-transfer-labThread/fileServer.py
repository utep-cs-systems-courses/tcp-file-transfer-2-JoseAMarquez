#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params,os
from os.path import exists
from threading import Thread;

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

from threading import Thread;
from encapFramedSock import EncapFramedSock
lock = threading.Lock()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            payload = self.fsock.receive(debug)
            if debug:
                print("rec'd: ", payload)

            if not payload:     # done
                if debug: print(f"thread connected to {addr} done")
                self.fsock.close()
                return          # exit


                while 1:
                    sock, addr = lsock.accept()


                    print("Connection from", addr)
                    while working:

                        payloadFileName = framedReceive(sock, debug)
                        if not payloadFileName:
                            working = False
                            break
                        lock.aquire()
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
                                lock.release()
                            try:
                                framedSend(sock,b"Message Completed!",debug)
                            except:
                                print("Connection with ",addr ,"lost ")
                                sys.exit(0)
                                lock.release()
                            output = open(payloadFileName, 'a')
                            payloadTxt = payloadTxt.decode()
                            output.write(payloadTxt)
                            output.close()
                            lock.release()

def main():
    while True:
        sock_addr = lsock.accept()
        server = Server(sock_addr)
        server.start()
    sock.close()
