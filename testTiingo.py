import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import pickle
import config
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# API_KEY = '' # your API KEY here
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
symbolname = 'MRNA'
df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
    fmt='csv',
    frequency='1min',
    startDate= '07-17-2020',
    endDate='12-30-2020')))

# print(df.iloc[-9,1])
# print(df)


# conn = sqlite3.connect("symbollistdb.db")
# cur = conn.cursor()
# query = 'SELECT * FROM symbols'
# cur.execute(query)
# rows = cur.fetchall()
# for row in rows:
# 	print(row[1])
tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
	fmt='csv',
	frequency='daily',
	startDate= '06/04/2020',
	endDate='12-30-2020')))


#try:
drange = tdf.high - tdf.low
Avalue = drange.values.mean()/5  #20% or 4 = 25%

n = 0
nowrangelist =[]
nowvolumelist =[]
while n < len(df):
	nowclose = round(df.iloc[n, 1],2)
	nowopen = round(df.iloc[n, 4],2)
	nowhigh = round(df.iloc[n,2],2)
	nowlow = round(df.iloc[n,3],2)
	nowrange = round((nowclose + nowlow + nowhigh)/3,2)
	nowvolume = round(df.iloc[n, 5],2)
	nowvolumelist.append(nowvolume)
	nowrangelist.append(nowrange)
	print(nowrange)
	n += 1
n =0
openingvolumelist =[]
while n < 20:
	nowvolume = round(df.iloc[n, 5],2)
	openingvolumelist.append(nowvolume)
	n+=1
avgopeningvolume = (sum(openingvolumelist)/20)
print(avgopeningvolume)

rangedf = pd.DataFrame(nowrangelist)
thisdf = rangedf.columns = ['price']
volumedf = pd.DataFrame(nowvolumelist)
# fixed fucking range index not allowing changing of column name !!!
volumedf.index = list(volumedf.index)
volumedf.columns =['volume',]
thisdf = pd.merge(rangedf,volumedf,how='left',left_index =True,right_index=True)
thisdf['relativevolume']= thisdf.volume/avgopeningvolume
thisdf['relativeprice'] = thisdf.relativevolume * thisdf.price 
thisdf['adjprice'] = thisdf['relativeprice'].rolling(10).sum()
thisdf['minprice'] = thisdf['price'].cummin()
thisdf['maxprice'] = thisdf['price'].cummax()
thisdf['avgvolume'] = thisdf['relativevolume'].rolling(10).sum()/10
openrangelow = thisdf.iloc[19,5]
openrangehigh = thisdf.iloc[19,6]
Aup = round(openrangehigh + Avalue,2)
Adwn = round(openrangelow - Avalue,2)

print(openrangehigh,openrangelow)
# TIME TIME TIME TIME

thisdf['timebelowAdwn'] = thisdf.apply(lambda x: x['price'] <= Adwn, axis=1)
#thisdf['timeaboveAdwn'] = thisdf.apply(lambda x: x['price'] >= openrangelow, axis=1)
#thisdf['timebelowORH'] = thisdf.apply(lambda x: x['price'] <= openrangehigh, axis=1)
thisdf['timeaboveAup'] = thisdf.apply(lambda x: x['price'] >= Aup, axis=1)
thisdf['profitpos'] = thisdf['price']/Aup
thisdf['profitneg']= thisdf['price']/Adwn
# if I test different timeaboveAup and sum of true profit for

thisdf['AUPTrue'] = thisdf['timeaboveAup'].rolling(10).sum()
thisdf['AUPTrueTrue'] = thisdf['timeaboveAup'].cumsum()
thisdf['AUPDWNTrue'] = thisdf['timebelowAdwn'].rolling(10).sum()
print(thisdf.columns)


n= 0
wasauplist=[]
output = []
# def wasaupfunc(thisdf):
while n < len(thisdf):
	if thisdf.iloc[n,12] >9:
		wasauplist.append(1)
	else:
		wasauplist.append(0)
	if sum(wasauplist) == 0:
		output.append(False) 
	else:
		output.append(True)
	n +=1


wasaupdf = pd.DataFrame({'wasaup':output})
thisdf = thisdf.append(wasaupdf)
print(thisdf.columns)

# next create wasdwndf, then can figure out the C's and the EOD positions --




	# 	if thisdf['wasAup'].shift(-1) == True:
	# 		wasAup == True
	# 	elif thisdf['AUPTrue'] == 10:
	# 		wasAup== True
	# return wasAup




#output = thisdf[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','timebelowAdwn','price','profitpos','avgvolume']].copy()
#print(thisdf[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','price','profitpos','avgvolume']].copy())


#output.to_csv('C:/Python37/ACD/output.csv')
#print(thisdf.wasAup)
#weighted by opening volume




#print(volumedf)
