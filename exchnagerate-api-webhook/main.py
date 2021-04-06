#!/usr/bin/env python

from datetime import datetime
import csv
import logging
import requests

logfilename = "exchangerate.log"
logging.basicConfig(filename=logfilename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

EXCHANGE_URL ='https://api.exchangeratesapi.io/'

CURRENCY = [
        "ILS",
        "GBP",
        "USD",
        "CAD",
        "RUB",
        ]

def main():
    """
    main program to invoke exchangeapi and then get historical data
    """
    try:
        history_data = fetch_history_exchange_data("2021-01-01", str(datetime.now().date()))

        logger.info(history_data)
        _write_to_csv_file(history_data)

    except Exception as ex:
        logger.exception(ex)

def fetch_history_exchange_data(start, end):
    """
    """
    query_params = {
            'start_at': start,
            'end_at': end,
            'symbols': ",".join(CURRENCY),
            }

    try:
        resp = requests.get("{}history/".format(EXCHANGE_URL) , params=query_params, timeout=60)
        logger.info(resp)
        data = resp.json()
        data = data.get('rates', {})
        tmp = [ v.update({'date': k, }) for k,v in data.items() ]
        data = [ v  for k,v in data.items() ]
        data = sorted(data, key=lambda k: k['date'])
        return data
    except Exception as ex:
        raise ex


def _write_to_csv_file(data=None):
    """
    """
    if not data:
        return
    f_p = csv.writer(open("output.csv", "w+"))

    # Write CSV Header, If you dont need that, remove this line
    f_p.writerow(["date", "base", "USD", "GBP", "ILS","RUB"])

    for each in data:
        f_p.writerow([each['date'], "EUR", each['USD'], each["GBP"], each["ILS"], each["RUB"] ])


if __name__ == "__main__":
    main()
