import io
import time

import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import requests
from pandas_datareader import data as pdr
#

import yfinance as yf
yf.pdr_override()



def get_symbols():
    url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    symbols = companies['Symbol'].tolist()
    return symbols


df = pd.DataFrame(columns=["Company", "Ticker", "Stock Price", "Trailing P/E Ratio", "Shares Held by Institutions",
                           "% Float Held by Institutions", "Forward Divident Yield","Forward Dividend",
                           "Last Year Dividend", "2021 Dividend", "2020 Dividend", "2019 Dividend"])
for s in get_symbols():


    URL = "https://finance.yahoo.com/quote/" + str(s) + "/key-statistics?p=" + str(s)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
    r = requests.get(url=URL, headers=headers)
    #time.sleep(5)
    try:
        msft = yf.Ticker(str(s))
        msft.dividends.to_csv("dividend.csv")
        df1 = pd.read_csv("dividend.csv")
        total_19 = df1.loc[df1['Date'].str.contains('2019'), 'Dividends'].sum()
        total_20 = df1.loc[df1['Date'].str.contains('2020'), 'Dividends'].sum()
        total_21 = df1.loc[df1['Date'].str.contains('2021'), 'Dividends'].sum()
        total_22 = df1.loc[df1['Date'].str.contains('2022'), 'Dividends'].sum()

        soup = BeautifulSoup(r.content,
                             'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
        # print(soup.prettify())
        dom = etree.HTML(str(soup))
        company = dom.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')[0].text
        ticker = s
        stock_price = dom.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text
        trailing_pe = dom.xpath(
            '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]')[
            0].text
        share_held_by_inst = dom.xpath(
            '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[7]/td[2]')[
            0].text
        forward_divident_yield = dom.xpath(
            '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[2]')[
            0].text
        forward_dividend = dom.xpath(
            '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[1]/td[2]')[
            0].text
        df.loc[len(df.index)] = [company, ticker, stock_price, trailing_pe, share_held_by_inst, '',
                                 forward_divident_yield, forward_dividend, total_22, total_21, total_20, total_19]
        print(s, " imported")

        df.to_csv("yfinance.csv")
    except:
        print(s, " cant be imported")

df.to_csv("yfinance.csv")
