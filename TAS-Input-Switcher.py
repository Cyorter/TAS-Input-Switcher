# (Ctrl+End) To see the introduction go to the end.

def time(fc,fps):
        f2t = fc / fps
        ms = int(f2t * 1000) % 1000
        s  = int(f2t) % 60
        m  = int(f2t / 60) % 60
        h  = int(f2t / 3600)
        if  (ms < 10): ms = '00' + str(ms)
        elif(ms < 100): ms= '0'  + str(ms)
        if  (s < 10): s  = '0'  + str(s)
        if  (m < 10): m  = '0'  + str(m)
        return '({0}:{1}:{2}.{3})'.format(h,m,s,ms)

#############################################################################
# PCE & VBoy Movies (PCEjin / VBjin <-> BizHawk)                            #
# 1-5 standard controllers for PCE                                          #
#############################################################################

def bk2tomc2(i):

        with open(i,mode='r',encoding='utf-8') as hawk:
                hawk.seek(9)
                bk2 = hawk.read()
                bk2 = bk2[bk2.find('\n')+1:-10]

        x = bk2.find('\n')
        w2f = ''

        if (x != 17) and (x != 10) and (x != 19) and (x != 28) and (x != 37) and (x != 46):
                print('Extract "Input Log.txt" from BK2 and do not edit the file!')
                return 'ERROR!'

        fc = int(len(bk2) / (x + 1)) + 1
        ft = time(fc, 50.274 if x == 17 else 59.827)

        print('\nConverting BK2',
              'PCE 1P' if x == 10 else
              'PCE 2P' if x == 19 else
              'PCE 3P' if x == 28 else
              'PCE 4P' if x == 37 else
              'PCE 5P' if x == 46 else 'VBoy','to MC2')
        print(fc, 'frames', ft)
        print('UDLRudlrBAlrsS -> SWCT^v<>ENLRBA' if x == 17 else 'UDLRsR21 -> UDLR12NS')

        with open('Converted-to-jin.mc2',mode='w',encoding='utf-8') as jin:

                while True:

                        t   = bk2[:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x): break

                        if  (x == 17): t = '|0|' + t[6:8] + t[-4:-2] + t[1:5] + t[8] + t[5] + t[-6:-4] + t[9:11] + '|'
                        elif(x == 10): t = '|0|' + t[1:5] + t[5:9][::-1] + '|'
                        elif(x == 19): t = '|0|' + t[1:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|'
                        elif(x == 28): t = '|0|' + t[1:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|'
                        elif(x == 37): t = '|0|' + t[1:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|' + t[28:32] + t[32:36][::-1] + '|'
                        elif(x == 46): t = '|0|' + t[1:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|' + t[28:32] + t[32:36][::-1] + '|' + t[37:41] + t[41:45][::-1] + '|'

                        w2f += t + '\n'

                jin.write(w2f)

        return 'SUCESS!'

def mc2tobk2(i):

        with open(i,mode='r',encoding='utf-8') as jin:
                mc2 = jin.read()
                mc2 = mc2[mc2.find('|0|'):] # Forward to the position of the input.

        x = y = mc2.find('\n') # Y because the detection below will change X.
        w2f = ''

        if (x == 33) or (x == 49) or (x == 63) or (x == 78): x = 18
        if (x != 18) and (x != 12) and (x != 21) and (x != 30) and (x != 39) and (x != 48):
                print('If there is a string "|0|" above the beginning of the input (e.g in the author notes) remove it and try again.')
                return 'ERROR!'

        fc = int(len(mc2) / (y + 1))
        ft = time(fc, 50.274 if x == 18 else 59.827)

        print('\nConverting MC2',
              'PCE 1P' if x == 12 else
              'PCE 2P' if x == 21 else
              'PCE 3P' if x == 30 else
              'PCE 4P' if x == 39 else
              'PCE 5P' if x == 48 else 'VBoy','to BK2')
        print(fc, 'frames', ft)
        print('SWCT^v<>ENLRBA -> UDLRudlrBAlrsS' if x == 18 else 'UDLR12NS -> UDLRsR21')

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                # First 'if' is for VBoy, all 'elif' are PCE 1-5 Players.
                if  (x == 18): hawk.write('[Input]\nLogKey:#L_Up|L_Down|L_Left|L_Right|R_Up|R_Down|R_Left|R_Right|B|A|L|R|Select|Start|Power|\n')
                elif(x == 12): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|\n')
                elif(x == 21): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|\n')
                elif(x == 30): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|\n')
                elif(x == 39): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Run|P4 B2|P4 B1|\n')
                elif(x == 48): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Run|P1 B2|P1 B1|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Run|P2 B2|P2 B1|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Run|P3 B2|P3 B1|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Run|P4 B2|P4 B1|#P5 Up|P5 Down|P5 Left|P5 Right|P5 Select|P5 Run|P5 B2|P5 B1|\n')

                while True:
                        t   = mc2[2:x]
                        mc2 = mc2[y+1:]
                        if(len(t) != x-2): break

                        if  (x == 18): t = t[0] + t[5:9] + t[10] + t[1:3] + t[9] + t[13:15] + t[11:13] + t[3:5] + '.|'
                        elif(x == 12): t = t[:5] + t[5:9][::-1] + '|'
                        elif(x == 21): t = t[:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|'
                        elif(x == 30): t = t[:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|'
                        elif(x == 39): t = t[:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|' + t[28:32] + t[32:36][::-1] + '|'
                        elif(x == 48): t = t[:5] + t[5:9][::-1] + '|' + t[10:14] + t[14:18][::-1] + '|' + t[19:23] + t[23:27][::-1] + '|' + t[28:32] + t[32:36][::-1] + '|' + t[37:41] + t[41:45][::-1] + '|'

                        w2f += t + '\n'

                hawk.write(w2f)
                hawk.write('[/Input]\n')
        return 'SUCESS!'

#############################################################################
# NES Movies (FCEUX <-> BizHawk <-> Mesen)                                  #
# 1-2 standard controllers, Zapper and Power Pad in port 2 if not FCEUX     #
#############################################################################

def bk2tofm2(i):

        with open(i,mode='r',encoding='utf-8') as hawk:
                hawk.seek(9)
                bk2 = hawk.read()
                bk2 = bk2[bk2.find('\n')+1:-10]

        x = bk2.find('\n')
        w2f = ''

        if (x != 13) and (x != 22):
                print('Extract "Input Log.txt" from BK2 and do not edit the file!\nUse Standard controllers only for FCEUX.')
                return 'ERROR!'

        fc = int(len(bk2) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting BK2','NES 1P' if x == 13 else 'NES 2P','to FM2')
        print(fc, 'frames', ft)
        print('UDLRSsBA -> RLDUTSBA')

        with open('Converted-to-fceux.fm2',mode='w',encoding='utf-8') as fceux:

                while True:

                        t   = bk2[4:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x-4): break

                        if  (x == 13): t = '|0|' + t[0:4][::-1] + t[4:8] + '|||'
                        elif(x == 22): t = '|0|' + t[0:4][::-1] + t[4:8] + '|' + t[9:13][::-1] + t[13:17] + '||'

                        w2f += t + '\n'

                fceux.write(w2f)

        return 'SUCESS!'

def bk2tommo(i):

        with open(i,mode='r',encoding='utf-8') as hawk:
                hawk.seek(9)
                bk2 = hawk.read()
                bk2 = bk2[bk2.find('\n')+1:-10]

        x = bk2.find('\n')
        w2f = ''

        if (x != 13) and (x != 22) and (x != 26) and (bk2.find(' ') == -1):
                print('Extract "Input Log.txt" from BK2 and do not edit the file!\nFor P1 use Standard.\nFor P2 use Standard or Zapper or Power Pad.')
                return 'ERROR!'

        fc = int(len(bk2) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting BK2',
              'NES 1P'       if x == 13 else
              'NES 2P'       if x == 22 else
              'NES PowerPad' if x == 26 else
              'NES Zapper','to MMO')
        print(fc, 'frames', ft)
        print('UDLRSsBA| -> UDLRSsBA' if x == 13 or x == 22 else
              '21596AB743C8 -> 123456789ABC' if x == 26 else
              '    X,    Y,F -> X,Y,F')

        with open('Input.txt',mode='w',encoding='utf-8') as mesen:

                while True:

                        t   = bk2[:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x): break

                        if  (x == 13) or (x == 22): t = t[:-1]
                        elif(x == 26): t = t[:13] + t[13:15][::-1] + t[21:23][::-1] + t[15] + t[17] + t[20] + t[24] + t[16] + t[18:20] + t[23]
                        elif(t.find(' ') != -1): t = t[:-1].replace(' ','').replace(',',' ')

                        w2f += t + '\n'

                mesen.write(w2f)

        return 'SUCESS!'

def fm2tobk2(i):
        Z = False # Zapper.

        with open(i,mode='r',encoding='utf-8') as fceux:
                fm2 = fceux.read()
                fm2 = fm2[fm2.find('|0|'):] # Forward to the position of the input.

        x = fm2.find('\n')
        w2f = ''

        if (x != 14) and (x != 22) and (fm2.find(' ') == -1):
                print('For P1 use Standard only.\nFor P2 use Standard or Zapper.\nPower Pad is not supported by FCEUX.')
                return 'ERROR!'
        if (fm2.find(' ') != -1): Z = True # Enable Zapper.

        fc = int(len(fm2) / (x + 1))
        ft = time(fc, 60.099)

        print('\nConverting FM2',
              'NES 1P' if x == 14 else
              'NES 2P' if x == 22 else
              'NES Zapper','to BK2')
        if (Z == True): print('Cannot calculate time :(')
        else: print(fc, 'frames', ft)
        print('RLDUTSBA -> UDLRSsBA' if Z == False else 'X,Y,2 ->     X,    Y,F')

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 14): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|\n')
                elif(x == 22): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Start|P2 Select|P2 B|P2 A|\n')
                elif(fm2.find(' ') != -1): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Zapper X|P2 Zapper Y|P2 Fire|\n')

                while Z == False:

                        t   = fm2[2:x]
                        fm2 = fm2[x+1:]
                        if(len(t) != x-2): break

                        if  (x == 14): t = '|..|' + t[1:5][::-1] + t[5:-2]
                        elif(x == 22): t = '|..|' + t[1:5][::-1] + t[5:10] + t[10:14][::-1] + t[14:-1]

                        w2f += t + '\n'

                while Z == True:

                        t   = fm2[2:22]
                        fm2 = fm2[fm2.find('\n')+1:]
                        if(len(t) != 20): break

                        t = '|..|' + t[1:10] + '  ' + t[10:13] + ',  ' + t[14:17] + ',' + t[18] + '|'
                        t = t.replace('0',' ')
                        t = t[:-3] + t[-3:].replace('1','.')
                        t = t[:-3] + t[-3:].replace('2','F')

                        w2f += t + '\n'

                hawk.write(w2f)
                hawk.write('[/Input]\n')
        return 'SUCESS!'

def fm2tommo(i):
        Z = False # Zapper.

        with open(i,mode='r',encoding='utf-8') as fceux:
                fm2 = fceux.read()
                fm2 = fm2[fm2.find('|0|'):] # Forward to the position of the input.

        x = fm2.find('\n')
        w2f = ''

        if (x != 14) and (x != 22) and (fm2.find(' ') == -1):
                print('For P1 use Standard only.\nFor P2 use Standard or Zapper.\nPower Pad is not supported by FCEUX.')
                return 'ERROR!'
        if (fm2.find(' ') != -1): Z = True # Enable Zapper.

        fc = int(len(fm2) / (x + 1))
        ft = time(fc, 60.099)

        print('\nConverting FM2',
              'NES 1P' if x == 14 else
              'NES 2P' if x == 22 else
              'NES Zapper','to MMO')
        if (Z == True): print('Cannot calculate time :(')
        else: print(fc, 'frames', ft)
        print('RLDUTSBA -> UDLRSsBA' if Z == False else 'X,Y,2 -> X,Y,F')

        with open('Input.txt',mode='w',encoding='utf-8') as mesen:

                while Z == False:

                        t   = fm2[2:x]
                        fm2 = fm2[x+1:]
                        if(len(t) != x-2): break

                        if  (x == 14): t = '|..|' + t[1:5][::-1] + t[5:-3]
                        elif(x == 22): t = '|..|' + t[1:5][::-1] + t[5:10] + t[10:14][::-1] + t[14:-2]

                        w2f += t + '\n'

                while Z == True:

                        t   = fm2[2:22]
                        fm2 = fm2[fm2.find('\n')+1:]
                        if(len(t) != 20): break

                        t = '|..|' + t[1:10] + t[10:14] + t[14:18] + t[18]
                        t = t.replace('0','' )
                        t = t[:-3] + t[-3:].replace('1','.')
                        t = t[:-3] + t[-3:].replace('2','F')

                        w2f += t + '\n'

                mesen.write(w2f)

        return 'SUCESS!'

def mmotobk2(i):
        Z = False #Zapper

        with open(i,mode='r',encoding='utf-8') as mesen:
                mmo = mesen.read()

        x = mmo.find('\n')
        w2f = ''

        if (x != 12) and (x != 21) and (x != 25) and (mmo.find(' ') == -1):
                print('Do not edit the file!\nFor P1 use Standard only.\nFor P2 use Standard or Zapper or Power Pad.')
                return 'ERROR!'
        if (mmo.find(' ') != -1): Z = True # Enable Zapper.

        fc = int(len(mmo) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting MMO',
              'NES 1P'       if x == 12 else
              'NES 2P'       if x == 21 else
              'NES PowerPad' if x == 25 else
              'NES Zapper','to BK2')
        if (Z == True): print('Cannot calculate time :(')
        else: print(fc, 'frames', ft)
        print('UDLRSsBA -> UDLRSsBA|' if x == 12 or x == 21 else
              '123456789ABC -> 21596AB743C8' if x == 25 else
              'X,Y,F ->     X,    Y,F')

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 12): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|\n')
                elif(x == 21): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Start|P2 Select|P2 B|P2 A|\n')
                elif(x == 25): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 PP2|P2 PP1|P2 PP5|P2 PP9|P2 PP6|P2 PP10|P2 PP11|P2 PP7|P2 PP4|P2 PP3|P2 PP12|P2 PP8|\n')
                elif(mmo.find(' ') != -1): hawk.write('[Input]\nLogKey:#Power|Reset|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|#P2 Zapper X|P2 Zapper Y|P2 Fire|\n')

                while Z == False: # Standard & Power Pad.

                        t   = mmo[:x]
                        mmo = mmo[x+1:]
                        if(len(t) != x): break

                        if  (x == 12) or (x == 21): t += '|'
                        elif(x == 25): t = t[0:13] + t[13:15][::-1] + t[17] + t[21] + t[18] + t[22:24] + t[19] + t[15:17][::-1] + t[24] + t[20] + '|'

                        w2f += t + '\n'

                while Z == True: # Zapper.

                        t   = mmo[:mmo.find('\n')]
                        mmo = mmo[mmo.find('\n')+1:]
                        if(len(t) < 18 or len(t) > 22): break

                        if  (t.find(' ') == 14): t = t[0:13] + '    ' + t[13] + ',' + t[14:]
                        elif(t.find(' ') == 15): t = t[0:13] + '   ' + t[13:15] + ',' + t[15:]
                        elif(t.find(' ') == 16): t = t[0:13] + '  ' + t[13:16] + ',' + t[16:]

                        if  (t[::-1].find(' ',2) == 3): t = t[0:19] + '    ' + t[20] + ',' + t[-1] + '|'
                        elif(t[::-1].find(' ',2) == 4): t = t[0:19] + '   ' + t[20:22] + ',' + t[-1] + '|'
                        elif(t[::-1].find(' ',2) == 5): t = t[0:19] + '  ' + t[20:23] + ',' + t[-1] + '|'

                        w2f += t + '\n'

                hawk.write(w2f)
                hawk.write('[/Input]\n')
        return 'SUCESS!'

def mmotofm2(i):

        with open(i,mode='r',encoding='utf-8') as mesen:
                mmo = mesen.read()

        x = mmo.find('\n')
        w2f = ''

        if (x != 12) and (x != 21):
                print('Do not edit the file!\nUse Standard controllers only for FCEUX.')
                return 'ERROR!'

        fc = int(len(mmo) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting MMO','NES 1P' if x == 12 else 'NES 2P','to FM2')
        print(fc, 'frames', ft)
        print('UDLRSsBA -> RLDUTSBA')

        with open('Converted-to-fceux.fm2',mode='w',encoding='utf-8') as fceux:

                while True:

                        t   = mmo[4:x]
                        mmo = mmo[x+1:]
                        if(len(t) != x-4): break

                        if  (x == 12): t = '|0|' + t[0:4][::-1] + t[4:8] + '|||'
                        elif(x == 21): t = '|0|' + t[0:4][::-1] + t[4:8] + '|' + t[9:13][::-1] + t[13:17] + '||'

                        w2f += t + '\n'

                fceux.write(w2f)

        return 'SUCESS!'

#############################################################################
# Super NES Movies (Lsnes <-> Snes9X <-> BizHawk)                           #
# 1-5 standard controllers (Multitap at port 2)                             #
#############################################################################

def bk2tolsmv(i):

        with open(i,mode='r',encoding='utf-8') as hawk:
                hawk.seek(9)
                bk2 = hawk.read()
                bk2 = bk2[bk2.find('\n')+1:-10]

        x = bk2.find('\n')
        w2f = ''

        if (x != 11) and (x != 17) and (x != 30) and (x != 70):
                print('Extract "Input Log.txt" from BK2 and do not edit the file!\nFor P1 use Standard.\nFor P2 use Standard or Multitap\nGame Boy is also supported!.')
                return 'ERROR!'

        fc = int(len(bk2) / (x + 1)) + 1
        ft = time(fc, 59.728 if x == 11 else 60.099)

        print('\nConverting BK2',
              'SNES 1P' if x == 17 else
              'SNES 2P' if x == 30 else
              'SNES 5P' if x == 70 else
              'Game Boy','to LSMV')
        print(fc, 'frames', ft)
        print('UDLRSsBA -> ABsSrlud' if x == 11 else
              'UDLRsSYBXAlr -> BYsSudlrAXLR')

        with open('input',mode='w',encoding='utf-8') as lsnes:

                while True:

                        t   = bk2[:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x): break

                        if  (x == 11): t = 'F.|' + t[5:9][::-1] + t[3:5][::-1] + t[1:3]
                        elif(x == 17): t = 'F. 0 0|' + t[10:12][::-1] + t[8:10] + t[4:8] + t[12:14][::-1] + t[14:16]
                        elif(x == 30): t = 'F. 0 0|' + t[10:12][::-1] + t[8:10] + t[4:8] + t[12:14][::-1] + t[14:16] + '|' + t[23:25][::-1] + t[21:23] + t[17:21] + t[25:27][::-1] + t[27:29]
                        elif(x == 70): t = 'F. 0 0|' + t[10:12][::-1] + t[8:10] + t[4:8] + t[12:14][::-1] + t[14:16] + '|' + t[23:25][::-1] + t[21:23] + t[17:21] + t[25:27][::-1] + t[27:29] + '.|' + t[37:39][::-1] + t[35:37] + t[31:35] + t[39:41][::-1] + t[41:43] + '|' + t[50:52][::-1] + t[48:50] + t[44:48] + t[52:54][::-1] + t[54:56] + '|' + t[63:65][::-1] + t[61:63] + t[57:61] + t[65:67][::-1] + t[67:69]

                        w2f += t + '\n'

                lsnes.write(w2f)

        return 'SUCESS!'

def bk2tosmv(i):

        with open(i,mode='r',encoding='utf-8') as hawk:
                hawk.seek(9)
                bk2 = hawk.read()
                bk2 = bk2[bk2.find('\n')+1:-10]

        x = bk2.find('\n')
        w2f = b''

        if (x != 17) and (x != 30) and (x != 69):
                print('Extract "Input Log.txt" from BK2 and do not edit the file!')
                return 'ERROR!'

        fc = int(len(bk2) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting BK2',
              'SNES 1P' if x == 17 else
              'SNES 2P' if x == 30 else
              'SNES 5P','to SMV')
        print(fc, 'frames', ft)
        print('UDLRsSYBXAlr -> BYsS0000udlrAXLR (binary)')

        with open('Coverted-s9x.smv',mode='wb') as s9x:

                while (x == 17):

                        t   = bk2[4:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x-4): break

                        t1 = ((2048 if t[ 7] != '.' else 0) + \
                              (1024 if t[ 6] != '.' else 0) + \
                              ( 512 if t[ 4] != '.' else 0) + \
                              ( 256 if t[ 5] != '.' else 0) + \
                              ( 128 if t[ 0] != '.' else 0) + \
                              (  64 if t[ 1] != '.' else 0) + \
                              (  32 if t[ 2] != '.' else 0) + \
                              (  16 if t[ 3] != '.' else 0) + \
                              (   8 if t[ 9] != '.' else 0) + \
                              (   4 if t[ 8] != '.' else 0) + \
                              (   2 if t[10] != '.' else 0) + \
                              (   1 if t[11] != '.' else 0)) << 4

                        w2f += t1.to_bytes(2,'little')

                while (x == 30):

                        t   = bk2[4:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x-4): break

                        t1 = ((2048 if t[ 7] != '.' else 0) + (1024 if t[ 6] != '.' else 0) + (512 if t[ 4] != '.' else 0) + (256 if t[ 5] != '.' else 0) + (128 if t[ 0] != '.' else 0) + (64 if t[ 1] != '.' else 0) + (32 if t[ 2] != '.' else 0) + (16 if t[ 3] != '.' else 0) + (8 if t[ 9] != '.' else 0) + (4 if t[ 8] != '.' else 0) + (2 if t[10] != '.' else 0) + (1 if t[11] != '.' else 0)) << 4
                        t2 = ((2048 if t[20] != '.' else 0) + (1024 if t[19] != '.' else 0) + (512 if t[17] != '.' else 0) + (256 if t[18] != '.' else 0) + (128 if t[13] != '.' else 0) + (64 if t[14] != '.' else 0) + (32 if t[15] != '.' else 0) + (16 if t[16] != '.' else 0) + (8 if t[22] != '.' else 0) + (4 if t[21] != '.' else 0) + (2 if t[23] != '.' else 0) + (1 if t[24] != '.' else 0)) << 4

                        w2f += t1.to_bytes(2,'little') + t2.to_bytes(2,'little')

                while (x == 69):

                        t   = bk2[4:x]
                        bk2 = bk2[x+1:]
                        if(len(t) != x-4): break

                        t1 = ((2048 if t[ 7] != '.' else 0) + (1024 if t[ 6] != '.' else 0) + (512 if t[ 4] != '.' else 0) + (256 if t[ 5] != '.' else 0) + (128 if t[ 0] != '.' else 0) + (64 if t[ 1] != '.' else 0) + (32 if t[ 2] != '.' else 0) + (16 if t[ 3] != '.' else 0) + (8 if t[ 9] != '.' else 0) + (4 if t[ 8] != '.' else 0) + (2 if t[10] != '.' else 0) + (1 if t[11] != '.' else 0)) << 4
                        t2 = ((2048 if t[20] != '.' else 0) + (1024 if t[19] != '.' else 0) + (512 if t[17] != '.' else 0) + (256 if t[18] != '.' else 0) + (128 if t[13] != '.' else 0) + (64 if t[14] != '.' else 0) + (32 if t[15] != '.' else 0) + (16 if t[16] != '.' else 0) + (8 if t[22] != '.' else 0) + (4 if t[21] != '.' else 0) + (2 if t[23] != '.' else 0) + (1 if t[24] != '.' else 0)) << 4
                        t3 = ((2048 if t[33] != '.' else 0) + (1024 if t[32] != '.' else 0) + (512 if t[30] != '.' else 0) + (256 if t[31] != '.' else 0) + (128 if t[26] != '.' else 0) + (64 if t[27] != '.' else 0) + (32 if t[28] != '.' else 0) + (16 if t[29] != '.' else 0) + (8 if t[35] != '.' else 0) + (4 if t[34] != '.' else 0) + (2 if t[36] != '.' else 0) + (1 if t[37] != '.' else 0)) << 4
                        t4 = ((2048 if t[46] != '.' else 0) + (1024 if t[45] != '.' else 0) + (512 if t[43] != '.' else 0) + (256 if t[44] != '.' else 0) + (128 if t[39] != '.' else 0) + (64 if t[40] != '.' else 0) + (32 if t[41] != '.' else 0) + (16 if t[42] != '.' else 0) + (8 if t[48] != '.' else 0) + (4 if t[47] != '.' else 0) + (2 if t[49] != '.' else 0) + (1 if t[50] != '.' else 0)) << 4
                        t5 = ((2048 if t[59] != '.' else 0) + (1024 if t[58] != '.' else 0) + (512 if t[56] != '.' else 0) + (256 if t[57] != '.' else 0) + (128 if t[52] != '.' else 0) + (64 if t[53] != '.' else 0) + (32 if t[54] != '.' else 0) + (16 if t[55] != '.' else 0) + (8 if t[61] != '.' else 0) + (4 if t[60] != '.' else 0) + (2 if t[62] != '.' else 0) + (1 if t[63] != '.' else 0)) << 4

                        w2f += t1.to_bytes(2,'little') + t2.to_bytes(2,'little') + t3.to_bytes(2,'little') + t4.to_bytes(2,'little') + t5.to_bytes(2,'little')

                s9x.write(w2f)

        return 'SUCESS!'

def lsmvtobk2(i):

        with open(i,mode='r',encoding='utf-8') as lsnes:
                lsmv = lsnes.read()

        x = lsmv.find('\n')
        w2f = ''

        if (x != 11) and (x != 19) and (x != 32) and (x != 71):
                print('Do not edit the file!\nFor P1 use Standard only\nFor P2 use Standard or Multitap\nGame Boy is also supported!.')
                return 'ERROR!'

        fc = int(len(lsmv) / (x + 1)) + 1
        ft = time(fc, 59.728 if x == 11 else 60.099)

        print('\nConverting LSNV',
              'SNES 1P' if x == 19 else
              'SNES 2P' if x == 32 else
              'SNES 5P' if x == 71 else
              'Game Boy','to BK2')
        print(fc, 'frames', ft)
        print('ABsSrlud -> UDLRSsBA' if x == 11 else
              'BYsSudlrAXLR -> UDLRsSYBXAlr')

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (x == 11): hawk.write('[Input]\nLogKey:#P1 Up|P1 Down|P1 Left|P1 Right|P1 Start|P1 Select|P1 B|P1 A|P1 Power|\n')
                elif(x == 19): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|\n')
                elif(x == 32): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Y|P2 B|P2 X|P2 A|P2 L|P2 R|\n')
                elif(x == 71): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Y|P2 B|P2 X|P2 A|P2 L|P2 R|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Start|P3 Y|P3 B|P3 X|P3 A|P3 L|P3 R|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Start|P4 Y|P4 B|P4 X|P4 A|P4 L|P4 R|#P5 Up|P5 Down|P5 Left|P5 Right|P5 Select|P5 Start|P5 Y|P5 B|P5 X|P5 A|P5 L|P5 R|\n')

                while True:

                        t    = lsmv[:x] # Would start from 6 but Game Boy starts from 2.
                        lsmv = lsmv[x+1:]
                        if(len(t) != x): break

                        if  (x == 11): t = '|' + t[-2:] + t[-4:-2][::-1] + t[3:7][::-1] + '.|'
                        elif(x == 19): t = '|..|' + t[11:15] + t[9:11] + t[7:9][::-1] + t[15:17][::-1] + t[17:19] + '|'
                        elif(x == 32): t = '|..|' + t[11:15] + t[9:11] + t[7:9][::-1] + t[15:17][::-1] + t[17:19] + '|' + t[24:28] + t[22:24] + t[20:22][::-1] + t[28:30][::-1] + t[30:32] + '|'
                        elif(x == 71): t = '|..|' + t[11:15] + t[9:11] + t[7:9][::-1] + t[15:17][::-1] + t[17:19] + '|' + t[24:28] + t[22:24] + t[20:22][::-1] + t[28:30][::-1] + t[30:32] + '.|' + t[37:41] + t[35:37] + t[33:35][::-1] + t[41:43][::-1] + t[43:45] + '|' + t[50:54] + t[48:50] + t[46:48][::-1] + t[54:56][::-1] + t[56:58] + '|' + t[63:67] + t[61:63] + t[59:61][::-1] + t[67:69][::-1] + t[69:71]

                        w2f += t + '\n'

                hawk.write(w2f)
                hawk.write('[/Input]\n')
        return 'SUCESS!'

def lsmvtosmv(i):

        with open(i,mode='r',encoding='utf-8') as lsnes:
                lsmv = lsnes.read()

        x = lsmv.find('\n')
        w2f = b''

        if (x != 19) and (x != 32) and (x != 71):
                print('Did you edited the file or open the right file?.')
                return 'ERROR!'

        fc = int(len(lsmv) / (x + 1)) + 1
        ft = time(fc, 60.099)

        print('\nConverting BK2',
              'SNES 1P' if x == 19 else
              'SNES 2P' if x == 32 else
              'SNES 5P','to SMV')
        print(fc, 'frames', ft)
        print('BYsSudlrAXLR -> BYsS0000udlrAXLR (binary)')

        with open('Coverted-s9x.smv',mode='wb') as s9x:

                while (x == 19):

                        t    = lsmv[7:x]
                        lsmv = lsmv[x+1:]
                        if(len(t) != x-7): break

                        t1 = ((2048 if t[ 0] != '.' else 0) + \
                              (1024 if t[ 1] != '.' else 0) + \
                              ( 512 if t[ 2] != '.' else 0) + \
                              ( 256 if t[ 3] != '.' else 0) + \
                              ( 128 if t[ 4] != '.' else 0) + \
                              (  64 if t[ 5] != '.' else 0) + \
                              (  32 if t[ 6] != '.' else 0) + \
                              (  16 if t[ 7] != '.' else 0) + \
                              (   8 if t[ 8] != '.' else 0) + \
                              (   4 if t[ 9] != '.' else 0) + \
                              (   2 if t[10] != '.' else 0) + \
                              (   1 if t[11] != '.' else 0)) << 4

                        w2f += t1.to_bytes(2,'little')

                while (x == 32):

                        t    = lsmv[7:x]
                        lsmv = lsmv[x+1:]
                        if(len(t) != x-7): break

                        t1 = ((2048 if t[ 0] != '.' else 0) + (1024 if t[ 1] != '.' else 0) + (512 if t[ 2] != '.' else 0) + (256 if t[ 3] == 'S' else 0) + (128 if t[ 4] == 'u' else 0) + (64 if t[ 5] == 'd' else 0) + (32 if t[ 6] == 'l' else 0) + (16 if t[ 7] == 'r' else 0) + (8 if t[ 8] == 'A' else 0) + (4 if t[ 9] == 'X' else 0) + (2 if t[10] == 'L' else 0) + (1 if t[11] == 'R' else 0)) << 4
                        t2 = ((2048 if t[13] != '.' else 0) + (1024 if t[14] != '.' else 0) + (512 if t[15] != '.' else 0) + (256 if t[16] == 'S' else 0) + (128 if t[17] == 'u' else 0) + (64 if t[18] == 'd' else 0) + (32 if t[19] == 'l' else 0) + (16 if t[20] == 'r' else 0) + (8 if t[21] == 'A' else 0) + (4 if t[22] == 'X' else 0) + (2 if t[23] == 'L' else 0) + (1 if t[24] == 'R' else 0)) << 4

                        w2f += t1.to_bytes(2,'little') + t2.to_bytes(2,'little')

                while (x == 71):

                        t    = lsmv[7:x]
                        lsmv = lsmv[x+1:]
                        if(len(t) != x-7): break

                        t1 = ((2048 if t[ 0] != '.' else 0) + (1024 if t[ 1] != '.' else 0) + (512 if t[ 2] != '.' else 0) + (256 if t[ 3] == 'S' else 0) + (128 if t[ 4] == 'u' else 0) + (64 if t[ 5] == 'd' else 0) + (32 if t[ 6] == 'l' else 0) + (16 if t[ 7] == 'r' else 0) + (8 if t[ 8] == 'A' else 0) + (4 if t[ 9] == 'X' else 0) + (2 if t[10] == 'L' else 0) + (1 if t[11] == 'R' else 0)) << 4
                        t2 = ((2048 if t[13] != '.' else 0) + (1024 if t[14] != '.' else 0) + (512 if t[15] != '.' else 0) + (256 if t[16] == 'S' else 0) + (128 if t[17] == 'u' else 0) + (64 if t[18] == 'd' else 0) + (32 if t[19] == 'l' else 0) + (16 if t[20] == 'r' else 0) + (8 if t[21] == 'A' else 0) + (4 if t[22] == 'X' else 0) + (2 if t[23] == 'L' else 0) + (1 if t[24] == 'R' else 0)) << 4
                        t3 = ((2048 if t[26] != '.' else 0) + (1024 if t[27] != '.' else 0) + (512 if t[28] != '.' else 0) + (256 if t[29] == 'S' else 0) + (128 if t[30] == 'u' else 0) + (64 if t[31] == 'd' else 0) + (32 if t[32] == 'l' else 0) + (16 if t[33] == 'r' else 0) + (8 if t[34] == 'A' else 0) + (4 if t[35] == 'X' else 0) + (2 if t[36] == 'L' else 0) + (1 if t[37] == 'R' else 0)) << 4
                        t4 = ((2048 if t[39] != '.' else 0) + (1024 if t[40] != '.' else 0) + (512 if t[41] != '.' else 0) + (256 if t[42] == 'S' else 0) + (128 if t[43] == 'u' else 0) + (64 if t[44] == 'd' else 0) + (32 if t[45] == 'l' else 0) + (16 if t[46] == 'r' else 0) + (8 if t[47] == 'A' else 0) + (4 if t[48] == 'X' else 0) + (2 if t[49] == 'L' else 0) + (1 if t[50] == 'R' else 0)) << 4
                        t5 = ((2048 if t[52] != '.' else 0) + (1024 if t[53] != '.' else 0) + (512 if t[54] != '.' else 0) + (256 if t[55] == 'S' else 0) + (128 if t[56] == 'u' else 0) + (64 if t[57] == 'd' else 0) + (32 if t[58] == 'l' else 0) + (16 if t[59] == 'r' else 0) + (8 if t[60] == 'A' else 0) + (4 if t[61] == 'X' else 0) + (2 if t[62] == 'L' else 0) + (1 if t[63] == 'R' else 0)) << 4

                        w2f += t1.to_bytes(2,'little') + t2.to_bytes(2,'little') + t3.to_bytes(2,'little') + t4.to_bytes(2,'little') + t5.to_bytes(2,'little')

                s9x.write(w2f)

        return 'SUCESS!'

def smvtobk2(i):

        with open(i,mode='rb') as s9x:

                s9x.seek(20)
                p = int.from_bytes(s9x.read(1),'little') # 1-5 Players detection.
                if (p != 1) and (p != 3) and (p != 7) and (p != 15) and (p != 31):
                        print('Are you using a weird set of controllers?\nFor example: a P5 connected and a P3-P4 unconnected.')
                        return 'ERROR!'

                s9x.seek(4)
                if (int.from_bytes(s9x.read(1),'little') >= 4):
                        s9x.seek(36)
                        a = int.from_bytes(s9x.read(1),'little')
                        b = int.from_bytes(s9x.read(1),'little')
                        if a != 1 or (b != 1 and b != 5):
                                print('Only Standard controllers or Super Multitap supported.')
                                return 'ERROR!'

                s9x.seek(21)
                s = int.from_bytes(s9x.read(1),'little') # Quicksave detection.
                if (s%2 != 1):
                        print('WARNING! Quicksave unsupported! And will never be.\nYou can continue but recommend stoping.')

                s9x.seek(28)
                o = int.from_bytes(s9x.read(4),'little') # Offset detection.
                s9x.seek(o)

                smv = s9x.read()

        w2f = ''
        fc = int(len(smv) / (2 if p == 1 else 4 if p == 3 else 6 if p == 7 else 8 if p == 15 else 10))
        ft = time(fc, 60.099)

        print('\nConverting SMV',
              'SNES 1P' if p == 0x1 else
              'SNES 2P' if p == 0x3 else
              'SNES 3P' if p == 0x7 else
              'SNES 4P' if p == 0xF else
              'SNES 5P','to BK2')
        print(fc, 'frames', ft)
        print('BYsS0000udlrAXLR (binary) -> UDLRsSYBXAlr')

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

                if  (p < 4): hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Y|P2 B|P2 X|P2 A|P2 L|P2 R|\n')
                else: hawk.write('[Input]\nLogKey:#Reset|Power|#P1 Up|P1 Down|P1 Left|P1 Right|P1 Select|P1 Start|P1 Y|P1 B|P1 X|P1 A|P1 L|P1 R|#P2 Up|P2 Down|P2 Left|P2 Right|P2 Select|P2 Start|P2 Y|P2 B|P2 X|P2 A|P2 L|P2 R|#P3 Up|P3 Down|P3 Left|P3 Right|P3 Select|P3 Start|P3 Y|P3 B|P3 X|P3 A|P3 L|P3 R|#P4 Up|P4 Down|P4 Left|P4 Right|P4 Select|P4 Start|P4 Y|P4 B|P4 X|P4 A|P4 L|P4 R|#P5 Up|P5 Down|P5 Left|P5 Right|P5 Select|P5 Start|P5 Y|P5 B|P5 X|P5 A|P5 L|P5 R|\n')

                while (p == 1):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4 # For lowest value.
                        t   = smv[:2] # Unuseful except for the if below.
                        smv = smv[2:]
                        if(len(t) != 2): break

                        t1 = ('U' if p1 & 128  else '.') + \
                             ('D' if p1 & 64   else '.') + \
                             ('L' if p1 & 32   else '.') + \
                             ('R' if p1 & 16   else '.') + \
                             ('s' if p1 & 512  else '.') + \
                             ('S' if p1 & 256  else '.') + \
                             ('Y' if p1 & 1024 else '.') + \
                             ('B' if p1 & 2048 else '.') + \
                             ('X' if p1 & 4    else '.') + \
                             ('A' if p1 & 8    else '.') + \
                             ('l' if p1 & 2    else '.') + \
                             ('r' if p1 & 1    else '.')

                        t = '|..|' + t1 + '|............|'

                        w2f += t + '\n'

                while (p == 3):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        t   = smv[:4]
                        smv = smv[4:]
                        if(len(t) != 4): break

                        t1 = ('U' if p1 & 128 else '.') + ('D' if p1 & 64 else '.') + ('L' if p1 & 32 else '.') + ('R' if p1 & 16 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('Y' if p1 & 1024 else '.') + ('B' if p1 & 2048 else '.') + ('X' if p1 & 4 else '.') + ('A' if p1 & 8 else '.') + ('l' if p1 & 2 else '.') + ('r' if p1 & 1 else '.')
                        t2 = ('U' if p2 & 128 else '.') + ('D' if p2 & 64 else '.') + ('L' if p2 & 32 else '.') + ('R' if p2 & 16 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('Y' if p2 & 1024 else '.') + ('B' if p2 & 2048 else '.') + ('X' if p2 & 4 else '.') + ('A' if p2 & 8 else '.') + ('l' if p2 & 2 else '.') + ('r' if p2 & 1 else '.')

                        t = '|..|' + t1 + '|' + t2 + '|'

                        w2f += t + '\n'

                while (p == 7):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        p3  = int.from_bytes(smv[4:6],'little') >> 4
                        t   = smv[:6]
                        smv = smv[6:]
                        if(len(t) != 6): break

                        t1 = ('U' if p1 & 128 else '.') + ('D' if p1 & 64 else '.') + ('L' if p1 & 32 else '.') + ('R' if p1 & 16 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('Y' if p1 & 1024 else '.') + ('B' if p1 & 2048 else '.') + ('X' if p1 & 4 else '.') + ('A' if p1 & 8 else '.') + ('l' if p1 & 2 else '.') + ('r' if p1 & 1 else '.')
                        t2 = ('U' if p2 & 128 else '.') + ('D' if p2 & 64 else '.') + ('L' if p2 & 32 else '.') + ('R' if p2 & 16 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('Y' if p2 & 1024 else '.') + ('B' if p2 & 2048 else '.') + ('X' if p2 & 4 else '.') + ('A' if p2 & 8 else '.') + ('l' if p2 & 2 else '.') + ('r' if p2 & 1 else '.')
                        t3 = ('U' if p3 & 128 else '.') + ('D' if p3 & 64 else '.') + ('L' if p3 & 32 else '.') + ('R' if p3 & 16 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('Y' if p3 & 1024 else '.') + ('B' if p3 & 2048 else '.') + ('X' if p3 & 4 else '.') + ('A' if p3 & 8 else '.') + ('l' if p3 & 2 else '.') + ('r' if p3 & 1 else '.')

                        t = '|..|' + t1 + '|' + t2 + '|' + t3 + '|............|............|'

                        w2f += t + '\n'

                while (p == 15):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        p3  = int.from_bytes(smv[4:6],'little') >> 4
                        p4  = int.from_bytes(smv[6:8],'little') >> 4
                        t   = smv[:8]
                        smv = smv[8:]
                        if(len(t) != 8): break

                        t1 = ('U' if p1 & 128 else '.') + ('D' if p1 & 64 else '.') + ('L' if p1 & 32 else '.') + ('R' if p1 & 16 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('Y' if p1 & 1024 else '.') + ('B' if p1 & 2048 else '.') + ('X' if p1 & 4 else '.') + ('A' if p1 & 8 else '.') + ('l' if p1 & 2 else '.') + ('r' if p1 & 1 else '.')
                        t2 = ('U' if p2 & 128 else '.') + ('D' if p2 & 64 else '.') + ('L' if p2 & 32 else '.') + ('R' if p2 & 16 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('Y' if p2 & 1024 else '.') + ('B' if p2 & 2048 else '.') + ('X' if p2 & 4 else '.') + ('A' if p2 & 8 else '.') + ('l' if p2 & 2 else '.') + ('r' if p2 & 1 else '.')
                        t3 = ('U' if p3 & 128 else '.') + ('D' if p3 & 64 else '.') + ('L' if p3 & 32 else '.') + ('R' if p3 & 16 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('Y' if p3 & 1024 else '.') + ('B' if p3 & 2048 else '.') + ('X' if p3 & 4 else '.') + ('A' if p3 & 8 else '.') + ('l' if p3 & 2 else '.') + ('r' if p3 & 1 else '.')
                        t4 = ('U' if p4 & 128 else '.') + ('D' if p4 & 64 else '.') + ('L' if p4 & 32 else '.') + ('R' if p4 & 16 else '.') + ('s' if p4 & 512 else '.') + ('S' if p4 & 256 else '.') + ('Y' if p4 & 1024 else '.') + ('B' if p4 & 2048 else '.') + ('X' if p4 & 4 else '.') + ('A' if p4 & 8 else '.') + ('l' if p4 & 2 else '.') + ('r' if p4 & 1 else '.')

                        t = '|..|' + t1 + '|' + t2 + '|' + t3 + '|' + t4 + '|............|'

                        w2f += t + '\n'

                while (p == 31):

                        p1  = int.from_bytes(smv[0: 2],'little') >> 4
                        p2  = int.from_bytes(smv[2: 4],'little') >> 4
                        p3  = int.from_bytes(smv[4: 6],'little') >> 4
                        p4  = int.from_bytes(smv[6: 8],'little') >> 4
                        p5  = int.from_bytes(smv[8:10],'little') >> 4
                        t   = smv[:10]
                        smv = smv[10:]
                        if(len(t) != 10): break

                        t1 = ('U' if p1 & 128 else '.') + ('D' if p1 & 64 else '.') + ('L' if p1 & 32 else '.') + ('R' if p1 & 16 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('Y' if p1 & 1024 else '.') + ('B' if p1 & 2048 else '.') + ('X' if p1 & 4 else '.') + ('A' if p1 & 8 else '.') + ('l' if p1 & 2 else '.') + ('r' if p1 & 1 else '.')
                        t2 = ('U' if p2 & 128 else '.') + ('D' if p2 & 64 else '.') + ('L' if p2 & 32 else '.') + ('R' if p2 & 16 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('Y' if p2 & 1024 else '.') + ('B' if p2 & 2048 else '.') + ('X' if p2 & 4 else '.') + ('A' if p2 & 8 else '.') + ('l' if p2 & 2 else '.') + ('r' if p2 & 1 else '.')
                        t3 = ('U' if p3 & 128 else '.') + ('D' if p3 & 64 else '.') + ('L' if p3 & 32 else '.') + ('R' if p3 & 16 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('Y' if p3 & 1024 else '.') + ('B' if p3 & 2048 else '.') + ('X' if p3 & 4 else '.') + ('A' if p3 & 8 else '.') + ('l' if p3 & 2 else '.') + ('r' if p3 & 1 else '.')
                        t4 = ('U' if p4 & 128 else '.') + ('D' if p4 & 64 else '.') + ('L' if p4 & 32 else '.') + ('R' if p4 & 16 else '.') + ('s' if p4 & 512 else '.') + ('S' if p4 & 256 else '.') + ('Y' if p4 & 1024 else '.') + ('B' if p4 & 2048 else '.') + ('X' if p4 & 4 else '.') + ('A' if p4 & 8 else '.') + ('l' if p4 & 2 else '.') + ('r' if p4 & 1 else '.')
                        t5 = ('U' if p5 & 128 else '.') + ('D' if p5 & 64 else '.') + ('L' if p5 & 32 else '.') + ('R' if p5 & 16 else '.') + ('s' if p5 & 512 else '.') + ('S' if p5 & 256 else '.') + ('Y' if p5 & 1024 else '.') + ('B' if p5 & 2048 else '.') + ('X' if p5 & 4 else '.') + ('A' if p5 & 8 else '.') + ('l' if p5 & 2 else '.') + ('r' if p5 & 1 else '.')

                        t = '|..|' + t1 + '|' + t2 + '|' + t3 + '|' + t4 + '|' + t5 + '|'

                        w2f += t + '\n'

                hawk.write(w2f)
                hawk.write('[/Input]\n')
        return 'SUCESS!'

def smvtolsmv(i):

        with open(i,mode='rb') as s9x:

                s9x.seek(20)
                p = int.from_bytes(s9x.read(1),'little') # 1-5 Players detection.
                if (p != 1) and (p != 3) and (p != 7) and (p != 15) and (p != 31):
                        print('Are you using a weird set of controllers?\nFor example: a P5 connected and a P3-P4 unconnected.')
                        return 'ERROR!'

                s9x.seek(4)
                if (int.from_bytes(s9x.read(1),'little') >= 4):
                        s9x.seek(36)
                        a = int.from_bytes(s9x.read(1),'little')
                        b = int.from_bytes(s9x.read(1),'little')
                        if a != 1 or (b != 1 and b != 5):
                                print('Only Standard controllers or Super Multitap supported.')
                                return 'ERROR!'

                s9x.seek(21)
                s = int.from_bytes(s9x.read(1),'little') # Quicksave detection.
                if (s%2 != 1):
                        print('WARNING! Quicksave unsupported! And will never be.\nYou can continue but recommend stoping.')

                s9x.seek(28)
                o = int.from_bytes(s9x.read(4),'little') # Offset detection.
                s9x.seek(o)

                smv = s9x.read()

        w2f = ''
        fc = int(len(smv) / (2 if p == 1 else 4 if p == 3 else 6 if p == 7 else 8 if p == 15 else 10))
        ft = time(fc, 60.099)

        print('\nConverting SMV',
              'SNES 1P' if p == 0x1 else
              'SNES 2P' if p == 0x3 else
              'SNES 3P' if p == 0x7 else
              'SNES 4P' if p == 0xF else
              'SNES 5P','to BK2')
        print(fc, 'frames', ft)
        print('BYsS0000udlrAXLR (binary) -> BYsSudlrAXLR')

        with open('input',mode='w',encoding='utf-8') as lsnes:

                while (p == 1):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4 # For lowest value.
                        t   = smv[:2] # Unuseful except for the if below.
                        smv = smv[2:]
                        if(len(t) != 2): break

                        t1 = ('B' if p1 & 2048 else '.') + \
                             ('Y' if p1 & 1024 else '.') + \
                             ('s' if p1 & 512  else '.') + \
                             ('S' if p1 & 256  else '.') + \
                             ('u' if p1 & 128  else '.') + \
                             ('d' if p1 & 64   else '.') + \
                             ('l' if p1 & 32   else '.') + \
                             ('r' if p1 & 16   else '.') + \
                             ('A' if p1 & 8    else '.') + \
                             ('X' if p1 & 4    else '.') + \
                             ('L' if p1 & 2    else '.') + \
                             ('R' if p1 & 1    else '.')

                        t = 'F. 0 0|' + t1 + '|............'

                        w2f += t + '\n'

                while (p == 3):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        t   = smv[:4]
                        smv = smv[4:]
                        if(len(t) != 4): break

                        t1 = ('B' if p1 & 2048 else '.') + ('Y' if p1 & 1024 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('u' if p1 & 128 else '.') + ('d' if p1 & 64 else '.') + ('l' if p1 & 32 else '.') + ('r' if p1 & 16 else '.') + ('A' if p1 & 8 else '.') + ('X' if p1 & 4 else '.') + ('L' if p1 & 2 else '.') + ('R' if p1 & 1 else '.')
                        t2 = ('B' if p2 & 2048 else '.') + ('Y' if p2 & 1024 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('u' if p2 & 128 else '.') + ('d' if p2 & 64 else '.') + ('l' if p2 & 32 else '.') + ('r' if p2 & 16 else '.') + ('A' if p2 & 8 else '.') + ('X' if p2 & 4 else '.') + ('L' if p2 & 2 else '.') + ('R' if p2 & 1 else '.')

                        t = 'F. 0 0|' + t1 + '|' + t2

                        w2f += t + '\n'

                while (p == 7):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        p3  = int.from_bytes(smv[4:6],'little') >> 4
                        t   = smv[:6]
                        smv = smv[6:]
                        if(len(t) != 6): break

                        t1 = ('B' if p1 & 2048 else '.') + ('Y' if p1 & 1024 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('u' if p1 & 128 else '.') + ('d' if p1 & 64 else '.') + ('l' if p1 & 32 else '.') + ('r' if p1 & 16 else '.') + ('A' if p1 & 8 else '.') + ('X' if p1 & 4 else '.') + ('L' if p1 & 2 else '.') + ('R' if p1 & 1 else '.')
                        t2 = ('B' if p2 & 2048 else '.') + ('Y' if p2 & 1024 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('u' if p2 & 128 else '.') + ('d' if p2 & 64 else '.') + ('l' if p2 & 32 else '.') + ('r' if p2 & 16 else '.') + ('A' if p2 & 8 else '.') + ('X' if p2 & 4 else '.') + ('L' if p2 & 2 else '.') + ('R' if p2 & 1 else '.')
                        t3 = ('B' if p3 & 2048 else '.') + ('Y' if p3 & 1024 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('u' if p3 & 128 else '.') + ('d' if p3 & 64 else '.') + ('l' if p3 & 32 else '.') + ('r' if p3 & 16 else '.') + ('A' if p3 & 8 else '.') + ('X' if p3 & 4 else '.') + ('L' if p3 & 2 else '.') + ('R' if p3 & 1 else '.')

                        t = 'F. 0 0|' + t1 + '|' + t2 + '|' + t3 + '|............|............'

                        w2f += t + '\n'

                while (p == 15):

                        p1  = int.from_bytes(smv[0:2],'little') >> 4
                        p2  = int.from_bytes(smv[2:4],'little') >> 4
                        p3  = int.from_bytes(smv[4:6],'little') >> 4
                        p4  = int.from_bytes(smv[6:8],'little') >> 4
                        t   = smv[:8]
                        smv = smv[8:]
                        if(len(t) != 8): break

                        t1 = ('B' if p1 & 2048 else '.') + ('Y' if p1 & 1024 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('u' if p1 & 128 else '.') + ('d' if p1 & 64 else '.') + ('l' if p1 & 32 else '.') + ('r' if p1 & 16 else '.') + ('A' if p1 & 8 else '.') + ('X' if p1 & 4 else '.') + ('L' if p1 & 2 else '.') + ('R' if p1 & 1 else '.')
                        t2 = ('B' if p2 & 2048 else '.') + ('Y' if p2 & 1024 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('u' if p2 & 128 else '.') + ('d' if p2 & 64 else '.') + ('l' if p2 & 32 else '.') + ('r' if p2 & 16 else '.') + ('A' if p2 & 8 else '.') + ('X' if p2 & 4 else '.') + ('L' if p2 & 2 else '.') + ('R' if p2 & 1 else '.')
                        t3 = ('B' if p3 & 2048 else '.') + ('Y' if p3 & 1024 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('u' if p3 & 128 else '.') + ('d' if p3 & 64 else '.') + ('l' if p3 & 32 else '.') + ('r' if p3 & 16 else '.') + ('A' if p3 & 8 else '.') + ('X' if p3 & 4 else '.') + ('L' if p3 & 2 else '.') + ('R' if p3 & 1 else '.')
                        t4 = ('B' if p4 & 2048 else '.') + ('Y' if p4 & 1024 else '.') + ('s' if p4 & 512 else '.') + ('S' if p4 & 256 else '.') + ('u' if p4 & 128 else '.') + ('d' if p4 & 64 else '.') + ('l' if p4 & 32 else '.') + ('r' if p4 & 16 else '.') + ('A' if p4 & 8 else '.') + ('X' if p4 & 4 else '.') + ('L' if p4 & 2 else '.') + ('R' if p4 & 1 else '.')

                        t = 'F. 0 0|' + t1 + '|' + t2 + '|' + t3 + '|' + t4 + '|............'

                        w2f += t + '\n'

                while (p == 31):

                        p1  = int.from_bytes(smv[0: 2],'little') >> 4
                        p2  = int.from_bytes(smv[2: 4],'little') >> 4
                        p3  = int.from_bytes(smv[4: 6],'little') >> 4
                        p4  = int.from_bytes(smv[6: 8],'little') >> 4
                        p5  = int.from_bytes(smv[8:10],'little') >> 4
                        t   = smv[:10]
                        smv = smv[10:]
                        if(len(t) != 10): break

                        t1 = ('B' if p1 & 2048 else '.') + ('Y' if p1 & 1024 else '.') + ('s' if p1 & 512 else '.') + ('S' if p1 & 256 else '.') + ('u' if p1 & 128 else '.') + ('d' if p1 & 64 else '.') + ('l' if p1 & 32 else '.') + ('r' if p1 & 16 else '.') + ('A' if p1 & 8 else '.') + ('X' if p1 & 4 else '.') + ('L' if p1 & 2 else '.') + ('R' if p1 & 1 else '.')
                        t2 = ('B' if p2 & 2048 else '.') + ('Y' if p2 & 1024 else '.') + ('s' if p2 & 512 else '.') + ('S' if p2 & 256 else '.') + ('u' if p2 & 128 else '.') + ('d' if p2 & 64 else '.') + ('l' if p2 & 32 else '.') + ('r' if p2 & 16 else '.') + ('A' if p2 & 8 else '.') + ('X' if p2 & 4 else '.') + ('L' if p2 & 2 else '.') + ('R' if p2 & 1 else '.')
                        t3 = ('B' if p3 & 2048 else '.') + ('Y' if p3 & 1024 else '.') + ('s' if p3 & 512 else '.') + ('S' if p3 & 256 else '.') + ('u' if p3 & 128 else '.') + ('d' if p3 & 64 else '.') + ('l' if p3 & 32 else '.') + ('r' if p3 & 16 else '.') + ('A' if p3 & 8 else '.') + ('X' if p3 & 4 else '.') + ('L' if p3 & 2 else '.') + ('R' if p3 & 1 else '.')
                        t4 = ('B' if p4 & 2048 else '.') + ('Y' if p4 & 1024 else '.') + ('s' if p4 & 512 else '.') + ('S' if p4 & 256 else '.') + ('u' if p4 & 128 else '.') + ('d' if p4 & 64 else '.') + ('l' if p4 & 32 else '.') + ('r' if p4 & 16 else '.') + ('A' if p4 & 8 else '.') + ('X' if p4 & 4 else '.') + ('L' if p4 & 2 else '.') + ('R' if p4 & 1 else '.')
                        t5 = ('B' if p5 & 2048 else '.') + ('Y' if p5 & 1024 else '.') + ('s' if p5 & 512 else '.') + ('S' if p5 & 256 else '.') + ('u' if p5 & 128 else '.') + ('d' if p5 & 64 else '.') + ('l' if p5 & 32 else '.') + ('r' if p5 & 16 else '.') + ('A' if p5 & 8 else '.') + ('X' if p5 & 4 else '.') + ('L' if p5 & 2 else '.') + ('R' if p5 & 1 else '.')

                        t = 'F. 0 0|' + t1 + '|' + t2 + '|' + t3 + '|' + t4 + '|' + t5

                        w2f += t + '\n'

                lsnes.write(w2f)

        return 'SUCESS!'

#############################################################################
# INTRODUCTION TO THE PROGRAM                                               #
#############################################################################

print('''TAS-Switcher: A script to convert NES, Super NES, PCE and VBoy TAS movies.
This script will only take the hardest work, the input, you will need to do the rest.

Formats supported (controllers supported): 

FM2 <-> BK2 (Std)
FM2 <-> MMO (Std)
MMO <-> BK2 (Std,Zap,PPad)

SMV <-> LSMV (Std,MTap)
SMV <-> BK2  (Std,MTap)
BK2 <-> LSMV (Std,MTap,GB)

MC2 <-> BK2 (All)

For FM2 and MC2: do not modify the file, but in case of issues, open it with text editor (e.g Notepad++) and remove all "|0|" before the input (comments, information, etc).
For BK2 and MMO and LSMV: open it with archive manager (e.g 7-Zip) and extract the input file.
For SMV: do not modify the file, I take care with this format to avoid accidents when using the hex editor.

Now, rather than writing and printing every input-frame, it writes to file at the end of process. This way is (by far) faster but you can't see the progress until finished, so be patient.

For further information read "README.md" at GitHub repository.
Once you know all this: Good luck with sync! :D''')

while True:
        f = input('\nType your filename here (or Q for quit): ')
        if (f == 'Q' or f == 'q'): break

        try:
                t = open(f)
                t.close()

        except FileNotFoundError:
                print('\nOPERATION: ERROR! File not found!')
                continue

        if  (f[-4:] == '.mc2'): result = mc2tobk2(f) # Too easy for me.

        elif(f[-4:] == '.smv'):
                c = input('\nSMV DETECTED!\n\nType 1 for SMV to BK2\nType 2 for SMV to LSMV\nOr type something else for quiting if mistake\n\nType here: ')
                if  (c == '1'): result = smvtobk2(f)
                elif(c == '2'): result = smvtolsmv(f)
                elif(c == 'something else'): result = 'DAMN SON, YOU ARE GREATELY A GENIUS.'
                else: result = 'Nothing happened here. TRYING AGAIN.'

        elif(f == 'input'):
                c = input('\nLSMV DETECTED!\n\nType 1 for LSMV to BK2\nType 2 for LSMV to SMV\nOr type something else for quiting if mistake\n\nType here: ')
                if  (c == '1'): result = lsmvtobk2(f)
                elif(c == '2'): result = lsmvtosmv(f)
                elif(c == 'something else'): result = 'EEH... THIS IS EMBARRASSING...'
                else: result = 'Do not worry. TRYING AGAIN.'

        elif(f[-4:] == '.fm2'):
                c = input('\nFM2 DETECTED!\n\nType 1 for FM2 to BK2\nType 2 for FM2 to MMO\nOr type something else for quiting if mistake\n\nType here: ')
                if  (c == '1'): result = fm2tobk2(f)
                elif(c == '2'): result = fm2tommo(f)
                elif(c == 'something else'): result = 'YOU TROLL!'
                else: result = 'Nobody is perfect. TRYING AGAIN.'

        elif(f[-4:] == '.txt'):
                with open(f,mode='r',encoding='utf-8') as h:
                        bk2d = h.read(7)
                if  (bk2d == '[Input]') or (bk2d == 'LogKey:') or (f.lower() == 'input log.txt'):
                        c = input('\nBK2 DETECTED!\n\nType 1 for BK2 to MC2\nType 2 for BK2 to FM2\nType 3 for BK2 to MMO\nType 4 for BK2 to LSMV\nType 5 for BK2 to SMV\nOr type something else for quiting if mistake\n\nType here: ')
                        if  (c == '1'): result = bk2tomc2(f)
                        elif(c == '2'): result = bk2tofm2(f)
                        elif(c == '3'): result = bk2tommo(f)
                        elif(c == '4'): result = bk2tolsmv(f)
                        elif(c == '5'): result = bk2tosmv(f)
                        elif(c == 'something else'): result = '*sigh*...'
                        else: result = 'FORGIVE... eh, TRYING AGAIN.'
                else:
                        if (f.lower() == 'input.txt'): c = input('\nMMO DETECTED!\n\nType 1 for MMO to BK2\nType 2 for MMO to FM2\nOr type something else for quiting if mistake\n\nType here: ')
                        else: c = input('\nMaybe this is MMO\n\nType 1 for MMO to BK2\nType 2 for MMO to FM2\nOr type something else for quiting if mistake\n\nWanted LSMV? File should be "input" with no extension.\n\nType here: ')
                        if  (c == '1'): result = mmotobk2(f)
                        elif(c == '2'): result = mmotofm2(f)
                        elif(c == 'something else'): result = 'HA HA HA, GOOD ONE...'
                        else: result = 'Human are not like TAS... TRYING AGAIN.'

        else:
                print('\nAuto-detection failed... that means you are free to choose everything! (If you like to see programs failing)\n')
                print('Type 1 for BK2 to MC2\nType 2 for MC2 to BK2\n\nType 3 for BK2 to FM2\nType 4 for BK2 to MMO\nType 5 for FM2 to BK2\nType 6 for FM2 to MMO\nType 7 for MMO to BK2\nType 8 for MMO to FM2\n\nType 9 for BK2 to LSMV\nType A for BK2 to SMV\nType B for LSMV to BK2\nType C for LSMV to SMV\nType D for SMV to BK2\nType E for SMV to LSMV\nOr type something else for quiting if mistake\n')
                c = input('Type here: ')
                print('')
                
                if  (c == '1'): result = bk2tomc2(f)
                elif(c == '2'): result = mc2tobk2(f)
                elif(c == '3'): result = bk2tofm2(f)
                elif(c == '4'): result = bk2tommo(f)
                elif(c == '5'): result = fm2tobk2(f)
                elif(c == '6'): result = fm2tommo(f)
                elif(c == '7'): result = mmotobk2(f)
                elif(c == '8'): result = mmotofm2(f)
                elif(c == '9'): result = bk2tolsmv(f)
                elif(c == 'A') or (c == 'a'): result = bk2tosmv(f)
                elif(c == 'B') or (c == 'b'): result = lsmvtobk2(f)
                elif(c == 'C') or (c == 'c'): result = lsmvtosmv(f)
                elif(c == 'D') or (c == 'd'): result = smvtobk2(f)
                elif(c == 'E') or (c == 'e'): result = smvtolsmv(f)
                elif(c == 'F') or (c == 'f'): result = 'PAID RESPECTS'
                elif(c == 'something else'): result = 'TROLLING A PROGRAM? WHY NOT?'
                else: result = 'NIAGA GNIYRTRYING AGAIN.'

        print('\nOPERATION:',result)
