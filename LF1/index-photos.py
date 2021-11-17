import boto3
import logging
import json
import time
import requests

s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    print('abc')
    label_list=[]
    for record in event['Records']:
        photo_bucket = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']
        response = s3_client.head_object(Bucket = photo_bucket, Key = file_name)
        
        metadata = response.get('Metadata', None)
        if metadata and metadata.get('customlabels', False):
            custom_labels = (''.join(response['Metadata']['customlabels'])).split(', ')
        else:
            custom_labels = []
    
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': photo_bucket,
                'Name': file_name
            }
        },
        MaxLabels=10,
        MinConfidence=90
    )
    
    logger.info('Detected labels for ' + file_name)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        logger.info(label['Name'] + ' : ' + str(label['Confidence']))
        label_list.append(label['Name'])
    
    created_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    logger.info('Image created at {}....'.format(created_time))
    
    label_list += custom_labels
    
    image_object = {
        'objectKey':file_name,
        'bucket':photo_bucket,
        'createdTimestamp':created_time,
        'labels': label_list
    }
    url = r'https://search-photos-fuuaaoxluhdwdu3vwewdnnkh7y.us-east-1.es.amazonaws.com/photos/_doc'
    obj = json.dumps(image_object)
    headers = {"Content-Type": "application/json"}
    req = requests.post(url, data = obj, headers = headers, auth = requests.auth.HTTPBasicAuth("Tian", "Xt998328!"))
    
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        'body': json.dumps("Image labels have been successfully detected!")
    }
