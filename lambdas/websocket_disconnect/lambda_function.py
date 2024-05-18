import boto3

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserConnection')
    response = table.get_item(Key={'connectionId': connection_id})
    table2 = dynamodb.Table('UserConnections')
    item = response.get('Item', {})
    table2.delete_item(Key={'userId':item['userId']})
    table.delete_item(Key={'connectionId': connection_id})
    return {'statusCode': 200} 