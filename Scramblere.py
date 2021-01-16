def open_file(txt):
    with open(txt, "r") as f:
        x = f.readlines()
        x = [i.strip().split("\t") for i in x]

    z = []
    for i in x:
        y = []
        for j in i:
            t = j.split(" ")
            t[1] = int(t[1])

            while t[1] > 2:
                y.append([t[0], 2])
                t[1] -= 2
            y.append([t[0], t[1]])

        z.append(y)

    return z



print(open_file("TestInput.txt"))