import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    
    # Reference to your table
    table = dynamodb.Table('Conversations')
    
    # Get itemId from the event that API Gateway passes
    print(event)
    #  = event.get('querystring', {}).get('message_id', None)
    item_id = event['params']['querystring']['user_id']
    
    # Check if itemId is provided
    if not item_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: Please provide an 'itemId'")
        }
    
    try:
        # Querying the table for items with the specified userId
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(item_id)
        )
        
        items = response.get('Items', [])
        print(items)
        if len(items) == 0:
            print("Reaching here!")
        
        # Return the found items
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
        
    except ClientError as e:
        # Handle potential errors in querying DynamoDB
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps("Internal server error")
        }