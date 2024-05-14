import json 
import boto3
from boto3.dynamodb.conditions import Attr
import requests
import base64
from requests.auth import HTTPBasicAuth
from boto3.dynamodb.conditions import Key
import io
import decimal

import os 
EC2_RECCO = os.getenv('EC2_RECCO')


s3 = boto3.client('s3')
bucket_name = 'studentlease-listing-images1'
dynamodb = boto3.resource('dynamodb')


# Lambda handler
def lambda_handler(event, context):
    
    user_info = get_user(event)
    
    if user_info:
        user_id = user_info['user_id']
        top_searches = user_info['top_searches']
        
        if top_searches: 
            print('hello')
            
            top_data = {
                "item_list": top_searches
            }
            
            url = EC2_RECCO + "/api/recommendation"
            
            response = requests.post(
            url,
            data=json.dumps(top_data),
            headers={'Content-Type': 'application/json'}
            )
            
            print("ec2 response", response.json())
            
            listings = [id['fields']['id'][0] for id in response.json()['hits']['hits']]
            
            print('listings', listings)
            
            details = get_details(listings)
            print(details[0])
            # Query Elasticsearch for vector embeddings of apartments
            # apartment_embeddings = query_apartment_embeddings(top_searches)
            # print('apartment_embeddings',apartment_embeddings[0][:3])
            
            
            
            
            
            # Now get reccomendations and return to frontend
            
            # return {
            #     'statusCode': 200,
            #     'body': {
            #         'user_id': user_id,
            #         'apartment_embeddings': apartment_embeddings
            #     }
            # }
        else:
            
            top_viewed_listings = get_top_viewed_listings()
            print('top_viewed_listings', top_viewed_listings)
            
            details = get_details(top_viewed_listings)
            print(details[0])
            # x = [i for i in details[0].values() if i.type() == 'Decimal']
            # print(x)
            # Handle the case when top_searches is empty
        return {
            'statusCode': 200,
            'body': {
                'user_id': user_id,
                'message': json.dumps(details) 
            }
        }
    else:
        # Handle the case when user information is not found
        
        
        return {
            'statusCode': 404,
            'body': {
                'error': 'User not found'
            }
        }
        


def get_user(event):
    try:
        # Extract email from event
        email = event['reqBody']['email']

        # Retrieve user ID
        user = retrieve_user(email)
        user_id = user['user_id']
        top_searches = user['recent_searches'] 
        # print(top_searches)

        return {
            'user_id': user_id,
            'top_searches': top_searches
        }
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        print(error_message)
        return None

def retrieve_user(email):
    table = dynamodb.Table('user_table')

    response = table.scan(
        FilterExpression=Attr('email').eq(email)
    )

    if 'Items' in response and len(response['Items']) > 0:
        return response['Items'][0]
    else:
        return None

def query_apartment_embeddings(listing_ids):
    embeddings = []
    for listing_id in listing_ids:
        # Query Elasticsearch for vector embeddings of the apartment with the given listing ID
        url = f'https://search-sublease-3f4v5554g2z6jojki2xbdd5jfu.us-east-1.es.amazonaws.com/sublease/_search'
        query = {
            "query": {
                "match": {
                    "id": listing_id
                }
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
            url, 
            data=json.dumps(query), 
            headers=headers,
            auth=HTTPBasicAuth('sublease', 'Elasticsearch@1')
        )
                                
        if response.status_code == 200:
            hits = response.json()['hits']['hits']
            # print(hits)
            if hits:
                embedding = hits[0]['_source']['embedding']
                embeddings.append(embedding)
    return embeddings
    
    
def get_top_viewed_listings():
    # Query Elasticsearch for the top 10 most viewed listings
    url = f'https://search-sublease-3f4v5554g2z6jojki2xbdd5jfu.us-east-1.es.amazonaws.com/sublease/_search'
    query = {
        "size": 10,
        "sort": [
            {"timesVisited": {"order": "desc"}}
        ],
        "_source": ["id"]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.get(
        url, 
        data=json.dumps(query), 
        headers=headers,
        auth=HTTPBasicAuth('sublease', 'Elasticsearch@1')
    )
                            
    if response.status_code == 200:
        hits = response.json()['hits']['hits']
        top_viewed_listing_ids = []
        for hit in hits:
            top_viewed_listing_ids.append(hit['_source']['id'])
        return top_viewed_listing_ids
    else:
        return None
        
def fetch_s3_object_as_base64(key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        print('fetch_s3_object_as_base64', response)
        binary_image_data = response['Body'].read()

        # Encode the binary image data into a Base64 string
        base64_image_data = base64.b64encode(binary_image_data).decode('utf-8')
        
        return base64_image_data
    except Exception as e:
        print(f"Error fetching S3 object: {e}")
        return None        
        
def get_details(listing_ids):
    
    apartment_details = []
    for apartment_id in listing_ids:
        table = dynamodb.Table('Listings')
        
        response = table.query(KeyConditionExpression = Key('id').eq(apartment_id))
        print('dynamodb response', response)
        apartment_info = response['Items'][0]
        # print('apartment_info',apartment_info)
        
        
        for item in apartment_info: 
            if isinstance(apartment_info[item], decimal.Decimal):
                apartment_info[item] = float(apartment_info[item]) 
                
            
            
            # for key, value in item.items():
            #     if isinstance(value, decimal.Decimal):
            #         # Convert decimal value to float or int
            #         item[key] = float(value)
        
        
        
        
        
        print('apartment_info', apartment_info)
        # Fetch images from S3 and encode them as base64 strings
        image_urls = apartment_info.get('images', {})
        print('image_urls')
        base64_images = []
        print('image_urls', image_urls)
        for image_url in image_urls:
            print('image_url', image_url)
            key = image_url.split('/')[-1]
            print('key', key)
            base64_image = fetch_s3_object_as_base64(key)
            # print('base64_image', base64_image) #??
            if base64_image:
                base64_images.append(base64_image)
#     #     # Add base64 encoded images to the apartment details
            apartment_info['base64_images'] = base64_images
            apartment_details.append(apartment_info)
            # print('apartment_details', apartment_details)
#     # Prepare response
    print('details', apartment_details)
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps({'details': apartment_details})
    # }
    # return response
    return apartment_details