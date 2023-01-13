# import RESTClient
from polygon import RESTClient
from polygon.rest.models.request import RequestOptionBuilder
from typing import cast
from urllib3 import HTTPResponse


import requests
import pandas as pd
import io

def get_symbols():
    url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    symbols = companies['Symbol'].tolist()
    return symbols


# for s in get_symbols():
#     print(s)
#
# exit()

# create client
client = RESTClient(api_key="tuQt2ur25Y7hTdGYdqI2VrE4dueVA8Xk")

# create request options
options = RequestOptionBuilder().edge_headers(
    edge_id="YOUR_EDGE_ID",  # required
    edge_ip_address="IP_ADDRESS",  # required
)
# get response
res = client.get_ticker_details("F")
res1 = client.get_aggs("F", 1, "day", "2023-01-12", "2023-01-12", options=options)

# do something with response
print(res)
print(res1)
dividends = [d for d in client.list_dividends("F")]
print(dividends)
