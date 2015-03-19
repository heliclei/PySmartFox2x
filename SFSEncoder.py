
def prepareTCPPacketObject(request, targetController, msgId):
    TCPPacket = {}
    TCPPacket['c'] = ('byte', targetController)
    TCPPacket['a'] = ('short', msgId)
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
    if (value < 0):
        value = (1 << 16) + value
    arr.append(3)
    arr.append((value >> 8) & 0xFF)
    arr.append(value & 0xFF)
    return arr

def binEncodeInt(value):
    arr = bytearray()
    if (value < 0):
        value = (1 << 32) + value
    print value
    arr.append(4)
    arr.append(value >> 24)
    arr.append((value >> 16) & 0xFF)
    arr.append((value >> 8) & 0xFF)
    arr.append(value & 0xFF)
    return arr

def binEncodeUTFString(strval):
    arr = bytearray()
    arr.append(8)
    arr.append(len(strval) >> 8)
    arr.append(len(strval) & 0xFF)
    for ch in strval:
        arr.append(ord(ch))
    return arr

def binEncodeLong(value):
    arr = bytearray()
    if ( value < 0):
        value = (1 << 64) + value
    arr.append(5)
    arr.append((value >> 56) & 0xFF)
    arr.append((value >> 48) & 0xFF)
    arr.append((value >> 40) & 0xFF)
    arr.append((value >> 32) & 0xFF)
    arr.append((value >> 24) & 0xFF)
    arr.append((value >> 16) & 0xFF)
    arr.append((value >> 8) & 0xFF)
    arr.append(value & 0xFF)
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

if __name__ == '__main__':
    array = binEncodeShort(-1)
    for ch in array:
        print ch
