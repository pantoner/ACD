import requests, json
import datetime
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay
base_url = "https://api.gemini.com/v2"
response = requests.get(base_url + "/candles/btcusd/1hr")
btc_candle_data = response.json()
print(btc_candle_data[0])
lasttime = int(str(btc_candle_data[-1][0])[:-3])
firsttime = int(str(btc_candle_data[0][0])[:-3])
lasttime = (datetime.fromtimestamp(lasttime) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
firsttime = (datetime.fromtimestamp(firsttime) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
df = pd.DataFrame(btc_candle_data)

def getstartdate():
	thistoday = pd.datetime.today()
	thirtydays	= (pd.datetime.today()-timedelta(days=29)).isoformat()
	startdate = thirtydays[0:10]
	return startdate

def getnewdate(df):
	n=0
	newdate =[]
	newtime =[]
	while n < len(df.index):
		firsttime = int(str(btc_candle_data[n][0])[:-3])
		firstdate = (datetime.fromtimestamp(firsttime) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M')[0:10]
		firsttime = (datetime.fromtimestamp(firsttime) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M')[11:16]
		newdate.append(firstdate)
		newtime.append(firsttime)
		n+=1
	newdatedf = pd.DataFrame(newdate)
	newtimedf = pd.DataFrame(newtime)
	df = pd.concat([df, newdatedf], axis=1, ignore_index=True)
	df.columns = ['thistime','open','high','low','close','volume','newdate']
	df = pd.concat([df, newtimedf], axis=1, ignore_index=True)
	df.columns = ['thistime','open','high','low','close','volume','newdate','newtime']
	return df


def getfirstdailyhour(df):
	n=0
	openrange = []
	while n < len(df):
		if df.newtime.values[n] == "00:00":
			openrange.append({'index':[0],'date':df.newdate[n],'time':df.newtime[n],'orhigh':df.high.values[n],'orlow':df.low.values[n],'open':df.open.values[n],'close':df.close.values[n]})
			n+=1
		else:
			n+=1
	ordf = pd.DataFrame(openrange)
	#alldf = pd.DataFrame(allelse)
	return ordf


def getminmax(df):
	n=0
	dictlist =[]
	while n < len(df):
		thedict = ({'index':[0],'date':df.newdate[n],'time':df.newtime[n],'allhigh':df.high.values[n],'alllow':df.low.values[n],'open':df.open.values[n],'close':df.close.values[n]})
		dictlist.append(thedict)
		n+=1
	outputdf = pd.DataFrame(dictlist)
	return outputdf

df = getnewdate(df)
openingrangedf = getfirstdailyhour(df)	
minmaxout = getminmax(df)
startdate = getstartdate()

#print(minmaxout)

 # def getonly30(df):
	# n=0
 # 	while n < len(df):
 # 		thedate = df.newtime[n][0:10]
 # 		btcprices[btcprices['date'] == startdate].index.values[0]
 # 		if theda

# thedate = df.newtime[n][0:10]
# thetime = df.newtime.values[n][11:16]

dfhighlow = minmaxout.groupby('date').agg({'allhigh': max, 'alllow': min}).reset_index()
thirtydayindex = dfhighlow[dfhighlow['date'] == startdate].index.values[0]
last30days = dfhighlow[dfhighlow.index >= thirtydayindex]


# openrangedf needs last30day timeframe -- 
openingrangedf['winloss'] = openingrangedf.open -openingrangedf.close
print(openingrangedf)
print(last30days)
openingrangedf = pd.merge(openingrangedf, last30days, how='right', left_on='date', right_on='date')
#print(output)
winlist =[]
notwinlist = []
n=0
try:
	while n < len(openingrangedf):
		x = 20
		while x < 120:
			if (openingrangedf.orhigh.values[n] + x) < openingrangedf.allhigh.values[n]:
				thisdict = {'index':[n],'number':x,'winloss': openingrangedf.winloss.values[n]}
				winlist.append(thisdict)
				x+= 1
			else:
				notwin = {'index':[n],'number':x,'winloss': openingrangedf.winloss.values[n]}
				notwinlist.append(notwin)
				x+=1
		n+=1
except IndexError:
	print('complete')

windf = pd.DataFrame(winlist)
notwindf = pd.DataFrame(notwinlist)
windf.columns =['index','number','outcome']

winoutcome = windf.groupby('number')['outcome'].sum()
print(winoutcome)


loselist =[]
notloselist = []
n=0
try:
	while n < len(openingrangedf):
		x = 20 
		while x < 120:
			if (openingrangedf.orlow.values[n] - x) < openingrangedf.alllow.values[n]:
				thisdict = {'index':[n],'number':x,'winloss': openingrangedf.winloss.values[n]}
				loselist.append(thisdict)
				x+= 1
			else:
				notlose = {'index':[n],'number':x,'winloss': openingrangedf.winloss.values[n]}
				notloselist.append(notlose)
				x+= 1
		n+=1
except IndexError:
	print('complete')


losedf = pd.DataFrame(loselist)
notlosedf = pd.DataFrame(notloselist)

losedf.columns =['index','number','outcome']

loseoutcome = losedf.groupby('number')['outcome'].sum()
print(loseoutcome)

windf = pd.DataFrame(winoutcome)
losedf = pd.DataFrame(loseoutcome)

outcomedf = pd.merge(windf,losedf,how='left',left_index =True,right_index =True)
outcomedf['bestworst'] = outcomedf.outcome_x - outcomedf.outcome_y

thebestwin = windf.loc[windf['outcome'].idxmax()]
# print(f'this is the best {thebestwin}')
thebestlose = losedf.loc[losedf['outcome'].idxmin()]

aplusadd = thebestwin.name
aminussubtract = thebestlose.name
print(thebestwin)
print(thebestlose)
print(aplusadd, aminussubtract)
print(openingrangedf.orhigh[0], openingrangedf.orlow[0],openingrangedf.date[0])
