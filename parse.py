import re

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
