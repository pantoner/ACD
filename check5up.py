import time
from io import StringIO
from tiingo import TiingoClient
import pandas as pd
import sqlite3
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
symbols = ['TBIO','DBX','ASMB','QDEL','KDP','PFSI','FTNT','LVGO','ALTM','AGLE','HAIN','NOMD','EIGR','AAWW','CNST','AWK','PVG','SRPT','CENTA','FSLY','LGND','ADTN','REAL','ATRA','AEIS',\
'FVRR','W','OSB','ABC','ENR','CLVS','BGS','LOPE','EXPI','GNMK','ACIA','KLAC','CHGG','TREX','CLX','PBFX','BAH','BERY','MPWR','FORM','BAND','HOLX','YUMC','PB','APAM','SPGI','DHI','GCAP',\
'VLY','DTE','SLGN','CALX','FNF','ETSY','BIDU','AA','STLD','IRBT','TMO','CLGX','DGX','NUE','TPX','WTER','TACO','MXL','TPB','HUN','SHW','PKI','MXIM','SBH','CRTO','FORM','ZYXI','RYI','PTC',\
'MAS','SAH','XLNX','QDEL','FRTA','LMNX','INMD','VCEL','MATX','NUS','GDDY','PCRX','HIMX','KOP','HEAR','LVGO','KINS','AXNX','FSCT','VERI','XP','MTBC','BLFS','WYY','PRCP','ADS','TBBK','VRSN',\
'PB','BLKB','BAH','MGP','WES','HEP','CIM','NDLS','CQP','CWK','DBX','G','UTI','VGR','AVYA','NBLX','ET','RICK','SUN','TAK','VVI','VMW','AEO','GIII','CIEN','ZUMZ','GCO','PRGS','AUY','NFLX','BLK',\
'SMPL','SNX','RAD','VIPS','DOYU','SINA','EQX','SSRM','JD','ETRN','CELH','HEAR','NTDOY','FOCS','ABBV']

today = '07-15-2020'
conn = sqlite3.connect("Plus5Earningsdb.db")
conn2 = sqlite3.connect("Plus5minbymin.db")
#plus5df = pd.read_sql_query("SELECT * from range", conn)
#print(plus5df)
n = 1
starttime = time.time()
while True:
	for symbolname in symbols:
		try:

			df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='1Min',
				startDate= today,
				endDate='12-30-2020')))

			#plus5df = pd.read_sql_query(f"SELECT * from range WHERE symbol = {str(symbolname)}", conn)
			cur = conn.cursor()
			rows = cur.fetchall()
			query = 'SELECT * FROM range WHERE symbol = ? AND today = ?'
			cur.execute(query, (symbolname,today,))
			records = cur.fetchall()
			#print(records[0][9])    
			highaup=0;openaup=0;lowaup=0;closeaup=0
			if df.iloc[-1,2] > records[0][9]:
				print((f"{symbolname} high is Aup"))
				highaup = 1
			if df.iloc[-1,4] > records[0][9]:
				print((f"{symbolname} open is Aup"))
				openaup = 1
			if df.iloc[-1,3] > records[0][9]:
				print((f"{symbolname} low is Aup"))
				lowaup = 1
			if df.iloc[-1,1] > records[0][9]:
				print((f"{symbolname} close is Aup"))
				closeaup = 1
			if (highaup + openaup + lowaup + closeaup) > 0:
				outputdict = {'today':[today],'thistime':df.iloc[-1,0],'symbol':symbolname,"highaup":highaup,"openaup":openaup,'lowaup':lowaup,'closeaup':closeaup,'iteration':n}
				outputdf = pd.DataFrame(outputdict)
				conn2 = sqlite3.connect("Plus5minbymin.db")
				outputdf.to_sql('aup', conn2, if_exists='append')
				print(outputdf)

			highadwn=0;openadwn=0;lowadwn=0;closeadwn=0	
			if df.iloc[-1,2] < records[0][10]:
				print((f"{symbolname} high is Adwn"))
				highadwn = 1
			if df.iloc[-1,4] < records[0][10]:
				print((f"{symbolname} open is Adwn"))
				openadwn = 1
			if df.iloc[-1,3] < records[0][10]:
				print((f"{symbolname} low is Adwn"))
				lowadwn = 1
			if df.iloc[-1,1] < records[0][10]:
				print((f"{symbolname} close is Adwn"))
				closeadwn = 1
			if (highadwn + openadwn + lowadwn + closeadwn) > 0:
				outputdict = {'today':[today],'thistime':df.iloc[-1,0],'symbol':symbolname,"highadwn":highadwn,"openadwn":openadwn,'lowadwn':lowadwn,'closeadwn':closeadwn,'iteration':n}
				outputdf = pd.DataFrame(outputdict)
				conn2 = sqlite3.connect("Plus5minbymin.db")
				outputdf.to_sql('adwn', conn2, if_exists='append')
				print(outputdf)
		except:
			continue
	
	#dfdwn = pd.read_sql_query("SELECT * from adwn", conn2)
	dfaup = pd.read_sql_query("SELECT * from aup", conn2)
	#print(dfdwn)
	print(dfaup)
	f'complete {n}'
	n+=1
	time.sleep(120.0 - ((time.time() - starttime) % 120.0))
	# close = df.iloc[-1,1]
	# high = df.iloc[-1,2]
	# low = df.iloc[-1,3]
	# topen = df.iloc[-1,4]
	# Aup = plus5df.Aup.values()
	# print(close,high,low,open,Aup)