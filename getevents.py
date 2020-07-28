import pandas as pd
import sqlite3
import alertsMap





conn2 = sqlite3.connect("thissymbolsevents.db")
cur2 = conn2.cursor()
query = 'DROP TABLE IF EXISTS events'
cur2.execute(query)

symbol = 'HD'
conn = sqlite3.connect("todaysevents.db")
df= pd.read_sql_query("select * from aup;", conn)
df = df[df.symbol == symbol]
if not df.empty:
	print(df)
	#thistime = df.loc[0,'timeofaup']
	thistime =df.timeofaup.items
	thistime = df['timeofaup'].values[0]
	hour = thistime[11:14]
	minutes = thistime[14:16]
	thisauptime = hour+minutes
	thisdict = {'event':'aup','thistime': [thisauptime]}
	thisdf = pd.DataFrame(thisdict)
	print(thisdf)

	thisdf.to_sql('events', conn2, if_exists='append')
	print('complete')

