import json
import boto3
import data_index
from botocore.vendored import requests

def lambda_handler(event, context):
    print(event)
    print(context)
    # print(event['queryStringParameters']['q'])
    # query = event['currentIntent']['slots']['feature']
    # if 'q' in event:
    #     keys = [event['q']]
    # else:
    #     query = event['sessionState']['intent']['slots']['feature']['values']
    #     print('query',query)
    
    #     keys = []
    #     for value in query:
    #         keys.append(value['value']['originalValue'])
    #     result = {
    #         "sessionState" : {
    #             "dialogAction":{
    #                 "type":"Close"
    #             },
    #             "intent": {
    #                 "confirmationState": "Confirmed",
    #                 "name": "SearchIntent",
    #                 "state":"Fulfilled"
    #             }
    #         },
    #         'messages': query
    #     }
    #     return result
        
    # keys = query.split(',')
    Res = []
    # es = data_index.connect_to_elastic_search()


    bot = boto3.client('lexv2-runtime')

    search_query = "show me water"# event['queryStringParameters']['q'] 

    response = bot.recognize_text(
        botId = 'XBEMOKGR56',
        botAliasId = 'TSTALIASID',
        localeId = 'en_US',
        sessionId = 'test',
        text = search_query)
    # return response
    
    keys = []
    for each in response['interpretations'][0]['intent']['slots']['feature']['values']:
	    keys.append(each['value']['interpretedValue'])
    

    
    out = []
    outS = ""
    outRes = []
    for i in range(len(keys)):
        print (keys[i])
        k = keys[i]
        url = f'https://search-photos-fuuaaoxluhdwdu3vwewdnnkh7y.us-east-1.es.amazonaws.com/photos/_search?q={k}'
        print("ES URL --- {}".format(url))
        response = requests.get(url, auth=("Tian", "Xt998328!"))
        res = json.loads(response.content.decode('utf-8'))
        Res.append(res)
        print(f"Got Hits: {res['hits']['total']}")
        print (res)
        for i in res['hits']['hits']:
            bucket = i['_source']['bucket']
            image = i['_source']['objectKey']
            a = "https://s3.amazonaws.com/" + bucket + "/" + image
            if a not in out:
                out.append(a)
                if outS=="":
                    outS += a 
                else:
                    outS += ", " + a 
                outRes.append(a)
                # outRes.append({
                #     # "contentType": "PlainText",
                #     "url": a,
                #     "label": k
                #     # "contentType": "ImageResponseCard", 
                    
                #     # "imageResponseCard": {
                #     #     "title": image.split(".")[0],
                #     #     "imageUrl": a,
                        
                #     # }
                # })
        print('File path: ', out)
        
    # if outRes==[]:
    #     outRes.append({"contentType":"PlainText", "content":'no photo found'})

    # res = {
    #           "results": json.dumps(outRes)
    #         }
    
    # return res
    
    result = {
        "statusCode": 200,
        'body': {
            'results': json.dumps(outRes),
        },
        'headers': {
            'Access-Control-Allow-Headers' : 'Access-Control-Allow-Origin, Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, GET'
        }
    }
    
    result = {
        # 'results': json.dumps(outRes)
        'results': outRes
        
    }
    
    
        # result[] = []
        # d= dict()
        # d["ImageResponseCard "] =  {
        #         'version': '0',
        #         'contentType': 'application/vnd.amazonaws.card.generic',
        #         'genericAttachments': outRes
        #     }
        # result['messages'].append(d)
    
    print(result)
    return result
    # return json.dumps(result) 