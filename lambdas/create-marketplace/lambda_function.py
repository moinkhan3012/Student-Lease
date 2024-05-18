import json
import boto3
import base64
import geopy
from geopy.geocoders import Photon
from geopy.exc import GeocoderTimedOut
import requests
from requests.auth import HTTPBasicAuth
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = 'Marketplace'
s3 = boto3.client('s3')
bucket_name = 'studentlease-listing-images1'
rekognitionClient = boto3.client('rekognition')

def lambda_handler(event, context):
        print('event', event)
    # try:
        request_body = event
        
        if 'title' not in request_body:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Title is required'})
            }
        user_id = ''
        if 'requestContext' in event:
            user_id = event['requestContext']['authorizer']['userId']  # Assuming user ID is included in the authorization context
        listing_id = request_body.get('id') or str(uuid.uuid4())
        # Check if listing already exists
        existing_listing = get_listing(listing_id)
        print('existing_listing', existing_listing)
        if existing_listing:
            # Update existing listing
            updated_listing = update_listing(existing_listing, request_body, user_id)
            # updated_listing = 
            print("updated_listing", updated_listing)
            update_index_listing(updated_listing)
            updated_listing['latitude'] = str(updated_listing['latitude'])
            updated_listing['longitude'] = str(updated_listing['longitude'])
            save_listing(updated_listing)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Listing updated successfully', 'listingId': listing_id})
            }
        else:
            # Create new listing
            new_listing = create_listing(request_body, listing_id, user_id)
            # print(new_listing)
            # return new_listing
            index_listing(new_listing)
            new_listing['latitude'] = str(new_listing['latitude'])
            new_listing['longitude'] = str(new_listing['longitude'])
            save_listing(new_listing)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Listing saved successfully', 'listingId': listing_id})
            }
    # except Exception as e:
    #     print('Error saving listing:', e)
    #     return {
    #         'statusCode': 500,
    #         'body': json.dumps({'message': 'Internal server error'})
    #     }
def get_listing(listing_id):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': listing_id})
    return response.get('Item')
    

def update_index_listing(listing):
    url = 'https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.aos.us-east-1.on.aws/marketplace/_search'
    headers = {"Content-Type": "application/json"}
    body = {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    { "match": { "id": listing['id'] }}
                ]
            }
        }
    }
    sublet_id=''
    try:
        response = requests.get(
            url,
            data=json.dumps(body),
            headers=headers,
        auth=HTTPBasicAuth('sublease', 'Elasticsearch@1')
        )
        sublet_id = response.json()['hits']['hits'][0]['_id']
        print("sublet_id", sublet_id)
    except:
        print('Error calling Elastic Search while retrieving listing id')
    
    esUrl = f"https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.aos.us-east-1.on.aws/marketplace/_update/{sublet_id}"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'id': listing['id'],
        'price': listing['price'],
        'labels': listing['labels'],
        'location': {
            'lon': listing['longitude'],
            'lat': listing['latitude']
        }
    }
    updated_doc = {
        "doc": esDoc
    }
    print(esDoc)
    response = requests.post(
        esUrl,
        json = updated_doc,
        # data=json.dumps(esDoc).encode("utf-8"),
        headers=headers,
        auth=HTTPBasicAuth('sublease', 'Elasticsearch@1')
    )
    
def detectLabels(images):
    labels = set()
    for i in images:
        image_binary = base64.b64decode(i)
        response = rekognitionClient.detect_labels(
                Image={
                    'Bytes': image_binary
                }, 
                MaxLabels = 10
                )
        # print([j['Name'].lower() for j in response['Labels']])
        for j in response['Labels']:
            labels.add(j['Name'].lower())
        # labels.add([j['Name'].lower() for j in response['Labels']])
    return list(labels)
    
def create_listing(request_body, listing_id, user_id):
    # Geocode address to get latitude and longitude
    latitude, longitude = geocode_address(request_body.get('address'))
    if latitude is None or longitude is None:
        raise Exception('Geocoding failed')
        
    labels = detectLabels(request_body.get('images', []))
    print(labels)
    
    # Upload images to S3 bucket and get URLs
    image_urls = upload_images(request_body.get('images', []))
    print('image_urls', image_urls)
    # Construct the item to be inserted into DynamoDB
    listing_item = {
        'id': listing_id,
        'user_id': request_body['user_id'],  # Include user ID
        'title': request_body['title'],
        'address': request_body.get('address', None),
        'latitude': latitude,
        'longitude': longitude,
        'price': request_body.get('price', None),
        'images': image_urls,
        'detailedDescription': request_body.get('detailedDescription', None),
        'labels': labels
    }
    return listing_item
    
def index_listing(listing):
    # https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.us-east-1.es.amazonaws.com
    esUrl = "https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.aos.us-east-1.on.aws/marketplace/_doc"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'id': listing['id'],
        'price': listing['price'],
        'labels': listing['labels'],
        'location': {
            'lon': listing['longitude'],
            'lat': listing['latitude']
        }
    }
    print(esDoc)
    response = requests.post(
        esUrl,
        data=json.dumps(esDoc).encode("utf-8"),
        headers=headers,
        auth=HTTPBasicAuth('sublease', 'Elasticsearch@1')
    )
    print(response)

def update_listing(existing_listing, request_body, user_id):
    # Update existing listing attributes
    existing_listing['title'] = request_body.get('title')
    existing_listing['address'] = request_body.get('address', None)
    
    latitude, longitude = geocode_address(request_body.get('address'))
    if latitude is None or longitude is None:
        raise Exception('Geocoding failed')
        
    new_labels = detectLabels(request_body.get('images', []))
    unique_labels = [i for i in new_labels if i not in existing_listing['labels']]
    print(new_labels) 
    
    new_image_urls = upload_images(request_body.get('images', []))
    existing_listing['images'].extend(new_image_urls)
    
    existing_listing['latitude'] = latitude
    existing_listing['longitude'] = longitude
    
    # Upload images to S3 bucket and get URLs
    # image_urls = upload_images(request_body.get('images', []))
    # print('image_urls', image_urls)
    # Construct the item to be inserted into DynamoDB
    
    existing_listing['price'] = request_body.get('price', None)
    
    existing_listing['detailedDescription']: request_body.get('detailedDescription', None)
    existing_listing['labels'].extend(unique_labels) 
    
    
    
    
    
    
    return existing_listing

def save_listing(listing_item):
    # Save the listing item to DynamoDB
    dynamodb.Table(table_name).put_item(Item=listing_item)

def geocode_address(address):
    geolocator = Photon(user_agent="myGeocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print("Geocoding service timed out")
        return None, None
    
def upload_images(images):
    image_urls = []
    
    for image_data in images:
        
        binary_data = base64.b64decode(image_data)
        
        
        mime_type = None
        if binary_data.startswith(b'\xFF\xD8'):
            mime_type = 'image/jpeg'
        elif binary_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
            mime_type = 'image/png'
        else:
            print('Unsupported file format.')
            continue
        
        file_extension = '.jpg' if mime_type == 'image/jpeg' else '.png'

        
        image_key = str(uuid.uuid4()) + file_extension  # Generate a unique key for the image
        
        try:
            response = s3.put_object(Body=binary_data, Bucket=bucket_name, Key=image_key)
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"  # Construct the URL of the uploaded image
            image_urls.append(image_url)
            print("s3response", response)
            print("image_urls", image_urls)
            
        except Exception as e:
            print('Error uploading file to S3: {}'.format(str(e)))
            # return image_urls
            
    return image_urls