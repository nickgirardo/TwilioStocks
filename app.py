from flask import Flask
from flask import request

#Twilio includes
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
from twilio.twiml import Response

from functools import partial

import scrape
import parse
import config

application = Flask(__name__)


def print_text(tickers, more):
    
    def print_ticker(t):
        if t['not_found']:
        	return '{} Not found'.format(t['ticker'])

        if t['delisted']:
        	return '{} ({}) has been delisted'.format(t['name'], t['ticker'])


        main_info = '{} ({}): {} {}{}'.format(t['name'], t['ticker'], t['price'], t['change_direction'], t['change_amount'] )

        if more:
            open_str = 'Open: {}'.format(t['open'])
            close_str = 'Previous Close: {}'.format(t['previous_close'])
            volume_str = 'Volume: {}'.format(t['volume'])
            ytd_str = 'YTD Return: {}'.format(t['ytd_return'])
            return '\n'.join([main_info, open_str, close_str, volume_str, ytd_str])
        else:
            return main_info
        

    if not tickers:
    	return 'No companies recieved'
    
    join_str = '\n\n' if more else '\n'

    return join_str.join(map(print_ticker,tickers))


@application.route('/', methods=['POST'])
def get_text():

    message = request.form['Body']

    (tickers, more) = parse.parse_text(message)

    stock_info = []

    if not tickers:
    	print 'No companies recieved'
    for t in tickers:
        stock_info = map(partial(scrape.get_stock_info,more_info=more),tickers)

    resp = Response()
    resp.message(print_text(stock_info, more))
    
    return str(resp)


if __name__ == '__main__':
	application.run(host='0.0.0.0')
