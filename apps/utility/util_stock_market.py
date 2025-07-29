import requests
from urllib.parse import urlparse
import time


class NSEAPI:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize session with required cookies"""
        self.session.get("https://www.nseindia.com", headers=self.headers)
        time.sleep(3)  # Be polite with delays
    
    def reset_session(self):
        """Completely reset the session"""
        self.session.close()
        self.session = requests.Session()
        self._initialize_session()
        return True
    
    def get_quote(self, nse_url):
        """Get equity quote for given symbol"""
        # url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        try:
            response = self.session.get(nse_url, headers=self.headers, cookies=self.session.cookies)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            # Auto-reset on failure and retry once
            self.reset_session()
            try:
                response = self.session.get(nse_url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Retry also failed: {e}")
                return None
    
    def __del__(self):
        self.session.close()

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
        session.close()
        return response.json()


if __name__ == '__main__':
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketTurnoverSummary
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketStatistics
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getIndexData&&type=All
    # https://www.nseindia.com/api/NextApi/apiClient?functionName=getGraphChart&&type=NIFTY%2050&flag=1D
    # obj = NEW_NSE_URL_FETCH(url="https://www.nseindia.com/api/NextApi/apiClient?functionName={}")    
    # out = obj('getMarketStatistics')
    # print(f"{out.json()}")
    
    # obj = NSE_URL_FETCH()
    # print(obj("api/etf"), flush=True)
    
    # Usage example
    nse = NSEAPI()

    # Get a quote
    # quote = nse.get_quote("https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketStatistics")
    # print(quote)

    # Reset session when needed
    # nse.reset_session()
    
    # Get another quote
    # quote = nse.get_quote("https://www.nseindia.com/api/NextApi/apiClient?functionName=getIndexData&&type=All")
    # print(quote)
    
    # Reset session when needed
    nse.reset_session()
    
    # Get another quote
    quote = nse.get_quote("https://www.nseindia.com/api/fiidiiTradeReact")
    print(quote)
    
    print("\n")
    print("\n")
    # Reset session when needed
    nse.reset_session()

    # Get another quote
    quote = nse.get_quote("https://www.nseindia.com/api/etf")
    print(quote)
    
    
    
    