from flask import Flask, request, jsonify

app = Flask(__name__)

import requests

API_KEY = "cd28b95b6587cc7efc886a2b"

def fetch_conversion_factor(source, target):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{source}"

    response = requests.get(url)
    data = response.json()

    print(data)  # For debugging

    if data["result"] != "success":
        return None

    return data["conversion_rates"][target]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "Webhook is running!"
    data = request.get_json()

    parameters = data.get("queryResult", {}).get("parameters", {})

    source_currency = parameters["unit-currency"]["currency"]
    amount = parameters["unit-currency"]["amount"]
    target_currency = parameters["currency-name"]

    conversion_factor = fetch_conversion_factor(source_currency, target_currency)

    if conversion_factor is None:
        return jsonify({
            "fulfillmentText": "Unable to fetch exchange rate."
        })

    final_amount = round(amount * conversion_factor, 2)

    response = {
        "fulfillmentText": f"{amount} {source_currency} = {final_amount} {target_currency}"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
