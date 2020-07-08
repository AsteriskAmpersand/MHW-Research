from crccheck.crc import Crc32, CrcXmodem, CrcJamcrc, Crc32Bzip2, Crc32c, Crc32d,Crc32Mpeg2,Crc32Posix,Crc32q

class CrapJamcrc:
    @staticmethod
    def calc(string):
        return CrcJamcrc.calc(string)&0xFFFFF
def hashString(string):
    return [ algorithm.calc(string) for algorithm in [CrapJamcrc,CrcJamcrc, Crc32]]#, CrcXmodem, Crc32Bzip2, Crc32c, Crc32d,Crc32Mpeg2,Crc32Posix,Crc32q]]   

with open("shader_strings.txt","r") as shader_strings:
    with open("hashed_strings.txt","w") as outf:
        for string in shader_strings.read().splitlines():
            hashes = hashString(string.encode())
            outf.write(string+","+",".join(map(lambda x: ''.join(map(lambda y: "%02X"%y,(x).to_bytes(4,"little",signed=False))),hashes))+"\n")
