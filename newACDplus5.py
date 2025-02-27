import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import sqlite3
import pickle
import config

client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
today = '07-15-2020'
yesterday = "07-14-2020"
start = "06-03-2020"
symbols =['TBIO','DBX','ASMB','QDEL','KDP','PFSI','FTNT','LVGO','ALTM','AGLE','HAIN','NOMD','EIGR','AAWW','CNST','AWK','PVG','SRPT','CENTA','FSLY','LGND','ADTN','REAL','ATRA','AEIS',\
'FVRR','W','OSB','ABC','ENR','CLVS','BGS','LOPE','EXPI','GNMK','ACIA','KLAC','CHGG','TREX','CLX','PBFX','BAH','BERY','MPWR','FORM','BAND','HOLX','YUMC','PB','APAM','SPGI','DHI','GCAP',\
'VLY','DTE','SLGN','CALX','FNF','ETSY','BIDU','AA','STLD','IRBT','TMO','CLGX','DGX','NUE','TPX','WTER','TACO','MXL','TPB','HUN','SHW','PKI','MXIM','SBH','CRTO','FORM','ZYXI','RYI','PTC',\
'MAS','SAH','XLNX','QDEL','FRTA','LMNX','INMD','VCEL','MATX','NUS','GDDY','PCRX','HIMX','KOP','HEAR','LVGO','KINS','AXNX','FSCT','VERI','XP','MTBC','BLFS','WYY','PRCP','ADS','TBBK','VRSN',\
'PB','BLKB','BAH','MGP','WES','HEP','CIM','NDLS','CQP','CWK','DBX','G','UTI','VGR','AVYA','NBLX','ET','RICK','SUN','TAK','VVI','VMW','AEO','GIII','CIEN','ZUMZ','GCO','PRGS','AUY','NFLX','BLK',\
'SMPL','SNX','RAD','VIPS','DOYU','SINA','EQX','SSRM','JD','ETRN','CELH','HEAR','NTDOY','FOCS','ABBV']

for symbolname in symbols:

	df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
		fmt='csv',
		frequency='20Min',
		startDate= today,
		endDate='12-30-2020')))
	try: 
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

		conn = sqlite3.connect("Plus5Earningsdb.db")
		outputdf.to_sql('range', conn, if_exists='append')
		# cur = conn.cursor()
	 #    cur.execute("SELECT * FROM range WHERE symbol=?", ("T",))
	 #    rows = cur.fetchall()

	 #    for row in rows:
	 #        print(row)
		df = pd.read_sql_query("SELECT * from range", conn)

		print(df)
	except:
		continue