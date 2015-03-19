
def prepareTCPPacketObject(request):
    TCPPacket = {}
    TCPPacket['c'] = ('byte', 0)
    TCPPacket['a'] = ('short', 1)
    TCPPacket['p'] = ('object', request)
    return TCPPacket

def encodeSFSObjectKey(key):
    key_len = len(key)
    arr = bytearray()
    arr.append(key_len / 256)
    arr.append(key_len % 256)

    for ch in key:
        arr.append(ord(ch))
    return arr

def binEncodeByte(value):
    arr = bytearray()
    arr.append(2)
    arr.append(value%256)
    return arr

def binEncodeShort(value):
    arr = bytearray()
    arr.append(3)
    arr.append((value/256)%256)
    arr.append(value%256)
    return arr

def binEncodeInt(value):
    arr = bytearray()
    arr.append(4)
    arr.append(value/(256 * 256 * 256))
    arr.append((value/(256 *256))%256)
    arr.append((value/256)%256)
    arr.append(value%256)
    return arr

def binEncodeUTFString(strval):
    arr = bytearray()
    arr.append(8)
    arr.append(len(strval)/256)
    arr.append(len(strval)%256)
    for ch in strval:
        arr.append(ord(ch))
    return arr

def binEncodeLong(value):
    arr = bytearray()
    arr.append(5)
    arr.append((value/(256**7))%256)
    arr.append((value/(256**6))%256)
    arr.append((value/(256**5))%256)
    arr.append((value/(256**4))%256)
    arr.append((value/(256**3))%256)
    arr.append((value/(256**2))%256)
    arr.append((value/256)%256)
    arr.append(value%256)
    return arr

def binEncodeBool(value):
    arr = bytearray()
    arr.append(1)
    if(value is True):
        arr.append(1)
    else:
        arr.append(0)
    return arr

def encodeData(data, dataType):
    if(dataType == 'byte'):
        return binEncodeByte(data)
    if(dataType == 'short'):
        return binEncodeShort(data)
    if(dataType == 'int'):
        return binEncodeInt(data)
    if(dataType == 'string'):
        return binEncodeUTFString(data)
    if(dataType == 'long'):
        return binEncodeLong(data)
    if(dataType == 'bool'):
        return binEncodeBool(data)
    if(dataType == 'object'):
        return object2binary(data)
    print "no matching type found"

def object2binary(obj):
    arr = bytearray()
    arr.append(18)
    obj_len = len(obj)
    arr.append(obj_len/256)
    arr.append(obj_len%256)
    for k in obj:
        print k, obj[k]
        #print obj[k][0], obj[k][1]
        #print encodeData(obj[k][1], obj[k][0])
        arr.extend(encodeSFSObjectKey(k))
        arr.extend(encodeData(obj[k][1], obj[k][0]))
    return arr

def buildTCPPacketStream(packet_obj):
    stream = bytearray()
    packet = object2binary(packet_obj)
    stream.append(8*16)
    stream.append((len(packet)/256)%256)
    stream.append(len(packet)%256)
    stream.extend(packet)
    return stream
