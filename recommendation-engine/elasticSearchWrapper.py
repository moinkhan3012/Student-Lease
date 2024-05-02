from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

class ElasticSearchWrapper:
    def __init__(self, host, ca_certs, http_auth: iter):
        print(host, ca_certs, http_auth)
        self.client = Elasticsearch(
            host,
            ca_certs=ca_certs,
            http_auth=http_auth
        )
        
    def create_index(self, index, properties):
        doc = {
          "settings": {
            "number_of_shards": 1
          },
          "mappings": {
            "properties": properties
          }
        }
        
        try:
            return self.client.indices.create(index=index,  body=doc)
        
        except Exception as err:
            print(err)
            return False
    
    def delete_index(self, index):
        try:
            return self.client.indices.delete(index=index)
        except Exception as err:
            print(err)
            return False
        
    def add_documents(self, documents):
        try:
            return bulk(self.client, documents)
        except Exception as err:
            print(err)
            return False
        
    def recommend(self, index, query_vector, k=50,num_candidates=50, stored_fields=[]):
        
        search_query = {
            "knn": {
                    'field': 'embedding',
                    'query_vector': query_vector,
                    'num_candidates': num_candidates,
                    'k': k,
            },
            "stored_fields": stored_fields,
        }
            
        return self.client.search(index=index, body=search_query)
    
    
    def search(self, index, query):
        return self.client.search(index=index, body=query)
        
    
    def search_by_id(self, index, id_list):
        query_template = {
            "query": {
                "terms": {
                "_id": id_list
                }
            } 
        }       
        print(query_template)
        return self.client.search(index=index, body=query_template)
