import pandas as pd
import pickle
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

symbol = "CHGG"
conn = sqlite3.connect("macroACD2.db")
df = pd.read_sql_query("SELECT * from macro", conn)
df = df.drop_duplicates()
df = df.reindex()

newdf = df.loc[df.symbol == symbol]
macro9 = newdf.macroACD.cumsum()
print(macro9)
lastmacro = macro9.iloc[-1]
firstmacro =  macro9.iloc[0]
if lastmacro >=5:
	newdf['threeday'] = newdf['macroACD'].rolling(10).sum()
	plt.plot(newdf.threeday)
	plt.ylabel(newdf.index)
	plt.title((symbol, lastmacro, firstmacro), fontsize=16)
	plt.show()