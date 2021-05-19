import JobIssuer
import simplejson as json

def lambda_handler(event, context):
    
    #Params
    params = {}
    
    params["city"] = "City1"
    params["idSimulacio"] = 1
    
    #Start simulation
    JobIssuer.start_simulation(params)
    
    #Retrieve information
    return {
        'statusCode': 200,
        'body': json.dumps("Test")
    }
    