import multiprocessing
from utils.rx_test import Observable
from utils.rx_test import ThreadPoolScheduler
import requests
from api_maytapi import variables

INSTANCE_URL = variables.INSTANCE_URL
API_TOKEN = variables.API_TOKEN
PRODUCT_ID = variables.PRODUCT_ID

headers = {
    "Content-Type": "application/json",
    "x-maytapi-key": API_TOKEN,
}


def sent_default_message(message):
    source = message['source']
    destination = message['destination']
    message = message['message']
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/" + source + "/sendMessage"
    payload = {"to_number": destination, "type": "text", "message": message}
    response = requests.request("POST", url, headers=headers, json=payload)
    result = response.json()
    return result


optimal_thread_count = multiprocessing.cpu_count() + 1
poo_scheduler = ThreadPoolScheduler(optimal_thread_count)
print(optimal_thread_count)

body1 = {"message": "tyrt", "source": "3076", "destination": "5493765139227"}
body2 = {"message": "tyrt", "source": "3076", "destination": "5493765112202"}



print("process 1 ")

Observable.of(body1)\
    .map(lambda s: sent_default_message(s)) \
    .subscribe_on(poo_scheduler) \
    .subscribe()

print("process 2 ")

Observable.of(body2)\
    .map(lambda s: sent_default_message(s)) \
    .subscribe_on(poo_scheduler) \
    .subscribe()

