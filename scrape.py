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

    #Find the name of the company
    name_element = tree.find_class('name')[0]
    stock_info['name'] = name_element.text_content().strip()

    #Check if the ticker has been delisted (e.g. APPL)
    market_status = tree.find_class('market-status')[0].text_content().strip()
    if market_status == "Ticker Delisted":
    	stock_info['delisted'] = True
    	return stock_info
    else:
    	stock_info['delisted'] = False

    price_element = tree.find_class('price')[0]
    stock_info['price'] = float(price_element.text_content())


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
    	cells = tree.find_class('cell')
        for c in cells:
            cell_label = c.find_class('cell__label')[0].text_content().strip()
            cell_value = c.find_class('cell__value')[0].text_content().strip()
            if cell_label == 'Open':
            	stock_info['open'] = cell_value
            elif cell_label == 'Previous Close':
                stock_info['previous_close'] = cell_value
            elif cell_label == 'Volume':
                stock_info['volume'] = cell_value
            elif cell_label == 'YTD Return':
                stock_info['ytd_return'] = cell_value

    return stock_info
