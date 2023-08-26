def momo(amount):
    import json
    import urllib.request
    import urllib
    import uuid
    import requests
    import hmac
    import hashlib

    # parameters send to MoMo get get payUrl
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO59AK20220907"
    accessKey = "zhk7tDktfUZmeR4Z"
    secretKey = "jKVBar49casmn7qyV5XlLVytM7gGpSDh"
    orderInfo = "pay with MoMo"
    redirectUrl = "http://localhost:8081/api/momo/webhook/"
    ipnUrl = "http://localhost:8081/api/momo/webhook/"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
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
