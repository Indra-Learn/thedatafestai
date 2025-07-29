import os
import sys
import pandas as pd

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from apps.utility.util_stock_market import NSE_URL_FETCH
from apps.config import stock_market_job_list

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


@bp.route('/stock_market_etf', methods=['GET'])
def stock_market_etf():
    nse_etf_obj = NSE_URL_FETCH()
    nse_etf_data = nse_etf_obj("api/etf/")
    nse_etf_data_df = pd.DataFrame(nse_etf_data.get("data"))
    print(f"{nse_etf_data_df.shape}")
    nse_etf_data_df = nse_etf_data_df.loc[:, ['symbol', 'open', 'high', 'low', 'ltP', 'nav', 'xDt', 'prevClose', 'perChange30d', 'perChange365d']]
    # nse_etf_data_df['symbol'] = nse_etf_data_df.apply(lambda x: f'<a title="{x["asset"]}" href="#">{x["symbol"]}</a>')
    nse_etf_data_html = nse_etf_data_df.to_html(index=False, classes="df-table", border=1, justify='center', escape=False)
    return render_template('stock_market/stock_market_etf.html',
                           first_contents = nse_etf_data_html,)


@bp.route('/admin_setting', methods=['GET'])
def admin_setting():
    stock_market_job_list_df = pd.DataFrame(stock_market_job_list)
    stock_market_job_list_df["checkpoint"] = stock_market_job_list_df["step_id"].apply(lambda x: f'<input type="checkbox" id="check_job_{x}" name="check_job_{x}"></input>')
    stock_market_job_list_html = stock_market_job_list_df.to_html(index=False, classes="df-table", border=1, justify='center', escape=False)
    return render_template('stock_market/stock_market_admin_setting.html',
                           first_contents = stock_market_job_list_html)