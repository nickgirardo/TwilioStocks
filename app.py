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

        if more:
            return '{} ({}): {} {}{}'.format(t['name'], t['ticker'], t['price'], t['change_direction'], t['change_amount'] )
        else:
            return '{} ({}): {} {}{}'.format(t['name'], t['ticker'], t['price'], t['change_direction'], t['change_amount'] )
        

    if not tickers:
    	return 'No companies recieved'
    
    join_str = '\n\n' if more else '\n'

    return join_str.join(map(print_ticker,tickers))


@application.route('/', methods=['POST'])
def get_text():

    message = request.form['Body']
    print 'message received'

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
