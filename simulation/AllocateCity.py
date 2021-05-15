import json

from simulation.Node import Node
from simulation.Person import Person
from simulation.Simulation import Simulation
import boto3

from simulation.Type import Type, Infection

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


def de_serialize_node(data):
    new_type = data['type'].replace("Type.", "")
    node = Node(data['id'], Type[new_type])
    node.x = data['x']
    node.y = data['y']
    node.people_in_this_node = de_serialize_people(data['people_in_this_node'])
    return node

def de_serialize_people(data):
    res = []
    for person in data:
        pers = Person(person['id'], person['type'])
        pers.agenda = json.loads(person['agenda'])
        new_infection = person['infection'].replace("Infection.","")
        if new_infection != 'None':
            pers.infection = Infection[new_infection]
        else:
            pers.infection = None
        pers.time_start_infection = person['time_start_infection']
        pers.time_start_quarantine = person['time_start_quarantine']
        pers.beacons = json.loads(person['beacons'])
        pers.workplace = person['workplace']
        pers.home = person['home']
        pers.school = person['school']
        res.append(pers)
    return res

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

def read_city_dynamodb():
    finish = False
    items = []
    start_key = None
    table = dynamodb.Table('City1')
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

    res = []
    for item in items:
        res.append(de_serialize_node(item))
    print(len(res))

def save_simulation(simulation):
    table = dynamodb.Table("Simulations")
    table.put_item(Item={
        'id': 1,
        'max_rounds': 30*4,
        'immunity': simulation.immunity,
        'incubation': simulation.incubation,
        'symptomatic': simulation.symptomatic,
        'mortality': simulation.mortality,
        'beacons': simulation.beacons,
        'round': simulation.round,
        'time_infection': simulation.time_infection,
        'stats':{
            'dead': 0,
            'immune': 0,
            'infected': 0
        }
    })


def allocate_city():
    individuals = 2000
    incubation = 2
    symptomatic = 4
    immunity = 14
    mortality = 10
    beacons = True
    scale_city = 200
    simulation = Simulation(individuals, incubation, symptomatic, immunity, mortality, beacons, scale_city)
    save_simulation(simulation)
    simulation.start_simulation()
    return simulation.city

if __name__ == "__main__":
    #create_table_dynamodb()
    store_city_dynamodb()
    #read_city_dynamodb()
