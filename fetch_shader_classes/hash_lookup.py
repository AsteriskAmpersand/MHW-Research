import sys
from pathlib import Path
from crccheck.crc import Crc32, CrcXmodem, CrcJamcrc, Crc32Bzip2, Crc32c, Crc32d,Crc32Mpeg2,Crc32Posix,Crc32q

convert = lambda x: ''.join(map(lambda y: "%02X"%y,x))

def transformInput(data):
    if type(data) is int:
        signed  = False
        if data < 0:
            signed = True
        l = (data).to_bytes(4,"little",signed=signed) 
        r = (data).to_bytes(4,"big",signed=signed)
        ls = (int.from_bytes(l,"little")&0xFFFFF).to_bytes(4,"little") 
        rs = (int.from_bytes(r,"little")&0xFFFFF).to_bytes(4,"little") 
    if type(data) is str:
        data = data.replace(" ","").replace("\n","")
        l = bytes.fromhex(data)
        r = bytes(reversed(l))
        ls = (int.from_bytes(l,"little")&0xFFFFF).to_bytes(4,"little") 
        rs = (int.from_bytes(r,"little")&0xFFFFF).to_bytes(4,"little")
    return tuple(map(convert,[ls,rs,l,r]))

def buildCompendium():
    algorithms = ["CrapJamcrc", "CrcJamcrc", "Crc32"]#, "CrcXmodem", "Crc32Bzip2", "Crc32c", "Crc32d","Crc32Mpeg2","Crc32Posix","Crc32q"]
    compendium = {algorithm:{} for algorithm in algorithms}
    with open("hashed_strings.txt","r") as inf:
        for line in inf.read().splitlines():
            data = line.split(",")
            name = data[0]
            for key,value in zip(algorithms,data[1:]):
                compendium[key][value] = name
    return compendium

c = buildCompendium()
def checkInput(data,compendium=c):
    for datum in transformInput(data):
        for algo in compendium:
            if datum in compendium[algo]:
                return True,compendium[algo][datum],algo,datum
    return False,"No Match","No Match",datum

def parseArg(arg):
    if Path(arg).exists():
        for line in Path(arg).open("r").read().splitlines():
            match,typing,algo,data = checkInput(line)
            print("%s [%s]: %s"%(typing,algo,data))
    else:
        match,typing,algo,data = checkInput(arg)
        print("%s [%s]: %s"%(typing,algo,data))

if __name__ in "__main__":
    args = sys.argv[1:]
    if not args:
        args = [''.join(input("Input ctc hash in hex string form: "))]
    for arg in args:
        parseArg(arg)
    input("Press enter to quit")
