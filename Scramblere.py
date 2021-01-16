import random as rnd

def open_file(txt):
    with open(txt, "r") as f:
        x = f.readlines()
        x = [i.strip().split("\t") for i in x]

    z = []
    for i in x:
        y = []
        for j in i:
            t = j.split(" ")

            for i in range(int(t[1])):
                y.append([t[0], 1])

        z.append(y)

    return z


def scrambeler(lst, day, hour):
    lessons = []
    rnd.shuffle(lst)
    tempList = lst.copy()

    i = len(tempList) - 1

    for hour_index in range(day):

        lessons_per_day = []
        temphour = 0

        while True:
            temphour += tempList[i][1]
            if(temphour > hour[hour_index]):
                break
            lessons_per_day.append(tempList[i])
            i -= 1
        lessons.append(lessons_per_day)

    return lessons


day = int(input("How many days do you take lessons?"))
print("Enter your daily lesson hour")

hour = []
hours = 0

for i in range(day):
    hour.append(int(input("Day " + str(len(hour)+1))))
    hours += hour[i]

lst = open_file("TestInput.txt")
lst = lst[0]
print(lst)

print(scrambeler(lst, day, hour))

