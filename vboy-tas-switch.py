#import re
def mc2tobk2(i):
        with open(f,mode='r',encoding='utf-8') as pvjin:
                mc2 = pvjin.read()
        n = 0
        x = mc2.find('\n')
        if (x == 19) or (x == 13) or (x == 22) or (x == 31) or (x == 40) or (x == 49):
                input("ERROR OPENING MC2 FILE. Have you removed the movie information?")
                exit(1)

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:

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

print("Welcome to BizHawk - VBjin TAS switcher!\nThis program will do the hardest work for you.\nYou have still to do the easiest work.\n\nInsert MC2 file for vbjin or TXT file for BizHawk.")

f = input('Insert filename (mc2/txt) to convert: ') #f for pay respects

if (f[-3:] == 'mc2'):
        mc2tobk2(f)
print('a')
