import simplejson as json
import boto3
import AllocateCity
import time

client = boto3.client('dynamodb')



def lambda_handler(event, context):
    print(event)
    params = json.loads(event["body"])
    print("params -> " + str(event["body"]))
    #Check if exists table dynamodb
    try:
        AllocateCity.create_table_dynamodb()
    except client.exceptions.ResourceInUseException:
        return {
        'statusCode': 500,
        'body': json.dumps("It exists a simulation already clean table City1")
        } 
    
    time.sleep(10)
    AllocateCity.store_city_dynamodb(params)

    #Retrieve information
    return {
        'statusCode': 200,
        'body': "done"
    }
    