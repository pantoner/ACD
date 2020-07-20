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
	#print(nowrange)
	n += 1
n =0
openingvolumelist =[]
while n < 20:
	nowvolume = round(df.iloc[n, 5],2)
	openingvolumelist.append(nowvolume)
	n+=1
avgopeningvolume = (sum(openingvolumelist)/20)
#print(avgopeningvolume)

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

#print(openrangehigh,openrangelow)
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
thisdf['ADWNTrue'] = thisdf['timebelowAdwn'].rolling(10).sum()
thisdf['ADWNTrueTrue'] = thisdf['timebelowAdwn'].cumsum()
#print(thisdf.columns)


n= 0
wasauplist=[]
output = []
# def wasaupfunc(thisdf):
while n < len(thisdf):
	if thisdf.loc[n,'AUPTrue'] >9:
		wasauplist.append(1)
	else:
		wasauplist.append(0)
	if sum(wasauplist) == 0:
		output.append(False) 
	else:
		output.append(True)
	n +=1


wasaupdf = pd.DataFrame({'wasaup':output})
thisdf2 = pd.merge(thisdf,wasaupdf, how='left',left_index=True,right_index=True)

#thisdf2 = thisdf2.append(wasaupdf)
#outputtocsv = thisdf2[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','timebelowAdwn','price','profitpos','avgvolume','wasaup']].copy()
#output.to_csv('C:/Python37/ACD/output.csv')
#print(thisdf2.columns)

n= 0
wasadwnlist=[]
output = []
# def wasaupfunc(thisdf):
while n < len(thisdf2):
	if thisdf2.loc[n,'ADWNTrue'] >9:
		wasadwnlist.append(1)
	else:
		wasadwnlist.append(0)
	if sum(wasadwnlist) == 0:
		output.append(False) 
	else:
		output.append(True)
	n +=1


wasadwndf = pd.DataFrame({'wasadwn':output})
thisdf3 = pd.merge(thisdf2,wasadwndf, how='left',left_index=True,right_index=True)
# print(thisdf3.columns)
# outputtocsv = thisdf3[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','timebelowAdwn','price','profitpos','avgvolume','wasaup','wasadwn']].copy()
# outputtocsv.to_csv('C:/Python37/ACD/output.csv')



# figure out fail -- 

# C dwn
thisdf3['timebelowCdwn'] = thisdf3.apply(lambda x: x['price'] <= Adwn and x['wasaup'] == True, axis=1)  #just like line 85
thisdf3['CDWNTrue'] = thisdf3['timebelowCdwn'].rolling(10).sum()  # line 93
thisdf3['CDWNTrueTrue'] = thisdf3['timebelowCdwn'].cumsum() # line 94

n= 0
wascdwnlist=[]
output = []
# def wasaupfunc(thisdf):
while n < len(thisdf3):
	if thisdf3.loc[n,'CDWNTrue'] >9:
		wascdwnlist.append(1)
	else:
		wascdwnlist.append(0)
	if sum(wascdwnlist) == 0:
		output.append(False) 
	else:
		output.append(True)
	n +=1

wascdwndf = pd.DataFrame({'wascdwn':output})
thisdf3 = pd.merge(thisdf3,wascdwndf, how='left',left_index=True,right_index=True)

# C UP
thisdf3['timeaboveCup'] = thisdf3.apply(lambda x: x['price'] >= Aup and x['wasadwn'] == True, axis=1)  #just like line 88
thisdf3['CUPTrue'] = thisdf3['timeaboveCup'].rolling(10).sum()  # line 95
thisdf3['CUPTrueTrue'] = thisdf3['timeaboveCup'].cumsum() # line 96

n= 0
wascuplist=[]
output = []
# def wasaupfunc(thisdf):
while n < len(thisdf3):
	if thisdf3.loc[n,'CUPTrue'] >9:
		wascuplist.append(1)
	else:
		wascuplist.append(0)
	if sum(wascuplist) == 0:
		output.append(False) 
	else:
		output.append(True)
	n +=1
# A fail
# #between 1 and 9 inclusive and then back to 0 for AupTrue is an Afail. 
# #max of AuP is less than nine for count of ten 
# thisdf3['Aupfailmaybe'] = thisdf3['AUPTrue'].rolling(10).max()  # line 95
# thisdf3['Aupfailmaybemaybe'] = thisdf3.apply(lambda x: x['Aupfailmaybe'] < 10 and x['wasaup'] == False and x['Aupfailmaybe'] > 0, axis=1)  #just like line 88

thistimeaboveaup = False
thistimeauptrue = 1
AUPfail = []
n=0
while n < len(thisdf3):
	if thisdf3.loc[n,'timeaboveAup'] == True:
		thistimeaboveaup = True
	else:
		thistimeaboveaup = thistimeaboveaup
	if thisdf3.loc[n,'AUPTrue'] == 0 and thistimeaboveaup == True:
		thistimeauptrue  = 0
	else:
		thistimeauptrue = thistimeauptrue 
	if thistimeaboveaup == True and thistimeauptrue == 0:
		AUPfail.append(True)
	else:
		AUPfail.append(False)
	n +=1

wasaupfaildf = pd.DataFrame({'wasaupfail':AUPfail})
thisdf3 = pd.merge(thisdf3,wasaupfaildf, how='left',left_index=True,right_index=True)


thistimebelowadwn = False
thistimeadwntrue = 1
ADWNfail = []
n=0
while n < len(thisdf3):
	if thisdf3.loc[n,'timebelowAdwn'] == True:
		thistimebelowadwn = True
	else:
		thistimebelowadwn = thistimebelowadwn
	if thisdf3.loc[n,'ADWNTrue'] == 0 and thistimebelowadwn == True:
		tthistimeadwntrue  = 0
	else:
		thistimeadwntrue = thistimeadwntrue 
	if thistimebelowadwn == True and thistimeadwntrue == 0:
		ADWNfail.append(True)
	else:
		ADWNfail.append(False)
	n +=1

wasadwnfaildf = pd.DataFrame({'wasadwnfail':ADWNfail})
thisdf3 = pd.merge(thisdf3,wasadwnfaildf, how='left',left_index=True,right_index=True)

thistimeabovecup = False
thistimecuptrue = 1
CUPfail = []
n=0
while n < len(thisdf3):
	if thisdf3.loc[n,'timeaboveCup'] == True:
		thistimeabovecup = True
	else:
		thistimeabovecup = thistimeabovecup
	if thisdf3.loc[n,'CUPTrue'] == 0 and thistimeabovecup == True:
		thistimecuptrue  = 0
	else:
		thistimecuptrue = thistimecuptrue 
	if thistimeabovecup == True and thistimecuptrue == 0:
		CUPfail.append(True)
	else:
		CUPfail.append(False)
	n +=1

wascupfaildf = pd.DataFrame({'wascupfail':CUPfail})
thisdf3 = pd.merge(thisdf3,wascupfaildf, how='left',left_index=True,right_index=True)

thistimebelowcdwn = False
thistimecdwntrue = 1
CDWNfail = []
n=0
while n < len(thisdf3):
	if thisdf3.loc[n,'timebelowCdwn'] == True:
		thistimebelowcdwn = True
	else:
		thistimebelowcdwn = thistimebelowcdwn
	if thisdf3.loc[n,'CDWNTrue'] == 0 and thistimebelowcdwn == True:
		thistimecdwntrue  = 0
	else:
		thistimecdwntrue = thistimecdwntrue 
	if thistimebelowcdwn == True and thistimecdwntrue == 0:
		CDWNfail.append(True)
	else:
		CDWNfail.append(False)
	n +=1

wascdwnfaildf = pd.DataFrame({'wascudwnfail':CDWNfail})
thisdf3 = pd.merge(thisdf3,wascdwnfaildf, how='left',left_index=True,right_index=True)

# "'bool' object has no attribute 'cumsum'", 'occurred at index 0')
# thisdf3['Aupfail'] = thisdf3.apply(lambda x: x['Aupfailmaybemaybe'].cumsum() > 20 and x['wasaup'] == False, axis=1) 
# # end of day 


thisdf3['EODoverAup'] = thisdf3.apply(lambda x: x['price'] >= Aup, axis=1)  #just like left_indexe 88
thisdf3['EODbelowAdwn'] = thisdf3.apply(lambda x: x['price'] <= Adwn, axis=1)  #just like line 88
thisdf3['EODbetweenOR'] = thisdf3.apply(lambda x: x['price'] <= openrangelow and x['price'] <= openrangehigh, axis=1)  #just like line 88
thisdf3['EODbelowAup'] = thisdf3.apply(lambda x: x['price'] < Aup, axis=1)  #just like line 88
thisdf3['EODaboveAdwn'] = thisdf3.apply(lambda x: x['price'] > Adwn, axis=1)  #just like line 88

wascupdf = pd.DataFrame({'wascup':output})
thisdf3 = pd.merge(thisdf3,wascupdf, how='left',left_index=True,right_index=True)


EODoverAup = thisdf3.iloc[-1].EODoverAup
EODbelowAdwn = thisdf3.iloc[-1].EODbelowAdwn
EODbetweenOR = thisdf3.iloc[-1].EODbetweenOR
EODbelowAup = thisdf3.iloc[-1].EODbelowAup
EODaboveAdwn = thisdf3.iloc[-1].EODaboveAdwn
EODAUPTrue = thisdf3.iloc[-1].AUPTrue
EODCUPTrue = thisdf3.iloc[-1].CUPTrue
EODADWNTrue = thisdf3.iloc[-1].ADWNTrue
EODCDWNTrue = thisdf3.iloc[-1].CDWNTrue

ACDMacro =[]
if EODAUPTrue and EODoverAup:
	ACDMacro=2
elif EODADWNTrue and EODbelowAdwn:
	ACDMacro =-2
elif EODAUPTrue and EODbetweenOR:
	ACDMacro=0
elif EODADWNTrue and EODbetweenOR:
	ACDMacro =-0
elif EODADWNTrue and EODoverAup and EODCUPTrue:
	ACDMacro =4
elif EODAUPTrue and EODunderAdwn and EODCDWNTrue:
	ACDMacro =-4
elif EODADWNTrue and EODbetweenOR  and EODCUPTrue:
	ACDMacro =0
elif EODAUPTrue and EODbetweenOR and EODCDWNTrue:
	ACDMacro =0


#print(ACDMacro)

outputtocsv = thisdf3[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','timebelowAdwn','price','profitpos','avgvolume','wasaup','CDWNTrue','CDWNTrueTrue','wascdwn',\
 'CUPTrue','CUPTrueTrue','wascup','wasaupfail','wasadwnfail','wascupfail','wascudwnfail']].copy()
outputtocsv.to_csv('C:/Python37/ACD/output.csv')
#if wasAup == True and w

# next create wasdwndf, then can figure out the C's and the EOD positions --

# 'ADWNTrue', 'ADWNTrueTrue', 'AUPTrue', 'AUPTrueTrue', 'adjprice',
#        'avgvolume', 'maxprice', 'minprice', 'price', 'profitneg', 'profitpos',
#        'relativeprice', 'relativevolume', 'timeaboveAup', 'timebelowAdwn',
#        'volume', 'wasadwn', 'wasdwn'],


	# 	if thisdf['wasAup'].shift(-1) == True:
	# 		wasAup == True
	# 	elif thisdf['AUPTrue'] == 10:
	# 		wasAup== True
	# return wasAup




#output = thisdf2[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','timebelowAdwn','price','profitpos','avgvolume','wasaup']].copy()
#print(thisdf[['AUPTrue','timeaboveAup','AUPTrue','AUPTrueTrue','price','profitpos','avgvolume']].copy())


#outputtocsv.to_csv('C:/Python37/ACD/output.csv')
#print(thisdf.wasAup)
#weighted by opening volume




#print(volumedf)
