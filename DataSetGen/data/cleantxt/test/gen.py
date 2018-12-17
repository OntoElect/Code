
for i in range(0,107):
    f = open(   ('000000'+str(i))[-5:]+'.txt', 'w' )
    f.write(str(i)+"\n")
    f.close()
