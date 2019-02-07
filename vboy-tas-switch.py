#import re
#X|Y|2 = F|1 = .|
#RLDUTSBA -> UDLRSsBA

def fm2tobk2(i):
        Z = False #Zapper
        with open(i,mode='r',encoding='utf-8') as fceux:
                fm2 = fceux.read()
        n = 0
        x = fm2.find('\n')
        if (x != 14) and (x != 22) and (fm2.find(' ') == -1):
                input('ERROR OPENING FM2 FILE. Remove all information first, keeping only the input.\nAlso, Power pad and Zapper must be P2 with a standard controller as P1.')
                exit(1)
        if (fm2.find(' ') != -1): Z = True #Enable Zapper

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 14): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|\n')
                elif(x == 22): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Start|P2 Select|P2 B|P2 A|\n')
                elif(fm2.find(' ') != -1): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Zapper X|P2 Zapper Y|P2 Fire|\n')

                while Z == False:
                        t = fm2[2:x]
                        fm2 = fm2[x+1:]
                        if(len(t) != x-2): break

                        if  (x == 14): t = '|..|' + t[1:5][::-1] + t[5:-2]
                        elif(x == 22): t = '|..|' + t[1:5][::-1] + t[5:10] + t[10:14][::-1] + t[14:-1]

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                while Z == True:
                        t = fm2[2:22]
                        fm2 = fm2[fm2.find('\n')+1:]
                        if(len(t) != 20): break

                        t = '|..|' + t[1:10] + '  ' + t[10:13] + ',  ' + t[14:17] + ',' + t[18] + '|'
                        t = t.replace('0',' ')
                        t = t[:-3] + t[-3:].replace('1','.')
                        t = t[:-3] + t[-3:].replace('2','F')

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                hawk.write('[/Input]\n')
        print('Finished!')

def lsmvtobk2(i):
        with open(i,mode='r',encoding='utf-8') as lsnes:
                lsmv = lsnes.read()
        n = 0
        x = lsmv.find('\n')
        if (x != 11) and (x != 19) and (x != 32):
                input('ERROR OPENING LSMV FILE. Did you edited the file or open the right file?.')
                exit(1)

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 11): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|P1 Power|\n')
                elif(x == 19): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|\n')
                elif(x == 32): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Y|P2 B|P2 X|P2 A|P2 L|P2 R|\n')

                while True:
                        t = lsmv[:x] #Would start from 6 but Game Boy starts from 2
                        lsmv = lsmv[x+1:]
                        if(len(t) != x): break

                        if  (x == 11): t = '|' + t[-2:] + t[-4:-2][::-1] + t[5:7][::-1] + t[3:5][::-1] + '.|'
                        elif(x == 19): t = '|..|' + t[11:15] + t[9:11] + t[7:9][::-1] + t[15:17][::-1] + t[17:19] + '|'
                        elif(x == 32): t = '|..|' + t[11:15] + t[9:11] + t[7:9][::-1] + t[15:17][::-1] + t[17:19] + '|' + t[24:28] + t[22:24] + t[20:22][::-1] + t[28:30][::-1] + t[30:32] + '|'

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                hawk.write('[/Input]\n')
        print('Finished!')

def mmotobk2(i):
        Z = False #Zapper
        with open(i,mode='r',encoding='utf-8') as mesen:
                mmo = mesen.read()
        n = 0
        x = mmo.find('\n')
        if (x != 12) and (x != 21) and (x != 25) and (mmo.find(' ') == -1):
                input('ERROR OPENING MMO FILE. Power pad and Zapper must be P2 with a standard controller as P1.')
                exit(1)
        if (mmo.find(' ') != -1): Z = True #Enable Zapper

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 12): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|\n')
                elif(x == 21): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Start|P2 Select|P2 B|P2 A|\n')
                elif(x == 25): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 PP2|P2 PP1|P2 PP5|P2 PP9|P2 PP6|P2 PP10|P2 PP11|P2 PP7|P2 PP4|P2 PP3|P2 PP12|P2 PP8|\n')
                elif(mmo.find(' ') != -1): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Zapper X|P2 Zapper Y|P2 Fire|\n')

                while Z == False: #Standard & Power Pad
                        t = mmo[:x]
                        mmo = mmo[x+1:]
                        if(len(t) != x): break

                        if  (x == 12) or (x == 21): t = t + '|'
                        elif(x == 25): t = t[0:13] + t[13:15][::-1] + t[17] + t[21] + t[18] + t[22:24] + t[19] + t[15:17][::-1] + t[24] + t[20] + '|'

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                while Z == True: #Zapper
                        t = mmo[:mmo.find('\n')]
                        mmo = mmo[mmo.find('\n')+1:]
                        if(len(t) < 18 or len(t) > 22): break

                        if  (t.find(' ') == 14): t = t[0:13] + '    ' + t[13] + ',' + t[14:]
                        elif(t.find(' ') == 15): t = t[0:13] + '   ' + t[13:15] + ',' + t[15:]
                        elif(t.find(' ') == 16): t = t[0:13] + '  ' + t[13:16] + ',' + t[16:]

                        if  (t[::-1].find(' ',2) == 3): t = t[0:19] + '    ' + t[20] + ',' + t[-1] + '|'
                        elif(t[::-1].find(' ',2) == 4): t = t[0:19] + '   ' + t[20:22] + ',' + t[-1] + '|'
                        elif(t[::-1].find(' ',2) == 5): t = t[0:19] + '  ' + t[20:23] + ',' + t[-1] + '|'

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                hawk.write('[/Input]\n')
        print('Finished!')

def mc2tobk2(i):
        with open(i,mode='r',encoding='utf-8') as pvjin:
                mc2 = pvjin.read()
        n = 0
        x = mc2.find('\n')
        if (x != 18) and (x != 12) and (x != 22) and (x != 30) and (x != 39) and (x != 48):
                input('ERROR OPENING MC2 FILE. Have you removed the movie information?')
                exit(1)

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                #if is for VBoy, all elif are PCE 1-5 Players
                if  (x == 18): hawk.write('[Input]\nLogKey:#L_Up|L_Down|L_Left|L_Right|R_Up|R_Down|R_Left|R_Right|B|A|L|R|Select|Start|Power|\n')
                elif(x == 12): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|\n')
                elif(x == 21): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|\n')
                elif(x == 30): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|\n')
                elif(x == 39): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Run|P4 B2|P4 B1|\n')
                elif(x == 48): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Run|P4 B2|P4 B1|#P5 Up|P5 Down|P5 Left|P5 Right|P5 Select|P5 Run|P5 B2|P5 B1|\n')

                while True:
                        t = mc2[2:x]
                        mc2 = mc2[x+1:]
                        if(len(t) != x-2): break

                        if  (x == 18): t = t[0] + t[5:9] + t[10] + t[1:3] + t[9] + t[13:15] + t[11:13] + t[3:5] + '.|'
                        elif(x == 12): t = t[:5] + t[5:9][::-1] + t[9]
                        elif(x == 21): t = t[:5] + t[5:9][::-1] + t[9] + t[10:14] + t[14:18][::-1] + t[18]
                        elif(x == 30): t = t[:5] + t[5:9][::-1] + t[9] + t[10:14] + t[14:18][::-1] + t[18] + t[19:23] + t[23:27][::-1] + t[27]
                        elif(x == 39): t = t[:5] + t[5:9][::-1] + t[9] + t[10:14] + t[14:18][::-1] + t[18] + t[19:23] + t[23:27][::-1] + t[27] + t[28:32] + t[32:36][::-1] + t[36]
                        elif(x == 48): t = t[:5] + t[5:9][::-1] + t[9] + t[10:14] + t[14:18][::-1] + t[18] + t[19:23] + t[23:27][::-1] + t[27] + t[28:32] + t[32:36][::-1] + t[36] + t[37:41] + t[41:45][::-1] + t[45]

                        hawk.write(t + '\n')
                        n += 1
                        print('frame {0}:'.format(n),t)

                hawk.write('[/Input]\n')
        print('Finished!')

print('Welcome to the TAS switcher!\nThis program will do the hardest work for you.\nYou have still to do the easiest work.\n\nCurrently supported:\nFCEUX to BizHawk\nLsnes to BizHawk\nMesen to BizHawk\nPCEjin to BizHawk\nVBjin to BizHawk')

f = input('\nType your filename here: ') #f for pay respects

fm2tobk2(f)
print('a')
<
