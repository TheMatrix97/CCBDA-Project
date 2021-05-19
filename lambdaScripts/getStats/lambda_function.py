import simplejson as json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    table = dynamodb.Table('Simulations')

    
    id = event['queryStringParameters']['id']
    
    response = table.get_item(Key={'id': int(id)})
   

    #Retrieve information
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }
    