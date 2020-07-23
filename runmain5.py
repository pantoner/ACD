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
from main3 import Ui_MainWindow
import pandas as pd
import pickle
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
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
		config.yesterday = self.dateEditYesterday.date().year();config.yesterday = self.dateEditYesterday.date().month();config.yesterday = self.dateEditYesterday.date().day()
		config.today = self.dateEditToday.date().year();config.today = self.dateEditToday.date().month();config.today = self.dateEditToday.date().day()
		config.start = self.dateEditStart.date().year();config.start = self.dateEditStart.date().month();config.start = self.dateEditStart.date().day()
		config.symbol = self.lineEditSymbol.text()
		self.checkBoxToday.stateChanged.connect(self.CalendarHide)

		
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
		#self.retrievemacrothread = retrievemacroThread()
 
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


	def getACD(self):
		self.resetcolor()
		if os.path.exists("yesterday.p"):
			os.remove("yesterday.p")

		if os.path.exists("today.p"):
			os.remove("today.p")

		if os.path.exists("thirtydays.p"):
			os.remove("thirtydays.p")

		symbol = str(self.lineEditSymbol.text())

		self.labelSymbol.setOpenExternalLinks(True);
		theurl = f"http://www.earningswhispers.com/tradeview/{symbol}"
		#theurl = f"https://stockcharts.com/h-sc/ui?s={symbol}"
		print(theurl)
		self.labelSymbol.setText(f"<a href= {theurl} >{symbol} Link</a>");
		

		yesterdayyear = str(self.dateEditYesterday.date().year())
		yesterdaymonth = str(self.dateEditYesterday.date().month()).zfill(2)
		yesterdayday = str(self.dateEditYesterday.date().day()).zfill(2)
		yesterdaydict = dict({'symbol': symbol, 'year': yesterdayyear, 'month': yesterdaymonth, "day" :yesterdayday })
		pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )

		todayyear = str(self.dateEditToday.date().year())
		todaymonth = str(self.dateEditToday.date().month()).zfill(2)
		todayday = str(self.dateEditToday.date().day()).zfill(2)
		todaydict = dict({'symbol': symbol, 'year': todayyear, 'month': todaymonth, "day" :todayday })
		pickle.dump( todaydict, open( "today.p", "wb" ) )

		startyear = str(self.dateEditStart.date().year())
		startmonth = str(self.dateEditStart.date().month()).zfill(2)
		startday = str(self.dateEditStart.date().day()).zfill(2)
		startdict = dict({'symbol': symbol, 'year': startyear, 'month': startmonth, "day" :startday })
		pickle.dump( startdict, open( "start.p", "wb" ) )

		client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
		# yesterdaysdate = "2020-07-09"  7/22/2020
		# todaysdate = '2020-07-10'  7/22/2020
		yesterday = pickle.load( open( "yesterday.p", "rb" ) )
		today = pickle.load( open( "today.p", "rb" ) )
		start = pickle.load( open( "start.p", "rb" ) )

		symbolname = str(yesterday['symbol'])
		yesterday = str(yesterday['year']+"-"+yesterday['month']+"-"+yesterday['day'])
		today = str(today['year']+"-"+today['month']+"-"+today['day'])
		start = str(start['year']+"-"+start['month']+"-"+start['day'])
		try:
			df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
				fmt='csv',
				frequency='20Min',
				startDate= today,
				endDate='12-30-2020')))
			openrangehigh = round(df.iloc[0, 2],2)
			openrangelow = round(df.iloc[0, 3],2)
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
				startDate= yesterday,
				endDate='12-30-2020')))
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
		tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
			fmt='csv',
			frequency='daily',
			startDate= start,
			endDate='12-30-2020')))


		try:
			drange = tdf.high - tdf.low
			Avalue = drange.values.mean()/4
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
				endDate='12-30-2020')))
			nowclose = round(df.iloc[-1, 1],2)
			nowopen = round(df.iloc[-1, 4],2)
			nowhigh = round(df.iloc[-1,2],2)
			nowlow = round(df.iloc[-1,3],2)
			nowrange = str(round((nowclose + nowlow + nowhigh)/3,2))
			relativevolume = str(round(volume.getlastvolume(df),3))
			self.lineEdit10mintdypivot.setText(nowrange)
			print(f"open range high {openrangehigh} open range low {openrangelow}")
			self.lineEditLastClose.setText(str(nowclose))
			self.lineEditRelativeVolume.setText(relativevolume)
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
				self.lineEditAup.setStyleSheet("color: rgb(0, 0, 0);")

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
		symboldf.to_sql('symbols', conn, if_exists='append')
		#pickle.dump( yesterdaydict, open( "yesterday.p", "wb" ) )
		self.labelSymbolAccepted.setText(str("Complete"))
		self.lineEditAddSymbol.clear()
		self.lineEditNotes.clear()
		self.labelSymbolAccepted.setStyleSheet("color: rgb(0, 170, 127);")
		self.load_initial_data()


	def createmacro(self):
		self.getmacrothread.start()
		self.pushButtonCreateMacro.setStyleSheet("color: rgb(0, 170, 127);")

	def retrievemacro(self):
		# self.retrievemacrothread.start()
		self.pushButtonRetrieveMacro.setStyleSheet("color: rgb(0, 170, 127);")
		conn = sqlite3.connect("macroACD2.db")
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
			newdf = df.loc[df.symbol == symbol]
			macro9 = newdf.macroACD.cumsum()
			lastmacro = macro9.iloc[-1]
			firstmacro =  macro9.iloc[0]
			if lastmacro >=5:
				newdf['threeday'] = newdf['macroACD'].rolling(10).sum()
				plt.plot(newdf.threeday)
				plt.ylabel(newdf.index)
				plt.title((symbol, lastmacro, firstmacro), fontsize=16)
				plt.show()
	
	def retrieveoneplot(self):
		try:
			conn = sqlite3.connect("macroACD2.db")
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
		# client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})
		# conn2 = sqlite3.connect("macroACD2.db")
		# # today = pd.datetime.today()
		# # year = today.year; month = today.month; day =today.day
		# # today= str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
		# n=31
		
		# macroACD =[]
		# while n > 0:
		# 	#try:
		# 	#thisstartdate = self.getthedate(n)
		# 	today = pd.datetime.today()
		# 	thirtydays = today - BDay(n)
		# 	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		# 	thisstartdate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)
			
		# 	#thirtydaysback = self.getthedate(n + 31)
		# 	today = pd.datetime.today()
		# 	thirtydays = today - BDay(n +31)
		# 	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		# 	thirtydaysback = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		# 	#thirtydayenddate = self.getthedate(n +1)
		# 	today = pd.datetime.today()
		# 	thirtydays = today - BDay(n +1)
		# 	year = thirtydays.year; month = thirtydays.month; day =thirtydays.day
		# 	thirtydayenddate = str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		# 	today = pd.datetime.today()
		# 	year = today.year; month = today.month; day =today.day
		# 	today= str(year) + "-"+ str(month).zfill(2) + "-" + str(day).zfill(2)

		# 	df = pd.read_csv(StringIO(client.get_ticker_price(symbolname,
		# 		fmt='csv',
		# 		frequency='1min',
		# 		startDate= thisstartdate,
		# 		endDate=thisstartdate)))

		# 	tdf = pd.read_csv(StringIO(client.get_ticker_price(symbolname,   # if empty dataframe you can add one and start over
		# 		fmt='csv',
		# 		frequency='daily',
		# 		startDate= thirtydaysback ,
		# 		endDate= thirtydayenddate)))
		# 	try:
		# 		macroACD.append(acdmacrofunction.acdmacro(tdf,df))
		# 	except:
		# 		 n-=1
		# 		 continue
		# 	n-=1
		# print(symbolname)
		# print(macroACD)
		# outputdf = pd.DataFrame({'symbol':symbolname,'date':thirtydaysback,'macroACD':macroACD,"thisdate":today})
		# outputdf.to_sql('macro', conn2, if_exists='append')
		self.pushButtonMacroCreate.setEnabled(False)

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
	
	# def getplot():
	# 	conn = sqlite3.connect("macroACD.db")
	# 	df = pd.read_sql_query("SELECT * from macro", conn)
	# 	df = df.drop_duplicates()
	# 	output =  df.groupby(['symbol'])[['macroACD']].sum()
	# 	output = output.sort_values('macroACD',ascending = False)
	# 	#print(output)

	# 	# symbol = 'QDEL'

	# 	df = pd.read_sql_query("SELECT * from macro", conn)
	# 	df = df.drop_duplicates()
	# 	df = df.reindex()
	# 	symbols = list(set(df.symbol.values))

	# 	print(symbols)

	# 	for symbol in symbols:
	# 		newdf = df.loc[df.symbol == symbol]
	# 		macro9 = newdf.macroACD.cumsum()
	# 		lastmacro = macro9.iloc[-1]
	# 		firstmacro =  macro9.iloc[0]
	# 		if lastmacro >=5:
	# 			newdf['threeday'] = newdf['macroACD'].rolling(10).sum()
	# 			plt.plot(newdf.threeday)
	# 			plt.ylabel(newdf.index)
	# 			plt.title((symbol, lastmacro, firstmacro), fontsize=16)
	# 			plt.show()



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
			print("not ready yet")

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