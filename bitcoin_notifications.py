import requests
import time
from datetime import datetime

bitcoin_api_url = 'https://api.coingecko.com/api/v3/simple/price/?ids=bitcoin&vs_currencies=chf'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/cyjuFCp8OIWWZSYrcYdWWr'
bitcoin_price_threshold = 20000

def get_btc_price():
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    bitcoinValue = response_json['bitcoin']
    bitcoinValueCHF = bitcoinValue['chf']

    #Convert Price to a floating point number    
    return float(bitcoinValueCHF)

def post_ifttt_webhook(event,value):
    #The payload that will be sent to IFTTT webhook
    data = {'value1': value}
    #Inserts our desired event
    ifttt_event_url = ifttt_webhook_url.format(event)
    # Sends a HTTP Post request to the webhook url
    requests.post(ifttt_event_url, json=data)
    
def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        #Formats date into a string
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']

        #<b> bold tag creates bolded text
        #24.02.2020 15:09: CHF<b>10123.4</b>
        row = '{}: CHF<b>{}</b>'.format(date,price)
        rows.append(row)

        #Use a <br> break tag to create a new line
        #Join the rows delimited by <br> tag: row1<br>row2<br>row3
        return '<br>'.join(rows)
             


def main():
    bitcoin_history = []
    while True:
        price = get_btc_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send emergency notification
        if price < bitcoin_price_threshold:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        print(len(bitcoin_history))
        if len(bitcoin_history) == 5:            
            post_ifttt_webhook('bitcoin_price_update',
                                format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        #Sleep 5mins
        time.sleep(5*60)

if __name__ == '__main__':
    main()
    
