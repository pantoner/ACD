import pandas as pd
from pandas.tseries.offsets import BDay
from io import StringIO
from tiingo import TiingoClient
import pickle
import config
import sqlite3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def acdmacroall(tdf,df):
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
	thisdf.to_csv('seethisdata.csv')
	# output is timeofaup
	n= 0
	wasauplist=[]
	output = []
	sentinal = 0
	timeofaup = {'timeofaup':[0]}
	# def wasaupfunc(thisdf):
	while n < len(thisdf):
		if thisdf.loc[n,'AUPTrue'] >9:
			wasauplist.append(1)
			if sentinal == 0:
				sentinal +=1
				timeofaup.update({"timeofaup": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
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
	sentinal = 0
	timeofadwn = {'timeofadwn':[0]}
	# def wasaupfunc(thisdf):
	while n < len(thisdf2):
		if thisdf2.loc[n,'ADWNTrue'] >9:
			wasadwnlist.append(1)
			if sentinal == 0:
				sentinal +=1
				timeofadwn.update({"timeofadwn": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
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
	sentinal = 0
	timeofcdwn = {'timeofcdwn':[0]}

	# def wasaupfunc(thisdf):
	while n < len(thisdf3):
		if thisdf3.loc[n,'CDWNTrue'] >9:
			wascdwnlist.append(1)
			if sentinal == 0:
				sentinal +=1
				timeofcdwn.update({"timeofcdwn": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
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
	sentinal = 0
	timeofcup = {'timeofcup':[0]}
	# def wasaupfunc(thisdf):
	while n < len(thisdf3):
		if thisdf3.loc[n,'CUPTrue'] >9:
			wascuplist.append(1)
			if sentinal == 0:
				sentinal +=1
				timeofcup.update({"timeofcup": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
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
	sentinal = 0
	timeofaupfail = {'timeofaupfail':[0]}
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
			if sentinal == 0:
				sentinal +=1
				timeofaupfail.update({"timeofaupfail": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
		else:
			AUPfail.append(False)
		n +=1

	wasaupfaildf = pd.DataFrame({'wasaupfail':AUPfail})
	thisdf3 = pd.merge(thisdf3,wasaupfaildf, how='left',left_index=True,right_index=True)


	thistimebelowadwn = False
	thistimeadwntrue = 1
	ADWNfail = []
	sentinal = 0
	timeofadwnfail = {'timeofadwnfail':[0]}
	n=0
	while n < len(thisdf3):
		if thisdf3.loc[n,'timebelowAdwn'] == True:
			thistimebelowadwn = True
		else:
			thistimebelowadwn = thistimebelowadwn
		if thisdf3.loc[n,'ADWNTrue'] == 0 and thistimebelowadwn == True:
			thistimeadwntrue  = 0
		else:
			thistimeadwntrue = thistimeadwntrue 
		if thistimebelowadwn == True and thistimeadwntrue == 0:
			ADWNfail.append(True)
			if sentinal == 0:
				sentinal +=1
				timeofadwnfail.update({"timeofadwnfail": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
		else:
			ADWNfail.append(False)
		n +=1

	wasadwnfaildf = pd.DataFrame({'wasadwnfail':ADWNfail})
	thisdf3 = pd.merge(thisdf3,wasadwnfaildf, how='left',left_index=True,right_index=True)

	thistimeabovecup = False
	thistimecuptrue = 1
	CUPfail = []
	sentinal = 0
	timeofcupfail = {'timeofcupfail':[0]}
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
			if sentinal == 0:
				sentinal +=1
				timeofcupfail.update({"timeofcupfail": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
		else:
			CUPfail.append(False)
		n +=1

	wascupfaildf = pd.DataFrame({'wascupfail':CUPfail})
	thisdf3 = pd.merge(thisdf3,wascupfaildf, how='left',left_index=True,right_index=True)

	thistimebelowcdwn = False
	thistimecdwntrue = 1
	CDWNfail = []
	sentinal = 0
	timeofcdwnfail = {'timeofcdwnfail':[0]}
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
			if sentinal == 0:
				sentinal +=1
				timeofcdwnfail.update({"timeofcdwnfail": [df.loc[n,"date"]], "relativevolume": thisdf.loc[n,'avgvolume']})
		else:
			CDWNfail.append(False)
		n +=1

	wascdwnfaildf = pd.DataFrame({'wascdwnfail':CDWNfail})
	thisdf3 = pd.merge(thisdf3,wascdwnfaildf, how='left',left_index=True,right_index=True)

	# "'bool' object has no attribute 'cumsum'", 'occurred at index 0')
	# thisdf3['Aupfail'] = thisdf3.apply(lambda x: x['Aupfailmaybemaybe'].cumsum() > 20 and x['wasaup'] == False, axis=1) 
	# # end of day 



	thisdf3['EODoverAup'] = thisdf3.apply(lambda x: x['price'] >= Aup, axis=1)  #just like left_indexe 88
	thisdf3['EODbelowAdwn'] = thisdf3.apply(lambda x: x['price'] <= Adwn, axis=1)  #just like line 88
	thisdf3['EODbetweenOR'] = thisdf3.apply(lambda x: x['price'] >= openrangelow and x['price'] <= openrangehigh, axis=1)  #just like line 88
	thisdf3['EODaboveOR'] = thisdf3.apply(lambda x: x['price'] >= openrangelow and x['price'] < Aup, axis=1)  #just like line 88
	thisdf3['EODbelowOR'] = thisdf3.apply(lambda x: x['price'] <= openrangehigh and x['price'] > Adwn, axis=1)  #just like line 88
	thisdf3['EODabovetopOR'] = thisdf3.apply(lambda x: x['price'] >= openrangehigh and x['price'] < Aup, axis=1)  #just like line 88
	thisdf3['EODbelowbottomOR'] = thisdf3.apply(lambda x: x['price'] <= openrangelow and x['price'] > Adwn, axis=1)  #just like line 88

	wascupdf = pd.DataFrame({'wascup':output})
	thisdf3 = pd.merge(thisdf3,wascupdf, how='left',left_index=True,right_index=True)

	EODabovetopOR = thisdf3.iloc[-1].EODabovetopOR  # 1 result
	EODbelowbottomOR = thisdf3.iloc[-1].EODbelowbottomOR  # 2 result
	EODoverAup = thisdf3.iloc[-1].EODoverAup  # 3 result
	EODbelowAdwn = thisdf3.iloc[-1].EODbelowAdwn  # 4 result
	EODbetweenOR = thisdf3.iloc[-1].EODbetweenOR  # 5 result
	EODaboveOR = thisdf3.iloc[-1].EODaboveOR  # 6 result
	EODbelowOR = thisdf3.iloc[-1].EODbelowOR  # 7 result

	EODAUPTrue = thisdf3.iloc[-1].wasaup  #1 succss  wasaup AUPTrue
	EODCUPTrue = thisdf3.iloc[-1].wascup  #2 success wascup CUPTrue 
	EODADWNTrue = thisdf3.iloc[-1].wasadwn#3 success wasadwm  ADWNTrue
	EODCDWNTrue = thisdf3.iloc[-1].wascdwn #4 success wascdwn  CDWNTrue

	EODAUPFail = thisdf3.iloc[-1].wasaupfail #1 fail
	EODCUPFail = thisdf3.iloc[-1].wascupfail #2 fail
	EODADWNFail = thisdf3.iloc[-1].wasadwnfail #3 fail
	EODCDWNFail = thisdf3.iloc[-1].wascdwnfail # fail

	# ACDMacro =0 
	# if EODADWNTrue and EODoverAup and EODCUPTrue:
	# 	ACDMacro +=4
	# elif EODAUPTrue and EODbelowAdwn and EODCDWNTrue:
	# 	ACDMacro -=4
	# elif EODADWNTrue and EODoverAup and EODCUPTrue:
	# 	ACDMacro +=4
	# elif EODAUPTrue and EODbelowAdwn and EODCDWNTrue:
	# 	ACDMacro -=4
	# elif EODAUPTrue and EODCDWNFail and EODbetweenOR:
	# 	ACDMacro +=3
	# elif EODADWNTrue and EODCUPFail and EODbetweenOR:
	# 	ACDMacro -=3
	# elif EODADWNFail and EODAUPTrue and EODoverAup:
	# 	ACDMacro +=3
	# elif EODADWNFail and EODAUPTrue and EODabovetopOR:
	# 	ACDMacro +=3
	# elif EODAUPTrue and EODoverAup:
	# 	ACDMacro +=2
	# elif EODADWNTrue and EODbelowAdwn:
	# 	ACDMacro -=2
	# elif EODAUPTrue   and EODCDWNFail and EODabovetopOR:
	#  	ACDMacro +=2
	# elif EODADWNTrue and EODCUPFail and EODbelowbottomOR:
	# 	ACDMacro -=2
	# elif EODAUPFail and EODADWNTrue and EODbetweenOR:
	# 	ACDMacro -=1	
	# elif EODADWNFail and EODAUPTrue and EODbetweenOR:
	# 	ACDMacro +=1
	# elif EODAUPFail  and EODADWNTrue and EODbelowbottomOR:
	#  	ACDMacro -=1
	# elif EODADWNFail and EODAUPTrue and EODaboveOR:
	#  	ACDMacro +=1
	# elif EODAUPTrue and EODbetweenOR:
	# 	ACDMacro +=0
	# elif EODADWNTrue and EODbetweenOR:
	# 	ACDMacro +=0
	# elif EODADWNTrue and EODbetweenOR  and EODCUPTrue:
	# 	ACDMacro =+0
	# elif EODAUPTrue and EODbetweenOR and EODCDWNTrue:
	# 	ACDMacro +=0
	# else:
	# 	ACDMacro +=0
	#thisdate = df.iloc[n, 0]
	#print(ACDMacro)
	#return ACDMacro
	relativevolume = thisdf.iloc[-1,3] #,"volume10":volume10
	print(timeofaup)
	# aupdf = pd.DataFrame(timeofaup)
	# conn5 = sqlite3.connect("todaysevents.db")
	# if aupdf['timeofaup'].any() != 0:
	# 	aupdf = aupdf[aupdf['timeofaup']!= 0]
	# 	aupdf.to_sql('aup', conn5, if_exists='append')
	# 	print(aupdf)
	if EODCUPTrue == True & EODAUPTrue == True:
		EODAUPTrue = False
	if EODADWNTrue == True & EODCDWNTrue == True:
		EODADWNTrue = False

	thisdate = df.iloc[-1,0]
	datadict = { "date": thisdate,"wasaup":[EODAUPTrue],"wascup":EODCUPTrue,"wasadwn":EODADWNTrue,"wascdwn":EODCDWNTrue,"volume10":relativevolume, "avgopeningvolume":avgopeningvolume,\
	"Aupfail":EODAUPFail,"Cupfail":EODCUPFail,"Adwnfail":EODADWNFail,"Cdwnfail":EODCDWNFail,'betweenOR':EODbetweenOR, "belowbottomOR":EODbelowbottomOR,'abovetopOR':EODabovetopOR,\
	 "overaup":EODoverAup,"belowadwn":EODbelowAdwn,"aboveOR":EODaboveOR,"belowOR":EODbelowOR}
	#datadf = pd.DataFrame(datadict)
	return ([datadict,timeofaup,timeofadwn,timeofcdwn,timeofcup,timeofaupfail,timeofadwnfail,timeofcdwnfail,timeofcupfail])

	# EODabovetopOR = thisdf3.iloc[-1].EODabovetopOR  # 1 result
	# EODbelowbottomOR = thisdf3.iloc[-1].EODbelowbottomOR  # 2 result
	# EODoverAup = thisdf3.iloc[-1].EODoverAup  # 3 result
	# EODbelowAdwn = thisdf3.iloc[-1].EODbelowAdwn  # 4 result
	# EODbetweenOR = thisdf3.iloc[-1].EODbetweenOR  # 5 result
	# EODaboveOR = thisdf3.iloc[-1].EODaboveOR  # 6 result
	# EODbelowOR = thisdf3.iloc[-1].EODbelowOR 
