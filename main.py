"""
Main Pipeline for Sales Analytics Dashboard
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import SalesDataGenerator
from sql_analyzer import SQLAnalyzer


def main():
    """Execute complete sales analytics pipeline"""
    
    print("="*80)
    print("SALES INTELLIGENCE DASHBOARD - COMPLETE PIPELINE")
    print("="*80)
    
    # Step 1: Generate Data
    print("\n" + "="*80)
    print("STEP 1: GENERATE SALES DATA")
    print("="*80)
    generator = SalesDataGenerator()
    generator.generate_products(n_products=200)
    generator.generate_regions()
    generator.generate_customers(n_customers=5000)
    generator.generate_orders(n_orders=50000)
    generator.save_all_data()
    
    # Step 2: Create Database and Run Analytics
    print("\n" + "="*80)
    print("STEP 2: SQL ANALYTICS")
    print("="*80)
    analyzer = SQLAnalyzer()
    analyzer.create_database()
    results, successful, failed = analyzer.run_analytics(limit=None)  # Run ALL queries
    analyzer.close()
    
    # Final Summary
    print("\n" + "="*80)
    print("PIPELINE COMPLETE!")
    print("="*80)
    
    print("\n✓ Generated realistic sales data:")
    print(f"  - 50,000 orders")
    print(f"  - 5,000 customers")
    print(f"  - 200 products")
    print(f"  - 5 regions, 20 states")
    
    print("\n✓ Created SQLite database with all data")
    print(f"✓ Executed {successful}/{successful + failed} business intelligence SQL queries")
    if failed > 0:
        print(f"  ⚠️  {failed} queries failed - check output above for details")
    
    print("\n" + "="*80)
    print("KEY DELIVERABLES:")
    print("="*80)
    print("  📁 data/raw/")
    print("      - products.csv, customers.csv, orders.csv, regions.csv")
    print("\n  📁 sales_data.db")
    print("      - SQLite database with all tables")
    print("\n  📁 sql/")
    print("      - analytics_queries.sql (20 BI queries)")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("  1. Import CSV files into Power BI Desktop")
    print("  2. Create relationships between tables")
    print("  3. Build visualizations:")
    print("      - Revenue trends (line chart)")
    print("      - Top products (bar chart)")
    print("      - Regional performance (map)")
    print("      - Customer segments (pie chart)")
    print("  4. Practice SQL queries on sales_data.db")
    print("  5. Explore data with pandas for deeper analysis")
    
    print("\n" + "="*80)
    print("READY FOR INTERVIEWS AND PORTFOLIO!")
    print("="*80)


if __name__ == "__main__":
    main()
