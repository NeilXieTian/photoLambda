import json
import json
import boto3

from botocore.vendored import requests


def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    result = {
            "sessionState" : {
                "dialogAction":{
                    "type":"Close"
                },
                "intent": {
                    "confirmationState": "Confirmed",
                    "name": "SearchIntent",
                    "state":"Fulfilled"
                }
            },
            'messages': [{"contentType":"PlainText", "content": 'sssssss'}]
        }
            
    return result
