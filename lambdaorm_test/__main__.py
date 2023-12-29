"""Test the LambdaORM library."""
import unittest
# import asyncio
import json
from lambdaorm.domain import QueryOptions
from lambdaorm.infrastructure import Orm

orm = Orm('http://localhost:9291')

class Test(unittest.IsolatedAsyncioTestCase):
    """Test class for the LambdaORM library."""

    async def test_expression(self):
        """Test the expression method."""
        expression = "Orders.filter(p=>p.customerId==customerId).include(p=>p.details).order(p=>p.orderDate).page(1,1)"
        query_options = QueryOptions(stage='default')            
        result = await orm.plan(expression, query_options)
        print(json.dumps(result.to_dict()))

        result = await orm.execute(expression, {"customerId": "CENTC"} , query_options)
        print(json.dumps(result))

if __name__ == '__main__':
    unittest.main()