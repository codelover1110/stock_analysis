import io
import time

import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import requests
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()


def get_symbols():
    url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    symbols = companies['Symbol'].tolist()
    return symbols


stock_list = pd.read_excel("stocks.xlsx", index_col=0)

df = pd.DataFrame(columns=["Company", "Ticker", "Stock Price", "Trailing P/E Ratio", "Shares Held by Institutions",
                           "% Float Held by Institutions", "Forward Divident Yield", "Forward Dividend",
                           "Last Year Dividend", "2021 Dividend", "2020 Dividend", "2019 Dividend"])
                           
for s_data in stock_list.iterrows():
    ticker = s_data[0]

    finance_url = "https://finance.yahoo.com/quote/" + str(ticker) + "/key-statistics?p=" + str(ticker)

    finance_url1 = "https://finance.yahoo.com/quote/" + str(ticker) + "/holders?p=" + str(ticker)

    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    try:
        # Calculate Dividends
        yfinance_obj = yf.Ticker(str(ticker))

        yfinance_obj.dividends.to_csv("dividend.csv")

        df1 = pd.read_csv("dividend.csv")

        total_19 = df1.loc[df1['Date'].str.contains('2019'), 'Dividends'].sum()

        total_20 = df1.loc[df1['Date'].str.contains('2020'), 'Dividends'].sum()

        total_21 = df1.loc[df1['Date'].str.contains('2021'), 'Dividends'].sum()

        total_22 = df1.loc[df1['Date'].str.contains('2022'), 'Dividends'].sum()

        soup = BeautifulSoup(requests.get(url=finance_url, headers=headers).content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

        dom = etree.HTML(str(soup))

        company = dom.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')[0].text

        stock_price = dom.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text

        trailing_pe = dom.xpath('//*[contains(text(), "Trailing P/E")]/../following-sibling::td[1]')[0].text

        share_held_by_inst = dom.xpath('//*[contains(text(), "Held by Institutions")]/../following-sibling::td[1]')[0].text

        forward_divident_yield = dom.xpath('//*[contains(text(), "Forward Annual Dividend Yield")]/../following-sibling::td[1]')[0].text

        forward_dividend = dom.xpath('//*[contains(text(), "Forward Annual Dividend Rate")]/../following-sibling::td[1]')[0].text

        dom1 = etree.HTML(str(BeautifulSoup(requests.get(url=finance_url1, headers=headers).content, 'html5lib')))

        float_held_by_institutions = dom1.xpath('//*[@id="Col1-1-Holders-Proxy"]/section/div[2]/div[2]/div/table/tbody/tr[3]/td[1]')[0].text
    
        df.loc[len(df.index)] = [
                                    company,
                                    ticker,
                                    stock_price,
                                    trailing_pe,
                                    share_held_by_inst,
                                    float_held_by_institutions,
                                    forward_divident_yield,
                                    forward_dividend,
                                    total_22,
                                    total_21,
                                    total_20,
                                    total_19]

        print(f'{ticker}, imported')

        df.to_csv("yfinance.csv")

    except:
        print(f"{ticker}, can't be imported")

df.to_csv("yfinance.csv")
