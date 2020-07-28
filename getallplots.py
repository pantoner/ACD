import pandas as pd
import sqlite3
import alertsMap


def getthisplot():
		conn = sqlite3.connect("alertsymbols.db")
		df= pd.read_sql_query("select * from symbols;", conn)
		symbollist = df['symbol'].tolist()
		print(symbollist)
		for symbol in symbollist:
			try:
				conn3 = sqlite3.connect("alerts.db")
				df= pd.read_sql_query("select * from alert2;", conn3)
			except:
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
				top = 'adwn'
			elif thisdf.wascup.all() == True:
				top = 'cdwn'
			elif thisdf.wascdwn.all() == True:
				top = 'cdwn'
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
			#alertsMap.addalertline(fail,top,now,symbol)
			alertsMap.addalertline(fail,top,now,symbol)

getthisplot()