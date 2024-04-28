import json
import boto3
import requests
import base64
from requests.auth import HTTPBasicAuth
import geopy
from geopy.geocoders import Photon
from geopy.exc import GeocoderTimedOut
from boto3.dynamodb.conditions import Key
import io

esUrl = "https://search-test-elastic-ku7jpzixjyqgxg5oqye5fskm3u.aos.us-east-1.on.aws/sublets/_search"
dynamo = boto3.resource('dynamodb')
dynamodb = dynamo.Table('Listings')
s3 = boto3.client('s3')
# bucket_name = 'studentlease-listing-images1'

def fetch_s3_object_as_base64(key):
    try:
        response = s3.get_object(Bucket='studentlease-listing-images1', Key=key)
        print('fetch_s3_object_as_base64', response)
        image_content = response['Body'].read().decode('utf-8')
        # print('image_content', image_content)
        # base64_image = base64.b64encode(image_content).decode('utf-8')
        # print('base64_image', base64_image)
        # print('base64_image', base64_image)
        return image_content
    except Exception as e:
        print(f"Error fetching S3 object: {e}")
        return None

def lambda_handler(event, context):
    # Extract search parameters from the event
    print('here')
    search_params = event
    lat, lon = geocode_address(search_params['location'])
    # Perform search in Elasticsearch
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"bedrooms": search_params['bedrooms']}},
                    {"range": {"monthlyRent": {"lte": int(search_params['monthlyRent'])}}},
                    {"range": {"bathrooms": {"gte": int(search_params['bathrooms'])}}},
                    {"range": {"dateAvailable": {"gte": search_params['dateAvailable']}}},
                    {"range": {"leaseDuration": {"gte": search_params['leaseDuration']}}}
                ],
                "filter": {
                    "geo_distance": {
                        "distance": "10km",
                        "location": {
                            "lon": lon,
                            "lat": lat
                        }
                    }
                }
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    search_result = requests.get(
        esUrl,
        data=json.dumps(body),
        headers=headers,
        auth=HTTPBasicAuth('', '')
    )
    # # Extract apartment IDs from search results
    print('search_result', search_result.json())
    apartment_details = []
    for hit in search_result.json()['hits']['hits']:
        apartment_id = hit['_source']['id']
        response = dynamodb.query(KeyConditionExpression = Key('id').eq(apartment_id))
        print('dynamodb response', response)
        apartment_info = response['Items'][0]
        print('apartment_info', apartment_info)
        # Fetch images from S3 and encode them as base64 strings
        image_urls = apartment_info.get('images', {})
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
    print('apartment_details', apartment_details)
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(apartment_details)
    # }
    # return response
    
    
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