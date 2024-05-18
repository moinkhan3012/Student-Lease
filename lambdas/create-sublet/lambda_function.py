import json
import boto3
import base64
import geopy
from geopy.geocoders import Photon, OpenCage
from geopy.exc import GeocoderTimedOut
import requests
from requests.auth import HTTPBasicAuth
import uuid
from decimal import Decimal
from datetime import datetime

import os 
EC2_RECCO = os.getenv('EC2_RECCO')
# print(EC2_RECCO)



dynamodb = boto3.resource('dynamodb')
table_name = 'Listings'
s3 = boto3.client('s3')
bucket_name = 'studentlease-listing-images1'

def lambda_handler(event, context):
        print(os.environ)
        print('event', event)
    # try:
        request_body = event['reqBody']
        if 'title' not in request_body:
            print('no title in request_body')
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
            print('new_listing', new_listing)
            embeddings = get_embeddings(new_listing)
            
            index_listing(new_listing, embeddings)
            new_listing['latitude'] = str(new_listing['latitude'])
            new_listing['longitude'] = str(new_listing['longitude'])
            save_listing(new_listing)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Listing saved successfully', 'ListingId': listing_id})
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
    city, zipcode = get_city_zip(latitude, longitude)
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
        'city': city,
        'zipcode': zipcode,
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
        'detailedDescription': request_body.get('detailedDescription', None),
        'timesVisited': 0 
    }
    return listing_item
    
def index_listing(listing, embeddings):
    # https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.us-east-1.es.amazonaws.com
    # esUrl = "https://search-search-test-elastic1-dedivdy53hkcwdyfce4yy7m36m.aos.us-east-1.on.aws/sublets/_doc"
    esUrl = "https://search-sublease-3f4v5554g2z6jojki2xbdd5jfu.us-east-1.es.amazonaws.com/sublease/_doc"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'id': listing['id'],
        'monthlyRent': listing['monthlyRent'],
        'leaseDuration': listing['leaseDuration'],
        'bedrooms': listing['bedrooms'],
        'bathrooms': listing['bathrooms'],
        'dateAvailable': listing['dateAvailable'],
        'embedding': embeddings,
        'timesVisited': listing['timesVisited'],
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
    
def get_embeddings(listing):
    url = EC2_RECCO + "/api/embeddings"
    
    
    true_keys = [key.lower() for key, value in listing['amenities'].items() if value]
    amenities = ",".join(true_keys)
    true_keys = [key.lower() for key, value in listing['preferences'].items() if value]
    preferences = ",".join(true_keys)
    
    print(listing['dateAvailable'])
    date_object = datetime.strptime(listing['dateAvailable'],"%Y-%m-%d")

    year = date_object.year
    month = date_object.month
    day = date_object.day

    
    # year, month, day  = listing['dateAvailable'].split("-")
    
    
    embedding_item = {
        "streetAddress": listing['address'],
        "cityRegion": listing['city'],
        "zipcode": listing['zipcode'],
        "bathrooms": listing['bathrooms'],
        "bedrooms": listing['bedrooms'],
        "description": listing['detailedDescription'],
        "homeStatus": 1,
        "latitude": listing['latitude'],
        "livingArea": listing['squareFeet'],
        "longitude": listing['longitude'],
        "price": listing['monthlyRent'],
        'leaseDuration': listing[ 'leaseDuration'],
        "homeType": listing['roomType'].lower(), 
        "Month": month,
        "Day": day,
        "Year": year,
        "preferences": preferences,
        "amenities": amenities
    }
    
    # print("embedding_item",json.dumps(embedding_item))
    
    
    
    
    
     
    
    response = requests.post(
            url,
            data=json.dumps(embedding_item),
            headers={'Content-Type': 'application/json'}
            )
            
    print("EC2 response",response.json()) 
    
    if response.status_code == 200:
        return response.json()['embedding']
        
    else:
        print(response.json())
        return None
        
    
    
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
        
def get_city_zip(lat, lon):
    # geolocator = Photon(user_agent="measurements")
    geolocator = OpenCage(api_key='ba33ad8a168544dd95143ebfd51bd20f')

    
    try:
        res= geolocator.reverse((str(lat),str(lon)), exactly_one=True)
        # res= geolocator.reverse(('40.877742767333984', '-73.9108657836914'))

        
        # print(res.raw)
        
       
        
        if res:
            locality = res.raw['components'].get('county',res.raw['components'].get('neighbourhood',res.raw['components'].get('city',None)))
            
            return locality , res.raw['components']['postcode']
        
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