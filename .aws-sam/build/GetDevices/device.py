import json

def get_device(context, event): 
    print("get_device")
    return { 
        "statusCode": 400, 
        "body": json.dumps({"deviceId": "a", "deviceType": "co2", "deviceName": "device1"}), 
        "headers": {'Access-Control-Allow-Origin': '*'} 
    } 