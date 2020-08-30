import requests, json
import datetime
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay
base_url = "https://api.gemini.com/v2"
response = requests.get(base_url + "/candles/ethusd/1hr")
btc_candle_data = response.json()
#print(btc_candle_data[0])
lasttime = int(str(btc_candle_data[-1][0])[:-3])
firsttime = int(str(btc_candle_data[0][0])[:-3])
lasttime = (datetime.fromtimestamp(lasttime) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
firsttime = (datetime.fromtimestamp(firsttime) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
df = pd.DataFrame(btc_candle_data)
n=0
newdate =[]
while n < len(df.index):
	firsttime = int(str(btc_candle_data[n][0])[:-3])
	firsttime = (datetime.fromtimestamp(firsttime) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M')
	newdate.append(firsttime)
	n+=1
newdatedf = pd.DataFrame(newdate)
#print(newdatedf)
df = pd.concat([df, newdatedf], axis=1, ignore_index=True)
df.columns = ['thistime','open','high','low','close','volume','newtime']
#df.to_csv('newoutput.csv')
n=0
openrange = [];allelse =[]

while n < len(df):
	if df.newtime.values[n][11:16] == "00:00":
		openrange.append({'date':df.newtime[n][0:10],'orhigh':df.high.values[n],'orlow':df.low.values[n],'open':df.open.values[n],'close':df.close.values[n]})
		n+=1
	else:
		#print(df.newtime.values[n][11:16])
		allelse.append({'date':df.newtime[n][0:10],'allhigh':df.high.values[n],'alllow':df.low.values[n],'open':df.open.values[n],'close':df.close.values[n]})
		n+=1

ordf = pd.DataFrame(openrange)
alldf = pd.DataFrame(allelse)
dfallhigh = alldf.groupby('date')['allhigh'].max()
dfalllow = alldf.groupby('date')['alllow'].min()
dfhighlow = alldf.groupby('date').agg({'allhigh': max, 'alllow': min}).reset_index()
btcprices = pd.merge(dfhighlow,ordf,how='left',left_on='date',right_on='date')
btcprices = btcprices.dropna()
btcprices.allhigh.astype(int);btcprices.orhigh.astype(int)
btcprices = btcprices.reset_index(drop=True)
# btcprices['higher'] = np.where(btcprices['allhigh'] >= btcprices['orhigh'], True, False)
# btcprices['lower'] = np.where(btcprices['alllow'] >= btcprices['orlow'], True, False)
# btcprices['answer'] = btcprices['lower'] + btcprices['higher']
#btcprices.to_csv('newoutput.csv')
#print('complete')
#print(btcprices)

thistoday = pd.datetime.today()
thirtydays	= (pd.datetime.today()-timedelta(days=30)).isoformat()
#print(thirtydays)
startdate = thirtydays[0:10]
# year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
# startdate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
#print(startdate)
#print(startdate)
thirtydayindex = btcprices[btcprices['date'] == startdate].index.values[0]

last30days = btcprices[btcprices.index >= thirtydayindex]
last30days
#print(last30days)
ordiff = sum(last30days.orhigh - last30days.orlow)/30
#print(ordiff)
alldiff = sum(last30days.allhigh - last30days.alllow)/30
#print(alldiff/5)
winloss = last30days.close - last30days.open
#print(winloss[winloss >0])

ordf = ordf[ordf.index >= thirtydayindex]
winloss = ordf.close - ordf.open
winlossdf = pd.DataFrame(winloss)
last30days = pd.merge(last30days,winlossdf,how='left',left_index =True,right_index=True)
last30days.columns = ['date','allhigh','alllow','orhigh','orlow','winloss','open','close']
# print(last30days)
truerange = sum(df.open - df.close)/30

winlist =[]
notwinlist = []
n=0
try:
	while n < len(last30days):
		x = 20
		while x < 120:
			if (last30days.orhigh.values[n] + x) < last30days.allhigh.values[n]:
				thisdict = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
				winlist.append(thisdict)
				x+= 1
			else:
				notwin = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
				notwinlist.append(notwin)
				x+=1
		n+=1
except IndexError:
	print('complete')

windf = pd.DataFrame(winlist)
notwindf = pd.DataFrame(notwinlist)
windf.columns =['index','number','outcome']
#losedf.columns =['index','number','outcome']

winoutcome = windf.groupby('number')['outcome'].sum()
# print(winoutcome)


loselist =[]
notloselist = []
n=0
try:
	while n < len(last30days):
		x = 20 
		while x < 120:
			if (last30days.orlow.values[n] - x) < last30days.alllow.values[n]:
				thisdict = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
				loselist.append(thisdict)
				x+= 1
			else:
				notlose = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
				notloselist.append(notlose)
				x+= 1
		n+=1
except IndexError:
	print('complete')


losedf = pd.DataFrame(loselist)
notlosedf = pd.DataFrame(notloselist)

losedf.columns =['index','number','outcome']

loseoutcome = losedf.groupby('number')['outcome'].sum()
# print(loseoutcome)

windf = pd.DataFrame(winoutcome)
losedf = pd.DataFrame(loseoutcome)

outcomedf = pd.merge(windf,losedf,how='left',left_index =True,right_index =True)
outcomedf['bestworst'] = outcomedf.outcome_x - outcomedf.outcome_y

thebestwin = windf.loc[windf['outcome'].idxmax()]
# print(f'this is the best {thebestwin}')
thebestlose = losedf.loc[losedf['outcome'].idxmin()]

aplusadd = thebestwin.name
aminussubtract = thebestlose.name
# print(thebestwin)
# print(thebestlose)
print(aplusadd, aminussubtract)
#print(ordf.orhigh[0]+aplusadd,ordf.orlow[0]-aminussubtract)
# print(truerange)
# print(thirtydayindex)
aplus = openrange[0]['orhigh'] + aplusadd
aminus = openrange[0]['orlow'] - aminussubtract
print(df.head(1))
print(aplus,aminus)

# middlelist =[]
# outlist = []
# n=0
# try:
# 	while n < len(last30days):
# 		x = 24 ; y = 84
# 		if (last30days.orhigh.values[n] + x) < last30days.alllow.values[n] and (last30days.orlow.values[n] - y) > last30days.alllow.values[n]:
# 			thisdict = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
# 			middlelist.append(thisdict)
# 			x+=1
# 		else:
# 			outlist = {'index':[n],'number':x,'winloss': last30days.winloss.values[n]}
# 			x+=1
# 		n+=1
# except IndexError:
# 	print('complete')

# middledf = pd.DataFrame(middlelist)
# outdf = pd.DataFrame(outlist)
# middledf.columns =['index','number','outcome']
# outdf.columns =['index','number','outcome']
# print(middledf)
# print(outdf)

#print(losedf.groupby('number')['outcome'].sum())


#can get opening range high and low and create Aup and Adwn

#to get pivot range only need the last day high low from max and min of high low from last30days[-1]
#
# for todays open range I only need the df.newtime.values[n][11:16] == "00:00": for this day which is the date == to today and "00:00"
