from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

class ElasticSearchWrapper:
    def __init__(self, host, http_auth: iter):
        """
        Initialize the ElasticSearchWrapper.

        Args:
            host (str): The hostname of the Elasticsearch cluster.
            ca_certs (str): The path to the CA certificate file.
            http_auth (iter): An iterable containing the HTTP authentication credentials.

        Returns:
            None
        """
        self.client = Elasticsearch(
                host,
                http_auth=http_auth,
                use_ssl=True,
                verify_certs=False  # Not recommended for production use
            )
        
    def create_index(self, index, properties):
        """
        Create an index in Elasticsearch.

        Args:
            index (str): The name of the index to create.
            properties (dict): The mapping properties for the index.

        Returns:
            bool: True if the index creation was successful, False otherwise.
        """
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
        """
        Delete an index from Elasticsearch.

        Args:
            index (str): The name of the index to delete.

        Returns:
            bool: True if the index deletion was successful, False otherwise.
        """
        try:
            return self.client.indices.delete(index=index)
        except Exception as err:
            print(err)
            return False
        
    def add_documents(self, documents):
        """
        Add documents to Elasticsearch in bulk.

        Args:
            documents (iter): An iterable of documents to add.

        Returns:
            bool: True if the bulk insertion was successful, False otherwise.
        """
        try:
            return bulk(self.client, documents)
        except Exception as err:
            print(err)
            return False
        
    def recommend(self, index, query_vector, k=50,num_candidates=50, stored_fields=[]):
        """
        Perform a nearest neighbor search in Elasticsearch.

        Args:
            index (str): The name of the index to search.
            query_vector (list): The query vector for the nearest neighbor search.
            k (int): The number of nearest neighbors to retrieve.
            num_candidates (int): The number of candidates to retrieve.
            stored_fields (list): A list of fields to retrieve from the search results.

        Returns:
            dict: The search results.
        """
        search_query = {
            "size": num_candidates,
            "query": {
                "knn": {
                    "embedding": {
                    "vector": query_vector,
                    "k": k
                    }
                }
            },
            "_source": False,
            "fields": stored_fields
        }    

            
        return self.client.search(index=index, body=search_query)
    
    
    def search(self, index, query):
        """
        Perform a search in Elasticsearch.

        Args:
            index (str): The name of the index to search.
            query (dict): The search query.

        Returns:
            dict: The search results.
        """
        return self.client.search(index=index, body=query)
        
    
    def search_by_id(self, index, id_list):
        """
        Perform a search by document IDs in Elasticsearch.

        Args:
            index (str): The name of the index to search.
            id_list (list): A list of document IDs to search for.

        Returns:
            dict: The search results.
        """
        
        query_template = {
            "_source": ["embedding"],
            "query": {
                "terms": {
                "id.keyword": id_list
                }
            } 
        }       

        return self.client.search(index=index, body=query_template)
