"""
Sales Data Generator
Generates realistic sales, customer, product, and regional data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)


class SalesDataGenerator:
    """Generate realistic sales data for analytics"""
    
    def __init__(self):
        self.products_df = None
        self.customers_df = None
        self.regions_df = None
        self.orders_df = None
        
    def generate_products(self, n_products=200):
        """Generate product catalog"""
        print("="*80)
        print("GENERATING PRODUCT DATA")
        print("="*80)
        
        categories = {
            'Electronics': ['Laptops', 'Smartphones', 'Tablets', 'Headphones', 'Cameras'],
            'Home & Kitchen': ['Cookware', 'Small Appliances', 'Furniture', 'Decor', 'Bedding'],
            'Clothing': ['Men', 'Women', 'Kids', 'Shoes', 'Accessories'],
            'Sports': ['Equipment', 'Apparel', 'Footwear', 'Supplements', 'Outdoor Gear'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children', 'Comics'],
            'Toys & Games': ['Action Figures', 'Board Games', 'Puzzles', 'Educational', 'Video Games'],
            'Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Fragrances', 'Tools'],
            'Health': ['Vitamins', 'Supplements', 'Fitness', 'Personal Care', 'Medical'],
            'Automotive': ['Parts', 'Accessories', 'Tools', 'Electronics', 'Care Products'],
            'Office': ['Supplies', 'Electronics', 'Furniture', 'Storage', 'Art Supplies'],
            'Garden': ['Tools', 'Plants', 'Furniture', 'Decor', 'Supplies'],
            'Pet Supplies': ['Food', 'Toys', 'Accessories', 'Health', 'Grooming']
        }
        
        products = []
        product_id = 1
        
        for category, subcategories in categories.items():
            for subcategory in subcategories:
                # Generate 1-3 products per subcategory
                for _ in range(random.randint(1, 3)):
                    # Generate realistic product name
                    brand = random.choice(['Premium', 'Pro', 'Elite', 'Essential', 'Deluxe', 'Ultra'])
                    adjective = random.choice(['Smart', 'Wireless', 'Compact', 'Professional', 'Eco', 'Digital'])
                    noun = subcategory.rstrip('s') if subcategory.endswith('s') else subcategory
                    
                    product_name = f"{brand} {adjective} {noun}"
                    
                    # Pricing based on category
                    base_prices = {
                        'Electronics': (200, 2000),
                        'Home & Kitchen': (30, 500),
                        'Clothing': (20, 200),
                        'Sports': (25, 400),
                        'Books': (10, 50),
                        'Toys & Games': (15, 150),
                        'Beauty': (10, 100),
                        'Health': (15, 80),
                        'Automotive': (20, 300),
                        'Office': (5, 200),
                        'Garden': (15, 300),
                        'Pet Supplies': (10, 80)
                    }
                    
                    price_range = base_prices[category]
                    list_price = round(random.uniform(price_range[0], price_range[1]), 2)
                    unit_cost = round(list_price * random.uniform(0.4, 0.7), 2)
                    profit_margin = round(((list_price - unit_cost) / list_price) * 100, 2)
                    
                    suppliers = ['Global Supply Co', 'MegaCorp Industries', 'Quality Imports', 
                                'Direct Wholesale', 'Premium Suppliers', 'Value Partners']
                    
                    products.append({
                        'ProductID': f'PRD{str(product_id).zfill(5)}',
                        'ProductName': product_name,
                        'Category': category,
                        'Subcategory': subcategory,
                        'UnitCost': unit_cost,
                        'ListPrice': list_price,
                        'ProfitMargin': profit_margin,
                        'Supplier': random.choice(suppliers),
                        'StockQuantity': random.randint(0, 1000),
                        'ReorderLevel': random.randint(10, 100),
                        'IsActive': random.choice([True, True, True, False])  # 75% active
                    })
                    
                    product_id += 1
        
        self.products_df = pd.DataFrame(products)
        print(f"✓ Generated {len(self.products_df)} products")
        print(f"  - Categories: {self.products_df['Category'].nunique()}")
        print(f"  - Subcategories: {self.products_df['Subcategory'].nunique()}")
        print(f"  - Avg Price: ${self.products_df['ListPrice'].mean():.2f}")
        
        return self.products_df
    
    def generate_regions(self):
        """Generate regional data"""
        print("\n" + "="*80)
        print("GENERATING REGIONAL DATA")
        print("="*80)
        
        regions_data = {
            'Northeast': {
                'states': ['New York', 'Pennsylvania', 'Massachusetts', 'New Jersey'],
                'cities': ['New York City', 'Philadelphia', 'Boston', 'Newark']
            },
            'Southeast': {
                'states': ['Florida', 'Georgia', 'North Carolina', 'Virginia'],
                'cities': ['Miami', 'Atlanta', 'Charlotte', 'Richmond']
            },
            'Midwest': {
                'states': ['Illinois', 'Ohio', 'Michigan', 'Wisconsin'],
                'cities': ['Chicago', 'Columbus', 'Detroit', 'Milwaukee']
            },
            'Southwest': {
                'states': ['Texas', 'Arizona', 'New Mexico', 'Oklahoma'],
                'cities': ['Houston', 'Phoenix', 'Albuquerque', 'Oklahoma City']
            },
            'West': {
                'states': ['California', 'Washington', 'Oregon', 'Nevada'],
                'cities': ['Los Angeles', 'Seattle', 'Portland', 'Las Vegas']
            }
        }
        
        sales_reps = [fake.name() for _ in range(20)]
        
        regions = []
        for region, data in regions_data.items():
            for state, city in zip(data['states'], data['cities']):
                regions.append({
                    'Region': region,
                    'State': state,
                    'City': city,
                    'SalesRep': random.choice(sales_reps)
                })
        
        self.regions_df = pd.DataFrame(regions)
        print(f"✓ Generated {len(self.regions_df)} regional entries")
        print(f"  - Regions: {self.regions_df['Region'].nunique()}")
        print(f"  - States: {self.regions_df['State'].nunique()}")
        
        return self.regions_df
    
    def generate_customers(self, n_customers=5000):
        """Generate customer data"""
        print("\n" + "="*80)
        print("GENERATING CUSTOMER DATA")
        print("="*80)
        
        if self.regions_df is None:
            self.generate_regions()
        
        customers = []
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        for i in range(n_customers):
            registration_date = fake.date_between(start_date=start_date, end_date=end_date)
            location = self.regions_df.sample(1).iloc[0]
            
            segments = ['High Value', 'Medium Value', 'Low Value']
            segment_weights = [0.15, 0.35, 0.50]
            
            customers.append({
                'CustomerID': f'CUST{str(i+1).zfill(6)}',
                'FirstName': fake.first_name(),
                'LastName': fake.last_name(),
                'Email': fake.email(),
                'Phone': fake.phone_number(),
                'RegistrationDate': registration_date,
                'City': location['City'],
                'State': location['State'],
                'Region': location['Region'],
                'CustomerSegment': random.choices(segments, weights=segment_weights)[0],
                'IsActive': random.choice([True, True, True, False])  # 75% active
            })
        
        self.customers_df = pd.DataFrame(customers)
        print(f"✓ Generated {len(self.customers_df)} customers")
        print(f"  - Segments: {self.customers_df['CustomerSegment'].value_counts().to_dict()}")
        print(f"  - Active: {self.customers_df['IsActive'].sum()}")
        
        return self.customers_df
    
    def generate_orders(self, n_orders=50000):
        """Generate order transactions"""
        print("\n" + "="*80)
        print("GENERATING ORDER DATA")
        print("="*80)
        
        if self.products_df is None:
            self.generate_products()
        if self.customers_df is None:
            self.generate_customers()
        
        # Active products and customers
        active_products = self.products_df[self.products_df['IsActive']].copy()
        active_customers = self.customers_df[self.customers_df['IsActive']].copy()
        
        print(f"  - Active products: {len(active_products)}")
        print(f"  - Active customers: {len(active_customers)}")
        
        orders = []
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']
        sales_channels = ['Online', 'In-Store', 'Mobile App', 'Phone']
        statuses = ['Completed', 'Completed', 'Completed', 'Shipped', 'Processing', 'Cancelled']
        
        for i in range(n_orders):
            # Select random customer
            customer = active_customers.sample(1).iloc[0]
            
            # Customers registered before order date
            customer_reg_date = pd.to_datetime(customer['RegistrationDate'])
            possible_order_date_start = max(start_date, customer_reg_date.to_pydatetime())
            order_date = fake.date_between(start_date=possible_order_date_start, end_date=end_date)
            
            # Select product
            product = active_products.sample(1).iloc[0]
            
            # Quantity (influenced by customer segment)
            if customer['CustomerSegment'] == 'High Value':
                quantity = random.randint(1, 10)
            elif customer['CustomerSegment'] == 'Medium Value':
                quantity = random.randint(1, 5)
            else:
                quantity = random.randint(1, 3)
            
            # Pricing
            unit_price = product['ListPrice']
            
            # Discount (higher for high-value customers)
            if customer['CustomerSegment'] == 'High Value':
                discount_pct = random.uniform(0, 15)
            elif customer['CustomerSegment'] == 'Medium Value':
                discount_pct = random.uniform(0, 10)
            else:
                discount_pct = random.uniform(0, 5)
            
            discount_amount = round(unit_price * quantity * discount_pct / 100, 2)
            subtotal = round(unit_price * quantity, 2)
            
            # Shipping
            if subtotal > 50:
                shipping_cost = 0  # Free shipping
            else:
                shipping_cost = round(random.uniform(5, 15), 2)
            
            total_amount = round(subtotal - discount_amount + shipping_cost, 2)
            
            orders.append({
                'OrderID': f'ORD{str(i+1).zfill(7)}',
                'OrderDate': order_date,
                'CustomerID': customer['CustomerID'],
                'ProductID': product['ProductID'],
                'ProductName': product['ProductName'],
                'Category': product['Category'],
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'Discount': discount_amount,
                'ShippingCost': shipping_cost,
                'TotalAmount': total_amount,
                'PaymentMethod': random.choice(payment_methods),
                'SalesChannel': random.choice(sales_channels),
                'OrderStatus': random.choice(statuses),
                'Region': customer['Region'],
                'State': customer['State']
            })
            
            if (i + 1) % 10000 == 0:
                print(f"  - Generated {i+1}/{n_orders} orders...")
        
        self.orders_df = pd.DataFrame(orders)
        self.orders_df['OrderDate'] = pd.to_datetime(self.orders_df['OrderDate'])
        
        print(f"\n✓ Generated {len(self.orders_df)} orders")
        print(f"  - Date range: {self.orders_df['OrderDate'].min()} to {self.orders_df['OrderDate'].max()}")
        print(f"  - Total revenue: ${self.orders_df['TotalAmount'].sum():,.2f}")
        print(f"  - Avg order value: ${self.orders_df['TotalAmount'].mean():.2f}")
        print(f"  - Unique customers: {self.orders_df['CustomerID'].nunique()}")
        
        return self.orders_df
    
    def save_all_data(self, output_dir='data/raw'):
        """Save all datasets to CSV"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*80)
        print("SAVING DATA FILES")
        print("="*80)
        
        datasets = {
            'products.csv': self.products_df,
            'customers.csv': self.customers_df,
            'regions.csv': self.regions_df,
            'orders.csv': self.orders_df
        }
        
        for filename, df in datasets.items():
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"✓ Saved {filepath} ({len(df)} rows)")
        
        print(f"\n✓ All data saved to {output_dir}/")
        
        return output_dir


def main():
    """Main execution"""
    generator = SalesDataGenerator()
    
    # Generate all data
    generator.generate_products(n_products=200)
    generator.generate_regions()
    generator.generate_customers(n_customers=5000)
    generator.generate_orders(n_orders=50000)
    
    # Save to CSV
    generator.save_all_data()
    
    print("\n" + "="*80)
    print("DATA GENERATION COMPLETE!")
    print("="*80)
    print("\nDataset Summary:")
    print(f"  📦 Products: {len(generator.products_df)}")
    print(f"  👥 Customers: {len(generator.customers_df)}")
    print(f"  📍 Regions: {len(generator.regions_df)}")
    print(f"  🛒 Orders: {len(generator.orders_df)}")
    print(f"  💰 Total Revenue: ${generator.orders_df['TotalAmount'].sum():,.2f}")


if __name__ == "__main__":
    main()
