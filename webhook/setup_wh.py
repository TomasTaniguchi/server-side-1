from pyngrok import ngrok
import requests
import sys
from api_maytapi import variables

variables.load_env_variables(1)

# Replace the values here.
INSTANCE_URL = variables.INSTANCE_URL
PRODUCT_ID = variables.PRODUCT_ID
API_TOKEN = variables.API_TOKEN


def setup_webhook():
    if PRODUCT_ID == "" or API_TOKEN == "":
        print(
            "You need to change PRODUCT_ID and API_TOKEN values in app.py file.", file=sys.stdout, flush=True
        )
        return

    public_url = ngrok.connect(8000)
    public_url = public_url.replace("http", "https", 1)
    print("Public Url " + public_url, file=sys.stdout, flush=True)

    url = INSTANCE_URL + "/" + PRODUCT_ID + "/setWebhook"


    headers = {
        "Content-Type": "application/json",
        "x-maytapi-key": API_TOKEN,
    }

    body = {"webhook": public_url + "/webhook"}

    response = requests.post(url, json=body, headers=headers)
    print(response.json(), file=sys.stdout, flush=True)


# Do not use this method in your production environment
setup_webhook()

