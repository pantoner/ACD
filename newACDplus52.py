import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import sqlite3
import pickle
import config

client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

def plus5():
	conn2 = sqlite3.connect("Plus5Earningsdb.db")
	cur2 = conn2.cursor()
	query2 = 'DROP TABLE IF EXISTS range'
	cur2.execute(query2)

	conn = sqlite3.connect("symbollistdb.db")
	cur = conn.cursor()
	query = 'SELECT * FROM symbols'
	cur.execute(query)
	rows = cur.fetchall()
	for row in rows:
		symbolname = str(row[1])
	# 	print(row[1])

	# for symbolname in symbollist:
		yesterday = pickle.load( open( "yesterday.p", "rb" ) )
		today = pickle.load( open( "today.p", "rb" ) )
		start = pickle.load( open( "start.p", "rb" ) )

		#symbolname = str(yesterday['symbol'])
		yesterday = str(yesterday['year']+"-"+yesterday['month']+"-"+yesterday['day'])
		today = str(today['year']+"-"+today['month']+"-"+today['day'])
		start = str(start['year']+"-"+start['month']+"-"+start['day'])
		try: 

			df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='20Min',
				startDate= today,
				endDate='12-30-2020')))
		
			openrangehigh = round(df.iloc[0, 2],2)
			openrangelow = round(df.iloc[0, 3],2)

			#conn = sqlite3.connect("test.db")
			#thisoutputdf.to_sql('opencloserange', conn, if_exists='append')

			ydf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='daily',
				startDate= yesterday,
				endDate='12-30-2020')))
			pivothigh = ydf.iloc[0, 2]
			pivotlow = ydf.iloc[0, 3]
			pivotclose = ydf.iloc[0, 1]
			dailypivotnumber = (pivotclose + pivotlow + pivothigh)/3
			dailypivotdifferential = ((pivotlow + pivothigh)/2)  -  dailypivotnumber
			dailypivotnumber =round(dailypivotnumber,2)
			pivottop = round(dailypivotnumber  + abs(dailypivotdifferential),2)
			pivotbottom = round(dailypivotnumber  - abs(dailypivotdifferential),2)
			if pivotclose > dailypivotnumber  - abs(dailypivotdifferential):
				tone = "Bullish"
			elif pivotclose < dailypivotnumber  - abs(dailypivotdifferential):
				tone = "Bearish"
			else:
				tone = "Neutral"

			tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
			fmt='csv',
			frequency='daily',
			startDate= start,
			endDate='12-30-2020')))

			drange = tdf.high - tdf.low
			Avalue = drange.values.mean()/4
			Aup = round(openrangehigh + Avalue,2)
			Adwn = round(openrangelow - Avalue,2)
			momentum1 = tdf.iloc[-1,1] - tdf.iloc[-9,1]
			momentum2 = tdf.iloc[-2,1] - tdf.iloc[-10,1] 
			momentum3 = tdf.iloc[-3,1] - tdf.iloc[-11,1] 

			output = {"today":today,"symbol":[symbolname],"openrangehigh":openrangehigh,"openrangelow":openrangelow,"dailypivotnumber":dailypivotnumber,"pivottop":pivottop,"pivotbottom":pivotbottom, "tone":tone, \
			"Aup":Aup,"Adwn":Adwn,"momentum":momentum1}
			outputdf = pd.DataFrame(output)

			conn2 = sqlite3.connect("Plus5Earningsdb.db")
			outputdf.to_sql('range', conn2, if_exists='append')
			# cur = conn.cursor()
		 #    cur.execute("SELECT * FROM range WHERE symbol=?", ("T",))
		 #    rows = cur.fetchall()

		 #    for row in rows:
		 #        print(row)
			df = pd.read_sql_query("SELECT * from range", conn2)

			print(df)
		except:
			continue