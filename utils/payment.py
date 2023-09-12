import os
from django.conf import settings
import json
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib


def momo(amount,orderId):
    
    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = settings.MOMO_PARTNER_CODE
    accessKey = settings.MOMO_ACCESS_KEY
    secretKey = settings.MOMO_SECRET_KEY
    orderInfo = "pay with MoMo"
    redirectUrl = "http://localhost:8081/api/momo/webhook/"
    ipnUrl = "http://localhost:8081/api/momo/webhook/"
    requestId = str(uuid.uuid4())
    orderId = orderId
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString

    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
    # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
    # &requestType=$requestType
    rawSignature = (f"accessKey={accessKey}" +
                    f"&amount={amount}" +
                    f"&extraData={extraData}" + 
                    f"&ipnUrl={ipnUrl}" +
                    f"&orderId={orderId}" +
                    f"&orderInfo={orderInfo}" +
                    f"&partnerCode={partnerCode}" +
                    f"&redirectUrl={redirectUrl}" +
                    f"&requestId={requestId}" +
                    f"&requestType={requestType}")  

    # puts raw signature
    print(rawSignature)
    # signature
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    # json object send to MoMo endpoint

    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    print(response.json())
    return response

def momo_vendor():
    pass

def get_momo_recurring_token(partnerClientId):
    partnerClientId = 'vuvietquang90@gmail.com'
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = settings.MOMO_PARTNER_CODE
    accessKey = settings.MOMO_ACCESS_KEY
    secretKey = settings.MOMO_SECRET_KEY
    orderInfo = "get token"
    redirectUrl = "http://localhost:8081/api/momo/webhook/"
    ipnUrl = "http://localhost:8081/api/momo/webhook/"
    requestId = str(uuid.uuid4())
    orderId = orderId
    requestType = "captureWallet"
    extraData = ""
    amount = 0
    orderId = str(uuid.uuid4())

    rawSignature = (f"accessKey={accessKey}" +
                    f"&amount={amount}" +
                    f"&extraData={extraData}" + 
                    f"&ipnUrl={ipnUrl}" +
                    f"&orderId={orderId}" +
                    f"&orderInfo={orderInfo}" +
                    f"&partnerCode={partnerCode}" +
                    f"partnerClientId={partnerClientId}" +
                    f"&redirectUrl={redirectUrl}" +
                    f"&requestId={requestId}" +
                    f"&requestType={requestType}")  
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'partnerClientId':partnerClientId,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    print(response.json())
    return response