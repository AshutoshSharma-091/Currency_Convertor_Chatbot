from flask import Flask, request, jsonify

import requests
app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency'] ['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}" . format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):
    url = "https://currencyapi.net/api/v2/rates?base={}_{}&output=json&key=8e7b582361ab50f6d759472ddb42c62123ed".format(source,target)

    response = requests.get(url)
    response.json()
    return response['{}_{}'.format(source,target)]

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask

app = Flask(__name__)

# Your routes here

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
