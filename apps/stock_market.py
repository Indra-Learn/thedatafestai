import os
import sys

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from apps.utility.util_stock_market import NSE_URL_FETCH

bp = Blueprint('stock_market', __name__, url_prefix='/stock_market') 

@bp.route('/', methods=['GET'])
def home():
    return render_template('stock_market/stock_market_home.html')

@bp.route('/shortterm_market_status', methods=['GET'])
def daily_market_status():
    daily_market_status_data_dict = dict()
    daily_market_status_obj = NSE_URL_FETCH(api_url="api/NextApi/apiClient?functionName=getMarketStatistics")
    data = daily_market_status_obj()
    daily_market_status_data_dict[data.get('data').get('timestamp')] = dict()
    daily_market_status_data_dict[data.get('data').get('timestamp')]['WeekHigh'] = data.get('data').get('fiftyTwoWeek').get('high')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['WeekLow'] = data.get('data').get('fiftyTwoWeek').get('low')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['UpperCircuit'] = data.get('data').get('circuit').get('upper')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['LowerCircuit'] = data.get('data').get('circuit').get('lower')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksAdvances'] = data.get('data').get('snapshotCapitalMarket').get('advances')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksDeclines'] = data.get('data').get('snapshotCapitalMarket').get('declines')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksUnchanged'] = data.get('data').get('snapshotCapitalMarket').get('unchange')
    
    
    return render_template('stock_market/stock_market_shortterm_market_status.html',
                           first_content = daily_market_status_data_dict)
