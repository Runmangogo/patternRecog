import WebCrawler as wcr
import DataFactory as dfy
import RecognitionEngine as rce
import merge2Excel as exl
import time

class PatternRecog:
    ###day interval with 1 year range
    # url = 'https://query1.finance.yahoo.com/v8/finance/chart/UVXY?region=US&lang=en-US&includePrePost=false&interval=1d&range=1y&corsDomain=finance.yahoo.com&.tsrc=finance'

    ##5 mins interval with 1 day range
    ## url = 'https://query1.finance.yahoo.com/v8/finance/chart/UVXY?region=US&lang=en-US&includePrePost=false&interval=5m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'

    #symbollist_url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    def PatternRecogWorker(self):
        wc = wcr.WebCrawler()

        ##get the list of symbols from wikipedia, we will implement this function later;
        ##symbollist_html = wc.url_open(symbollist_url)

        # debug by some specific symbol:
        # indiceslist = ['S&P500_test']

        indiceslist = ['S&P500', 'RussellMidCap', 'Russell2000']

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
                if df.is_excepttion == 0:
                    # bug fix when today's volume is None.
                    if df.volume[-1] is not None:
                        # if df.volume[-1] < 0.3M, I dont even bother checking it:
                        if df.open_price != 0 and df.volume[-1] > 150000:
                            re = rce.RecognitionEngine()
                            re.timespansChecker(eachindex, each, df.open_price, df.close_price, df.high_price, df.low_price,
                                                df.volume[-1])

                time.sleep(2)

        print('done with patter recognition jobs, start merging data and write it to excel')


        merg_indiceslist = ['RussellMidCap', 'Russell2000']
        # merg_indiceslist = ['S&P500', 'RussellMidCap', 'Russell2000']

        listtype = ['_HighAlert']
        # listtype = ['_HighAlert', '_WatchList']

        for each in merg_indiceslist:
            for lt in listtype:
                mergexl = exl.merge2Excel()
                mergexl.merge2ExcelWorker(each, lt)



if __name__ == '__main__':
    Pattern = PatternRecog()
    Pattern.PatternRecogWorker()


