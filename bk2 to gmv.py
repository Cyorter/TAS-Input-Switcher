with open ('Input Log.txt','r') as hawk:
    hawk.seek(9)
    bk2 = hawk.read()
    bk2 = bk2[bk2.find('\n')+1:-10]

n = 0
x = bk2.find('\n')

with open ('Gens.gmv','wb') as gens:

    while True:

        t   = bk2[4:x]
        bk2 = bk2[x+1:]
        if(len(t) != x-4): break

        t1 = 255 - ((1   if t[ 0] != '.' else 0) + \
                    (2   if t[ 1] != '.' else 0) + \
                    (4   if t[ 2] != '.' else 0) + \
                    (8   if t[ 3] != '.' else 0) + \
                    (16  if t[ 4] != '.' else 0) + \
                    (32  if t[ 5] != '.' else 0) + \
                    (64  if t[ 6] != '.' else 0) + \
                    (128 if t[ 7] != '.' else 0))

        t2 = 255 - ((1   if t[13] != '.' else 0) + \
                    (2   if t[14] != '.' else 0) + \
                    (4   if t[15] != '.' else 0) + \
                    (8   if t[16] != '.' else 0) + \
                    (16  if t[17] != '.' else 0) + \
                    (32  if t[18] != '.' else 0) + \
                    (64  if t[19] != '.' else 0) + \
                    (128 if t[20] != '.' else 0))

        t3 = 255 - ((1   if t[ 8] != '.' else 0) + \
                    (2   if t[ 9] != '.' else 0) + \
                    (4   if t[10] != '.' else 0) + \
                    (8   if t[11] != '.' else 0) + \
                    (16  if t[21] != '.' else 0) + \
                    (32  if t[22] != '.' else 0) + \
                    (64  if t[23] != '.' else 0) + \
                    (128 if t[24] != '.' else 0))

        t = t1.to_bytes(1,'little') + t2.to_bytes(1,'little') + t3.to_bytes(1,'little')
        w = int.from_bytes(t,'big')

        gens.write(t)
        n += 1
        print('frame {0}:'.format(n),hex(w))
