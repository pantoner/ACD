import os
import ctypes
from operator import itemgetter
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import QMessageBox
from io import StringIO
from tiingo import TiingoClient
from main8 import Ui_MainWindow
import pandas as pd
import pickle
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.widgets import Button
from pandas.tseries.offsets import BDay
from contextlib import suppress
# import algos
# import paramind
# import tickersymbols
# import getcloudmultithread
# import getcloudsinglethread	
# from directoryloading import *
# from indicatorformulas import *
# import mybucketfunctions
# import getaggregate
import getACD
import newACDminus42
import newACDplus52
import check5up
import check4dwn3
import getalertsLong
import getalertsdwn5plus
import getalertsBulkowski
import getMacroDaily
import acdmacrofunction
import createonemacro
import testimport
import saveoutput
#import getminalertdata
#import macroACDfinalUI
import volume
import config


#pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
#ftp.nasdaqtrader.com/symboldirectory
class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		self.show()


		# self.lineEditStockDir.setText(getdailypath())
		# self.lineEditStockWeekly.setText(getweeklypath())
		# self.lineEditStockCloudDaily.setText(getclouddailypath())
		# self.lineEditStockCloudWeekly.setText(getcloudweeklypath())
		# self.lineEditIndDaily.setText(getinddailypath())
		# self.lineEditIndWeekly.setText(getindweeklypath())
		# self.lineEditStockDirConfigbyStock.setText(getindbucketall())
		# self.lineEditStockDirConfigbyStockEach.setText(getindbucketeach())

		# if os.path.exists("dateset_daily"):
		# 	dateset_daily = pickle.load( open( "{}.p".format("dateset_daily"), "rb" ) )
		# dateset_daily = [0,0]
		# if os.path.exists("dateset_weekly"):
		# 	dateset_weekly = pickle.load( open( "{}.p".format("dateset_weekly"), "rb" ) )
		# dateset_weekly = [0,0]
		# self.lineEditCreateLatest.setText(str(len(dateset_daily)))
		# self.lineEditCreateLatest_2.setText(str(len(dateset_weekly)))

		#self.dailydownloadthread = DailyDownLoadThread()
		#self.weeklydownloadthread = WeeklyDownLoadThread()
		# config.yesterday = self.dateEditYesterday.date().year();config.yesterday = self.dateEditYesterday.date().month();config.yesterday = self.dateEditYesterday.date().day()
		# config.today = self.dateEditToday.date().year();config.today = self.dateEditToday.date().month();config.today = self.dateEditToday.date().day()
		# config.start = self.dateEditStart.date().year();config.start = self.dateEditStart.date().month();config.start = self.dateEditStart.date().day()
		# config.symbol = self.lineEditSymbol.text()
		# self.checkBoxToday.stateChanged.connect(self.CalendarHide)

		
		#self.radioButtonWeekly_2.clicked.connect(self.resetindicators)
		# self.cloudthread = cloudThread()
		# self.indicatorthread = indicatorThread()
		# self.datesetthread = datesetThread()
		# self.resultsthread = resultsThread()
		# self.bucketsthread = bucketsThread()
		# self.aggregatethread = aggregateThread()
		# self.aggregateachthread = aggregateachThread()
		self.acdthread = acdThread()
		self.minus4thread = minus4Thread()
		self.plus5thread = plus5Thread()
		self.auplongthread = auplongThread()
		self.adwnshortthread = adwnshortThread()
		self.aplusalertsthread = aplusalertsThread()
		self.bulkowskialertsthread = bulkowskialertsThread()
		self.getmacrothread  = getmacroThread()
		self.createonemacrothread = createonemacroThread()
		self.getminalertdatathread = getminalertdataThread()
		#self.retrievemacrothread = retrievemacroThread()
		self.comboBox.currentIndexChanged.connect(self.changeText)
		# if os.path.exists("historylist.p"):
		# 	os.remove("historylist.p")
		# historylist = ['SPY']
		# pickle.dump( historylist, open( "historylist.p", "wb" ) )
	
	def changeText(self,index):
		self.lineEditSymbol.setText(self.comboBox.itemText(index))

	def addbidask(self):
		try:
			df = pd.read_csv('companies_latest.csv')
			print(df.columns)
			symbol = str(self.lineEditSymbol.text())
			thisdata = df[df[' Ticker (Sector)'] == symbol]
			bidask = thisdata[' BidaskScore'].values[0]
			self.lineEditBidAsk.setText(bidask)
			if bidask == 'Strongly Bought':
				self.lineEditBidAsk.setStyleSheet("color: rgb(51, 102, 0);")
			elif bidask == "Bought":
				self.lineEditBidAsk.setStyleSheet("color: rgb(76, 153, 0);")
			elif bidask == "Held":
				self.lineEditBidAsk.setStyleSheet("color: rgb(51, 255, 255);")
			elif bidask == "Sold":
				self.lineEditBidAsk.setStyleSheet("color: rgb(255, 51, 51);")
			elif bidask == "Strongly Sold":
				self.lineEditBidAsk.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				self.lineEditBidAsk.setStyleSheet("color: rgb(0, 0, 0);")
		except:
				self.lineEditBidAsk.setText("None")
				self.lineEditBidAsk.setStyleSheet("color: rgb(0, 0, 0);")

	def addalertline(self,failure,top,now,symbol):

		fig2 = plt.figure(constrained_layout=True)
		fig2.canvas.set_window_title(symbol)
		spec2 = gridspec.GridSpec(ncols=1, nrows=5, figure=fig2)
		f2_ax1 = fig2.add_subplot(spec2[0, 0])
		f2_ax2 = fig2.add_subplot(spec2[1, 0])
		f2_ax3 = fig2.add_subplot(spec2[2, 0])
		f2_ax4 = fig2.add_subplot(spec2[3, 0])
		f2_ax5 = fig2.add_subplot(spec2[4, 0])


		f2_ax1.get_xaxis().set_ticks([])
		f2_ax1.get_yaxis().set_ticks([])
		f2_ax2.get_xaxis().set_ticks([])
		f2_ax2.get_yaxis().set_ticks([])
		f2_ax3.get_xaxis().set_ticks([])
		f2_ax3.get_yaxis().set_ticks([])
		f2_ax4.get_xaxis().set_ticks([])
		f2_ax4.get_yaxis().set_ticks([])
		f2_ax5.get_xaxis().set_ticks([])
		f2_ax5.get_yaxis().set_ticks([])

		if failure == 1:
			f2_ax1.axhline(y=0.25, color='r', linestyle='-')
			f2_ax1.axhline(y=0.5, color='r', linestyle='-')
			f2_ax1.axhline(y=1, color='r', linestyle='-')
			f2_ax1.axhline(y=0.75, color='r', linestyle='-')

		if failure == 5:
			f2_ax5.axhline(y=0.25, color='r', linestyle='-')
			f2_ax5.axhline(y=0.5, color='r', linestyle='-')
			f2_ax5.axhline(y=1, color='r', linestyle='-')
			f2_ax5.axhline(y=0.75, color='r', linestyle='-')

		if failure == 6:
			f2_ax5.axhline(y=0.25, color='r', linestyle='-')
			f2_ax5.axhline(y=0.5, color='r', linestyle='-')
			f2_ax5.axhline(y=1, color='r', linestyle='-')
			f2_ax5.axhline(y=0.75, color='r', linestyle='-')

			f2_ax1.axhline(y=0.25, color='r', linestyle='-')
			f2_ax1.axhline(y=0.5, color='r', linestyle='-')
			f2_ax1.axhline(y=1, color='r', linestyle='-')
			f2_ax1.axhline(y=0.75, color='r', linestyle='-')

		if top == 'aup':
			f2_ax1.set_facecolor('lightgreen')
		if top == 'cup':
			f2_ax1.set_facecolor('lightblue')
		if top == 'adwn':
			f2_ax5.set_facecolor('lightgreen')
		if top == 'cdwn':
			f2_ax5.set_facecolor('lightblue')

		if top == 'cupadwn':
			f2_ax1.set_facecolor('lightblue')
			f2_ax5.set_facecolor('lightgreen')
		if top == 'cdwnaup':
			f2_ax5.set_facecolor('lightblue')
			f2_ax1.set_facecolor('lightgreen')

		if now == 1:
			f2_ax1.set_facecolor('green')
		if now == 2:
			f2_ax2.set_facecolor('green')
		if now == 3:
			f2_ax3.set_facecolor('green')
		if now == 4:
			f2_ax4.set_facecolor('green')
		if now == 5:
			f2_ax5.set_facecolor('green')
		if now == 6:
			f2_ax1.set_facecolor('blue')
		if now == 7:
			f2_ax5.set_facecolor('blue')
		plt.show()

	def getthisplot(self):
		symbol = str(self.lineEditSymbol.text())
		conn3 = sqlite3.connect("alerts.db")
		conn3.isolation_level = None
		for i in range(5):
			try:
				df= pd.read_sql_query("select * from alert;", conn3)
				thisdf = df[df.symbol == symbol]

				fail = 0
				if thisdf.Aupfail.all() == True:
					fail = 1
				elif thisdf.Adwnfail.all() == True:
					fail = 5
				elif thisdf.Cdwnfail.all() == True:
					fail = 5
				elif thisdf.Cupfail.all() == True:
					fail = 1
				elif thisdf.Aupfail.all() + thisdf.Adwnfail.all() + thisdf.Cupfail.all() + thisdf.Cdwnfail.all() == 2:
					fail = 6

				top = 0
				if thisdf.wasaup.all() == True:
					top = 'aup'
				elif thisdf.wasadwn.all() == True:
					top = 'adwn'
				elif thisdf.wascup.all() == True:
					top = 'cdwn'
				elif thisdf.wascdwn.all() == True:
					top = 'cdwn'
				elif thisdf.wascup.all() == True and thisdf.wasadwn.all() == True:
					top = 'cupadwn'
				elif thisdf.wascdwn.all() == True and thisdf.wasaup.all() == True:
					top = 'cdwnaup'
				elif thisdf.wascup.all() == True and thisdf.wasaup.all() == True:
					top = 'cup'
				elif thisdf.wascdwn.all() == True and thisdf.wasadwn.all() == True:
					top = 'cdwn'

				now = 0

				if thisdf.overaup.all() == True:
					now = 1
				elif thisdf.abovetopOR.all() == True:
					now = 2
				elif thisdf.betweenOR.all() == True:
					now = 3
				elif thisdf.belowbottomOR.all() == True:
					now = 4
				elif thisdf.belowadwn.all() == True:
					now = 5
				elif thisdf.belowadwn.all() == True and thisdf.wascdwn.all() == True:
					now = 7
				elif thisdf.overaup.all() == True and thisdf.wascup.all() == True:
					now = 6
			except:
				ctypes.windll.user32.MessageBoxW(0, str(symbol), "Try again later...  this data is being gathered for a fresh outlook!", 1)
				continue


		# failure = 0
		# top = 'cdwnaup'
		# now = 7
		print(symbol)

			#alertsMap.addalertline(fail,top,now,symbol)
		self.addalertline(fail,top,now,symbol)

	def highup(self):
		self.lineEditAup.setStyleSheet("color: rgb(255, 255, 0);")
		self.lineEditOpenRangeLow.setStyleSheet("color:rgb(85, 0, 255);")
		if pivottop > nowclose:
			self.lineEditPivotRangeTop.setStyleSheet("color: rgb(255, 0 ,0);")
		elif pivottop < nowclose:
			self.lineEditPivotRangeTop.setStyleSheet("color:rgb(85, 0, 255);")
	
	def resetcolor(self):
		self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
		self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
		self.lineEditPivotRangeTop.setStyleSheet("color: rgb(0, 0, 0);")
		self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
		self.pushButtonAddAlert.setStyleSheet("color: rgb(0, 0, 0);")

	def getevents(self):
		conn2 = sqlite3.connect("thissymbolsevents.db")
		cur2 = conn2.cursor()
		query = 'DROP TABLE IF EXISTS events'
		cur2.execute(query)

		symbol = str(self.lineEditSymbol.text())
		conn = sqlite3.connect("todaysevents.db")
		df= pd.read_sql_query("select * from aup;", conn)
		df = df.loc[df['symbol'] ==symbol]
		n =0
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2))})('aup','timeofaup' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1

		df= pd.read_sql_query("select * from adwn;", conn)
		df = df.loc[df['symbol'] ==symbol]
		
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2) )})('adwn','timeofadwn' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1


		df= pd.read_sql_query("select * from adwnfail;", conn)
		df = df.loc[df['symbol'] ==symbol]
	
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2) )})('adwnfail','timeofadwnfail' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1

		df= pd.read_sql_query("select * from aupfail;", conn)
		df = df.loc[df['symbol'] ==symbol]
	
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2) )})('aupfail','timeofaupfail' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1
		
		df= pd.read_sql_query("select * from cup;", conn)
		df = df.loc[df['symbol'] ==symbol]
		
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2))})('cup','timeofcup' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1

		df= pd.read_sql_query("select * from cdwn;", conn)
		df = df.loc[df['symbol'] ==symbol]
	
		if not df.empty:
			thisdict = (lambda x, y:{'event':[x],'thistime':df[y].values[0][11:14] + df[y].values[0][14:16],'relativevolume':str(round(df['relativevolume'].values[0],2) )})('cdwn','timeofcdwn' )
			thisdf = pd.DataFrame(thisdict)
			thisdf.to_sql('events', conn2, if_exists='append')
			n+=1



			# thistime = df['timeofaup'].values[0]
			# hour = thistime[11:14]
			# minutes = thistime[14:16]
			# thisauptime = hour+minutes
			# thisdict = {'event':'aup','thistime': [thisauptime]}
		self.load_event_data()
		if n ==0:
			self.tableWidgetEvent.setRowCount(0);
		


	def getACD(self):
		try:
			self.getevents()
		except:
			pass
		self.resetcolor()
		self.getalleventsnow()

		if os.path.exists("yesterday.p"):
			os.remove("yesterday.p")

		if os.path.exists("today.p"):
			os.remove("today.p")

		if os.path.exists("thirtydays.p"):
			os.remove("thirtydays.p")

		symbol = str(self.lineEditSymbol.text())
		# historylist = pickle.load( open( "historylist.p", "rb" ) )
		# historylist.append(symbol)
		# historylist2 = list(set(historylist))
		# pickle.dump( historylist2, open( "historylist.p", "wb" ) )

		self.addbidask()
		self.comboBox.addItem(symbol) 

		self.labelSymbol.setOpenExternalLinks(True);
		theurl = f"http://www.earningswhispers.com/tradeview/{symbol}"
		#theurl = f"https://stockcharts.com/h-sc/ui?s={symbol}"
		print(theurl)
		self.labelSymbol.setText(f"<a href= {theurl} >{symbol} Link</a>");

		self.labelTodayDate.setOpenExternalLinks(True);
		theurl2 = f"https://www.barchart.com/stocks/quotes/{symbol}/interactive-chart"
		#theurl = f"https://stockcharts.com/h-sc/ui?s={symbol}"
		print(theurl2)
		self.labelTodayDate.setText(f"<a href= {theurl2} >{symbol} Chart</a>");


		# yesterdayyear = str(self.dateEditYesterday.date().year())
		# yesterdaymonth = str(self.dateEditYesterday.date().month()).zfill(2)
		# yesterdayday = str(self.dateEditYesterday.date().day()).zfill(2)
		# yesterdaydict = dict({'symbol': symbol, 'year': yesterdayyear, 'month': yesterdaymonth, "day" :yesterdayday })
		# pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )

		# todayyear = str(self.dateEditToday.date().year())
		# todaymonth = str(self.dateEditToday.date().month()).zfill(2)
		# todayday = str(self.dateEditToday.date().day()).zfill(2)
		# todaydict = dict({'symbol': symbol, 'year': todayyear, 'month': todaymonth, "day" :todayday })
		# pickle.dump( todaydict, open( "today.p", "wb" ) )

		#new today
		today = pd.datetime.today()
		year = today.year; month = today.month; day =today.day
		today = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		# startyear = str(self.dateEditStart.date().year())
		# startmonth = str(self.dateEditStart.date().month()).zfill(2)
		# startday = str(self.dateEditStart.date().day()).zfill(2)
		# startdict = dict({'symbol': symbol, 'year': startyear, 'month': startmonth, "day" :startday })
		# pickle.dump( startdict, open( "start.p", "wb" ) )

		client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
		# yesterdaysdate = "2020-07-09"  7/22/2020
		# todaysdate = '2020-07-10'  7/22/2020
		# yesterday = pickle.load( open( "yesterday.p", "rb" ) )
		# today = pickle.load( open( "today.p", "rb" ) )
		# start = pickle.load( open( "start.p", "rb" ) )

		thistoday = pd.datetime.today()
		thirtydays = thistoday - BDay(31)
		year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		startdate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		thistoday = pd.datetime.today()
		thirtydays = thistoday - BDay(1)
		year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		enddate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		symbolname = str(self.lineEditSymbol.text())
		
		# yesterday = str(yesterday['year']+"-"+yesterday['month']+"-"+yesterday['day'])
		# today = str(today['year']+"-"+today['month']+"-"+today['day'])
		# start = str(start['year']+"-"+start['month']+"-"+start['day'])
		
		try:
			df = pd.read_csv(StringIO(client.get_ticker_price(symbol,
				fmt='csv',
				frequency='1min',
				startDate= today,
				endDate=today)))

			df['highprice'] = df['high'].cummax()
			df['lowprice'] = df['low'].cummin()
			openrangelow = df.loc[19,'lowprice']
			openrangehigh = df.loc[19,'highprice']
			
			print(f"open range high {openrangehigh} open range low {openrangelow}")
			self.lineEditOpenRangeHigh.setText(str(openrangehigh))
			self.lineEditOpenRangeLow.setText(str(openrangelow))
		except:
			self.lineEditOpenRangeHigh.setText(str("not time yet"))
			self.lineEditOpenRangeLow.setText(str("not time yet"))

		 #get pivot from yesterday
		try:
			ydf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='daily',
				startDate= enddate,
				endDate=enddate)))
			pivothigh = ydf.iloc[0, 2]
			pivotlow = ydf.iloc[0, 3]
			pivotclose = ydf.iloc[0, 1]
			print(pivothigh)
			print(pivotlow)
			print(pivotclose)
			dailypivotnumber = (pivotclose + pivotlow + pivothigh)/3
			dailypivotdifferential = ((pivotlow + pivothigh)/2)  -  dailypivotnumber
			print(f"this is the daily pivot number {dailypivotnumber}, this is the daily pivot differential {abs(dailypivotdifferential)}")
			self.lineEditDailyPivotNumber.setText(str(round(dailypivotnumber,2)))
			print(f" The top pivot range is {dailypivotnumber  + abs(dailypivotdifferential)} , bottom pivot range {dailypivotnumber  - abs(dailypivotdifferential)}")
			pivottop = round(dailypivotnumber  + abs(dailypivotdifferential),2)
			pivotbottom = round(dailypivotnumber  - abs(dailypivotdifferential),2)
			self.lineEditPivotRangeTop.setText(str(pivottop))
			self.lineEditPivotRangeBottom.setText(str(pivotbottom))
			if pivotclose > dailypivotnumber  - abs(dailypivotdifferential):
				print("Bullish tone")
				self.lineEditTone.setText("Bullish")
				self.lineEditTone.setStyleSheet("color: rgb(0, 170, 127);")
			elif pivotclose < dailypivotnumber  - abs(dailypivotdifferential):
				print("Bearish tone")
				self.lineEditTone.setText("Bearish")
				self.lineEditTone.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				print("Neutral tone")
				self.lineEditTone.setText("Neutral")
				self.lineEditTone.setStyleSheet("color: rgb(0, 0, 0);")
		except:
			self.lineEditDailyPivotNumber.setText(str("Not Ready"))
			self.lineEditPivotRangeTop.setText(str("Not Ready"))
			self.lineEditPivotRangeBottom.setText(str("Not Ready"))
			self.lineEditTone.setText("Not Ready")
			#get 30 days back
		# tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
		# 	fmt='csv',
		# 	frequency='daily',
		# 	startDate= startdate,
		# 	endDate=enddate)))


		try:
			tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
			fmt='csv',
			frequency='daily',
			startDate= startdate,
			endDate=enddate)))
			drange = tdf.high - tdf.low
			Avalue = drange.values.mean()/5
			Aup = round(openrangehigh + Avalue,2)
			Adwn = round(openrangelow - Avalue,2)
			momentum1 = tdf.iloc[-1,1] - tdf.iloc[-9,1]
			momentumyesterday2 = tdf.iloc[-2,1] - tdf.iloc[-10,1] 
			momentumyesterday3 = tdf.iloc[-3,1] - tdf.iloc[-11,1] 
			print(momentumyesterday2)

			momentum2 = float(round(momentum1,2))
			self.lineEditMomentum.setText(str(momentum2))
			if momentum2 > 0:
				self.lineEditMomentum.setStyleSheet("color: rgb(0, 170, 127);")
			elif momentum2 < 0:
				self.lineEditMomentum.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				self.lineEditMomentum.setStyleSheet("color: rgb(0, 0, 0);")

			momentumyesterday2 = float(round(momentumyesterday2,2))
			self.lineEditMomentumYesterday2.setText(str(momentumyesterday2))
			if momentumyesterday2 > 0:
				self.lineEditMomentumYesterday2.setStyleSheet("color: rgb(0, 170, 127);")
			elif momentumyesterday2 < 0:
				self.lineEditMomentumYesterday2.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				self.llineEditMomentumYesterday2.setStyleSheet("color: rgb(0, 0, 0);")

			momentumyesterday3 = float(round(momentumyesterday3,2))
			self.lineEditMomentumYesterday3.setText(str(momentumyesterday3))
			if momentumyesterday3 > 0:
				self.lineEditMomentumYesterday3.setStyleSheet("color: rgb(0, 170, 127);")
			elif momentumyesterday3 < 0:
				self.lineEditMomentumYesterday3.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				self.lineEditMomentumYesterday3.setStyleSheet("color: rgb(0, 0, 0);")	

			print(f" Top A value {Aup} , bottom A value {Adwn}")
			self.lineEditAup.setText(str(Aup))
			self.lineEditAdwn.setText(str(Adwn))
		except:
			self.lineEditAup.setText(str("not ready yet"))
			self.lineEditAdwn.setText(str("not ready yet"))
#want to add the last 10 minute close to this99
		try:
			df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='1Min',
				startDate= today,
				endDate=today)))
			nowclose = round(df.iloc[-1, 1],2)
			nowopen = round(df.iloc[-1, 4],2)
			nowhigh = round(df.iloc[-1,2],2)
			nowlow = round(df.iloc[-1,3],2)
			nowrange = str(round((nowclose + nowlow + nowhigh)/3,2))
			
			self.lineEdit10mintdypivot.setText(nowrange)
			print(f"open range high {openrangehigh} open range low {openrangelow}")
			self.lineEditLastClose.setText(str(nowclose))
			relativevolume = round(volume.getlastvolume(df),3)
			
			if relativevolume >= 1.0:
				self.lineEditRelativeVolume.setStyleSheet("color: rgb(0, 170, 127);")
			if relativevolume < 1.0:
				self.lineEditRelativeVolume.setStyleSheet("color: rgb(255, 0, 0);")

			self.lineEditRelativeVolume.setText(str(relativevolume))
			
			self.lineEditLastOpen.setText(str(nowopen))

			if float(nowrange) > Aup:
				self.lineEdit10mintdypivot.setStyleSheet("color: rgb(0, 170, 127);")
			elif float(nowrange) < Adwn:
				self.lineEdit10mintdypivot.setStyleSheet("color: rgb(255, 0, 0);")
			else:
				self.lineEdit10mintdypivot.setStyleSheet("color: rgb(0, 0, 0);")
				
			if nowclose > Aup and nowopen > Aup and pivottop < Aup and pivottop > openrangelow: 
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(85, 0, 255);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
			elif nowclose > Aup and nowopen > Aup and pivottop < Aup and pivottop < openrangelow:
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(85, 0, 255);")
			elif nowclose > Aup and nowopen > Aup and pivottop > nowclose and pivottop > nowopen:
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(255, 255, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")


			elif nowclose < Adwn and nowopen < Adwn and pivotbottom < Adwn and pivotbottom < openrangehigh: 
				self.lineEditLastClose.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(85, 0, 255);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
			elif nowclose < Adwn and nowopen < Adwn and pivotbottom < Adwn and pivotbottom > openrangehigh: 
				self.lineEditLastClose.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(85, 0, 255);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
			elif nowclose < Adwn and nowopen < Adwn and pivotbottom  < nowclose and pivottbottom < nowopen:
				self.lineEditLastClose.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(255, 255, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")

		
			elif nowopen > Aup and nowclose < Aup:
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
			elif nowopen < Adwn and nowclose > Adwn:
				self.lineEditLastOpen.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
			elif nowopen < Aup and nowclose > Aup:
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
			elif nowopen > Adwn and nowclose < Adwn:
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditLastClose.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
			elif nowopen < Adwn and nowclose < Adwn:
				self.lineEditLastClose.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(255, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(85, 0, 255);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")

			elif nowclose > Aup and nowopen > Aup: 
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(0, 170, 127);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(85, 0, 255);")
			else:
				self.lineEditLastOpen.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditLastClose.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditOpenRangeLow.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeTop.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditOpenRangeHigh.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditPivotRangeBottom.setStyleSheet("color:rgb(0, 0, 0);")
				self.lineEditAdwn.setStyleSheet("color: rgb(0, 0, 0);")
				self.lineEditAup.setStyleSheet("color: rgb(85, 0, 255);")
				self.lineEdit10mintdypivot.setStyleSheet("color:rgb(85, 0, 255);")

		except:
			self.lineEditLastClose.setText(str("not time yet"))
			self.lineEditLastOpen.setText(str("not time yet"))


		self.acdthread.start()

	def getminus4(self):
		self.minus4thread.start()
		self.pushButtonACDgetshorts.setStyleSheet("color: rgb(0, 170, 127);")

	def getplus5(self):
		self.plus5thread.start()
		self.pushButtonACDgetlongs.setStyleSheet("color: rgb(0, 170, 127);")

	def getauplong(self):
		self.auplongthread.start()
		self.pushButtonAuplongs.setStyleSheet("color: rgb(0, 170, 127);")

	def getadwnshorts(self):
		self.adwnshortthread.start()
		self.pushButtonAdwnshorts.setStyleSheet("color: rgb(0, 170, 127);")

	def getaplusalerts(self):
		self.aplusalertsthread.start()
		self.pushButtonAplusAlerts.setStyleSheet("color: rgb(0, 170, 127);")

	def getbulkowskialerts(self):
		self.bulkowskialertsthread.start()
		self.pushButtonBulkowskiAlerts.setStyleSheet("color: rgb(0, 170, 127);")

	def getminalertdata(self):
		self.getminalertdatathread.start()
		self.pushButtongetminalertdata.setStyleSheet("color: rgb(0, 170, 127);")

	def load_initial_data(self):
		# where c is the cursor
		self.tableWidget.setRowCount(0)
		conn = sqlite3.connect("symbollistdb.db")
		cur = conn.cursor()
		query = 'SELECT * FROM symbols'
		cur.execute(query)
		rows = cur.fetchall()
		
		for row in rows:
			inx = rows.index(row)
			self.tableWidget.insertRow(inx)
			# add more if there is more columns in the database.
			self.tableWidget.setItem(inx, 0, QTableWidgetItem(row[1]))
			self.tableWidget.setItem(inx, 1, QTableWidgetItem(row[2]))
			self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))

	def load_event_data(self):
		# where c is the cursor
		self.tableWidgetEvent.setRowCount(0)
		conn = sqlite3.connect("thissymbolsevents.db")
		cur = conn.cursor()
		query = 'SELECT * FROM events'
		cur.execute(query)
		rows = cur.fetchall()
		print(rows)
		
		for row in rows:
			inx = rows.index(row)
			self.tableWidgetEvent.insertRow(inx)
			# add more if there is more columns in the database.
			self.tableWidgetEvent.setItem(inx, 0, QTableWidgetItem(row[1]))
			self.tableWidgetEvent.setItem(inx, 1, QTableWidgetItem(row[2]))
			self.tableWidgetEvent.setItem(inx, 2, QTableWidgetItem(row[3]))
			#self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))


	def addsymbols(self):
		thissymbol = str(self.lineEditAddSymbol.text())
		thisnotes = str(self.lineEditNotes.text())
		self.dateEditDeleteDate
		deleteyear = str(self.dateEditDeleteDate.date().year())
		deletemonth = str(self.dateEditDeleteDate.date().month()).zfill(2)
		deleteday = str(self.dateEditDeleteDate.date().day()).zfill(2)
		deletedict = dict({ 'year': deleteyear , 'month': deletemonth, "day" :deleteday})
		deletedaystr = str(deletedict['year']+"-"+deletedict['month']+"-"+deletedict['day'])
		symbollistdict = dict({'symbol': [thissymbol],'notes':thisnotes,'deleteday':deletedaystr})
		symboldf = pd.DataFrame(symbollistdict)
		conn = sqlite3.connect("symbollistdb.db")
		#indexquery = 'CREATE UNIQUE INDEX index_symbol__on_symbols ON symbols(symbol);'
		#pd.read_sql_query(indexquery, conn)
		try:
			symboldf.to_sql('symbols', conn, if_exists='append')
			#pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )
			self.labelSymbolAccepted.setText(str("Complete"))
			self.lineEditAddSymbol.clear()
			self.lineEditNotes.clear()
			self.labelSymbolAccepted.setStyleSheet("color: rgb(0, 170, 127);")
			self.load_initial_data()
		except:
			print('not today')
			ctypes.windll.user32.MessageBoxW(0, str(symbol), "Is already in the database, I saved you a double entry!!", 1)

	def addalertsymbol(self):
		thissymbol = str(self.lineEditSymbol.text())
		symbollistdict = dict({'symbol': [thissymbol]})
		symboldf = pd.DataFrame(symbollistdict)
		conn = sqlite3.connect("alertsymbols.db")
		#cur = conn.cursor()

		# indexquery = 'CREATE UNIQUE INDEX index_symbol__on_symbols ON symbols(symbol);'
		# pd.read_sql_query(indexquery, conn)
		try:
			symboldf.to_sql('symbols', conn, if_exists='append')
		# cur.execute('INSERT OR REPLACE INTO symbols  VALUES(%?,%?)',(0,thissymbol)
			self.pushButtonAddAlert.setStyleSheet("color: rgb(0, 170, 127);")
			print(f"{thissymbol} has been added to alertsymbols")
		except:
			print('not today')
			ctypes.windll.user32.MessageBoxW(0, str(symboldf.symbol), "Is already in the database, I saved you a double entry!!", 1)

		# except :
		# 	ctypes.windll.user32.MessageBoxW(0, "There was an unaccounted for problem!!", 1)
		# 	self.pushButtonAddAlert.setStyleSheet("color: rgb(0, 170, 127);")

		#pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )
		# self.pushButtonAddAlert.setStyleSheet("color: rgb(0, 170, 127);")
		# print(f"{thissymbol} has been added to alertsymbols")


	def alertfrommacro(self):
		symbollistdict =  pickle.load( open( "alertsymbol.p", "rb" ) )
		#symbollistdict = dict({'symbol': [thissymbol]})
		symboldf = pd.DataFrame(symbollistdict)
		conn = sqlite3.connect("alertsymbols.db")
		symboldf.to_sql('symbols', conn, if_exists='append')
		#pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )
		#self.pushButtonAddAlert.setStyleSheet("color: rgb(0, 170, 127);")
		#print(f"{symbol} has been added to alertsymbols")
		print('added symbol to alerts')

	def createmacro(self):
		self.getmacrothread.start()
		self.pushButtonCreateMacro.setStyleSheet("color: rgb(0, 170, 127);")

	def retrievemacro(self):
		# self.retrievemacrothread.start()
		self.pushButtonRetrieveMacro.setStyleSheet("color: rgb(0, 170, 127);")
		conn = sqlite3.connect("macroACD.db")
		df = pd.read_sql_query("SELECT * from macro", conn)
		df = df.drop_duplicates()
		output =  df.groupby(['symbol'])[['macroACD']].sum()
		output = output.sort_values('macroACD',ascending = False)
		df = pd.read_sql_query("SELECT * from macro", conn)
		df = df.drop_duplicates()
		df = df.reindex()
		symbols = list(set(df.symbol.values))
		print(symbols)

		for symbol in symbols:
			conn = sqlite3.connect("alertsymbols.db")
			pickle.dump( {'symbol':[symbol]}, open( "alertsymbol.p", "wb" ) )
			newdf = df.loc[df.symbol == symbol]
			macro9 = newdf.macroACD.cumsum()
			lastmacro = macro9.iloc[-1]
			firstmacro =  macro9.iloc[0]
			plottitle = symbol+" "+ str(lastmacro)+" "+str(firstmacro)
			if lastmacro >=5:
				newdf['threeday'] = newdf['macroACD'].rolling(10).sum()
				fig = plt.figure()
				ax = fig.add_subplot()
				ax.plot(newdf.threeday)
				#ax.ylabel(newdf.index)
				axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
				alertb = Button(axnext,'Alert')
				#(lambda x: pd.DataFrame(dict({'symbol': [x]})).to_sql('symbols', conn, if_exists='append'))(symbol)
				alertb.on_clicked(self.alertfrommacro())
				ax.set_title(plottitle)
				plt.show()
	
	def retrieveoneplot(self):
		try:
			conn = sqlite3.connect("macroACD.db")
			df = pd.read_sql_query("SELECT * from macro", conn)
			df = df.drop_duplicates()
			df = df.reindex()
			symbol = str(self.lineEditSymbol.text())
			newdf = df.loc[df.symbol == symbol]
			macro9 = newdf.macroACD.cumsum()
			print(macro9)
			lastmacro = macro9.iloc[-1]
			firstmacro =  macro9.iloc[0]
			#if lastmacro >=5:
			newdf['threeday'] = newdf['macroACD'].rolling(10).sum()
			plt.plot(newdf.threeday)	
			plt.ylabel(newdf.index)
			plt.title((symbol, lastmacro, firstmacro), fontsize=16)
			plt.show()
		except:
			self.pushButtonMacroCreate.setEnabled(True)
			ctypes.windll.user32.MessageBoxW(0, str(symbol), "No ACD Macro for this symbol; PRESS MACRO BUTTON TO CREATE", 1)


	def getonemacro(self):
		symbolname = str(self.lineEditSymbol.text())
		symboldict = dict({'symbol': symbolname })
		pickle.dump( symboldict , open( "symboldictnow.p", "wb" ) )
		self.pushButtonMacroCreate.setStyleSheet("color: rgb(0, 170, 127);")
		self.createonemacrothread.start()   # create thread 
		self.pushButtonMacroCreate.setEnabled(False)

	def getalleventsnow(self):
		tablenamelist = ['aup','adwn','adwnfail','aupfail','cup','cdwn','cupfail','cdwnfail']
		timeofauplist = ['timeofaup','timeofadwn','timeofadwnfail','timeofaupfail','timeofcup','timeofcdwn','timeofcupfail''timeofcdwnfail']
		listoflist = []
		for tablename,timeofaup in zip(tablenamelist,timeofauplist):
			thelist = testimport.geteachlabel(tablename,timeofaup)
			listoflist.append(thelist)
		print(listoflist)
		saveoutput.savepickle(listoflist)
		with suppress(IndexError):self.commandLinkButtonAddAlertAup1.setText(listoflist[0][0])
		with suppress(IndexError):self.commandLinkButtonAddAlertAup2.setText(listoflist[0][1])
		with suppress(IndexError):self.commandLinkButtonAddAlertAup3.setText(listoflist[0][2])
		with suppress(IndexError):self.commandLinkButtonAddAlertAup4.setText(listoflist[0][3])
		with suppress(IndexError):self.commandLinkButtonAddAlertAup5.setText(listoflist[0][4])
		with suppress(IndexError):self.commandLinkButtonAddAlertAup6.setText(listoflist[0][5])

		with suppress(IndexError): self.commandLinkButtonAddAlertCup1.setText(listoflist[4][0])
		with suppress(IndexError): self.commandLinkButtonAddAlertCup2.setText(listoflist[4][1])
		with suppress(IndexError): self.commandLinkButtonAddAlertCup3.setText(listoflist[4][2])

		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn1.setText(listoflist[1][0])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn2.setText(listoflist[1][1])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn3.setText(listoflist[1][2])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn4.setText(listoflist[1][3])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn5.setText(listoflist[1][4])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwn6.setText(listoflist[1][5])

		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail1.setText(listoflist[2][0])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail2.setText(listoflist[2][1])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail3.setText(listoflist[2][2])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail4.setText(listoflist[2][3])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail5.setText(listoflist[2][4])
		with suppress(IndexError):self.commandLinkButtonAddAlertAdwnfail6.setText(listoflist[2][5])

		with suppress(IndexError): self.commandLinkButtonAddAlertCdwn1.setText(listoflist[5][0])
		with suppress(IndexError): self.commandLinkButtonAddAlertCdwn2.setText(listoflist[5][1])
		with suppress(IndexError): self.commandLinkButtonAddAlertCdwn3.setText(listoflist[5][2])

		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail1.setText(listoflist[3][0])
		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail2.setText(listoflist[3][1])
		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail3.setText(listoflist[3][2])
		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail4.setText(listoflist[3][3])
		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail5.setText(listoflist[3][4])
		with suppress(IndexError):self.commandLinkButtonAddAlertAupfail6.setText(listoflist[3][5])

	def aup1(self):
		thissymbol1 = pickle.load( open( "pfiles/aup1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def aup2(self):
		thissymbol2 = pickle.load( open( "pfiles/aup2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def aup3(self):
		thissymbol3 = pickle.load( open( "pfiles/aup3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)
	def aup4(self):
		thissymbol4 = pickle.load( open( "pfiles/aup4.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol4)
	def aup5(self):
		thissymbol5 = pickle.load( open( "pfiles/aup5.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol5)
	def aup6(self):
		thissymbol6 = pickle.load( open( "pfiles/aup6.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol6)
	
	def cup1(self):
		thissymbol1 = pickle.load( open( "pfiles/cup1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def cup2(self):
		thissymbol2 = pickle.load( open( "pfiles/cup2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def cup3(self):
		thissymbol3 = pickle.load( open( "pfiles/cup3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)

	def adwn1(self):
		thissymbol1 = pickle.load( open( "pfiles/adwn1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def adwn2(self):
		thissymbol2 = pickle.load( open( "pfiles/adwn2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def adwn3(self):
		thissymbol3 = pickle.load( open( "pfiles/adwn3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)
	def adwn4(self):
		thissymbol4 = pickle.load( open( "pfiles/adwn4.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol4)
	def adwn5(self):
		thissymbol5 = pickle.load( open( "pfiles/adwn5.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol5)
	def adwn6(self):
		thissymbol6 = pickle.load( open( "pfiles/adwn6.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol6)

	def adwnfail1(self):
		thissymbol1 = pickle.load( open( "pfiles/adwnfail1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def adwnfail2(self):
		thissymbol2 = pickle.load( open( "pfiles/adwnfail2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def adwnfail3(self):
		thissymbol3 = pickle.load( open( "pfiles/adwnfail3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)
	def adwnfail4(self):
		thissymbol4 = pickle.load( open( "pfiles/adwnfail4.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol4)
	def adwnfail5(self):
		thissymbol5 = pickle.load( open( "pfiles/adwnfail5.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol5)
	def adwnfail6(self):
		thissymbol6 = pickle.load( open( "pfiles/adwnfail6.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol6)

	def cdwn1(self):
		thissymbol1 = pickle.load( open( "pfiles/cdwn1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def cdwn2(self):
		thissymbol2 = pickle.load( open( "pfiles/cdwn2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def cdwn3(self):
		thissymbol3 = pickle.load( open( "pfiles/cdwn3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)

	def aupfail1(self):
		thissymbol1 = pickle.load( open( "pfiles/aupfail1.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol1)
	def aupfail2(self):
		thissymbol2 = pickle.load( open( "pfiles/aupfail2.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol2)
	def aupfail3(self):
		thissymbol3 = pickle.load( open( "pfiles/aupfail3.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol3)
	def aupfail4(self):
		thissymbol4 = pickle.load( open( "pfiles/aupfail4.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol4)
	def aupfail5(self):
		thissymbol5 = pickle.load( open( "pfiles/aupfail5.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol5)
	def aupfail6(self):
		thissymbol6 = pickle.load( open( "pfiles/aupfail6.p", "rb" ) )
		self.lineEditSymbol.setText(thissymbol6)

	def getallsymbols(self):
		config.startyear = self.dateEditStart.date().year();config.startmonth = self.dateEditStart.date().month();config.startday = self.dateEditStart.date().day()
		config.endyear = self.dateEditEnd.date().year();config.endmonth = self.dateEditEnd.date().month();config.endday = self.dateEditEnd.date().day()
		if self.radioButtonDaily.isChecked():
			if os.path.exists("dailystock.p"):
				directory = pickle.load( open( "dailystock.p", "rb" ) )
				path = directory['daily']
				#print(path)
				config.rawstockdatapath = path
			else:
				print('no daily path configured')
			self.pushButtonStop.setEnabled(True);self.pushButtonTickers.setEnabled(False)
			self.dailydownloadthread.start()
		if self.radioButtonWeekly.isChecked():
			if os.path.exists("weeklystock.p"):
				directory = pickle.load( open( "weeklystock.p", "rb" ) )
				path = directory['weekly']
				#print(path)
			else:
				print('no weekly path configured')
			config.rawstockdatapath = path			
			self.dateEditStart.setEnabled(False);self.dateEditEnd.setEnabled(False);self.checkBoxToday.setEnabled(False)
			self.pushButtonStop.setEnabled(True);self.pushButtonTickers.setEnabled(False)
			self.weeklydownloadthread.start()


	def resetindicators(self):
		#self.daysback = self.lineEditCreateLatest.text()
		if os.path.exists("indicators.p"):
			os.remove("indicators.p")
		self.daily = True if self.radioButtonDaily_2.isChecked() else False
		self.weekly = True if self.radioButtonWeekly_2.isChecked() else False
		self.cloud = True if self.checkBoxCloud.isChecked() else False
		self.rsi = True if self.checkBoxRSI.isChecked() else False
		self.bb = True if self.checkBoxBBPercent.isChecked() else False
		self.alld = True if self.radioButtonIndDownloadAll.isChecked() else False
		self.latest = True if self.radioButtonDownloadLatest.isChecked() else False
		self.indicators = dict({'CLOUD': self.cloud,'RSI':self.rsi,'BB':self.bb,'ALL':self.alld,'LATEST':self.latest,'DAILY':self.daily,'WEEKLY':self.weekly})
		pickle.dump(self.indicators, open( "indicators.p", "wb" ) )

	def getindicators(self):
		#self.pushButtonStopIndicators.setEnabled(True)  #not ready with code for stop
		#self.pushButtonGetIndicator.setEnabled(False)
		#self.daysback = self.lineEditCreateLatest.text()
		if os.path.exists("indicators.p"):
			os.remove("indicators.p")
		self.daily = True if self.radioButtonDaily_2.isChecked() else False
		self.weekly = True if self.radioButtonWeekly_2.isChecked() else False
		self.cloud = True if self.checkBoxCloud.isChecked() else False
		self.rsi = True if self.checkBoxRSI.isChecked() else False
		self.bb = True if self.checkBoxBBPercent.isChecked() else False
		self.alld = True if self.radioButtonIndDownloadAll.isChecked() else False
		self.latest = True if self.radioButtonDownloadLatest.isChecked() else False

		self.indicators = dict({'CLOUD': self.cloud,'RSI':self.rsi,'BB':self.bb,'ALL':self.alld,'LATEST':self.latest,'DAILY':self.daily,'WEEKLY':self.weekly})
		#print(self.indicators)
		pickle.dump(self.indicators, open( "indicators.p", "wb" ) )
		self.cloudthread.start()

	def getresults(self):
		if os.path.exists("algobuttons.p"):
			os.remove("algobuttons.p")
		self.daily = True if self.radioButtonDailyBucket.isChecked() else False
		self.weekly = True if self.radioButtonWeeklyBucket.isChecked() else False
		self.spinday  = self.spinBox.text();config.days = self.spinday 
		self.algobuttons = dict({'DAILY':self.daily,'WEEKLY':self.weekly, 'DAYS':self.spinday})
		pickle.dump(self.algobuttons, open( "algobuttons.p", "wb" ) )
		self.resultsthread.start()
	
	def getbuckets(self):
		if os.path.exists("algobuttons.p"):
			os.remove("algobuttons.p")
		self.justtoday = True if self.checkBoxTodayOnly.isChecked() else False 
		self.daily = True if self.radioButtonDailyBucket.isChecked() else False
		self.weekly = True if self.radioButtonWeeklyBucket.isChecked() else False
		self.spinday  = self.spinBox.text();config.days = self.spinday 
		self.algobuttons = dict({'DAILY':self.daily,'WEEKLY':self.weekly, 'DAYS':self.spinday, 'JUST':self.justtoday})
		pickle.dump(self.algobuttons, open( "algobuttons.p", "wb" ) )
		self.bucketsthread.start()


	def picklethis(self,endyear,endmonth,endday):
		if os.path.exists("enddate.p"):
			os.remove("enddate.p")
		if endyear:
			hmtwsl = dict({'endyear': endyear, 'endmonth': endmonth, 'endday': endday})
			pickle.dump( hmtwsl, open( "enddate.p", "wb" ) )

	def stopdailydownload(self):  #stops daily or weekly data
		QMessageBox.about(self, "See Data", "Press to Wait for Data!")
		self.pushButtonStop.setEnabled(False)
		self.pushButtonTickers.setEnabled(True)
		self.dateEditStart.setEnabled(True)
		self.dateEditEnd.setEnabled(True)
		self.checkBoxToday.setEnabled(True)
		self.dailydownloadthread.stopdailydownload()
		

	def CalendarHide(self, state):
		if self.checkBoxToday.isChecked(): 
			self.dateEditToday.setEnabled(False)
			endyear = datetime.today().strftime('%Y')
			endmonth = datetime.today().strftime('%m')
			endday = datetime.today().strftime('%d')
			#self.picklethis(endyear,endmonth,endday)
		else: 
			self.dateEditToday.setEnabled(True)


	def browseforstockdir(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("dailystock.p"):
			os.remove("dailystock.p")
		if fileName:
			directory = dict({'daily': fileName})
			pickle.dump(directory, open( "dailystock.p", "wb" ) )
			#print(fileName)
			config.rawstockdatapath = fileName
			self.lineEditStockDir.setText(fileName)

	def browseweeklyrawstock(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("weeklystock.p"):
			os.remove("weeklystock.p")
		if fileName:
			directory = dict({'weekly': fileName})
			pickle.dump(directory, open( "weeklystock.p", "wb" ) )
			#print(fileName)
			config.weeklyrawstockdatapath = fileName
			self.lineEditStockWeekly.setText(fileName)

	def browsedailycloud(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("clouddaily.p"):
			os.remove("clouddaily.p")
		if fileName:
			directory = dict({'daily': fileName})
			pickle.dump(directory, open( "clouddaily.p", "wb" ) )
			#print(fileName)
			config.dailycloud = fileName
			self.lineEditStockCloudDaily.setText(fileName)

	def browseweeklycloud(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("cloudweekly.p"):
			os.remove("cloudweekly.p")
		if fileName:
			directory = dict({'weekly': fileName})
			pickle.dump(directory, open( "cloudweekly.p", "wb" ) )
			#print(fileName)
			config.weeklycloud = fileName
			self.lineEditStockCloudWeekly.setText(fileName)

	def browseinddailydir(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("inddaily.p"):
			os.remove("inddaily.p")
		if fileName:
			directory = dict({'daily': fileName})
			pickle.dump(directory, open( "inddaily.p", "wb" ) )
			#print(fileName)
			config.inddaily = fileName
			self.lineEditIndDaily.setText(fileName)

	def browseindweekly(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("indweekly.p"):
			os.remove("indweekly.p")
		if fileName:
			directory = dict({'weekly': fileName})
			pickle.dump(directory, open( "indweekly.p", "wb" ) )
			#print(fileName)
			config.indweekly = fileName
			self.lineEditIndWeekly.setText(fileName)

	def browsebucketbystock(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Database Files (*.db)", options=options)
		fileName = os.path.basename(fileName)
		if os.path.exists("bucketybystock.p"):
			os.remove("bucketbystock.p")
		if fileName:
			directory = dict({'daily': fileName})
			pickle.dump(directory, open( "bucketbystock.p", "wb" ) )
			#print(fileName)
			config.bucketfilename = fileName
			self.lineEditStockDirConfigbyStock.setText(fileName)

	def browsebucketbystockeach(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Pickle Files (*.p)", options=options)
		fileName1 = os.path.basename(fileName)
		dirName = os.path.dirname(fileName)
		print(dirName);print(fileName1)
		if os.path.exists("bucketybystockeach.p"):
			os.remove("bucketbystockeach.p")
		if fileName:
			directory1 = dict({'daily': dirName+"/" +fileName1})
			pickle.dump(directory1, open( "bucketbystockeach.p", "wb" ) )
			#print(fileName)
			config.bucketfilenametoday = fileName1
			self.lineEditStockDirConfigbyStockEach.setText(fileName1)


	def indicatorsbyday(self):
		self.resetindicators()
		self.indicatorthread.start()

	def getdateset(self):
		self.resetindicators()
		self.datesetthread.start()

	def vieweachconfig(self):

		#good code for getting the choice of mulitple radio buttons. 
		buttongroupdict ={}
		newdict={}
		dailyview = buttongroupdict.update({'dailyview':True}) if self.radioButtonViewStockDaily.isChecked() else {'dailyview':False}
		weeklyview = buttongroupdict.update({'weeklyview':True}) if self.radioButtonViewStockWeekly.isChecked() else {'weeklyview':False}
		clouddailyview = buttongroupdict.update({'clouddaily':True}) if self.radioButtonViewCloudDaily.isChecked() else {'clouddailyview':False}
		cloudweeklyview = buttongroupdict.update({'cloudweekly':True}) if self.radioButtonViewCloudWeekly.isChecked() else {'cloudweekly':False}
		inddailyview = buttongroupdict.update({'inddaily':True}) if self.radioButtonViewIndDaily.isChecked() else {'indview':False}
		indweeklyview = buttongroupdict.update({'indweekly':True}) if self.radioButtonViewIndWeekly.isChecked() else {'indweekly':False}
		
		for key, value in buttongroupdict.items():
			if value == True:
				newdict[key] = value
		#print([*newdict][0])
		getpath(str([*newdict][0]),self.lineEditConfigViewData.text(),self.lineEditConfigViewDataDate.text())


	def getaggregateall(self):
		self.resetindicators()
		self.aggregatethread.start

	def getaggregateeach(self):
		self.resetindicators()
		self.aggregateachthread.start()



class acdThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		try:
			getACD.gethissymbol()
		except:
			print("not ready yet 11")

class minus4Thread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		newACDminus42.minus4()
		#except:
			#print("not ready yet")

class plus5Thread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		newACDplus52.plus5()               
		#except:
			#print("not ready yet")

class auplongThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		check5up.check5up()

class adwnshortThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		check4dwn3.check4dwn()


		

class aplusalertsThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		getalertsLong.fiveplusAup()
		#getalertsdwn5plus.fiveplusAdwn()



class bulkowskialertsThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		getalertsBulkowski.patternAup()
		#getalertsdwn5plus.fiveplusAdwn()

class getminalertdataThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		getminalertdata.buildminutealerts()
		#getalertsdwn5plus.fiveplusAdwn()


class getmacroThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		#try:
		getMacroDaily.getmacroall()
		#getalertsdwn5plus.fiveplusAdwn()

class createonemacroThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		createonemacro.getonemacro()

class DailyDownLoadThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		try:
			tickersymbols.getallsymbols2()
		except ValueError:
			exit()

	def stopdailydownload(self):
		tickersymbols.stopthread()

class WeeklyDownLoadThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		tickersymbols.getallsymbolsweekly()

	def stopdailydownload(self):
		tickersymbols.stopthread()

class cloudThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		indicators = pickle.load( open( "indicators.p", "rb" ) )
		if indicators['DAILY'] == True:
			if os.path.exists("dailystock.p"):
				directory = pickle.load( open( "dailystock.p", "rb" ) )
				path = directory['daily']
				config.rawstockdatapath = path
				config.indpath = getclouddailypath()

		if indicators['WEEKLY'] == True:
			if os.path.exists("weeklystock.p"):
				directory = pickle.load( open( "weeklystock.p", "rb" ) )
				path = directory['weekly']
				config.rawstockdatapath = path
				config.indpath = getcloudweeklypath()

		paramind.runallindicators()


class indicatorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		indicators = pickle.load( open( "indicators.p", "rb" ) )
		if indicators['ALL'] == True:
			algos.createdateset()
			algos.transformind()
		if indicators['LATEST'] == True:
			algos.datesetlatest()
			# dateset_daily = pickle.load( open( "{}.p".format("dateset_daily"), "rb" ) )
			# dateset_weekly = pickle.load( open( "{}.p".format("dateset_weekly"), "rb" ) )
			# self.lineEditCreateLatest.setText(str(len(dateset_daily)))
			# self.lineEditCreateLatest_2.setText(str(len(dateset_weekly)))
			algos.transformind()

class datesetThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		indicators = pickle.load( open( "indicators.p", "rb" ) )
		if indicators['ALL'] == True:
			algos.createdateset()
			dateset_daily = pickle.load( open( "{}.p".format("dateset_daily"), "rb" ) )
			dateset_weekly = pickle.load( open( "{}.p".format("dateset_weekly"), "rb" ) )
		if indicators['LATEST'] == True:
			algos.datesetlatest()
			dateset_daily = pickle.load( open( "{}.p".format("dateset_daily"), "rb" ) )
			dateset_weekly = pickle.load( open( "{}.p".format("dateset_weekly"), "rb" ) )
		#	self.lineEditCreateLatest.setText(str(len(dateset_daily)))
	#	self.lineEditCreateLatest_2.setText(str(len(dateset_weekly)))
class resultsThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		algobuttons = pickle.load( open( "algobuttons.p", "rb" ) )
		if algobuttons['DAILY'] == True:
				config.whichresults = "daily"
				config.indpath = getclouddailypath()
				mybucketfunctions.dailyresults()

		if algobuttons['WEEKLY'] == True:
			config.whichresults = "weekly"
			if os.path.exists("cloudweekly.p"):
				config.indpath = getcloudweeklypath()
				mybucketfunctions.weeklyresults()

class bucketsThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		
		algobuttons = pickle.load( open( "algobuttons.p", "rb" ) )
		if algobuttons['DAILY'] == True:
				config.whichresults = "daily"
				config.indpath = getclouddailypath()
				mybucketfunctions.startbuildingbuckets()

		if algobuttons['WEEKLY'] == True:
			config.whichresults = "weekly"
			if os.path.exists("cloudweekly.p"):
				config.indpath = getcloudweeklypath()
				mybucketfunctions.startbuildingbuckets()

class aggregateThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		getaggregate.finalaggregate()

class aggregateachThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)  

	def run(self):
		getaggregate.usetodaysrow()


	# def getlatestcloud(self):
	# 	getcloudsinglethread.getlatestcloud()

	# def stopdailydownload(self):
	# 	tickersymbols.stopthread()

#https://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix
if __name__ == '__main__':
  app = QApplication([])
  w = MainWindow()
  app.exec_()