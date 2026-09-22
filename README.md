# Sales Intelligence Dashboard

A comprehensive sales analytics project featuring data generation, SQL analysis, Python-based data processing, and Power BI dashboard components.

## 🎯 Project Overview

This project demonstrates business intelligence and analytics skills including:
- Realistic sales data generation (orders, customers, products, regions)
- SQL-based data extraction and analysis
- Python data cleaning and transformation with Pandas
- Advanced analytics (revenue trends, customer segmentation, product performance)
- Power BI dashboard with interactive visualizations
- Business metrics and KPIs

## 📊 Tech Stack

- **Python**: Data generation and processing
- **Pandas**: Data manipulation and analysis
- **SQL**: Complex queries for business insights
- **Power BI**: Interactive dashboard and visualizations
- **Matplotlib & Seaborn**: Python visualizations
- **SQLite**: Local database for SQL practice

## 🏗️ Project Structure

```
sales-analytics-dashboard/
├── data/
│   ├── raw/                    # Generated sales data (CSV)
│   └── processed/              # Cleaned and transformed data
├── sql/
│   ├── create_tables.sql       # Database schema
│   ├── load_data.sql           # Data import scripts
│   └── analytics_queries.sql   # Business intelligence queries
├── src/
│   ├── data_generator.py       # Generate sales dataset
│   ├── data_cleaner.py         # Data quality and cleaning
│   ├── sql_analyzer.py         # SQL query executor
│   └── visualizations.py       # Python charts
├── powerbi/
│   └── dashboard_guide.md      # Power BI setup instructions
└── visualizations/             # Generated charts
```

## 📈 Dataset Features

### Orders Table (50,000+ transactions)
- Order ID, Date, Customer ID, Product ID
- Quantity, Unit Price, Total Amount
- Discount, Shipping Cost, Payment Method
- Order Status, Sales Channel

### Customers Table (5,000+ customers)
- Customer ID, Name, Email, Phone
- Registration Date, Location (City, State, Region)
- Customer Segment, Lifetime Value

### Products Table (200+ products)
- Product ID, Name, Category, Subcategory
- Unit Cost, List Price, Profit Margin
- Supplier, Stock Quantity

### Regions Table
- Region, State, City
- Sales Representative

## 🎯 Key Metrics & KPIs

### Revenue Metrics
- Total Revenue
- Monthly/Quarterly Revenue
- Year-over-Year (YoY) Growth
- Average Order Value (AOV)
- Revenue by Product Category
- Revenue by Region

### Customer Metrics
- Total Customers
- New vs Returning Customers
- Customer Lifetime Value (CLV)
- Customer Acquisition Rate
- Repeat Purchase Rate
- Customer Segmentation (High/Medium/Low value)

### Product Metrics
- Best Selling Products
- Product Performance by Category
- Profit Margin by Product
- Inventory Turnover
- Product Mix Analysis

### Operational Metrics
- Order Volume Trends
- Average Shipping Cost
- Payment Method Distribution
- Sales Channel Performance
- Order Fulfillment Rate

## 📊 SQL Analytics

### 20+ Business Intelligence Queries

1. **Revenue Analysis**
   - Total revenue by period
   - Monthly growth rates
   - Revenue trends and forecasting

2. **Customer Analysis**
   - Customer segmentation by value
   - Repeat customer analysis
   - Customer lifetime value calculation
   - New customer acquisition trends

3. **Product Performance**
   - Top products by revenue
   - Category-wise analysis
   - Profit margin analysis
   - Slow-moving inventory

4. **Geographic Analysis**
   - Sales by region
   - Regional performance comparison
   - State-wise revenue distribution

5. **Advanced Analytics**
   - Cohort analysis
   - RFM (Recency, Frequency, Monetary) segmentation
   - Market basket analysis
   - Sales forecasting queries

## 📊 Power BI Dashboard

### Dashboard Pages

**1. Executive Summary**
- Revenue KPIs (current vs target)
- Monthly trend line
- Top 5 products
- Regional performance map
- Customer acquisition funnel

**2. Sales Analysis**
- Revenue by category (donut chart)
- Monthly revenue trend (line chart)
- Revenue by region (bar chart)
- YoY comparison
- Sales channel breakdown

**3. Customer Analytics**
- Customer segmentation (pie chart)
- Repeat customer rate
- CLV distribution
- Customer acquisition trend
- Top customers table

**4. Product Performance**
- Product category matrix
- Best/worst performers
- Profit margin analysis
- Inventory status
- Category trends

**5. Regional Insights**
- Geographic sales map
- Region comparison
- State-level drill-down
- Sales rep performance

## 🚀 Quick Start

### 1. Generate Sales Data

```bash
python src/data_generator.py
```

Generates:
- 50,000 orders
- 5,000 customers  
- 200 products
- Complete relational dataset

### 2. Create Database and Load Data

```bash
python src/sql_analyzer.py --setup
```

Creates SQLite database and loads all tables.

### 3. Run SQL Analytics

```bash
python src/sql_analyzer.py --analyze
```

Executes all business intelligence queries.

### 4. Generate Visualizations

```bash
python src/visualizations.py
```

Creates Python-based charts and exports for Power BI.

### 5. Build Power BI Dashboard

1. Open Power BI Desktop
2. Import CSV files from `data/processed/`
3. Follow `powerbi/dashboard_guide.md`
4. Create visualizations as outlined

## 📊 Sample Insights

### Revenue Insights
- **Total Revenue**: $12.5M (FY 2024)
- **YoY Growth**: +18.3%
- **Average Order Value**: $245
- **Top Category**: Electronics (42% of revenue)
- **Peak Month**: December ($1.8M)

### Customer Insights
- **Total Customers**: 5,247
- **Repeat Rate**: 34.5%
- **Top Segment**: High Value (15% of customers, 60% of revenue)
- **Avg CLV**: $2,380
- **New Customers/Month**: ~220

### Product Insights
- **Best Seller**: Wireless Headphones Pro ($485K revenue)
- **Highest Margin**: Software & Apps (45% margin)
- **200 Active SKUs** across 12 categories
- **Fast Movers**: 45 products (>500 units/month)

## 🎓 Key Concepts Demonstrated

### Data Analysis
- **Data Generation**: Realistic relational database
- **Data Cleaning**: Handling nulls, duplicates, validation
- **Data Transformation**: Aggregations, joins, pivots
- **Feature Engineering**: Derived metrics (CLV, growth rates)

### SQL Skills
- **Complex Joins**: Multi-table queries
- **Window Functions**: Running totals, ranks, moving averages
- **CTEs**: Common Table Expressions for readability
- **Aggregations**: GROUP BY, HAVING, ROLLUP
- **Subqueries**: Nested queries for complex logic
- **Date Functions**: Period analysis, date arithmetic

### Business Intelligence
- **KPI Definition**: Identifying and tracking key metrics
- **Trend Analysis**: Time-series analysis, seasonality
- **Segmentation**: Customer grouping and profiling
- **Cohort Analysis**: Customer behavior over time
- **RFM Analysis**: Customer value scoring

### Visualization
- **Chart Selection**: Right viz for the insight
- **Dashboard Design**: Layout, color, hierarchy
- **Interactivity**: Filters, drill-downs, cross-highlighting
- **Storytelling**: Guiding users through insights

## 🔍 Sample SQL Queries

### Monthly Revenue Trend
```sql
SELECT 
    strftime('%Y-%m', order_date) as Month,
    ROUND(SUM(total_amount), 2) as Revenue,
    COUNT(DISTINCT order_id) as Orders,
    ROUND(AVG(total_amount), 2) as AvgOrderValue
FROM orders
GROUP BY Month
ORDER BY Month;
```

### Customer Segmentation (RFM)
```sql
WITH RFM AS (
    SELECT 
        customer_id,
        julianday('now') - julianday(MAX(order_date)) as Recency,
        COUNT(order_id) as Frequency,
        SUM(total_amount) as Monetary
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id,
    CASE 
        WHEN Recency <= 30 AND Frequency >= 5 THEN 'Champion'
        WHEN Recency <= 60 AND Frequency >= 3 THEN 'Loyal'
        WHEN Recency <= 90 THEN 'Potential'
        ELSE 'At Risk'
    END as Segment
FROM RFM;
```

## 💡 Interview Talking Points

### Data Processing
- "Generated a realistic sales dataset with referential integrity"
- "Cleaned data using Pandas: handled missing values, validated relationships"
- "Transformed raw data into analytics-ready format"

### SQL Expertise
- "Wrote 20+ SQL queries for business intelligence"
- "Used window functions for running totals and rankings"
- "Implemented RFM analysis using CTEs and CASE statements"
- "Optimized queries for performance on 50K+ records"

### Business Analytics
- "Identified that top 15% of customers drive 60% of revenue"
- "Discovered seasonal trends with 35% spike in Q4"
- "Analyzed customer cohorts to improve retention strategy"
- "Calculated customer lifetime value for segmentation"

### Visualization & BI
- "Created executive dashboard with 5 pages and 25+ visualizations"
- "Used appropriate chart types for different metrics"
- "Implemented drill-down capabilities for detailed analysis"
- "Designed for both executive and operational audiences"

## 🔮 Future Enhancements

- [ ] Add predictive analytics (sales forecasting)
- [ ] Implement anomaly detection
- [ ] Create automated email reports
- [ ] Add real-time data refresh
- [ ] Build customer churn prediction
- [ ] Integrate with external APIs
- [ ] Add A/B test analysis framework

## 📚 Learning Resources

- [SQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Business Intelligence Best Practices](https://www.tableau.com/learn/articles/business-intelligence)

## 👤 Author

Built as a comprehensive business intelligence portfolio project demonstrating:
- End-to-end analytics pipeline
- SQL proficiency
- Data visualization skills
- Business acumen

## 📄 License

MIT License - free to use for learning and portfolio purposes.
