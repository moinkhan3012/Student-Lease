from flask import Flask, request, json
import cloudpickle
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()


from config import ES_CA_CERT, ES_INDEX, ES_HOST, ES_PASSWORD, ES_USERNAME
from elasticSearchWrapper import ElasticSearchWrapper


app = Flask(__name__)


def load_pipeline():
        
    with open('./data/pipeline.pkl', 'rb') as file:
        pipeline = cloudpickle.load(file)
    return pipeline

#load pipeline
pipeline = load_pipeline()

#make elasticsearch connection
es = ElasticSearchWrapper(host=ES_HOST,
        ca_certs=ES_CA_CERT,
        http_auth=(ES_USERNAME, ES_PASSWORD))


columns = ['streetAddress','cityRegion','zipcode','bathrooms','bedrooms','description','homeStatus','latitude','livingArea','longitude','price','homeType','Month','Day','Year','preferences','laundary','amenities']

@app.route('/embeddings', methods = ['POST'])
def embeddings():
    try:
        df = pd.DataFrame([request.json])
        
        embedding = pipeline.transform(df)
        response = {
            
            'embedding': embedding.ravel().tolist()
        }


        print(response)
        return (json.dumps(response), 200)

    except Exception as err:
        response = {
            "message": "Internal Server error",
            "err": err.__str__()
        }
        return (json.dumps(response), 500)


@app.route('/recommendation', methods = ['GET'])
def recommmendation():
    #data_item list
    try:
        print(request)

        item_list = request.json["item_list"]
        print(item_list)
        result = es.search_by_id(ES_INDEX, item_list)
        print(result)

        embeddings =  np.array([ res['_source']['embedding'] for res in result['hits']['hits']]).mean(axis=0)
        
        
        response = es.recommend(ES_INDEX, embeddings)
        return (json.dumps(response.body), 200)

    except Exception as err:
        response = {
            "message": "Internal Server error",
            "err": err.__str__()
        }
        
        print(response)
        return (json.dumps(response), 500)


if __name__ == "__main__":
        
    app.run("0.0.0.0", port=5000)