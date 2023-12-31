"""Test the LambdaORM library."""
import json
import asyncio
from lambdaorm.domain import QueryOptions
from lambdaorm.infrastructure import Orm

async def lab()->None:
    """Test the LambdaORM library."""
    # Create an Orm instance by consuming the Lambda ORM service
    orm = Orm('http://localhost:9291')
    expression = "Orders.filter(p=>p.customerId==customerId).include(p=>p.details).order(p=>p.orderDate).page(1,1)"
    query_options = QueryOptions(stage='default')
    # Get the execution plan
    result = await orm.plan(expression, query_options)
    print(json.dumps(result.to_dict(),indent=2))
    # Run the query
    result = await orm.execute(expression, {"customerId": "CENTC"} , query_options)
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
      asyncio.run(lab())