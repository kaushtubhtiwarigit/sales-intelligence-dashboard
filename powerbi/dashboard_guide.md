# Power BI Dashboard Setup Guide

## 📊 Building the Sales Intelligence Dashboard

### Step 1: Import Data

1. **Open Power BI Desktop**

2. **Get Data from CSV files:**
   - Click "Get Data" → "Text/CSV"
   - Navigate to `data/raw/` folder
   - Import all 4 files:
     - `orders.csv`
     - `customers.csv`
     - `products.csv`
     - `regions.csv`

3. **Transform Data (if needed):**
   - Click "Transform Data"
   - Verify data types:
     - OrderDate → Date
     - TotalAmount → Decimal
     - Quantity → Whole Number
   - Click "Close & Apply"

### Step 2: Create Relationships

Go to **Model View** and create relationships:

1. **Orders ↔ Customers**
   - Drag `CustomerID` from orders to `CustomerID` in customers
   - Cardinality: Many-to-One (*)
   - Cross filter direction: Single

2. **Orders ↔ Products**
   - Drag `ProductID` from orders to `ProductID` in products
   - Cardinality: Many-to-One (*)

3. **Customers ↔ Regions**
   - Drag `State` from customers to `State` in regions
   - Cardinality: Many-to-One (*)

### Step 3: Create Measures (DAX)

Go to **Data View** → Create new measures:

```dax
// Revenue Measures
Total Revenue = SUM(orders[TotalAmount])

Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    DATEADD(orders[OrderDate], -1, MONTH)
)

Revenue Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Last Month],
    [Revenue Last Month],
    0
) * 100

// Order Measures
Total Orders = COUNTROWS(orders)

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

// Customer Measures
Total Customers = DISTINCTCOUNT(orders[CustomerID])

Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT(orders[CustomerID]),
    FILTER(
        VALUES(orders[CustomerID]),
        CALCULATE(COUNTROWS(orders)) > 1
    )
)

Repeat Rate % = DIVIDE([Repeat Customers], [Total Customers], 0) * 100

// Product Measures
Products Sold = SUM(orders[Quantity])

Total Discount = SUM(orders[Discount])

// Profitability (if cost data available)
Gross Profit = 
SUMX(
    orders,
    orders[Quantity] * 
    RELATED(products[ListPrice]) - 
    orders[Quantity] * 
    RELATED(products[UnitCost])
)

Profit Margin % = DIVIDE([Gross Profit], [Total Revenue], 0) * 100
```

### Step 4: Dashboard Pages

## Page 1: Executive Summary

**KPI Cards (Top Row):**
1. Total Revenue (with growth %)
2. Total Orders
3. Total Customers
4. Average Order Value

**Main Visualizations:**
1. **Line Chart: Revenue Trend**
   - X-axis: OrderDate (Month)
   - Y-axis: Total Revenue
   - Add trend line

2. **Bar Chart: Top 10 Products**
   - Y-axis: ProductName
   - X-axis: Total Revenue
   - Sort: Descending

3. **Map: Sales by Region**
   - Location: State
   - Size: Total Revenue
   - Color: Profit Margin %

4. **Donut Chart: Revenue by Category**
   - Legend: Category
   - Values: Total Revenue

**Filters:**
- OrderDate (Date Range Slicer)
- Region (Dropdown)
- Category (Dropdown)

---

## Page 2: Sales Analysis

**Visualizations:**

1. **Clustered Column Chart: Monthly Revenue by Channel**
   - X-axis: OrderDate (Month)
   - Y-axis: Total Revenue
   - Legend: SalesChannel

2. **Stacked Bar Chart: Revenue by Category**
   - Y-axis: Category
   - X-axis: Total Revenue
   - Legend: OrderStatus

3. **Line and Stacked Column Chart: Orders vs Revenue**
   - X-axis: OrderDate (Month)
   - Column: Total Orders
   - Line: Total Revenue

4. **Matrix: Year-over-Year Comparison**
   - Rows: Month
   - Columns: Year
   - Values: Total Revenue

**Additional Cards:**
- Revenue Growth %
- Orders Growth %
- AOV Trend

---

## Page 3: Customer Analytics

**Visualizations:**

1. **Pie Chart: Customer Segmentation**
   - Legend: CustomerSegment
   - Values: Total Customers
   - Show percentages

2. **Funnel: Customer Journey**
   - Stages: New → First Purchase → Repeat → Loyal
   - Values: Customer counts at each stage

3. **Scatter Chart: RFM Analysis**
   - X-axis: Recency (days since last order)
   - Y-axis: Frequency (order count)
   - Size: Monetary (lifetime value)
   - Color: CustomerSegment

4. **Table: Top 20 Customers**
   - Columns: CustomerName, TotalOrders, LifetimeValue
   - Sort by LifetimeValue descending

5. **Line Chart: Customer Acquisition**
   - X-axis: RegistrationDate (Month)
   - Y-axis: Count of Customers

**Metrics:**
- Repeat Customer Rate
- Average Lifetime Value
- Customer Acquisition Cost (if available)

---

## Page 4: Product Performance

**Visualizations:**

1. **Matrix: Category × Subcategory Performance**
   - Rows: Category
   - Columns: Subcategory
   - Values: Total Revenue (heat map conditional formatting)

2. **Waterfall Chart: Revenue Contributors**
   - Show top categories contributing to total revenue

3. **Combo Chart: Units Sold vs Profit Margin**
   - X-axis: ProductName (Top 20)
   - Columns: Products Sold
   - Line: Profit Margin %

4. **Table: Product Details**
   - Columns: Product, Category, Units Sold, Revenue, Margin%
   - Conditional formatting on Margin%

5. **Scatter Chart: Price vs Volume**
   - X-axis: ListPrice
   - Y-axis: Units Sold
   - Size: Total Revenue
   - Color: Category

---

## Page 5: Regional Insights

**Visualizations:**

1. **Filled Map: Sales by State**
   - Location: State
   - Values: Total Revenue
   - Tooltips: Orders, Customers, AOV

2. **Clustered Bar Chart: Top 10 States**
   - Y-axis: State
   - X-axis: Total Revenue
   - Sort: Descending

3. **Table: Regional Performance**
   - Columns: Region, Orders, Revenue, Customers, AOV
   - Sort by Revenue

4. **Line Chart: Regional Trends**
   - X-axis: OrderDate (Month)
   - Y-axis: Total Revenue
   - Legend: Region

5. **Card Visuals:**
   - Best Performing Region
   - Fastest Growing Region

---

## Step 5: Add Interactivity

### Slicers (Add to all pages)
1. **Date Range Slicer**
   - Field: OrderDate
   - Style: Between
   - Position: Top right

2. **Region Dropdown**
   - Field: Region
   - Style: Dropdown
   - Allow "All"

3. **Category Multi-Select**
   - Field: Category
   - Style: Tile or List

### Drill-Through Pages
Create detail pages for:
- Customer Detail (drill from customer name)
- Product Detail (drill from product name)
- Regional Detail (drill from state/region)

### Bookmarks
Create bookmarks for:
- Current Year view
- Last Year view
- YoY Comparison
- High Value Customers only

---

## Step 6: Formatting & Polish

### Theme
- Use consistent color palette
- Recommended: Blue gradient for revenue
- Green for growth, Red for decline

### Titles
- Add clear titles to each visual
- Use dynamic titles with selected filters

### Tooltips
- Create custom tooltip pages
- Show relevant metrics on hover

### Mobile Layout
- Create mobile-optimized layouts
- Prioritize key metrics

---

## Step 7: Publish (Optional)

1. Save your .pbix file
2. Click "Publish" to Power BI Service
3. Set up scheduled refresh
4. Share with stakeholders

---

## 📊 Sample DAX Patterns

### Time Intelligence
```dax
// Same Period Last Year
Revenue LY = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(orders[OrderDate])
)

// Year to Date
Revenue YTD = 
TOTALYTD([Total Revenue], orders[OrderDate])

// Moving Average (3 months)
Revenue 3M Avg = 
AVERAGEX(
    DATESINPERIOD(orders[OrderDate], LASTDATE(orders[OrderDate]), -3, MONTH),
    [Total Revenue]
)
```

### Ranking
```dax
// Product Rank by Revenue
Product Rank = 
RANKX(
    ALL(products[ProductName]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)
```

### Segmentation
```dax
// Customer Value Tier
Customer Tier = 
VAR CustomerRevenue = [Total Revenue]
RETURN
    SWITCH(
        TRUE(),
        CustomerRevenue >= 10000, "Platinum",
        CustomerRevenue >= 5000, "Gold",
        CustomerRevenue >= 1000, "Silver",
        "Bronze"
    )
```

---

## 🎓 Tips for Interviews

### When Discussing This Dashboard:

1. **Data Model:**
   - "Created star schema with fact table (orders) and dimension tables"
   - "Established proper relationships with referential integrity"
   - "Optimized for query performance"

2. **DAX Measures:**
   - "Implemented time intelligence for YoY comparisons"
   - "Created calculated columns for customer segmentation"
   - "Used CALCULATE for complex filtering logic"

3. **Visualizations:**
   - "Selected appropriate chart types based on data characteristics"
   - "Line charts for trends, bars for comparisons, maps for geography"
   - "Implemented drill-through for detailed analysis"

4. **Business Insights:**
   - "Identified that Electronics category drives 40% of revenue"
   - "Discovered repeat customers have 3x higher AOV"
   - "Found Q4 seasonal spike of 35% in sales"

---

## 🔧 Troubleshooting

**Issue: Relationships not working**
- Check data types match in both tables
- Verify no blank or null values in key columns
- Use "Manage Relationships" to review

**Issue: Measures returning blank**
- Check filter context
- Verify table references are correct
- Use DAX Studio for debugging

**Issue: Slow performance**
- Reduce data volume (filter at source)
- Use aggregations
- Optimize DAX (avoid nested CALCULATE)

---

## 📚 Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [Power BI Community](https://community.powerbi.com/)
- [Enterprise DNA](https://enterprisedna.co/)

---

**Your Dashboard is Ready! 🎉**

This dashboard demonstrates:
✓ Data modeling skills
✓ DAX proficiency
✓ Visualization expertise
✓ Business intelligence understanding
