def bin2str(bin):
    ret = ""
    for ch in bin:
        ret += "%c" % ch
    return ret 

class SFSBuffer:
    __idx = 0
    __buffer = bytearray()
    
    def __init__(self, buf):
        self.__buffer = buf
    
    def getIdx(self):
        return self.__idx

    def setIdx(self, idx):
        self.__idx = idx

    def getByte(self):
        ret = self.__buffer[self.__idx]
        self.__idx += 1
        return ret

    def getShort(self):
        ret = self.__buffer[self.__idx] * 256 + self.__buffer[self.__idx+1]
        self.__idx += 2
        return ret
    
    def getInt(self):
        k = self.__idx
        val = 0
        for n in range(k, k+4):
            val = val*256 + self.__buffer[n]
        self.__idx += 4
        return val 

    def getLong(self):
        k = self.__idx
        val = 0
        for n in range(k, k+8):
            val = val*256 + self.__buffer[n]
        self.__idx += 8
        return val 

    def get(self, length):
        k = self.__idx
        ret = self.__buffer[k:k+length]
        self.__idx += length
        return ret

    def getBuffer(self):
        return self.__buffer[self.__idx:]
#end of Class SFSBuffer

def binDecodeBool(sfsBuffer):
    val = sfsBuffer.getByte()
    if val == 1:
        return ('bool', True)
    else:
        return ('bool', False)

def binDecodeByte(sfsBuffer):
    val = sfsBuffer.getByte()
    return ('byte', val)

def binDecodeShort(sfsBuffer):
    val = sfsBuffer.getShort()
    return ('short', val)

def binDecodeInt(sfsBuffer):
    val = sfsBuffer.getInt()
    return ('int', val)

def binDecodeString(sfsBuffer):
    strLen = sfsBuffer.getShort()
    strData = bin2str(sfsBuffer.get(strLen))
    return ('string', strData)

def binDecodeLong(sfsBuffer):
    val = sfsBuffer.getLong()
    return ('long', val)

def binDecodeByteArray(sfsBuffer):
    #arr = bytearray()
    arrSize = sfsBuffer.getInt()
    arr = sfsBuffer.get(arrSize)
    return ('byte_array', arr)

def binDecodeIntArray(sfsBuffer):
    arr = []
    arrSize = sfsBuffer.getShort()
    for n in range(0, arrSize):
        val = sfsBuffer.getInt()
        arr.append(val)
    return ('int_array', arr)

def binDecodeLongArray(sfsBuffer):
    arr = []
    arrSize = sfsBuffer.getShort()
    for n in range(0, arrSize):
        val = sfsBuffer.getLong()
        arr.append(val)
    return ('long_array', arr)

def decodeSFSArray(sfsBuffer):
    sfsArray = []
    size = sfsBuffer.getShort()
    for n in range(0, size):
        obj = decodeObject(sfsBuffer)
        sfsArray.append(obj)
    return ('array', sfsArray)


def decodeObject(sfsBuffer):
    typeId = sfsBuffer.getByte()
    if (typeId == 1):
        return binDecodeBool(sfsBuffer)
    if (typeId == 2):
        return binDecodeByte(sfsBuffer)
    if (typeId == 3):
        return binDecodeShort(sfsBuffer)
    if (typeId == 4):
        return binDecodeInt(sfsBuffer)
    if (typeId == 5):
        return binDecodeLong(sfsBuffer)
    if (typeId == 8):
        return binDecodeString(sfsBuffer)
    if (typeId == 10):
        return binDecodeByteArray(sfsBuffer)
    if (typeId == 12):
        return binDecodeIntArray(sfsBuffer)
    if (typeId == 13):
        return binDecodeLongArray(sfsBuffer)
    if (typeId == 17):
        return decodeSFSArray(sfsBuffer)
    if (typeId == 18):
        sfsBuffer.setIdx(sfsBuffer.getIdx() - 1)
        return ('object', decodeSFSObject(sfsBuffer))
    print "no matching typeId:" + str(typeId)
def decodeSFSObject(sfsBuffer):
    sfsObj = {}
    #sfsBuffer = SFSBuffer(buffer)
    header = sfsBuffer.getByte()
    #print "header"
    #print header
    dataSize = sfsBuffer.getShort()
    #print "dataSize"
    #print dataSize
    for n in range(0, dataSize):
        keySize = sfsBuffer.getShort()
        #print "keySize:" + str(keySize)
        keyName = bin2str(sfsBuffer.get(keySize))
        #print "keyName:" + keyName
        aObj = decodeObject(sfsBuffer)
        sfsObj[keyName] = aObj

    return sfsObj