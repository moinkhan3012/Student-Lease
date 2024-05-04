from flask import Flask, request, json
from flask_swagger_ui import get_swaggerui_blueprint
from elasticSearchWrapper import ElasticSearchWrapper
import cloudpickle
import pandas as pd
import numpy as np
import boto3

from dotenv import load_dotenv
load_dotenv()


from config import COLUMNS, ES_CA_CERT, ES_INDEX, ES_HOST, \
    ES_PASSWORD, ES_USERNAME, BUCKET_NAME, BUCKET_KEY, \
    AWS_ACCESS_KEY, AWS_SECRET_KEY

app = Flask(__name__)

#swagger 
SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

import boto3
import cloudpickle

def load_pipeline_from_s3(bucket_name, key):
    """
    Load a pre-trained pipeline object from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        key (str): The key (path) of the object in the S3 bucket.

    Returns:
        pipeline: The pre-trained pipeline object loaded from S3.

    Raises:
        botocore.exceptions.ClientError: If an error occurs while accessing S3.
        cloudpickle.pickle.UnpicklingError: If an error occurs while unpickling the pipeline object.
    """
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    # Get the object from S3
    obj = s3.get_object(Bucket=bucket_name, Key=key)

    # Load the pipeline object from the object's Body
    pipeline = cloudpickle.loads(obj['Body'].read())

    return pipeline


#load pipeline
pipeline = load_pipeline_from_s3(BUCKET_NAME, BUCKET_KEY)

#make elasticsearch connection
es = ElasticSearchWrapper(host=ES_HOST,
        ca_certs=ES_CA_CERT,
        http_auth=(ES_USERNAME, ES_PASSWORD))

@app.route("/api")
def home():
    return (json.dumps({
        "message": "app up and running successfully"
    }), 200)

@app.route('/api/embeddings', methods=['POST'])
def embeddings():
    """
    Endpoint for generating embeddings from JSON data.

    This endpoint accepts a JSON payload containing property details,
    converts it into a DataFrame, transforms it using a pre-trained pipeline,
    and returns the generated embeddings.

    Args:
        None

    Returns:
        A JSON response containing the generated embeddings.
        If successful, the response will have a status code of 200.
        If an internal server error occurs, the response will have a status code of 500.

    Raises:
        None

    Expected JSON Request Format:
        {
            "streetAddress": "string",
            "cityRegion": "string",
            "zipcode": float,
            "bathrooms": float,
            "bedrooms": float,
            "description": "string",
            "homeStatus": int,
            "latitude": float,
            "livingArea": float,
            "longitude": float,
            "price": float,
            "homeType": "string",
            "Month": int,
            "Day": int,
            "Year": int,
            "preferences": "string",
            "laundary": int,
            "amenities": "string"
        }
    """
    try:
        df = pd.DataFrame([request.json])
        
        embedding = pipeline.transform(df[COLUMNS])
        response = {
            'embedding': embedding.ravel().tolist()
        }

        return (json.dumps(response), 200)

    except Exception as err:
        response = {
            "message": "Internal Server error",
            "err": err.__str__()
        }
        return (json.dumps(response), 500)


@app.route('/api/recommendation', methods=['POST'])
def recommmendation():
    """
    Endpoint for getting recommendations based on item list.

    This endpoint accepts a JSON payload containing a list of item IDs,
    retrieves embeddings for these items from Elasticsearch, calculates
    the mean embedding, and then returns recommendations based on this
    mean embedding.

    Args:
        None

    Returns:
        A JSON response containing the recommendations.
        If successful, the response will have a status code of 200.
        If an internal server error occurs, the response will have a status code of 500.

    Raises:
        None

    Expected JSON Request Format:
        {
            "item_list": [
                "item_id_1",
                "item_id_2",
                ...
            ]
        }
    """
    try:
        item_list = request.json["item_list"]
        result = es.search_by_id(ES_INDEX, item_list)

        embeddings = np.array([res['_source']['embedding'] for res in result['hits']['hits']]).mean(axis=0)

        response = es.recommend(ES_INDEX, embeddings)
        return (json.dumps(response.body), 200)

    except Exception as err:
        response = {
            "message": "Internal Server error",
            "err": err.__str__()
        }

        return (json.dumps(response), 500)



if __name__ == "__main__":
        

    app.run("0.0.0.0", port=8000)