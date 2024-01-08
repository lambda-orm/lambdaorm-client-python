"""Test the LambdaORM library."""
import json
import asyncio
from lambdaorm.domain import QueryOptions
from lambdaorm.infrastructure import Orm

async def metadata_lab(orm:Orm,query:str,options:QueryOptions)->None:
    """Metadata lab."""     
    result = await orm.parameters(query)
    print('Parameters:')
    print(json.dumps(result,indent=2))

    result = await orm.model(query)
    print('Model:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.constraints(query)
    print('Constraints:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.metadata(query)
    print('Metadata:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.plan(query, options)
    print('Plan:')
    print(json.dumps(result.to_dict(),indent=2))

async def execute_lab(orm:Orm,query:str,options:QueryOptions)->None:
    """Execute lab."""     
    result = await orm.execute(query, {"customerId": "CENTC"} , options)
    print('Execute:')
    print(json.dumps(result,indent=2))


async def general_lab(orm:Orm)->None:
    """General lab."""     
    result = await orm.version()
    print('Version:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.ping()
    print('Ping:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.health()
    print('Health:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.metrics()
    print('Metrics:')
    print(json.dumps(result,indent=2))


async def schema_lab(orm:Orm)->None:
    """Schema lab."""     
    result = await orm.schema.version()
    print('Schema Version:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.schema()
    print('Schema:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.domain()
    print('Domain:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.enums()
    print('Enums:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.entities()
    print('Entities:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.entity('Orders')
    print('Entity:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.mappings()
    print('Mappings:')
    print(json.dumps(result.to_dict(),indent=2))  

    result = await orm.schema.mapping('default')
    print('Mapping:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.entityMapping('default','Orders')
    print('Entity Mapping:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.sources()
    print('Sources:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.source('default')
    print('Source:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.stages()
    print('Stages:')
    print(json.dumps(result.to_dict(),indent=2))

    result = await orm.schema.stage('default')
    print('Stage:')
    print(json.dumps(result.to_dict(),indent=2))    

async def stage_lab(orm:Orm)->None:
    """Stage lab."""     
    result = await orm.stage.export()
    print('export:')
    print(json.dumps(result.to_dict(),indent=2))

async def lab()->None:
    """Test the LambdaORM library."""
    # Create an Orm instance by consuming the Lambda ORM service
    orm = Orm('http://localhost:9291')
    query = "Orders.filter(p=>p.customerId==customerId).include(p=>p.details).order(p=>p.orderDate).page(1,1)"
    options = QueryOptions(stage='default')
    # Get the execution plan
    await metadata_lab(orm,query,options)
    await execute_lab(orm,query,options)
    await general_lab(orm)
    await schema_lab(orm)
    await stage_lab(orm)   

if __name__ == '__main__':
      asyncio.run(lab())