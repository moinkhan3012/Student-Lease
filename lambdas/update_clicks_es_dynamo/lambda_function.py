import json
import boto3
import os
from requests.auth import HTTPBasicAuth
import requests


sqs = boto3.client('sqs')

def lambda_handler(event, context):
    result = sqs_receive_message()
    
    print(result)
    message_list = []

    if not 'Messages' in result:
        return {
            "message": "No message in SQS",
            'statusCode': 200
        }
    
    
    for message in result['Messages']:
        
        listing_id = message["MessageAttributes"]['listing_id']['StringValue']
        user_id = message["MessageAttributes"]['user_id']['StringValue']
        
        message_list.append([user_id,listing_id])
        print(sqs.delete_message(
                QueueUrl=os.environ.get('QUEUE_URL'),  # replace with your queue URL
                ReceiptHandle=message['ReceiptHandle']
            ))
            
        print("SQS deleted")
    
    print(update_dynamo(message_list))
    print(udpate_es_views(message_list))
        
        
    return {
        'statusCode': 200,
        'body': json.dumps('Update successful')
    }
        

    
def update_dynamo(message_list):

    dynamodb = boto3.resource('dynamodb')
    table_name = 'user_table'  # replace with your DynamoDB table name

    # Prepare batch items
    batch_items = {'RequestItems': {table_name: []}}

    table = dynamodb.Table(table_name)
    print(dir(table))
    
    for message in message_list:
        user_id = message[0]
        listing_id = message[1]
    # Update DynamoDB
    
        print(user_id, listing_id)
        response = table.get_item(
              # replace with your table name
            Key={'user_id': user_id}
        )
        
        if 'Item' in response:
            print(response)
            recent_searches = response['Item']['recent_searches']
            print(recent_searches)
            # Prepend the new listing_id and ensure the list has at most 10 items
            recent_searches.append(listing_id)
            if len(recent_searches) > 10:
                recent_searches = recent_searches[:10]
                

            print(recent_searches)
            print(table.update_item(
                Key={'user_id':  user_id},
                UpdateExpression='SET recent_searches = :val',
                ExpressionAttributeValues={':val':  list(set(recent_searches))}
            ))

            
    return {
        'statusCode': 200,
        'body': 'Processed successfully'
        
    }

def udpate_es_views(message_list):

    es_host = "https://search-sublease-3f4v5554g2z6jojki2xbdd5jfu.us-east-1.es.amazonaws.com/sublease/_update_by_query"  # replace with your Elasticsearch endpoint
    headers = {'Content-Type': 'application/json'}

    # Script for updating the field
    script = {
            "source": "ctx._source.timesVisited += 1",
            "lang": "painless"
        }
    
    for message in message_list:
        listing_id = message[1]

        update_request_body = {
            "script": script,
            "query": {
                "match": {
                    "id": listing_id
                }
            }
        }

        # Send the update request
        response = requests.post(es_host, auth=HTTPBasicAuth('sublease', 'Elasticsearch@1'), json=update_request_body)

        # Check if the update was successful
        if response.status_code == 200:
            print(f"Document with ID {listing_id} updated successfully.")
        else:
            print(f"Failed to update document with ID {listing_id}. Response: {response.text}")

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    
def sqs_receive_message():
    
    result = sqs.receive_message(
        QueueUrl = os.environ.get('QUEUE_URL'), 
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
        )

    return result
