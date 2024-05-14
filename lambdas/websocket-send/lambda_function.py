import json
import boto3
import os
from datetime import datetime


def lambda_handler(event, context):
    sender =  target = json.loads(event['body'])['sender']
    message = json.loads(event['body'])['message']
    print(sender)
    target = json.loads(event['body'])['target']
    print(target)
    print(event)
    dynamodb = boto3.resource('dynamodb')
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    msg_id = "_".join(sorted([sender, target]))
    
    print(msg_id)
    full_message = {"message_id": msg_id, "sender" : sender,"msg": message, "target": target, "timestamp": current_time }
    msg_payload = {"sender" : sender,"msg": message}
    print(full_message)
    
    msg_table = dynamodb.Table('messages')
    msg_table.put_item(Item={"message_id": msg_id, "sender" : sender, "msg": message, "target": target, "timestamp": current_time })
    print("Here!")
    
    table = dynamodb.Table('UserConnections')
    response = table.get_item(
        Key={
            'userId': target
        }
    )
    print(response)
    try: 
    # Extract the item from the response
        print("Getting Here!")
        item = response.get('Item', {})
        print(item["connectionId"])
        client = boto3.client('apigatewaymanagementapi', endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])
        client.post_to_connection(
            Data=json.dumps(msg_payload),
            ConnectionId=item["connectionId"]
        )
    except:
        print("Can't Connect to User!")
        

    return {'statusCode': 200}
    

    