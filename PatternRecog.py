import WebCrawler as wcr
import DataFactory as dfy
import RecognitionEngine as rce
import merge2Excel as exl
import time

###day interval with 1 year range
# url = 'https://query1.finance.yahoo.com/v8/finance/chart/UVXY?region=US&lang=en-US&includePrePost=false&interval=1d&range=1y&corsDomain=finance.yahoo.com&.tsrc=finance'

##5 mins interval with 1 day range
## url = 'https://query1.finance.yahoo.com/v8/finance/chart/UVXY?region=US&lang=en-US&includePrePost=false&interval=5m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'


#symbollist_url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


wc = wcr.WebCrawler()

##get the list of symbols from wikipedia, we will implement this function later;
##symbollist_html = wc.url_open(symbollist_url)

# debug by some specific symbol:
indiceslist = ['S&P500']

#indiceslist = ['S&P500', 'RussellMidCap', 'Russell2000']

##read the list of symbol from local file:
for eachindex in indiceslist:
    print('>>>>>>>>>>start processing ' + eachindex + '<<<<<<<<<<')
    f = open('C:\\MyProjects\\PatternRecog\\' + eachindex + '.md')
    symbolList = f.read().split(sep='|')


    for each in symbolList:

        print('processing ' + each)
        symboldata_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + each + '?&region=US&lang=en-US&includePrePost=false&interval=1d&range=2y&corsDomain=finance.yahoo.com'
        df = dfy.DataFactory()
        df.json_digest(wc.url_open(symboldata_url))
        if df.open_price != 0:
            re = rce.RecognitionEngine()
            re.timespansChecker(eachindex, each, df.open_price, df.close_price, df.high_price, df.low_price)

        time.sleep(2)

print('done with patter recognition jobs, start merging today data into excel')

mergexl = exl.merge2Excel()

merg_indiceslist = ['S&P500']
# merg_indiceslist = ['S&P500', 'RussellMidCap', 'Russell2000']

listtype = ['_HighAlert']
# listtype = ['_HighAlert', '_WatchList']

for each in merg_indiceslist:
    for lt in listtype:
        mergexl.merge2ExcelWorker(each, lt)

print('all done!!!')

# todo:


#for debug
'''
#symboldata_url = 'https://query1.finance.yahoo.com/v8/finance/chart/UVXY?region=US&lang=en-US&includePrePost=false&interval=1d&range=1y&corsDomain=finance.yahoo.com&.tsrc=finance'

each = 'bf-b'
symboldata_url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + each + '?region=US&lang=en-US&includePrePost=false&interval=1d&range=2y&corsDomain=finance.yahoo.com&.tsrc=finance'

df = dfy.DataFactory()
df.json_digest(wc.url_open(symboldata_url))
#print(df.datetime_format)
#'2018-06-07T09:30:00', '2018-06-08T09:30:00'
#print(df.high_price)
#54.650001525878906
#print(df.timestamps)
#1528378200, 1528464600
#print(df.high_price[3]-df.high_price[0]
re = rce.RecognitionEngine()
re.timespansChecker('UVXY', df.open_price, df.close_price, df.high_price, df.low_price)
print(df.high_price.__len__())
print(df.timestamps.__len__())
'''

