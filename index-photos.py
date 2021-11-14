import json
import boto3
import data_index
import time
import logging
import requests


s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_url(index, type):
    url = 'https://search-photos-fuuaaoxluhdwdu3vwewdnnkh7y.us-east-1.es.amazonaws.com' + '/' + index + '/' + type
    return url

def lambda_handler(event, context):
    print(event)
    label_list=[]
    
    for record in event['Records']:
        PHOTO_BUCKET = record['s3']['bucket']['name']
        FILE_NAME = record['s3']['object']['key']

    print('reading image: {} from s3 bucket {}'.format(FILE_NAME, PHOTO_BUCKET))
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': PHOTO_BUCKET,
                'Name': FILE_NAME
            }
        },
        MaxLabels=10,
        MinConfidence=80
    )
    
    print(response)
    
    print('Detected labels for ' + FILE_NAME)
    logger.info('Detected labels for ' + FILE_NAME)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        logger.info(label['Name'] + ' : ' + str(label['Confidence']))
        label_list.append(label['Name'])
    
    ts = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%S", ts)
    logger.info('Image created at {}....'.format(created_time))
    
    image_object = {
        'objectKey':FILE_NAME,
        'bucket':PHOTO_BUCKET,
        'createdTimestamp':created_time,
        'labels':label_list
    }
    
    # es = data_index.connect_to_elastic_search()
    # es.index(index="photos", doc_type="_doc", id=created_time, body=image_object)

    # response = es.get(index="photos", doc_type="_doc", id=created_time)
    
    url = r'https://search-photos-fuuaaoxluhdwdu3vwewdnnkh7y.us-east-1.es.amazonaws.com/photos/_doc'
    print("ES URL --- {}".format(url))
    obj = json.dumps(image_object)
    headers = { "Content-Type": "application/json" }
    
    

    req = requests.post(url, data=obj, headers=headers, auth=requests.auth.HTTPBasicAuth("Tian", "Xt998328!"))
    
        
    print("Success: ", req)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        'body': json.dumps("Image labels have been successfully detected!")
    }