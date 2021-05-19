import time

from Simulation import Simulation
import boto3
import Utils as utils


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


def store_city_dynamodb(params):
    city = allocate_city(params)
    # Write city content to dynamodb
    table = dynamodb.Table('City1')
    with table.batch_writer() as batch:
        for node in city.get_nodes().values():
            json_str = utils.serialize_node(node)
            print(json_str)
            batch.put_item(Item=json_str)

def save_simulation(simulation, max_rounds):
    table = dynamodb.Table("Simulations")
    table.put_item(Item={
        'id': 1,
        'max_rounds': max_rounds,
        'immunity': simulation.immunity,
        'incubation': simulation.incubation,
        'symptomatic': simulation.symptomatic,
        'mortality': simulation.mortality,
        'beacons': simulation.beacons,
        'round': simulation.round,
        'time_infection': simulation.time_infection,
        'start_other_places': min(simulation.city.others, key=int),
        'end_other_places': max(simulation.city.others, key=int),
        'stats':{
            'dead': 0,
            'immune': 0,
            'infected': 0
        }
    })


def allocate_city(params):
    individuals = int(params["individuals"])
    incubation = int(params["incubation"])
    symptomatic = int(params["symptomatic"])
    immunity = int(params["immunity"])
    mortality = int(params["mortality"])
    beacons = bool(params["beacons"])
    scale_city = int(params["scale_city"])
    max_rounds = int(params["max_rounds"])
    
    simulation = Simulation(individuals, incubation, symptomatic, immunity, mortality, beacons, scale_city)
    save_simulation(simulation, max_rounds)
    simulation.start_simulation()
    return simulation.city
	