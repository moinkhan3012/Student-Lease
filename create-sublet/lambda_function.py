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
table_name = 'Listings'
s3 = boto3.client('s3')
bucket_name = 'studentlease-listing-images1'
google_maps_api_key = ''

def lambda_handler(event, context):
    # print('event', event)
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
        if existing_listing:
            # Update existing listing
            updated_listing = update_listing(existing_listing, request_body, user_id)
            save_listing(updated_listing)
            update_index_listing(updated_listing)
        else:
            # Create new listing
            new_listing = create_listing(request_body, listing_id, user_id)
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
    url = 'https://search-test-elastic-ku7jpzixjyqgxg5oqye5fskm3u.aos.us-east-1.on.aws/sublets/_search'
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
            auth=HTTPBasicAuth('', '')
        )
        sublet_id = response.json()['hits']['hits']['_source']['id']
    except e:
        print('Error calling Elastic Search while retrieving listing id')
    
    esUrl = f"https://search-test-elastic-ku7jpzixjyqgxg5oqye5fskm3u.aos.us-east-1.on.aws/sublets/_update/{sublet_id}"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'id': listing['id'],
        'monthlyRent': listing['monthlyRent'],
        'leaseDuration': listing['leaseDuration'],
        'bedrooms': listing['bedrooms'],
        'bathrooms': listing['bathrooms'],
        'dateAvailable': listing['dateAvailable'],
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
        auth=HTTPBasicAuth('', '')
    )
    
def create_listing(request_body, listing_id, user_id):
    # Geocode address to get latitude and longitude
    latitude, longitude = geocode_address(request_body.get('address'))
    if latitude is None or longitude is None:
        raise Exception('Geocoding failed')
    # Upload images to S3 bucket and get URLs
    image_urls = upload_images(request_body.get('images', []))
    print('image_urls', image_urls)
    # Construct the item to be inserted into DynamoDB
    listing_item = {
        'id': listing_id,
        'user_id': user_id,  # Include user ID
        'title': request_body['title'],
        'address': request_body.get('address', None),
        'latitude': latitude,
        'longitude': longitude,
        'monthlyRent': request_body.get('monthlyRent', None),
        'roomType': request_body.get('roomType', None),
        'securityDeposit': request_body.get('securityDeposit', None),
        'bedrooms': request_body.get('bedrooms', None),
        'bathrooms': request_body.get('bathrooms', None),
        'squareFeet': request_body.get('squareFeet', None),
        'dateAvailable': request_body.get('dateAvailable', None),
        'leaseDuration': request_body.get('leaseDuration', None),
        'images': image_urls,
        'amenities': request_body.get('amenities', {}),
        'preferences': request_body.get('preferences', {}),
        'detailedDescription': request_body.get('detailedDescription', None)
    }
    return listing_item
    
def index_listing(listing):
    esUrl = "https://search-test-elastic-ku7jpzixjyqgxg5oqye5fskm3u.aos.us-east-1.on.aws/sublets/_doc"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'id': listing['id'],
        'monthlyRent': listing['monthlyRent'],
        'leaseDuration': listing['leaseDuration'],
        'bedrooms': listing['bedrooms'],
        'bathrooms': listing['bathrooms'],
        'dateAvailable': listing['dateAvailable'],
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
        auth=HTTPBasicAuth('', '')
    )

def update_listing(existing_listing, request_body, user_id):
    # Update existing listing attributes
    existing_listing['title'] = request_body.get('title')
    existing_listing['address'] = request_body.get('address', None)
    # Geocode address to get latitude and longitude
    latitude, longitude = geocode_address(request_body.get('address'))
    if latitude is not None and longitude is not None:
        existing_listing['latitude'] = latitude
        existing_listing['longitude'] = longitude
    # Upload new images to S3 bucket and update image URLs
    new_image_urls = upload_images(request_body.get('images', []))
    existing_listing['images'].extend(new_image_urls)
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
        image_key = str(uuid.uuid4()) + '.jpg'  # Generate a unique key for the image
        # image_key = "test1.jpg"
        # binary_data = base64.b64decode(image_data)
        try:
            response = s3.put_object(Body=image_data, Bucket=bucket_name, Key=image_key)
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"  # Construct the URL of the uploaded image
            image_urls.append(image_url)
            return image_urls
        except Exception as e:
            print('Error uploading file to S3: {}'.format(str(e)))
            return image_urls