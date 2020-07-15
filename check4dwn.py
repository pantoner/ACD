import time
from io import StringIO
from tiingo import TiingoClient
import pandas as pd
import sqlite3
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
symbols = ['MASI','SPY','ROAD','SYBX','SWIR','GKOS','RLJ','AQN','SERV','AVRO','MRO','SEDG','GBT','WYNN','AYX','AKR','AERI','CLDT','IONS','JNCE','PCG','PTCT','LADR','SJW','CEMI','BHLB',\
'MRK','POR','PBF','NWL','VFC','MPW','PFPT','MHK','GIL','COLM','GPC','ELAN','ORBC','UPS','TFX','NOC','TS','MC','CODI','EQC','TYL','TTEK','APLS','LIVN','ETN','HAFC','FCF','CHRW','NCR',\
'SBUX','LW','WAT','FBP','MEDP','CURO','FIBK','HSII','SCI','E','GT','INDB','GBCI','FFIN','SBCF','MAT','IEX','FFBC','FWRD','HTBK','COLB','APD','HFWA','UBSI','WSO','KMI','BRKL','NTGR','ECHO',\
'BPFH','ICLR','ARCH','HCA','FCFS','UCBI','WRB','FMBI','IBKR','CBSH','PACW','ELS','HSTM', 'SNAP''SIMO','SHAK','X','CEMI','BGCP','PQG','LNDC','IO','NEPH','IVC','NVCN','TSLA','ALKS','ASPS', \
'EHTH','MAT','GHL','VNE','SILK','VCRA','NOV','ALIM','IVAC','SQNS','PEGA','ATRC','TWOU','NBR','FEYE','SHOP','SPOT','HES','CCJ','AMRN','APLS','STNG','INFY','MS','PPG','ALLY','STLD','PM','MLI',\
'KO','GATX','IBKR','FE','ISRG','WRB','DB','APH','CP','DOV','IBM','GGG','PLXS','UFPI','UNP','STM','TRV','HSY','ALLE','FIX','STC','MAT','NEP','HON','LECO','SANM','NXPI','BRO','SJM','NAV','ENS',\
'CIR','MNRO','HPQ','HRL','MDT','LB','RXN','FLOW','PRA','UFS','WCN','FLS','CBT','LNT','NWSA','SLF','RSG','PNW','CFX','CCOI','BLL','BDX','AAON','AES','ZTS','WTS','HCC','ALB','QNST','RYN','NI','TRI',\
'PERI','AVNS','ARES','AEP','ALE','ES','DIS','EXR','PRU','MEOH','ZBH','WRK','JELD','ITW','AME','CRI','EXC','FN','CWST','MWA','MOS','TKR','WY','PEG','ITT','JCI','FCAU','CAT','AON','AJG','F','FTAI',\
'FND','HUBG','GFF','HIG','MTX','LBRDK','WM','WLTW','XYL','WCC','TRS','K','LM','MMC','MT','OSK'.'ODFL','SO','SWK','HBI','CNHI','CMCSA','ELAN','CNMD','ADM','FBHS','TSE','SKY','SIGI','WNC','NSC','R',\
'GIB','ETN','BG','EIX','CE','CCS','FTV','HRZN','RNR','MDLX','UNM','XRX','WAT','HUN','MDC','MMM','MLM','ST','GLW','CINF']

today = '07-14-2020'
conn = sqlite3.connect("Minus4Earningsdb.db")
conn2 = sqlite3.connect("Minus4minbymin.db")
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
				conn2 = sqlite3.connect("Minus4minbymin.db")
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
				conn2 = sqlite3.connect("Minus4minbymin.db")
				outputdf.to_sql('adwn', conn2, if_exists='append')
				print(outputdf)
		except:
			continue
	
	#dfdwn = pd.read_sql_query("SELECT * from adwn", conn2)
	dfadwn = pd.read_sql_query("SELECT * from adwn", conn2)
	#print(dfdwn)
	print(dfadwn)
	f'complete {n}'
	n+=1
	time.sleep(120.0 - ((time.time() - starttime) % 120.0))
	# close = df.iloc[-1,1]
	# high = df.iloc[-1,2]
	# low = df.iloc[-1,3]
	# topen = df.iloc[-1,4]
	# Aup = plus5df.Aup.values()
	# print(close,high,low,open,Aup)