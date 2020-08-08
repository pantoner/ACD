import pandas as pd
import json
import sqlite3
import re

row1 = ['F','978','879','0','','','','','','','','','','','','','','','','','','']
row2 = ['1','','','','','','','','','','','','','','','','','','','','','']
row3 = ['Symbol','Name','Last','Change','%Chg','High','Low','Volume','Notes','Time','','','','','','','','','','','','']
row4 = ['120','180','80','68','68','80','80','64','120','54','','','','','','','','','','','','']
row5 = ['#Indices','','Main','','','','','','','','','','','','','','','','','','','']
row6 = ['CARG',	'Cargurus','1','Main','0.01','CARG','0','CARG', '31.8','1.1','30.7','30.2','30.93','31','31.91','30.39','3283700','0','200806','21:57:21','qv','-0.111']
df = pd.DataFrame(data={"col1": row1, "col2": row2,  "col3": row3, "col4": row4, "col5": row5, "col6": row6 }).T

symbollist = []
conn = sqlite3.connect("alertsymbols.db")

df1 = pd.read_sql_query("SELECT * from symbols", conn)
df1 = df1.drop_duplicates()
df1 = df1.reindex()  
symbollist = df1.symbol.values                                

nextdict =[]
for symbol in symbollist:
	thisdict = {0: symbol,1:"",2:"1",3:'Main',4:'0.01',5:symbol,6:"0",7:symbol,8:"",9:"",10:"",11:"",12:"",13:"",14:"",15:"",16:"",17:"",18:"",19:"",20:"",21:""}
	nextdict.append(thisdict)
nextdf = pd.DataFrame(nextdict)
df3 = df.append(nextdf).reset_index(drop=True)
df3.to_csv("./QUOTES.COL", sep=',',index=False,header=False)
print('complete')