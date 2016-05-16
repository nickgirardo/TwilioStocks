from lxml import html
import requests as r

def get_stock_info(ticker, more_info=False):

    #direction of stock change
    #one of either 'up' or 'down'
    change = 'up' 

    #initialization of stock_info dict
    stock_info = {'ticker':ticker, 'more': more_info}

    #scraping stock information from bloombergs website
    query_string = 'http://www.bloomberg.com/quote/' + ticker + ':US'
    page = r.get(query_string)
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
            change = '+'
        if c == 'down':
            change = '-'

    change_container = tree.find_class('change-container')[0]
    stock_info['change_direction'] = change
    stock_info['change_amount'] = float(change_container[0].text_content())
    stock_info['change_percent'] = float(change_container[1].text_content().replace('%',''))

    #If requested, add extra info here
    if more_info:
    	pass

    return stock_info