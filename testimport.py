import sqlite3
import pandas as pd
conn1 = sqlite3.connect("todaysevents.db")
conn1.isolation_level = None

def getlabel(n,timeofaup,tablename):
		query = f"select * from {tablename}; "
		df= pd.read_sql_query(query, conn1)
		df = df.sort_values(by=[timeofaup],ascending=False)
		thisdict = (lambda x,  y:{'symbol':df['symbol'].values[x].ljust(5),'thistime':df[y].values[x][11:14] + df[y].values[x][14:16],'relativevolume':str(round(df['relativevolume'].values[x],2))})(n,timeofaup )
		label = thisdict['thistime'] +"_" +thisdict['symbol'] +"_"+ thisdict['relativevolume']
		return label


def geteachlabel(tablename,timeofaup):
	labelist = []
	n= 0
	while n <=5:
		try:
			label = getlabel(n,timeofaup,tablename)
			labelist.append(label)
			n+=1
		except:
			n+=1
	return labelist

tablenamelist = ['aup','adwn','adwnfail','aupfail','cup','cdwn','cupfail','cdwnfail']
timeofauplist = ['timeofaup','timeofadwn','timeofadwnfail','timeofaupfail','timeofcup','timeofcdwn','timeofcupfail''timeofcdwnfail']

listoflist = []
for tablename,timeofaup in zip(tablenamelist,timeofauplist):
	thelist = geteachlabel(tablename,timeofaup)
	listoflist.append(thelist)
print(listoflist[0])


#listoflist[0][0][6:11]
