print("Welcome to BizHawk - VBjin TAS switcher!\nThis program will do the hardest work for you.\nYou have still to do the easiest work.\n\nInsert MC2 file for vbjin or TXT file for BizHawk.")

f = input('Insert filename (mc2/txt) to convert: ') #f for pay respects
n = 1 #for use in while

if (f[-3:] == 'mc2'): #if vbjin file to bizhawk
        
        with open(f,mode='r',encoding='utf-8') as vbjin:
                mc2 = vbjin.read()

        x,y = 2,18

        with open('Input Log.txt',mode='w',encoding='utf-8') as hawk:
                
                hawk.write('[Input]\nLogKey:#L_Up|L_Down|L_Left|L_Right|R_Up|R_Down|R_Left|R_Right|B|A|L|R|Select|Start|Power|\n')
                while (n > 0):
                        t = mc2[x:y]
                        x += 19
                        y += 19
                        if(len(t) != 16):
                                break
                        t = t[0] + t[5:9] + t[10] + t[1:3] + t[9] + t[13:15] + t[11:13] + t[3:5]
                        hawk.write(t + '.|\n')
                        print('frame {0}:'.format(n),t + '.|')
                        n += 1
                hawk.write('[/Input]\n')

elif (f[-3:] == 'txt'): #if vbhawk file

        with open(f,mode='r',encoding='utf-8') as vbhawk:
                vbhawk.seek(100)
                bk2 = vbhawk.read()
                bk2 = bk2[:-10]

        x,y = 0,17
        
        with open('converted-to-vbjin.mc2',mode='w',encoding='utf-8') as jin:

                while (n > 0):
                        t = bk2[x:y]
                        x += 18
                        y += 18
                        if(len(t) != 17):
                                break
                        t = '|0' + t[0] + t[6:8] + t[13:15] + t[1:5] + t[8] + t[5] + t[11:13] + t[9:11] + t[16]
                        jin.write(t + '\n')
                        print('frame {0}:'.format(n),t)
                        n += 1
        
else:
        print("Didn't got what expected, I'm out! Goodbye! Farewell! See you soon!\nCome back when you want to use vbjin-vbhawk files.")
        input('Your file is:',f[-3:])
