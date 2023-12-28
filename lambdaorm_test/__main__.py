"""Test module for the LambdaORM library."""
import unittest
from lambdaorm.domain import QueryOptions
from lambdaorm.infrastructure import LambdaOrmRestClient

api = LambdaOrmRestClient('workspace', 'http://localhost:9291')

class Test(unittest.TestCase):
    """Test class for the LambdaORM library."""

    def test_expression(self):
        """Test the expression method."""
        expression = "Orders.filter(p=>p.customerId==customerId).include(p=>[p.details.include(p=>p.product.map(p=>p.name)).map(p=>{subTotal:p.quantity*p.unitPrice}),p.customer.map(p=>p.name)]).order(p=>p.orderDate).page(1,1)"
        query_options = QueryOptions(stage ='default')
            
        result = api.plan(expression,query_options)
        print(result)

unittest.main()
