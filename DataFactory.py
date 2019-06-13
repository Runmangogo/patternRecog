import json
import datetime


class DataFactory:

    #symbols = []

#    def findSymbol(symbolspage):
#       if
#           'www.nasdaq.com/symbol/' sample: http://www.nasdaq.com/symbol/xlnx
#           'www.nyse.com/quote/XNYS:' sample: https://www.nyse.com/quote/XNYS:XRX

    def json_digest(self, page):

        if page == 99:
            self.open_price = 0

        else:
            target = json.loads(page)

            #check timezone: make sure target['chart']['result'][0]['meta']['timezone'] == 'EST'

            self.timestamps = target['chart']['result'][0]['timestamp']
            self.open_price = target['chart']['result'][0]['indicators']['quote'][0]['open']
            self.close_price = target['chart']['result'][0]['indicators']['quote'][0]['close']
            self.high_price = target['chart']['result'][0]['indicators']['quote'][0]['high']
            self.low_price = target['chart']['result'][0]['indicators']['quote'][0]['low']
            self.volume = target['chart']['result'][0]['indicators']['quote'][0]['volume']

            #self.timestampconvertor(self.timestamps)

    def timestampconvertor(self, timestamps):
        self.datetime_format = []
        for each in timestamps:
            self.datetime_format.append(datetime.datetime.fromtimestamp(each).isoformat())


