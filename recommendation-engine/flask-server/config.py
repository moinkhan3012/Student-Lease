import os

ES_HOST= os.getenv("ES_HOST")
ES_CA_CERT= os.getenv("ES_CA_CERT")
ES_USERNAME=os.getenv("ES_USERNAME")
ES_PASSWORD=os.getenv("ES_PASSWORD")
ES_INDEX=os.getenv("ES_INDEX")
BUCKET_NAME=os.getenv("BUCKET_NAME")
BUCKET_KEY=os.getenv("BUCKET_KEY")
AWS_ACCESS_KEY=os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY=os.getenv("AWS_SECRET_KEY")
COLUMNS = ['streetAddress','cityRegion','zipcode','bathrooms','bedrooms','description','homeStatus','latitude','livingArea','longitude','price','homeType','Month','Day','Year','preferences','laundary','amenities']
