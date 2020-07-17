import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import sqlite3
import pickle
import config

client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
today = "07-15-2020"
yesterday = "07-14-2020"
start = "06-03-2020"
# symbollist = [ 'MASI','SPY','ROAD','SYBX','SWIR','GKOS','RLJ','AQN','SERV','AVRO','MRO','SEDG','GBT','WYNN','AYX','AKR','AERI','CLDT','IONS','JNCE','PCG','PTCT','LADR','SJW','CEMI','BHLB',\
# 'MRK','POR','PBF','NWL','VFC','MPW','PFPT','MHK','GIL','COLM','GPC','ELAN','ORBC','UPS','TFX','NOC','TS','MC','CODI','EQC','TYL','TTEK','APLS','LIVN','ETN','HAFC','FCF','CHRW','NCR',\
# 'SBUX','LW','WAT','FBP','MEDP','CURO','FIBK','HSII','SCI','E','GT','INDB','GBCI','FFIN','SBCF','MAT','IEX','FFBC','FWRD','HTBK','COLB','APD','HFWA','UBSI','WSO','KMI','BRKL','NTGR','ECHO',\
# 'BPFH','ICLR','ARCH','HCA','FCFS','UCBI','WRB','FMBI','IBKR','CBSH','PACW','ELS','HSTM','SNAP','SIMO','SHAK','X','CEMI','BGCP','PQG','LNDC','IO','NEPH','IVC','NVCN','TSLA','ALKS','ASPS', \
# 'EHTH','MAT','GHL','VNE','SILK','VCRA','NOV','ALIM','IVAC','SQNS','PEGA','ATRC','TWOU','NBR','FEYE','SHOP','SPOT','HES','CCJ','AMRN','APLS','STNG','INFY','MS','PPG','ALLY','STLD','PM','MLI',\
# 'KO','GATX','IBKR','FE','ISRG','WRB','DB','APH','CP','DOV','IBM','GGG','PLXS','UFPI','UNP','STM','TRV','HSY','ALLE','FIX','STC','MAT','NEP','HON','LECO','SANM','NXPI','BRO','SJM','NAV','ENS',\
# 'CIR','MNRO','HPQ','HRL','MDT','LB','RXN','FLOW','PRA','UFS','WCN','FLS','CBT','LNT','NWSA','SLF','RSG','PNW','CFX','CCOI','BLL','BDX','AAON','AES','ZTS','WTS','HCC','ALB','QNST','RYN','NI','TRI',\
# 'PERI','AVNS','ARES','AEP','ALE','ES','DIS','EXR','PRU','MEOH','ZBH','WRK','JELD','ITW','AME','CRI','EXC','FN','CWST','MWA','MOS','TKR','WY','PEG','ITT','JCI','FCAU','CAT','AON','AJG','F','FTAI',\
# 'FND','HUBG','GFF','HIG','MTX','LBRDK','WM','WLTW','XYL','WCC','TRS','K','LM','MMC','MT','OSK','ODFL','SO','SWK','HBI','CNHI','CMCSA','ELAN','CNMD','ADM','FBHS','TSE','SKY','SIGI','WNC','NSC','R',\
# 'GIB','ETN','BG','EIX','CE','CCS','FTV','HRZN','RNR','MDLX','UNM','XRX','WAT','HUN','MDC','MMM','MLM','ST','GLW','CINF','CCK','RNST','TBK','OGI','FE','DOV','DB','CAJ','SCL','EIG','OBNK','CVBF',\
# 'GGG','RLI','UVSP','DOW','JPM']

def minus4():
	symbollist = [ 'MASI','SPY','ROAD','SYBX','SWIR','GKOS','RLJ','AQN','SERV','AVRO','MRO','SEDG','GBT','WYNN','AYX','AKR','AERI','CLDT','IONS','JNCE','PCG','PTCT','LADR','SJW','CEMI','BHLB',\
	'MRK','POR','PBF','NWL','VFC','MPW','PFPT','MHK','GIL','COLM','GPC','ELAN','ORBC','UPS','TFX','NOC','TS','MC','CODI','EQC','TYL','TTEK','APLS','LIVN','ETN','HAFC','FCF','CHRW','NCR',\
	'SBUX','LW','WAT','FBP','MEDP','CURO','FIBK','HSII','SCI','E','GT','INDB','GBCI','FFIN','SBCF','MAT','IEX','FFBC','FWRD','HTBK','COLB','APD','HFWA','UBSI','WSO','KMI','BRKL','NTGR','ECHO',\
	'BPFH','ICLR','ARCH','HCA','FCFS','UCBI','WRB','FMBI','IBKR','CBSH','PACW','ELS','HSTM','SNAP','SIMO','SHAK','X','CEMI','BGCP','PQG','LNDC','IO','NEPH','IVC','NVCN','TSLA','ALKS','ASPS', \
	'EHTH','MAT','GHL','VNE','SILK','VCRA','NOV','ALIM','IVAC','SQNS','PEGA','ATRC','TWOU','NBR','FEYE','SHOP','SPOT','HES','CCJ','AMRN','APLS','STNG','INFY','MS','PPG','ALLY','STLD','PM','MLI',\
	'KO','GATX','IBKR','FE','ISRG','WRB','DB','APH','CP','DOV','IBM','GGG','PLXS','UFPI','UNP','STM','TRV','HSY','ALLE','FIX','STC','MAT','NEP','HON','LECO','SANM','NXPI','BRO','SJM','NAV','ENS',\
	'CIR','MNRO','HPQ','HRL','MDT','LB','RXN','FLOW','PRA','UFS','WCN','FLS','CBT','LNT','NWSA','SLF','RSG','PNW','CFX','CCOI','BLL','BDX','AAON','AES','ZTS','WTS','HCC','ALB','QNST','RYN','NI','TRI',\
	'PERI','AVNS','ARES','AEP','ALE','ES','DIS','EXR','PRU','MEOH','ZBH','WRK','JELD','ITW','AME','CRI','EXC','FN','CWST','MWA','MOS','TKR','WY','PEG','ITT','JCI','FCAU','CAT','AON','AJG','F','FTAI',\
	'FND','HUBG','GFF','HIG','MTX','LBRDK','WM','WLTW','XYL','WCC','TRS','K','LM','MMC','MT','OSK','ODFL','SO','SWK','HBI','CNHI','CMCSA','ELAN','CNMD','ADM','FBHS','TSE','SKY','SIGI','WNC','NSC','R',\
	'GIB','ETN','BG','EIX','CE','CCS','FTV','HRZN','RNR','MDLX','UNM','XRX','WAT','HUN','MDC','MMM','MLM','ST','GLW','CINF','CCK','RNST','TBK','OGI','FE','DOV','DB','CAJ','SCL','EIG','OBNK','CVBF',\
	'GGG','RLI','UVSP','DOW','JPM']
	for symbolname in symbollist:
		yesterday = pickle.load( open( "yesterday.p", "rb" ) )
		today = pickle.load( open( "today.p", "rb" ) )
		start = pickle.load( open( "start.p", "rb" ) )

		#symbolname = str(yesterday['symbol'])
		yesterday = str(yesterday['year']+"-"+yesterday['month']+"-"+yesterday['day'])
		today = str(today['year']+"-"+today['month']+"-"+today['day'])
		start = str(start['year']+"-"+start['month']+"-"+start['day'])


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

			conn = sqlite3.connect("Minus4Earningsdb.db")
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