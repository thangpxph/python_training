x =8745
y = 546895
num = 0
z = y
list_z = []
while True:
    if x > z:
        break
    elif z % 2 == 0:
        while True:
            if x > z:
                break
            if z % 2 == 0:
                z /= 2
                list_z += [z]
            else:
                break
    else:
        if x > z:
            break
        else:
            num+=1
            z +=1
li = list_z[::-1]
for i in li:
    while True:
        if x < i:
            num+=1
            x*=2
        elif x > i:
            num+=1
            x -=1
        else:
            num+=1
            x *=2
            break
print(x)
print("the minimum number of steps to x = y: " + str(num))