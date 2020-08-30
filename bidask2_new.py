import pandas as pd
import sqlite3


df = pd.read_csv('watchlistimport.csv')
print(df.columns)
#thisdata = df[df[' BidaskScore'] == 'Strongly Bought']
#bidask = thisdata[' BidaskScore'].values[0]
thisdata = df.drop_duplicates()
conn = sqlite3.connect("symbollistdb.db")
n=0
while n < len(thisdata):
	thisdict ={'symbol':[thisdata['Symbol'].values[n] ],'notes':thisdata['Source'].values[n],'deleteday':'08-14-2020'}  
	thisdf = pd.DataFrame(thisdict)
	print(thisdf)
	thisdf.to_sql('symbols', conn, if_exists='append')
	n+=1

print('complete')

