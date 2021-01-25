a = "123456789"
symbol= ["+"," ", "-"]
num = 100

def permute(list, n):
    if list == 1:
        return n
    else:
        return [ y + x
                 for y in permute(1, n)
                 for x in permute(list - 1, n)
                 ]
bt = permute(8, symbol)
for i in bt:
	b = ""
	b += a[:1] + i[0] + a[1:1] + a[1:2] + i[1] + a[2:2]+ a[2:3] + i[2] + a[3:3]
	b += a[3:4] + i[3] + a[4:4]+ a[4:5] + i[4] + a[5:5]+ a[5:6] + i[5] + a[6:6]
	b += a[6:7] + i[6] + a[7:7]+ a[7:8] + i[7] + a[8:8] + a[8:9]
	if eval(b.replace(" ","")) == num:
		print(b.replace(" ","") + "== 100")