"""
SQL Analyzer - Execute business intelligence queries on sales data
"""

import sqlite3
import pandas as pd
import os


class SQLAnalyzer:
    """Execute and analyze SQL queries on sales database"""
    
    def __init__(self, db_path='sales_data.db'):
        self.db_path = db_path
        self.conn = None
        
    def create_database(self, data_dir='data/raw'):
        """Create SQLite database and load data"""
        print("="*80)
        print("CREATING DATABASE")
        print("="*80)
        
        # Remove existing database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        self.conn = sqlite3.connect(self.db_path)
        
        # Load CSV files
        tables = ['products', 'customers', 'regions', 'orders']
        
        for table in tables:
            csv_path = os.path.join(data_dir, f'{table}.csv')
            df = pd.read_csv(csv_path)
            df.to_sql(table, self.conn, if_exists='replace', index=False)
            print(f"✓ Loaded {table}: {len(df)} rows")
        
        print(f"\n✓ Database created: {self.db_path}")
        
    def execute_query(self, query, description=""):
        """Execute a SQL query and return results"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
        
        if description:
            print(f"\n{description}")
            print("-" * 80)
        
        try:
            df = pd.read_sql_query(query, self.conn)
            print(df.to_string())
            print(f"\nRows returned: {len(df)}")
            return df
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def run_analytics(self, sql_file='sql/analytics_queries.sql', limit=None):
        """Run all analytics queries
        
        Args:
            sql_file: Path to SQL file
            limit: Optional limit on number of queries (None = all queries)
        """
        print("\n" + "="*80)
        print("RUNNING BUSINESS INTELLIGENCE QUERIES")
        print("="*80)
        
        # Read SQL file
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Split by queries (split on semicolon, filter empty and comment-only blocks)
        queries = [q.strip() for q in sql_content.split(';') if q.strip() and not q.strip().startswith('--')]
        
        # Filter out queries that are only comments
        valid_queries = []
        for q in queries:
            # Check if query has actual SQL (not just comments)
            non_comment_lines = [line for line in q.split('\n') 
                               if line.strip() and not line.strip().startswith('--')]
            if non_comment_lines:
                valid_queries.append(q)
        
        queries = valid_queries
        total_queries = len(queries)
        queries_to_run = queries if limit is None else queries[:limit]
        
        print(f"Found {total_queries} valid queries")
        if limit:
            print(f"Running first {limit} queries (use limit=None for all)")
        else:
            print(f"Running all {total_queries} queries")
        print()
        
        results = {}
        successful = 0
        failed = 0
        
        for idx, query in enumerate(queries_to_run, 1):
            # Extract description from comments
            lines = query.split('\n')
            description = f"Query {idx}"
            for line in lines:
                if '--' in line and len(line.strip()) > 3:
                    description = line.replace('--', '').strip()
                    break
            
            print(f"\n{'='*80}")
            print(f"Query {idx}/{len(queries_to_run)}: {description}")
            print('='*80)
            
            result = self.execute_query(query)
            if result is not None:
                results[f"query_{idx}"] = result
                successful += 1
            else:
                failed += 1
        
        # Summary
        print("\n" + "="*80)
        print("QUERY EXECUTION SUMMARY")
        print("="*80)
        print(f"Total queries in file: {total_queries}")
        print(f"Queries executed: {len(queries_to_run)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print("="*80)
        
        return results, successful, failed
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main execution"""
    analyzer = SQLAnalyzer()
    
    # Create database
    analyzer.create_database()
    
    # Run ALL analytics queries
    results, successful, failed = analyzer.run_analytics(limit=None)  # None = all queries
    
    # Close
    analyzer.close()
    
    print("\n" + "="*80)
    print("SQL ANALYSIS COMPLETE!")
    print(f"Successfully executed {successful}/{successful + failed} queries")
    print("="*80)


if __name__ == "__main__":
    main()
