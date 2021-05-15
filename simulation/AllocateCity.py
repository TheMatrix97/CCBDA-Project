import json

from simulation.Simulation import Simulation
import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def create_table_dynamodb():
    # Crear taula dynamodb
    response = client.create_table(
        TableName='City1',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            "WriteCapacityUnits": 10,
            "ReadCapacityUnits": 10
        }
    )
    print(response)

def serialize_node(node):
    if node is None:
        return {}
    return {
        "type": str(node.type),
        "id": node.id,
        "people_in_this_node": serialize_people_node(node.people_in_this_node),
        "x": node.x,
        "y": node.y
    }

def serialize_people_node(people):
    res = []
    for person in people:
        val = {
            'id': person.id,
            'type': person.type,
            'agenda': json.dumps(person.agenda),
            'infection': str(person.infection),
            'time_start_infection': person.time_start_infection,
            'time_start_quarantine': person.time_start_quarantine,
            'beacons': json.dumps(person.beacons),
            'workplace': person.workplace,
            'home': person.home,
            'school': person.school
        }
        res.append(val)
    return res

def store_city_dynamodb():
    city = allocate_city()
    # Write city content to dynamodb
    table = dynamodb.Table('City1')
    with table.batch_writer() as batch:
        for node in city.get_nodes().values():
            json_str = serialize_node(node)
            print(json_str)
            batch.put_item(Item=json_str)


def allocate_city():
    individuals = 2000
    incubation = 2
    symptomatic = 4
    immunity = 14
    mortality = 10
    beacons = True
    scale_city = 200
    simulation = Simulation(individuals, incubation, symptomatic, immunity, mortality, beacons, scale_city)
    simulation.start_simulation()
    return simulation.city

if __name__ == "__main__":
    store_city_dynamodb()
