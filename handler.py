import json
import urllib.parse
import boto3
from sqsHandler import SqsHandler
from datetime import datetime


sqs_client = boto3.client('sqs')
queue_preparing_url = sqs_client.get_queue_url(QueueName='em-preparacao-pizzaria')['QueueUrl']
queue_done_url = sqs_client.get_queue_url(QueueName='pronto-pizzaria')['QueueUrl']

def eventRouter(event, context):
    destination_queue = ''
    
    sqs_preparing = SqsHandler(queue_preparing_url)
    sqs_done = SqsHandler(queue_done_url)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    if key.startswith('em-preparacao/'):
        orderAndCustomer = key.replace("em-preparacao/", "").split("-")
        order = orderAndCustomer[0]
        customer = orderAndCustomer[1]
        destination_queue = queue_preparing_url
        print('sending order ' + order + ' to queue ' + destination_queue)
        message = json.dumps({'order': order, 'datetime': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), 'customer': customer})
        sqs_preparing.send(message)
    elif key.startswith('pronto/'):
        orderAndCustomer = key.replace("pronto/", "").split("-")
        order = orderAndCustomer[0]
        customer = orderAndCustomer[1]
        destination_queue = queue_done_url
        print('sending order ' + order + ' to queue ' + destination_queue)
        message = json.dumps({'order': order, 'datetime': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), 'customer': customer})
        sqs_done.send(message)
    else:
        raise Exception('Structure of ' + key + 'was unexpected')
    
    body = {
        "message": message,
        "destination": destination_queue, 
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def preparing(event, context):
    print(json.dumps(event))
    for record in event['Records']:
        print(json.dumps(record['body']))

        body = json.loads(record['body'])
        print(body['order'])
        print(body['datetime'])
        print(body['customer'])
        
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(TableName='pedidos-pizzaria', Item={'pedido':{'S':body['order']},'datetime':{'S':body['datetime']},'cliente':{'S':body['customer']},'status':{'S':'em-preparacao'}})

    
    
def done(event, context):
    print(json.dumps(event))
    for record in event['Records']:
        print(json.dumps(record['body']))
        
        body = json.loads(record['body'])
        print(body['order'])
        print(body['datetime'])
        print(body['customer'])

        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(TableName='pedidos-pizzaria', Item={'pedido':{'S':body['order']},'datetime':{'S':body['datetime']},'cliente':{'S':body['customer']},'status':{'S':'pronto'}})
