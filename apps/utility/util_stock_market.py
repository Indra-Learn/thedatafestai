import requests
from urllib.parse import urlparse
# from time import sleep
        

class NSE_URL_FETCH(object):
    base_url = "https://www.nseindia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    def __init__(self, base_url=None, headers=None, session=None):        
        if headers == None:
            self.headers = NSE_URL_FETCH.headers
        else:
            self.headers = headers
            
        if not base_url:
            self.base_url = NSE_URL_FETCH.base_url
        else:
            self.base_url = base_url
            
        # if not session:
        #     self.session = requests.Session()
        # else:
        #     self.session = session
        # self.session.get(self.base_url, headers=self.headers)
    
        
    def __call__(self, *args, **kwargs):
        session = requests.Session()
        session.get(self.base_url, headers=self.headers)
        nse_url = f"{self.base_url}/{args[0]}"
        response = session.get(nse_url, headers=self.headers)
        return response.json()


if __name__ == '__main__':
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketTurnoverSummary
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketStatistics
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getIndexData&&type=All
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getGraphChart&&type=NIFTY%2050&flag=1D
    # obj = NEW_NSE_URL_FETCH(url="https://www.nseindia.com/api/NextApi/apiClient?functionName={}")    
    # out = obj('getMarketStatistics')
    # print(f"{out.json()}")
    
    obj = NSE_URL_FETCH(api_url="api/NextApi/apiClient?functionName=getMarketStatistics")
    print(obj())
    