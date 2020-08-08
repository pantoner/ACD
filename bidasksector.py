import pandas as pd
import sqlite3


# df = pd.read_csv('companies_latest.csv')
# print(df.columns)
# thisdata = df[df[' BidaskScore'] == 'Strongly Bought']
# #bidask = thisdata[' BidaskScore'].values[0]
# thisdata = thisdata.drop_duplicates()
conn = sqlite3.connect("BidAsk.db")
sectornumbers = pd.read_sql_query("SELECT * from BidaskClubSectors", conn)
SP500 = pd.read_sql_query("SELECT * from SP500SymbolsSectors", conn)
todaysector = pd.read_sql_query("SELECT * from sector_latest", conn)

print(sectornumbers)
print(SP500)
print(todaysector)

sc1 = pd.merge(sectornumbers,todaysector, how ='left',left_on ='Id',right_on ='Sector')
sc2 = pd.merge(SP500,sc1, how ='left',left_on ='Sector',right_on ='Sector_x')
sc2 = sc2.drop_duplicates(subset='Symbol', keep='first')
sc2 = sc2.dropna()

sc3 = pd.merge(SP500,sc1, how ='left',left_on ='SubSector',right_on ='Sector_x')
sc3 = sc3.drop_duplicates(subset='Symbol', keep='first')
sc3 = sc3.dropna()


subsectorscore2 = sc3[sc3['Symbol'] == 'AMD'].BidaskScore.values[0]
subsectorname2 =  sc3[sc3['Symbol'] == 'AMD'].Sector_x.values[0]
print(subsectorname2,subsectorscore2)

subsectorscore1 = sc2[sc2['Symbol'] == 'AMD'].BidaskScore.values[0]
subsectorname1 =  sc2[sc2['Symbol'] == 'AMD'].Sector.values[0]
print(subsectorname1,subsectorscore1)

