a = "123456789"
symbol= ["+"," ", "-"]
num = 100
for x1 in symbol:
	for x2 in symbol:
		for x3 in symbol:
			for x4 in symbol:
				for x5 in symbol:
					for x6 in symbol:
						for x7 in symbol:
							for x8 in symbol:
								b = ""
								b += a[:1] + x1 + a[1:1] + a[1:2] + x2 + a[2:2]+ a[2:3] + x3 + a[3:3]
								b += a[3:4] + x4 + a[4:4]+ a[4:5] + x5 + a[5:5]+ a[5:6] + x6 + a[6:6]
								b += a[6:7] + x7 + a[7:7]+ a[7:8] + x8 + a[8:8] + a[8:9]
								if eval(b.replace(" ","")) == num:
									print(b.replace(" ","") + "==> 100")			