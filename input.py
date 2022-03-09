f = open("text.txt",mode = 'r',encoding = 'utf-8')

a = f.readline()
a = a.split()
if int(a[0]) > 0:
    print(a[0])

f.close()