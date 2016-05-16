import requests
from lxml import html
import re


"""a
TODO return info instead of printing
TODO get more info
"""
def get_stock_info(ticker, more_info=False):

    #direction of stock change
    #one of either 'up' or 'down'
    change = 'up' 

    #initialization of stock_info dict
    stock_info = {'ticker':ticker, 'more': more_info}

    #scraping stock information from bloombergs website
    query_string = 'http://www.bloomberg.com/quote/' + ticker + ':US'
    page = requests.get(query_string)
    tree = html.fromstring(page.content)
    #If this div doesn't extist, a company with the given stock ticker doesn't exist
    price_container = tree.find_class('price-container')
    
    stock_info['not_found'] = not price_container
    if not price_container:
    	return stock_info
    else:
    	price_container = price_container[0]
    price_element = tree.find_class('price')[0]
    stock_info['price'] = float(price_element.text_content())

    #Find the name of the company
    name_element = tree.find_class('name')[0]
    stock_info['name'] = name_element.text_content().strip()

    #the price container will either be given a class up or down for styling
    #this is how we can tell the direction the stock has moved as the
    #change itself doesn't have a '+' or '-' in the actual string
    for c in price_container.classes:
        if c == 'up':
            change = 'up'
        if c == 'down':
            change = 'down'

    change_container = tree.find_class('change-container')[0]
    stock_info['change_amount'] = float(change_container[0].text_content())
    stock_info['change_percent'] = float(change_container[1].text_content().replace('%',''))
    #Once again, this is necessary because the '-' character is just added with css
    if c == 'down':
    	stock_info['change_amount'] *= -1
    	stock_info['change_percent'] *= -1

    #If requested, add extra info here
    if more_info:
    	pass

    return stock_info


def parse_text(message):

    more = False

    #Set string to uppercase, does not affect stock tickers and makes looking for 'more info' easier
    message = message.upper()
    if 'MORE INFO' in message:
        more = True
    else:
        more = False

    #If the string has had 'more info', remove it now, we're done with it
    message = message.replace('MORE INFO','')

    #remove all non-alphaneumeric characters
    message = re.sub(r'([^\s\w]|_)+', '', message)

    #Each seperate word is a different stock ticker
    tickers = message.split()

    return (tickers, more)


def get_text(message):
    (tickers, more) = parse_text(message)

    if not tickers:
    	print 'No companies recieved'
    for t in tickers:
        print get_stock_info(t, more)

