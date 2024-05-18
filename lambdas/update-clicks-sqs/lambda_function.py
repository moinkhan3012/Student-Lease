import json
import boto3

def lambda_handler(event, context):
    sqs_queue_name = 'ListingClicks'
    print('event',event)
    if 'listing_id' in event:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
        listing_id = event['listing_id']
        user_id = event['user_id']
        response = queue.send_message(MessageBody='listing clicked', MessageAttributes={
            'listing_id': {
                'StringValue': listing_id,
                'DataType': 'String'
            },
            
            'user_id':{
                'StringValue': user_id,
                'DataType': 'String'
            }
        })
        print('sqs response', response)
        return {
            'statusCode': 200,
            'body': json.dumps('Added to queue')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing listingId')
        }
