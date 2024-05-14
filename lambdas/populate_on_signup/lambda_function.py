import json
import boto3
import uuid

table_name = 'user_table'
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    try:
        email = event['reqBody']['email']
        response = create_user(email)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'statusCode': 200,
                'body': json.dumps('User created successfully!')
            }
        else:
            error_message = 'Failed to create user: ' + json.dumps(response)
            print(error_message)
            return {
                'statusCode': 500,
                'body': json.dumps(error_message)
            }
    except KeyError as e:
        error_message = 'Missing required parameter: {}'.format(e)
        print(error_message)
        return {
            'statusCode': 400,
            'body': json.dumps(error_message)
        }


def create_user(email):
    unique_id = str(uuid.uuid4())
    recent_searches = [] 
    
    user = {
        'user_id': unique_id,
        'email': email,
        'recent_searches': recent_searches
    }
    
    response = dynamodb.Table(table_name).put_item(Item=user)
    
    return response