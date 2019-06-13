import urllib.request

class WebCrawler:

#    def __init__(self, symbollist_url, symboldata_url):
#        self.symbollist_url = symbollist_url
#        self.symboldata_url = symboldata_url


# fetch the symbol list from wikipedia
#    def fetch_symbollist(self):
#        return self.url_open(self.symbollist_url)

# fetch raw data for one symbol
#    def fetch_symboldata:


    def url_open(self, url):
        req = urllib.request.Request(url)
        req.method = 'GET'

        try:
            #Windows 7: 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')
        except Exception as e:
            print('url_open: ')
            print(e)
            return 99
        ##print(html)
        return html


# def massagedata(data):


#    if __name__ == '__main__':
#       json_digest(url_open(url))


