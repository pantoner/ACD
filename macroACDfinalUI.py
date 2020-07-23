import pandas as pd
import pickle
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt

# this gets the plot for those over 5

def getplot():
	conn = sqlite3.connect("macroACD.db")
	df = pd.read_sql_query("SELECT * from macro", conn)
	df = df.drop_duplicates()
	output =  df.groupby(['symbol'])[['macroACD']].sum()
	output = output.sort_values('macroACD',ascending = False)
	#print(output)

	# symbol = 'QDEL'

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




# plt.plot(df.threeday)
# plt.ylabel(df.index)
# plt.title(symbol, fontsize=16)
# plt.show()
# # plt.plot(df.threeday)
# # plt.ylabel(df.index)
# # plt.show()

# fig = plt.figure()

# plt.subplot(2,2,1)
# plt.plot(df.threeday)
# plt.ylabel(df.index)
# plt.title(symbol, fontsize=16)

# plt.subplot(2,2,2)
# plt.plot(df.threeday)
# plt.ylabel(df.index)
# plt.title(symbol, fontsize=16)

# plt.show()