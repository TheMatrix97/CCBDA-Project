import json
import boto3

client = boto3.client('ecs')

def lambda_handler(event, context):
    input_data = json.loads(event["body"])
    res = {
        'statusCode': 404,
        'body': json.dumps("Method not implemented")
    }

    if input_data['command'] == "run":
        if not exists_running_task():
            id = run_job_issuer_task()
            res['statusCode'] = 200
            res['body'] = json.dumps({'id': id})

        else:
            res['statusCode'] = 500
            res['body'] = json.dumps("Job issuer is already running")


    elif input_data['command'] == "stop":
        id = input_data['id']
        stop_job_issuer_task(id)
        res['statusCode'] = 200
        res['body'] = json.dumps("Job issuer stop command issued")

    return res

def exists_running_task():
    response = client.list_tasks(
        desiredStatus='RUNNING',
        launchType='FARGATE'
    )

    response2 = client.list_tasks(
        desiredStatus='PENDING',
        launchType='FARGATE'
    )

    return len(response['taskArns']) != 0 or len(response2['taskArns'])




def run_job_issuer_task():
    response = client.run_task(taskDefinition='first-run-task-definition',
                               networkConfiguration={
                                   'awsvpcConfiguration': {
                                       'subnets': [
                                           'subnet-0c8da3a737e8c2f57',
                                       ],
                                       'securityGroups': [
                                           'sg-0474b93c000f411f7',
                                       ],
                                       'assignPublicIp': 'ENABLED'
                                   }
                               }, launchType='FARGATE')
    return response['tasks'][0]['attachments'][0]['id']


def stop_job_issuer_task(id):
    print(id)
    response = client.stop_task(task=id)
    print(response)
