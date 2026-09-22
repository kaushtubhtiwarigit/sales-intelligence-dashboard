"""
Tests for sales data generation
"""

import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_generator import SalesDataGenerator


class TestSalesDataGenerator(unittest.TestCase):
    """Test sales data generation"""
    
    def setUp(self):
        """Set up test generator"""
        self.generator = SalesDataGenerator()
    
    def test_generate_products(self):
        """Test product generation"""
        products = self.generator.generate_products(n_products=50)
        
        assert len(products) > 0
        assert 'ProductID' in products.columns
        assert 'ProductName' in products.columns
        assert 'Category' in products.columns
        assert 'ListPrice' in products.columns
        assert 'UnitCost' in products.columns
        
        # Check prices are valid
        assert (products['ListPrice'] > 0).all()
        assert (products['UnitCost'] > 0).all()
        assert (products['ListPrice'] >= products['UnitCost']).all()
    
    def test_generate_regions(self):
        """Test region generation"""
        regions = self.generator.generate_regions()
        
        assert len(regions) > 0
        assert 'Region' in regions.columns
        assert 'State' in regions.columns
        assert 'City' in regions.columns
        assert regions['Region'].nunique() == 5  # Should have 5 regions
    
    def test_generate_customers(self):
        """Test customer generation"""
        self.generator.generate_regions()
        customers = self.generator.generate_customers(n_customers=100)
        
        assert len(customers) == 100
        assert 'CustomerID' in customers.columns
        assert 'FirstName' in customers.columns
        assert 'Email' in customers.columns
        assert 'Region' in customers.columns
        assert 'CustomerSegment' in customers.columns
        
        # Check email format
        assert customers['Email'].str.contains('@').all()
    
    def test_generate_orders(self):
        """Test order generation"""
        self.generator.generate_products(n_products=20)
        self.generator.generate_regions()
        self.generator.generate_customers(n_customers=50)
        orders = self.generator.generate_orders(n_orders=100)
        
        assert len(orders) == 100
        assert 'OrderID' in orders.columns
        assert 'OrderDate' in orders.columns
        assert 'CustomerID' in orders.columns
        assert 'ProductID' in orders.columns
        assert 'TotalAmount' in orders.columns
        
        # Check amounts are valid
        assert (orders['TotalAmount'] > 0).all()
        assert (orders['Quantity'] > 0).all()
    
    def test_data_relationships(self):
        """Test referential integrity"""
        self.generator.generate_products(n_products=10)
        self.generator.generate_regions()
        self.generator.generate_customers(n_customers=20)
        orders = self.generator.generate_orders(n_orders=50)
        
        # All orders should reference valid customers
        valid_customers = set(self.generator.customers_df['CustomerID'])
        assert set(orders['CustomerID']).issubset(valid_customers)
        
        # All orders should reference valid products
        valid_products = set(self.generator.products_df['ProductID'])
        assert set(orders['ProductID']).issubset(valid_products)


if __name__ == '__main__':
    unittest.main()
