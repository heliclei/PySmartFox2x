import socket
from SFSEncoder import *

def printByteArray(data):
    strData = ""
    for ch in data:
        strData += "%.02x " % ch

    print strData

def prepareTCPPacketObject(request, targetController, msgId):
    TCPPacket = {}
    TCPPacket['c'] = ('byte', targetController)
    TCPPacket['a'] = ('short', msgId)
    TCPPacket['p'] = ('object', request)
    return TCPPacket

def buildTCPPacketStream(packet_obj):
    stream = bytearray()
    packet = object2binary(packet_obj)
    stream.append(8*16)
    stream.append((len(packet)/256)%256)
    stream.append(len(packet)%256)
    stream.extend(packet)
    return stream

def buildLoginRequest(zone, uname, pw, sfsObj):
    r = {}
    r['zn'] = ('string',zone)#"dgr_808001")
    r['un'] = ('string', uname)#"130225")
    r['pw'] = ('string', pw)#"")
    r['p'] = ('object', sfsObj)
    return r

#roomId == -1 if no room
def buildExtensionRequest(cmd, roomId, sfsObj):
    r = {}
    r['c'] = ('string', cmd)
    r['r'] = ('int', roomId)
    r['p'] = ('object',sfsObj)
    return r 

def send(s, packet):
    s.send(packet)
    header = s.recv(3)
    dataLen = ord(header[1]) * 256 + ord(header[2])
    print 'recv data len:' + str(dataLen)
    recv_len = 0
    data = bytearray()
    while recv_len < dataLen:
        r = s.recv(1024)
        data.extend(r)
        recv_len += len(r)
    return data

#connect to sfs server via tcp socket
def connect(addr, port):
    address = (addr, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    return s

def login(s, zone, uname, pw, sfsObj):
    r = buildLoginRequest(zone, uname, pw, sfsObj)
    obj = prepareTCPPacketObject(r,0,1)
    packet = buildTCPPacketStream(obj)
    return send(s, packet)




