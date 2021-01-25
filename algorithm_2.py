x =6
y =13 
num = 0
while True:
    if x > y:
        num += 1
        y+=1
    elif y == x:
        break
    elif y % 2 == 0:
        while True:
            if x >= y:
                break
            if y % 2 == 0:
                num += 1
                y /= 2
            else:
                break
    else:
        num+=1
        y +=1
print("the minimum number of steps to x = y: " + str(num))