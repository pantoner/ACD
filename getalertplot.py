import pandas as pd
import sqlite3
import alertsMap




conn = sqlite3.connect("alertsymbols.db")
df= pd.read_sql_query("select * from symbols;", conn)
symbollist = df['symbol'].tolist()
print(symbollist)
for symbol in symbollist:
	conn3 = sqlite3.connect("alerts.db")
	df= pd.read_sql_query("select * from alert;", conn3)
	thisdf = df[df.symbol == symbol]

	fail = 0
	if thisdf.Aupfail.all() == True:
		fail = 1
	elif thisdf.Adwnfail.all() == True:
		fail = 5
	elif thisdf.Cdwnfail.all() == True:
		fail = 5
	elif thisdf.Cupfail.all() == True:
		fail = 1
	elif thisdf.Aupfail.all() + thisdf.Adwnfail.all() + thisdf.Cupfail.all() + thisdf.Cdwnfail.all() == 2:
		fail = 6


	top = 0
	if thisdf.wasaup.all() == True:
		top = 'aup'
	elif thisdf.wasadwn.all() == True:
		top = 'cup'
	elif thisdf.wascup.all() == True:
		top = 'cdwn'
	elif thisdf.wascdwn.all() == True:
		top = 'adwn'
	elif thisdf.wascup.all() == True and thisdf.wasadwn.all() == True:
		top = 'cupadwn'
	elif thisdf.wascdwn.all() == True and thisdf.wasaup.all() == True:
		top = 'cdwnaup'

	now = 0

	if thisdf.overaup.all() == True:
		now = 1
	elif thisdf.abovetopOR.all() == True:
		now = 2
	elif thisdf.betweenOR.all() == True:
		now = 3
	elif thisdf.belowbottomOR.all() == True:
		now = 4
	elif thisdf.belowadwn.all() == True:
		now = 5
	elif thisdf.belowadwn.all() == True and thisdf.wascdwn.all() == True:
		now = 7
	elif thisdf.overaup.all() == True and thisdf.wascup.all() == True:
		now = 6

	# failure = 0
	# top = 'cdwnaup'
	# now = 7
	print(symbol)
	alertsMap.addalertline(fail,top,now)
			# if outputdf.iloc[0]['Adwnfail'] == True and symbolname not in  Adwnfailsymbollist:
			# 	ret_val = ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A down FAIL", 1)
			# 	Adwnfailsymbollist.append(symbolname)
			# 	addalertline(failure,'adwn',now)

			# elif outputdf.iloc[0]['Aupfail'] == True and symbolname not in  Aupfailsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up FAIL", 1)
			# 	Aupfailsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['Cdwnfail'] == True and symbolname not in  Cdwnfailsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C down FAIL", 1)
			# 	Cdwnfailsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['Cupfail'] == True and symbolname not in  Cupfailsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C up FAIL", 1)
			# 	Cupfailsymbollist.append(symbolname)
			
			# elif outputdf.iloc[0]['wasaup'] == True and symbolname not in  Aupsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A up", 1)
			# 	Aupsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['wasadwn'] == True and symbolname not in  Adwnsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "A down", 1)
			# 	Adwnsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['wascdwn'] == True and symbolname not in  Cdwnsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C down ", 1)
			# 	Cdwnsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['wascup'] == True and symbolname not in  Cupsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "C up ", 1)
			# 	Cupsymbollist.append(symbolname)

			# elif outputdf.iloc[0]['belowOR'] == True and symbolname not in  belowORsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below OR", 1)
			# 	belowORsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['aboveOR'] == True and symbolname not in  aboveORsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "above OR", 1)
			# 	aboveORsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['belowadwn'] == True and symbolname not in  belowadwnsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below A down ", 1)
			# 	belowadwnsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['overaup'] == True and symbolname not in  overaupsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "over A up ", 1)
			# 	overaupsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['abovetopOR'] == True and symbolname not in  abovetopORsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "above top OR", 1)
			# 	abovetopORsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['belowbottomOR'] == True and symbolname not in  belowbottomORsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "below bottom OR ", 1)
			# 	belowbottomORsymbollist.append(symbolname)
			# elif outputdf.iloc[0]['betweenOR'] == True and symbolname not in  betweenORsymbollist:
			# 	ctypes.windll.user32.MessageBoxW(0, str(symbolname), "between OR", 1)
			# 	betweenORsymbollist.append(symbolname)