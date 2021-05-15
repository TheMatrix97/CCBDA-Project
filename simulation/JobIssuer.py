import simplejson as json

import boto3

sqs = boto3.resource('sqs')
dynamodb = boto3.resource('dynamodb')


def retrieve_nodes(tableName):
    finish = False
    items = []
    start_key = None
    table = dynamodb.Table(tableName)
    while not finish:
        if start_key:
            response = table.scan(ExclusiveStartKey=start_key)
        else:
            response = table.scan()
        items.extend(response['Items'])
        if 'LastEvaluatedKey' not in response:
            finish = True
        else:
            start_key = response['LastEvaluatedKey']
    return items

def start_simulation(params):
    queue = sqs.get_queue_by_name(QueueName='workers.fifo')
    nodes = retrieve_nodes(params['city'])
    contador = 0
    for node in nodes:
        response = queue.send_message(MessageBody=json.dumps(node),
                                      MessageDeduplicationId=str(params['idSimulacio']) + '_' + str(contador)
                                      ,MessageGroupId='workers', MessageAttributes={
            'idSimulacio': {
                'StringValue': str(params['idSimulacio']),
                'DataType': 'String'
            }
        })
        contador += 1
        print(response)



if __name__ == "__main__":
    params = {}
    params['city'] = "City1"
    params['idSimulacio'] = 1
    start_simulation(params)
