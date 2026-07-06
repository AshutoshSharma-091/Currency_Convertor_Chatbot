from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "8e7b582361ab50f6d759472ddb42c62123ed"


def fetch_conversion_factor(source, target):
    url = f"https://currencyapi.net/api/v2/rates?base={source}&output=json&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    print(data)

    if "rates" not in data:
        return None

    return data["rates"].get(target)


@app.route("/", methods=["POST"])
def index():
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
