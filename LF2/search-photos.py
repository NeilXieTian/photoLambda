import json
import boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    Res = []
    lexbot = boto3.client('lexv2-runtime')
    search_query = event['q']
    response = lexbot.recognize_text(
        botId = 'XBEMOKGR56',
        botAliasId = 'TSTALIASID',
        localeId = 'en_US',
        sessionId = 'test',
        text = search_query)
    
    keys = []
    for each in response['interpretations'][0]['intent']['slots']['feature']['values']:
	    keys.append(each['value']['interpretedValue'])
    
    out = []
    outstring = ""
    outresult = []
    for i in range(len(keys)):
        k = keys[i]
        url = f'https://search-photos-fuuaaoxluhdwdu3vwewdnnkh7y.us-east-1.es.amazonaws.com/photos/_search?q={k}'
        response = requests.get(url, auth=("Tian", "Xt998328!"))
        res = json.loads(response.content.decode('utf-8'))
        Res.append(res)
        for i in res['hits']['hits']:
            bucket = i['_source']['bucket']
            image = i['_source']['objectKey']
            a = "https://s3.amazonaws.com/" + bucket + "/" + image
            if a not in out:
                out.append(a)
                if outstring=="":
                    outstring += a 
                else:
                    outstring += ", " + a 
                outresult.append(a)
    
    result = {
        "statusCode": 200,
        'body': {
            'results': json.dumps(outresult),
        },
        'headers': {
            'Access-Control-Allow-Headers' : 'Access-Control-Allow-Origin, Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, GET'
        }
    }
    
    result = {
        'results': outresult
        
    }
    return result
