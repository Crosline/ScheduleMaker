def oopen(txt):
    """ opens txt file and returns a list of classes """
    x = open(txt+".txt","r")
    z =[]
    k = []
    
    for i in x:
        y = i.strip().split("\t")
        z.append(y)
    x.close()
    
    for i in z:
        y = []
        for j in i:
           x = j.split(" ")
           y.append(x)
        k.append(y)
    return k

def scrambeler(inp):
    """takes classes list of a class and returns possible schedules"""
    allclasses = []
    clastypes =[]
    allschedules =[]
    
    for i in inp:
        clastypes.append(i[0])
        for j in range(int(i[1])):
            allclasses.append(i[0])
    
    

    return allclasses
x = oopen("TestInput")
for i in x:
    y = scrambeler(i)
    print(y)