a = "123456789"
symbol= ["+"," ", "-"]
num = 100
def test1(symbol, a, num):
	for x1 in symbol:
		num1 = a[:1] + x1 + a[1:]
		if eval(num1.replace(" ","")) == 100:
			print(num1.replace(" ",""))
		for x2 in symbol:
			num2 = num1[:3] + x2 + num1[3:]
			if eval(num2.replace(" ","")) == 100:
				print(num2.replace(" ",""))
			for x3 in symbol:
				num3 = num2[:5] + x3 + num2[5:]
				if eval(num3.replace(" ","")) == 100:
					print(num3.replace(" ",""))
				for x4 in symbol:
					num4 = num3[:7] + x4 + num3[7:]
					if eval(num4.replace(" ","")) == 100:
						print(num4.replace(" ",""))
					for x5 in symbol:
						num5 = num4[:9] + x5 + num4[9:]
						if eval(num5.replace(" ","")) == 100:
							print(num5.replace(" ",""))
						for x6 in symbol:
							num6 = num5[:11] + x6 + num5[11:]
							if eval(num6.replace(" ","")) == 100:
								print(num6.replace(" ",""))
							for x7 in symbol:
								num7 = num6[:13] + x7 + num6[13:]
								if eval(num7.replace(" ","")) == 100:
									print(num7.replace(" ",""))
								for x8 in symbol:
									if x8 == " ":
										pass
									else:
										num8 = num7[:15] + x8 + num7[15:]
										if eval(num8.replace(" ","")) == 100:
											print(num8.replace(" ",""))
test1(symbol, a, num)