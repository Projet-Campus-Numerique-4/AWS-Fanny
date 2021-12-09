import boto3
import json
import os

# Get environment variable
DEVICES_TABLE = os.environ['DEVICES_TABLE']

def get_devices(context, event):
    print("")
    print(DEVICES_TABLE)
    print("")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DEVICES_TABLE)
    print("")
    print(table)
    print("")
    data = table.scan()
    result = data["Items"]
    print("")
    print(result)
    print("")
    return {
    "statusCode": 200,
    "body": {"devices": json.dumps(result)},
    "headers": {'Access-Control-Allow-Origin': '*'}
  }
    # return { 
    #     "statusCode": 400, 
    #     "body": json.dumps([
    #         {"deviceId": "a", "deviceType": "co2", "deviceName": "device1"}, 
    #         {"deviceId": "b", "deviceType": "pir", "deviceName": "device2"}]), 
    #     "headers": {'Access-Control-Allow-Origin': '*'} 
    # } 

