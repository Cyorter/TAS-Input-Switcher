filename = ''

def binary(filename,offset):
    # Not even started yet...
    pass

def text(filename,offset):
    with open(filename,'r',-1,'utf-8') as psxjin:
        psxjin.seek(offset)
        pjm = psxjin.read()
        pjm = pjm[:-34]

    x = pjm.find('\n')
    w2f = ''

    if (x != 18) and (x != 32):
        print(x,'ERROR!')
        exit(1)

    print('\nConverting PJM 2P to BK2')
    print('#XO^1234LDRUSs -> UDLRsSQTOXlrLR')

    with open('Input Log.txt','w',-1,'utf-8') as hawk:

        hawk.write('[Input]\nLogKey:#Disc Select|Open|Close|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Square|P1 Triangle|P1 Circle|P1 Cross|P1 L1|P1 R1|P1 L2|P1 R2|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Square|P2 Triangle|P2 Circle|P2 Cross|P2 L1|P2 R1|P2 L2|P2 R2|\n')

        while True:

            t   = pjm[:x]
            pjm = pjm[x+1:]
            if(len(t) != x): break

            if (x == 18): t = '|    1,...|' + t[11] + t[9] + t[8] + t[10] + t[12:14][::-1] + t[0] + t[1:4][::-1] + t[4:6][::-1] + t[6:8][::-1]
            else: t = '|    1,...|' + t[11] + t[9] + t[8] + t[10] + t[12:14][::-1] + t[0] + t[1:4][::-1] + t[4:6][::-1] + t[6:8][::-1] + '|' + t[26] + t[24] + t[23] + t[25] + t[27:29][::-1] + t[15] + t[16:19][::-1] + t[19:21][::-1] + t[21:23][::-1]

            w2f += t + '|\n'

        hawk.write(w2f)

###########################################

try:
    f = open(filename,'rb')
    f.close()
except FileNotFoundError: input('NOPE! :D')

with open(filename,'rb') as psxjin:
    psxjin.seek(12)
    f = int.from_bytes(psxjin.read(2),'little')

    if (f &    2): print('WARNING: SAVESTATES!')
    if (f &    8): print('WARNING: MEMORY CARTS!')
    if (f &   16): print('WARNING: CHEATS!')
    if (f & 1568): print('WARNING: HACKS!')

    mode = 'T' if (f & 64) else 'B'

    f = int.from_bytes(psxjin.read(2),'little')
    if (f & 0x00FF !=    4 and f & 0x00FF !=    8):
        print('Only standard controller is supported')
        exit(1)
    if (f & 0xFF00 != 1024 and f & 0xFF00 != 2048):
        print('Only standard controller is supported')
        exit(1)

    psxjin.seek(44)
    f = int.from_bytes(psxjin.read(4),'little')
    # print('Done')

if (mode == 'B'): binary(filename,f)
if (mode == 'T'): text(filename,f)
