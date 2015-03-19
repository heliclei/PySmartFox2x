import socket
from SFSEncoder import *

def buildLoginRequest(zone, uname, pw, sfsObj):
    loginRequest = {}
    loginRequest['zn'] = ('string',zone)#"dgr_808001")
    loginRequest['un'] = ('string', uname)#"130225")
    loginRequest['pw'] = ('string', pw)#"")
    loginRequest['p'] = ('object', sfsObj)
    return loginRequest

#connect to sfs server via tcp socket
def connect(addr, port):
    address = (addr, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    return s

def login(s, zone, uname, pw, sfsObj):
    r = buildLoginRequest(zone, uname, pw, sfsObj)
    obj = prepareTCPPacketObject(r)
    packet = buildTCPPacketStream(obj)
    # print len(packet)
    # strPacket = ""
    # for ch in packet:
    #     strPacket += "%.02x " % ch
    # print strPacket
    s.send(packet)
    data = s.recv(1024)
    return data



