print('Welcome to Game Boy Hawk input joiner!\nNow also supports Game Gear!\n')

def fopen(player):
    try:
        with open(player,'r',-1,'utf-8') as f:
            f.seek(9)
            t = f.read()
            rn = t.find('\n')
            return t[rn+1:-10]
    except FileNotFoundError: return '4E4F5420464F554E4421'

def time(fc,fps):
        f2t = fc / fps
        ms = int(f2t * 1000) % 1000
        s  = int(f2t) % 60
        m  = int(f2t / 60) % 60
        h  = int(f2t / 3600)
        return '({0:02d}:{1:02d}:{2:02d}.{3:03d})'.format(h,m,s,ms)

def gg(l,r):
    rn = l.find('\n')
    result = ''

    long = len(l) if (len(l) > len(r)) else len(r)
    fc = int(long / (rn + 1)) + 1
    ft = time(fc, 59,922743404312)

    print('Joining Game Gear inputs')
    print(fc, 'frames', ft)

    with open('Input Log.txt','w',-1,'utf-8') as dual:
        dual.write('[Input]\n')
        dual.write('LogKey:#Toggle Cable|#P1 Up|P1 Down|P1 Left|P1 Right|P1 B1|P1 B2|P1 Start|#P2 Up|P2 Down|P2 Left|P2 Right|P2 B1|P2 B2|P2 Start|\n')

        while True:
            a,b = l[3:rn] , r[3:rn]
            l,r = l[rn+1:],r[rn+1:]

            if (len(a) != rn-3) and (len(b) != rn-3): break
            #Finish join when both input files finishes.

            a = a if (len(a) == rn-3) else '.......|'
            b = b if (len(b) == rn-3) else '.......|'

            result += '|.|' + a + b + '\n'

        dual.write(result)
        dual.write('[/Input]\n')

def gb(l,r):
    rn = l.find('\n')
    result = ''

    long = len(l) if (len(l) > len(r)) else len(r)
    fc = int(long / (rn + 1)) + 1
    ft = time(fc, 59.727500569606)

    print('Joining Game Boy inputs')
    print(fc, 'frames', ft)

    with open('Input Log.txt','w',-1,'utf-8') as dual:
        dual.write('[Input]\n')
        dual.write('LogKey:Toggle Cable|#P1 Up|P1 Down|P1 Left|P1 Right|P1 A|P1 B|P1 Select|P1 Start|P1 Power|#P2 Up|P2 Down|P2 Left|P2 Right|P2 A|P2 B|P2 Select|P2 Start|P2 Power|\n')

        while True:
            a,b = l[1:rn] , r[1:rn]
            l,r = l[rn+1:],r[rn+1:]

            if (len(a) != rn-1) and (len(b) != rn-1): break
            #Finish join when both input files finishes.

            a = a[0:4] + a[4:8][::-1] + a[8:10] if (len(a) == rn-1) else '.........|'
            b = b[0:4] + b[4:8][::-1] + b[8:10] if (len(b) == rn-1) else '.........|'
            #In DualGB 'SsBA' are backwards ('ABsS').

            result += '|.|' + a + b + '\n'

        dual.write(result)
        dual.write('[/Input]\n')

'''INTRODUCTION'''

while True:
    l = input('Player 1 (left) : ')
    l = fopen(l)
    if (l == '4E4F5420464F554E4421'):
        print('ERROR! File not Found!')
        continue

    r = input('Player 2 (right): ')
    r = fopen(r)
    if (r == '4E4F5420464F554E4421'):
        print('ERROR! File not Found!')
        continue

    if (l.find('\n') != r.find('\n')):
        print('ERROR! Left and right input must have same LogKey.')
        continue

    #Be sure "Input Log.txt" is empty or doesn't exist.
    if   (l.find('|.........|') != -1): gb(l,r)
    elif (l.find('|.|.......|') != -1): gg(l,r)
    else:
        print('ERROR! Unknown!',l.find('\n'))
        continue

    print('Finished!\n')
