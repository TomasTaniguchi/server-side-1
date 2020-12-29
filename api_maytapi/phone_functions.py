import requests
from api_maytapi import variables
INSTANCE_URL = variables.INSTANCE_URL
API_TOKEN = variables.API_TOKEN
PRODUCT_ID = variables.PRODUCT_ID

headers = {
    "Content-Type": "application/json",
    "x-maytapi-key": API_TOKEN,
}


def setAckPreference():
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/setAckPreference"
    payload = "{\"ack_delivery\": \"true\"}"
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    print(result)


def addPhone(phone):
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/addPhone"
    phone = str(phone)
    payload = "{\"number\": \"" + phone + "\"}"
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    try:
        id = result['id']
    except:
        id = '0000'

    if id != '0000':
        getQrCode(id)
    return id


def getQrCode(id_phone):
    id_phone = str(id_phone)
    if getStatus(id_phone)== True:
        url = INSTANCE_URL + "/" + PRODUCT_ID + "/"+id_phone+"/qrCode"
        response = requests.request("GET", url, headers=headers)
        file = open("img_data/"+id_phone+".png", "wb")
        file.write(response.content)
        file.close()
        return True

    return False


def getStatus(id_phone):
    id_phone = str(id_phone)
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/"+id_phone+"/status"
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    try:
        result = result['success']
    except:
        result = False
    return result


def getStatusLoggedIn(id_phone):
    id_phone = str(id_phone)
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/"+id_phone+"/status"
    response = requests.request("GET", url, headers=headers)
    result =response.json()
    try:
        result = result['status']['loggedIn']
    except:
        result = False
    return result


def delete(id_phone):
    id_phone = str(id_phone)
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/"+id_phone+"/delete"
    response = requests.request("GET", url, headers=headers)
    result =response.json()
    try:
        result = result['success']
    except:
        result = False
    return result


def logout(id_phone):
    id_phone = str(id_phone)
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/"+id_phone+"/logout"
    response = requests.request("GET", url, headers=headers)
    result =response.json()
    try:
        result = result['success']
    except:
        result = False
    return result


#setAckPreference()
#print(addPhone(5493765139227))
#print(getQrCode(2989))
#print(getStatus(2989))
#print(logout(2989))
#print(getStatusLoggedIn(2989))
#print(delete(3038))
