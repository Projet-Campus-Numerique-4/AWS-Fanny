import json
import os

# Get environment variable
DEVICES_TABLE = os.environ['DEVICES_TABLE']

def get_devices(context, event): 
    print(DEVICES_TABLE)
    return { 
        "statusCode": 400, 
        "body": json.dumps([
            {"deviceId": "a", "deviceType": "co2", "deviceName": "device1"}, 
            {"deviceId": "b", "deviceType": "pir", "deviceName": "device2"}]), 
        "headers": {'Access-Control-Allow-Origin': '*'} 
    } 


