import os
import sys
import pandas as pd

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from apps.utility.util_stock_market import NSE_URL_FETCH

bp = Blueprint('stock_market', __name__, url_prefix='/stock_market') 

def df_col_style_advanced(row):
    percentage = row["percChange"]
    if percentage > 0:
        class_name = "green-header"
        tooltip = f"Exceeded target by {percentage:.1f}%"
    else:
        class_name = "red-header"
        tooltip = f"Missed target by {abs(percentage):.1f}%"
    return f'<a class="{class_name}" title="{tooltip}" href="#">{row["percChange"]}</a>'
    
    
@bp.route('/', methods=['GET'])
def home():
    return render_template('stock_market/stock_market_home.html')

@bp.route('/shortterm_market_status', methods=['GET'])
def daily_market_status():
    daily_market_status_data_dict = dict()
    daily_market_status_obj = NSE_URL_FETCH()
    data = daily_market_status_obj("api/NextApi/apiClient?functionName=getMarketStatistics")
    daily_market_status_data_dict[data.get('data').get('timestamp')] = dict()
    daily_market_status_data_dict[data.get('data').get('timestamp')]['WeekHigh'] = data.get('data').get('fiftyTwoWeek').get('high')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['WeekLow'] = data.get('data').get('fiftyTwoWeek').get('low')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['UpperCircuit'] = data.get('data').get('circuit').get('upper')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['LowerCircuit'] = data.get('data').get('circuit').get('lower')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksAdvances'] = data.get('data').get('snapshotCapitalMarket').get('advances')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksDeclines'] = data.get('data').get('snapshotCapitalMarket').get('declines')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['StocksUnchanged'] = data.get('data').get('snapshotCapitalMarket').get('unchange')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['MarketCapLacCr'] = data.get('data').get('tlMKtCapLacCr')
    daily_market_status_data_dict[data.get('data').get('timestamp')]['MarketCapTriDol'] = data.get('data').get('tlMKtCapTri')
    
    
    nse_index_obj = NSE_URL_FETCH()
    index_data = nse_index_obj("api/NextApi/apiClient?functionName=getIndexData&&type=All")
    index_data_df = pd.DataFrame(index_data.get('data'))
    index_data_df.drop(columns=["timeVal", "constituents"], inplace=True)
    index_data_df.drop(["indicativeClose", "icChange", "icPerChange", "isConstituents"], axis=1, inplace=True)
    index_data_df['indexName'] = index_data_df['indexName'].apply(lambda x: f'''<a href="https://www.nseindia.com/index-tracker/{x}" target="_blank">{x}</a>''')
    second_contents_details_tupple = (index_data_df['percChange'] > 0).sum(), (index_data_df['percChange'] <= 0).sum()
    index_data_df['percChange'] = index_data_df.apply(df_col_style_advanced, axis=1)
    index_data_html = index_data_df.to_html(index=False, classes="df-table", border=1, 
                                            float_format=lambda x: f'{x:,.2f}', justify='center', escape=False)
    
    fii_dii_obj = NSE_URL_FETCH()
    fii_dii_data = fii_dii_obj("api/fiidiiTradeReact")
    fii_dii_data_df = pd.DataFrame(fii_dii_data)
    fii_dii_data_df["netValue"] = fii_dii_data_df["netValue"].apply(lambda x: f'<button class="pill-btn green-header">{x}</button>' if float(x) > 0 else f'<button class="pill-btn red-header">{x}</button>')
    print(f"{fii_dii_data_df=}")
    fii_dii_data_html = fii_dii_data_df.to_html(index=False, classes="df-table", border=1, float_format=lambda x: f'{x:,.2f}', justify='center', escape=False)
    return render_template('stock_market/stock_market_shortterm_market_status.html',
                           first_contents = daily_market_status_data_dict,
                           second_contents_details = second_contents_details_tupple, second_contents = index_data_html, 
                           third_contents_fii_dii = fii_dii_data_html)
