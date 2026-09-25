"""
Test Suite for SQL Analytics Queries

Validates that all 20+ business intelligence queries execute successfully
"""

import unittest
import os
import sys
import sqlite3

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_generator import SalesDataGenerator
from sql_analyzer import SQLAnalyzer


class TestSQLQueries(unittest.TestCase):
    """Test all SQL analytics queries"""
    
    @classmethod
    def setUpClass(cls):
        """Setup: Generate data and create database once for all tests"""
        print("\n" + "="*80)
        print("SETTING UP SQL QUERY TEST SUITE")
        print("="*80)
        
        # Generate test data (smaller dataset for faster tests)
        cls.test_db = 'test_sales_queries.db'
        cls.test_data_dir = 'test_data_sql'
        
        print("\nGenerating test data...")
        generator = SalesDataGenerator(
            n_products=50,      # Smaller dataset for faster tests
            n_customers=500,
            n_orders=5000,
            output_dir=cls.test_data_dir
        )
        generator.generate_all()
        
        print("\nCreating test database...")
        cls.analyzer = SQLAnalyzer(db_path=cls.test_db)
        cls.analyzer.create_database(data_dir=cls.test_data_dir)
        
        print("\n✓ Test setup complete")
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup: Remove test database and files"""
        cls.analyzer.close()
        
        # Remove test database
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
        
        # Remove test data directory
        import shutil
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)
        
        print("\n✓ Test cleanup complete")
    
    def test_sql_file_exists(self):
        """Test that SQL file exists"""
        sql_file = os.path.join('sql', 'analytics_queries.sql')
        self.assertTrue(os.path.exists(sql_file), 
                       f"SQL file not found: {sql_file}")
    
    def test_all_queries_discovered(self):
        """Test that SQL file contains expected number of queries"""
        sql_file = os.path.join('sql', 'analytics_queries.sql')
        
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Count queries (split by semicolon)
        queries = [q.strip() for q in sql_content.split(';') 
                  if q.strip() and not q.strip().startswith('--')]
        
        # Filter valid queries
        valid_queries = []
        for q in queries:
            non_comment_lines = [line for line in q.split('\n') 
                               if line.strip() and not line.strip().startswith('--')]
            if non_comment_lines:
                valid_queries.append(q)
        
        # Should have 20 queries
        self.assertGreaterEqual(len(valid_queries), 20, 
                               f"Expected at least 20 queries, found {len(valid_queries)}")
        
        print(f"\n✓ Found {len(valid_queries)} valid SQL queries")
    
    def test_all_queries_execute_successfully(self):
        """Test that ALL queries execute without errors"""
        sql_file = os.path.join('sql', 'analytics_queries.sql')
        
        # Run all queries
        results, successful, failed = self.analyzer.run_analytics(
            sql_file=sql_file, 
            limit=None  # Execute ALL queries
        )
        
        # Assert all queries succeeded
        self.assertEqual(failed, 0, 
                        f"{failed} queries failed. Check output for details.")
        self.assertGreater(successful, 0, 
                          "No queries were executed successfully")
        
        print(f"\n✓ All {successful} queries executed successfully")
    
    def test_query_01_revenue_overview(self):
        """Test Query 1: Revenue Overview"""
        query = """
        SELECT 
            COUNT(DISTINCT OrderID) as TotalOrders,
            COUNT(DISTINCT CustomerID) as UniqueCustomers,
            SUM(TotalAmount) as TotalRevenue,
            AVG(TotalAmount) as AvgOrderValue
        FROM orders
        WHERE OrderStatus = 'Completed'
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertEqual(len(result), 1, "Should return exactly 1 row")
        self.assertGreater(result['TotalOrders'].iloc[0], 0, 
                          "Should have orders")
        self.assertGreater(result['TotalRevenue'].iloc[0], 0, 
                          "Should have revenue")
    
    def test_query_02_monthly_trend(self):
        """Test Query 2: Monthly Revenue Trend"""
        query = """
        SELECT 
            strftime('%Y-%m', OrderDate) as Month,
            COUNT(DISTINCT OrderID) as Orders,
            SUM(TotalAmount) as Revenue
        FROM orders
        WHERE OrderStatus IN ('Completed', 'Shipped')
        GROUP BY Month
        ORDER BY Month
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertGreater(len(result), 0, "Should return monthly data")
        self.assertIn('Month', result.columns)
        self.assertIn('Revenue', result.columns)
    
    def test_query_04_top_products(self):
        """Test Query 4: Top 10 Products"""
        query = """
        SELECT 
            p.ProductName,
            COUNT(DISTINCT o.OrderID) as TimesSold,
            SUM(o.TotalAmount) as TotalRevenue
        FROM orders o
        JOIN products p ON o.ProductID = p.ProductID
        WHERE o.OrderStatus = 'Completed'
        GROUP BY p.ProductID, p.ProductName
        ORDER BY TotalRevenue DESC
        LIMIT 10
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertLessEqual(len(result), 10, "Should return max 10 products")
        self.assertIn('ProductName', result.columns)
        self.assertIn('TotalRevenue', result.columns)
    
    def test_query_06_customer_lifetime_value(self):
        """Test Query 6: Customer Lifetime Value"""
        query = """
        SELECT 
            c.CustomerID,
            COUNT(DISTINCT o.OrderID) as TotalOrders,
            SUM(o.TotalAmount) as LifetimeValue,
            AVG(o.TotalAmount) as AvgOrderValue
        FROM customers c
        JOIN orders o ON c.CustomerID = o.CustomerID
        WHERE o.OrderStatus = 'Completed'
        GROUP BY c.CustomerID
        ORDER BY LifetimeValue DESC
        LIMIT 20
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertGreater(len(result), 0, "Should return customer data")
        self.assertIn('LifetimeValue', result.columns)
    
    def test_query_07_rfm_segmentation(self):
        """Test Query 7: RFM Customer Segmentation"""
        # Using simplified version without 'now' function issues
        query = """
        WITH RFM AS (
            SELECT 
                CustomerID,
                CAST(julianday((SELECT MAX(OrderDate) FROM orders)) - julianday(MAX(OrderDate)) AS INTEGER) as Recency,
                COUNT(DISTINCT OrderID) as Frequency,
                SUM(TotalAmount) as Monetary
            FROM orders
            WHERE OrderStatus = 'Completed'
            GROUP BY CustomerID
        ),
        RFM_Scores AS (
            SELECT 
                CustomerID,
                Recency,
                Frequency,
                Monetary,
                NTILE(5) OVER (ORDER BY Recency DESC) as R_Score,
                NTILE(5) OVER (ORDER BY Frequency) as F_Score,
                NTILE(5) OVER (ORDER BY Monetary) as M_Score
            FROM RFM
        )
        SELECT 
            CASE 
                WHEN R_Score >= 4 AND F_Score >= 4 THEN 'Champions'
                WHEN R_Score >= 3 AND F_Score >= 3 THEN 'Loyal Customers'
                WHEN R_Score >= 4 AND F_Score <= 2 THEN 'Promising'
                WHEN R_Score <= 2 AND F_Score >= 4 THEN 'At Risk'
                WHEN R_Score <= 2 AND F_Score <= 2 THEN 'Lost'
                ELSE 'Potential Loyalists'
            END as Segment,
            COUNT(*) as Customers
        FROM RFM_Scores
        GROUP BY Segment
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertGreater(len(result), 0, "Should return segments")
        self.assertIn('Segment', result.columns)
        self.assertIn('Customers', result.columns)
    
    def test_query_09_regional_sales(self):
        """Test Query 9: Regional Sales Performance"""
        query = """
        SELECT 
            Region,
            COUNT(DISTINCT OrderID) as Orders,
            SUM(TotalAmount) as Revenue,
            AVG(TotalAmount) as AvgOrderValue
        FROM orders
        WHERE OrderStatus = 'Completed'
        GROUP BY Region
        ORDER BY Revenue DESC
        """
        
        result = self.analyzer.execute_query(query, "")
        
        self.assertIsNotNone(result, "Query failed to execute")
        self.assertGreater(len(result), 0, "Should return regional data")
        self.assertIn('Region', result.columns)
        self.assertIn('Revenue', result.columns)
    
    def test_database_integrity(self):
        """Test database has all required tables and data"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('products', 'customers', 'orders', 'regions')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertEqual(len(tables), 4, "Should have 4 tables")
        
        # Check tables have data
        for table in ['products', 'customers', 'orders', 'regions']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0, f"{table} should have data")
        
        conn.close()
        print("\n✓ Database integrity check passed")
    
    def test_no_syntax_errors_in_queries(self):
        """Test that all queries have valid SQL syntax"""
        sql_file = os.path.join('sql', 'analytics_queries.sql')
        
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        queries = [q.strip() for q in sql_content.split(';') 
                  if q.strip() and not q.strip().startswith('--')]
        
        syntax_errors = []
        
        for idx, query in enumerate(queries, 1):
            # Skip comment-only blocks
            non_comment_lines = [line for line in query.split('\n') 
                               if line.strip() and not line.strip().startswith('--')]
            if not non_comment_lines:
                continue
            
            try:
                # Try to prepare the query (doesn't execute, just validates syntax)
                conn = sqlite3.connect(self.test_db)
                cursor = conn.cursor()
                cursor.execute("EXPLAIN QUERY PLAN " + query)
                conn.close()
            except sqlite3.Error as e:
                syntax_errors.append(f"Query {idx}: {str(e)}")
        
        self.assertEqual(len(syntax_errors), 0, 
                        f"Syntax errors found:\n" + "\n".join(syntax_errors))


def run_tests():
    """Run the test suite"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSQLQueries)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
