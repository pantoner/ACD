import requests
import io
import gzip
import pandas as pd
import sqlite3

resp = requests.get('https://api.bidaskclub.com/company/latest_day?key=Qxpo6FRo7tCB+RFf0aDRQqnlJw64vocjHPEehZmF7hU=&secret=r01P19fwW+ouyLI3A8WPCCj9oaBRL4aIKeEdrCFkJ5M=')
#resp = requests.get('https://api.bidaskclub.com/company/all?key=Qxpo6FRo7tCB+RFf0aDRQqnlJw64vocjHPEehZmF7hU=&secret=r01P19fwW+ouyLI3A8WPCCj9oaBRL4aIKeEdrCFkJ5M=')
try:

    srcFileName="companies_latest.csv.zip"
    with open(srcFileName, 'w') as f:
        f.write(srcFileName)
except Exception as e:
	print(e)
# def fixBadZipfile(zipFile):  
#  f = open(zipFile, 'r+b')  
#  content = zipFileContainer.read()
#  pos = content.rfind('\x50\x4b\x05\x06') # End of central directory signature  
#     if pos>0:
#         zipFileContainer.seek(pos+20) # +20: see secion V.I in 'ZIP format' link above.
#         zipFileContainer.truncate()
#         zipFileContainer.write('\x00\x00') # Zip file comment length: 0 byte length; tell zip applications to stop reading.
#         zipFileContainer.seek(0)
#     return zipFileContainer
#  else:  
#      print('error')

# fixBadZipfile(zipFile)
# zf = zipfile.ZipFile('companies_latest.csv.zip') 
# df = pd.read_csv(zf.open('companies_latest.csv'))
# print(df)

# decompressedFile = gzip.GzipFile(fileobj='companies_latest.csv.zip', mode='rb')

# with open('C:/Python37/ACD', 'w') as outfile:
#     outfile.write(decompressedFile.read())

# # print(resp.headers)
# send_file(io.BytesIO(res.content),
# attachment_filename='companies_latest.csv.zip',
# mimetype='application/zip')


    #res = requests.get('http://<rest_api_host>/v1.2/admin/logs', stream=True)
#    # return send_file(
#         io.BytesIO(res.content),
#         attachment_filename='console_log.zip',
#         mimetype='application/zip'
# # try:
#     srcFileName="filename"
#     with open(srcFileName, 'wb') as f:
#         f.write(srcFileName)
# except Exception as e:
#     print(e)
# # jData = json.loads(resp.content)
# # print("The response contains {0} properties".format(len(jData)))
# print("\n")
# for key in jData:
#     print (key + " : " + jData[key])
# else:
#   # If response code is not ok (200), print the resulting http error code with description
#     myResponse.raise_for_status()
# from requests.auth import HTTPBasicAuth
# import requests

# headers = {
#     'key': '=Qxpo6FRo7tCB+RFf0aDRQqnlJw64vocjHPEehZmF7hU=&' ,
#     'secret': '=r01P19fwW+ouyLI3A8WPCCj9oaBRL4aIKeEdrCFkJ5M='
# }
# r = requests.get('https://api.bidaskclub.com/company/latest_day?', headers=headers)

# df = pd.read_csv('companies_latest.csv')
# print(df.columns)
# thisdata = df[df[' Ticker (Sector)'] == 'AAPL']
# print(thisdata[' BidaskScore'].values[0

df = pd.read_csv('companies_latest.csv')
print(df.columns)
thisdata = df[df[' BidaskScore'] == 'Strongly Bought']
#bidask = thisdata[' BidaskScore'].values[0]
thisdata = thisdata.drop_duplicates()
conn = sqlite3.connect("symbollistdb.db")
n=0
while n < len(thisdata):
	thisdict ={'symbol':[thisdata[' Ticker (Sector)'].values[n] ],'notes':thisdata[' BidaskScore'].values[n],'deleteday':'08-07-2020'}  
	thisdf = pd.DataFrame(thisdict)
	print(thisdf)
	thisdf.to_sql('symbols', conn, if_exists='append')
	n+=1

print('complete')