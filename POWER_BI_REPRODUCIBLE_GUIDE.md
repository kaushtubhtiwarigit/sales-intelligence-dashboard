# Power BI Dashboard - Reproducible Setup Guide

**Time Required**: 15-20 minutes  
**Difficulty**: Beginner-friendly  
**Prerequisites**: Power BI Desktop installed

## Overview

This guide provides **exact steps** to recreate the Sales Intelligence Dashboard in Power BI Desktop. Follow each section to build a professional dashboard that matches the SQL analytics.

---

## Step 1: Import Data (5 minutes)

### 1.1 Open Power BI Desktop
- Launch Power BI Desktop
- Click "Get Data" → "Text/CSV"

### 1.2 Import Each CSV File

Import in this order:

**File 1: regions.csv**
- Navigate to `data/raw/regions.csv`
- Click "Load"
- ✅ Should see 20 rows (5 regions × 4 states each)

**File 2: products.csv**
- Get Data → Text/CSV → `data/raw/products.csv`
- Click "Load"
- ✅ Should see 200 rows

**File 3: customers.csv**
- Get Data → Text/CSV → `data/raw/customers.csv`
- Click "Load"
- ✅ Should see 5,000 rows

**File 4: orders.csv**
- Get Data → Text/CSV → `data/raw/orders.csv`
- Click "Transform Data" (not "Load" - we need to fix date format)

#### Transform orders.csv
In Power Query Editor:
1. Select `OrderDate` column
2. Right-click → Change Type → Date
3. Select `RegistrationDate` column (if visible from customers)
4. Right-click → Change Type → Date
5. Click "Close & Apply"

---

## Step 2: Create Relationships (3 minutes)

### 2.1 Open Model View
- Click "Model" icon on left sidebar (looks like connected boxes)

### 2.2 Create Relationships

Create these relationships by dragging fields:

**Relationship 1: orders → products**
- Drag `orders[ProductID]` to `products[ProductID]`
- Cardinality: Many to One (*:1)
- Cross filter direction: Single
- ✅ Should see line connecting tables

**Relationship 2: orders → customers**
- Drag `orders[CustomerID]` to `customers[CustomerID]`
- Cardinality: Many to One (*:1)
- Cross filter direction: Single

**Relationship 3: orders → regions**
- Drag `orders[State]` to `regions[State]`
- Cardinality: Many to One (*:1)
- Cross filter direction: Single

### 2.3 Verify Relationships
You should now have a star schema:
```
        products
             ↑
             |
        orders (fact table)
        /    \
       /      \
customers   regions
```

---

## Step 3: Create Measures (5 minutes)

### 3.1 Create Measures Table
- Right-click in Fields pane
- New Table
- Name: `_Measures`
- Formula: `_Measures = ROW("X", 1)`

### 3.2 Add Key Measures

Click "New Measure" and add each:

**Total Revenue**
```dax
Total Revenue = 
SUM(orders[TotalAmount])
```

**Total Orders**
```dax
Total Orders = 
COUNTROWS(orders)
```

**Average Order Value**
```dax
Avg Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

**Total Customers**
```dax
Total Customers = 
DISTINCTCOUNT(orders[CustomerID])
```

**Total Quantity Sold**
```dax
Total Quantity = 
SUM(orders[Quantity])
```

**Completed Orders**
```dax
Completed Orders = 
CALCULATE(
    [Total Orders],
    orders[OrderStatus] = "Completed"
)
```

**Completed Revenue**
```dax
Completed Revenue = 
CALCULATE(
    [Total Revenue],
    orders[OrderStatus] = "Completed"
)
```

**YoY Revenue Growth**
```dax
YoY Growth % = 
VAR CurrentYear = [Completed Revenue]
VAR PreviousYear = 
    CALCULATE(
        [Completed Revenue],
        SAMEPERIODLASTYEAR(orders[OrderDate])
    )
RETURN
    DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100
```

---

## Step 4: Build Dashboard Pages (7 minutes)

### Page 1: Executive Overview

**Create these visuals:**

**1. KPI Cards (Top Row)**
- Insert → Card visual (4 cards across)
- Card 1: `Completed Revenue` 
  - Format: Currency, $
  - Title: "Total Revenue"
- Card 2: `Completed Orders`
  - Format: Whole number
  - Title: "Total Orders"
- Card 3: `Total Customers`
  - Title: "Unique Customers"
- Card 4: `Avg Order Value`
  - Format: Currency, $
  - Title: "Avg Order Value"

**2. Revenue Trend (Large Chart)**
- Visual: Line Chart
- X-axis: `orders[OrderDate]` (by Month)
- Y-axis: `Completed Revenue`
- Title: "Monthly Revenue Trend"
- Enable data labels

**3. Top 10 Products (Right Side)**
- Visual: Horizontal Bar Chart
- Y-axis: `products[ProductName]`
- X-axis: `Completed Revenue`
- Top N filter: Top 10 by Revenue
- Title: "Top 10 Products by Revenue"

**4. Regional Performance (Bottom Left)**
- Visual: Map or Filled Map
- Location: `regions[Region]`
- Size: `Completed Revenue`
- Title: "Sales by Region"

**5. Category Mix (Bottom Right)**
- Visual: Donut Chart
- Legend: `orders[Category]`
- Values: `Completed Revenue`
- Title: "Revenue by Category"
- Enable percentage labels

---

### Page 2: Customer Analysis

**Create these visuals:**

**1. Customer Segment Performance**
- Visual: Clustered Bar Chart
- Y-axis: `customers[CustomerSegment]`
- X-axis: `Completed Revenue`, `Total Orders`
- Title: "Performance by Customer Segment"

**2. Repeat Customer Distribution**
- Visual: Pie Chart
- Create calculated column in customers table:
```dax
Order Bucket = 
VAR OrderCount = CALCULATE(COUNTROWS(orders), orders[OrderStatus] = "Completed")
RETURN
    SWITCH(
        TRUE(),
        OrderCount = 1, "One-Time",
        OrderCount <= 5, "Repeat (2-5)",
        OrderCount <= 10, "Frequent (6-10)",
        "VIP (11+)"
    )
```
- Legend: `customers[Order Bucket]`
- Values: Count of customers
- Title: "Customer Type Distribution"

**3. Top 20 Customers (CLV)**
- Visual: Table
- Columns:
  - `customers[FirstName]` & `LastName` (combine)
  - `customers[CustomerSegment]`
  - `Completed Revenue` (rename to "Lifetime Value")
  - `Completed Orders`
- Top N filter: Top 20 by Lifetime Value
- Title: "Top 20 Customers by CLV"

**4. Customer Acquisition Trend**
- Visual: Area Chart
- X-axis: `customers[RegistrationDate]` (by Month)
- Y-axis: Count of customers
- Title: "Monthly Customer Acquisition"

---

### Page 3: Product & Category Insights

**1. Category Performance Matrix**
- Visual: Matrix
- Rows: `orders[Category]`
- Values: 
  - `Completed Revenue`
  - `Completed Orders`
  - `Avg Order Value`
  - `Total Quantity`
- Enable conditional formatting on Revenue (color scale)

**2. Sales Channel Comparison**
- Visual: Clustered Column Chart
- X-axis: `orders[SalesChannel]`
- Y-axis: `Completed Revenue`
- Legend: `orders[Category]`
- Title: "Revenue by Channel and Category"

**3. Payment Method Usage**
- Visual: Donut Chart
- Legend: `orders[PaymentMethod]`
- Values: Count of orders
- Title: "Payment Method Distribution"

**4. Product Profitability**
- Visual: Scatter Chart
- X-axis: `Total Quantity` (units sold)
- Y-axis: `Completed Revenue`
- Size: `products[ProfitMargin]`
- Details: `products[ProductName]`
- Title: "Product Performance: Volume vs Revenue"

---

### Page 4: Time Analysis

**1. Sales by Day of Week**
- Visual: Column Chart
- Create calculated column:
```dax
Day of Week = 
FORMAT(orders[OrderDate], "dddd")
```
- X-axis: `orders[Day of Week]`
- Y-axis: `Completed Revenue`
- Sort by: Day number (Monday=1, Sunday=7)

**2. Hourly Sales Pattern** (if time data exists)
- Visual: Line Chart
- X-axis: Hour of day
- Y-axis: `Completed Revenue`

**3. YoY Comparison**
- Visual: Clustered Column Chart
- X-axis: Month
- Y-axis: `Completed Revenue`
- Legend: Year
- Title: "Year-over-Year Revenue Comparison"

**4. Sales Velocity Indicator**
- Visual: Gauge
- Value: `YoY Growth %`
- Min: -50%
- Max: 50%
- Target: 0%

---

## Step 5: Add Slicers & Filters (2 minutes)

### Add Slicers to Each Page

**Common Slicers (all pages)**:
- Date Range: `orders[OrderDate]` (Between slicer)
- Region: `regions[Region]` (Dropdown)
- Category: `orders[Category]` (Checkbox list)
- Status: `orders[OrderStatus]` (Dropdown, default: "Completed")

**Position**: Place slicers in left sidebar (10% width)

### Sync Slicers Across Pages
1. View → Sync Slicers
2. Select Date Range slicer
3. Check all pages
4. Repeat for other slicers

---

## Step 6: Format & Polish (3 minutes)

### 6.1 Apply Theme
- View → Themes → Choose modern theme (e.g., "Executive")

### 6.2 Format Visuals
For all visuals:
- Title: Bold, 14pt
- Background: Light gray (#F5F5F5)
- Border: 1px solid #E0E0E0
- Padding: 10px

### 6.3 Format Cards
- Font size: 36pt for value
- Font size: 12pt for label
- Alignment: Center

### 6.4 Color Scheme
Use consistent colors:
- Revenue: Blue (#1F77B4)
- Orders: Orange (#FF7F0E)
- Customers: Green (#2CA02C)
- Products: Red (#D62728)

---

## Step 7: Test & Validate (2 minutes)

### Validation Checklist

- [ ] All 4 CSV files imported
- [ ] All 3 relationships active
- [ ] All 8 measures calculating correctly
- [ ] All visualizations showing data
- [ ] Slicers filter all pages
- [ ] No error messages in any visual
- [ ] Date range slicer works
- [ ] Export to PDF works

### Quick Tests

**Test 1: Filter by Region**
- Select "Northeast" region
- Revenue should be ~20% of total
- All visuals should update

**Test 2: Filter by Date**
- Select Jan-Mar 2024
- All metrics should decrease
- Trend chart should show only selected period

**Test 3: Drill Down**
- Click on a product in Top 10
- Other visuals should filter to that product

---

## Step 8: Save & Export

### 8.1 Save Dashboard
- File → Save As
- Name: `sales_intelligence_dashboard.pbix`
- Location: Project root folder

### 8.2 Export Screenshots
For documentation:
1. File → Export → PDF
2. Save as: `dashboard_screenshots.pdf`

### 8.3 Publish (Optional)
If you have Power BI Pro:
- File → Publish → To Power BI
- Select workspace
- Share with team

---

## Expected Results

### Key Metrics You Should See

Based on generated data (50K orders, 5K customers):

- **Total Revenue**: ~$25M - $35M
- **Total Orders**: ~45,000 completed
- **Average Order Value**: ~$550 - $650
- **Total Customers**: ~5,000
- **Top Region**: Varies (roughly equal distribution)
- **Top Category**: Varies (roughly equal)
- **Peak Month**: Should see seasonal trends

### Visual Appearance

**Page 1 Layout**:
```
┌────────────────────────────────────────────────────────┐
│  Revenue     Orders      Customers    Avg Order Value  │
│  $30.5M      45,234      4,987        $624             │
├─────────────────────────────────┬──────────────────────┤
│                                 │  Top 10 Products     │
│   Monthly Revenue Trend         │  1. Product A $2.1M  │
│   (Line Chart)                  │  2. Product B $1.9M  │
│                                 │  ...                 │
├──────────────────┬──────────────┴──────────────────────┤
│  Regional Map    │  Category Donut Chart               │
│                  │                                     │
└──────────────────┴─────────────────────────────────────┘
```

---

## Troubleshooting

### Issue: No data in visuals
**Solution**: Check relationships are active and correct cardinality

### Issue: Dates not sorting correctly
**Solution**: Ensure OrderDate is Date type, not Text

### Issue: Measures showing blank
**Solution**: Check filter context - ensure "Completed" orders selected

### Issue: Regional map not working
**Solution**: Verify State field matches regions.csv exactly

### Issue: Performance slow
**Solution**: 
- Reduce data volume in testing
- Use Import mode (not DirectQuery)
- Remove unnecessary columns in Power Query

---

## Advanced Enhancements (Optional)

### Add Bookmarks
- Create bookmark for each key insight
- Add buttons to navigate bookmarks

### Add Drill-Through Pages
- Create detail page for product deep-dive
- Enable drill-through from product visuals

### Add Tooltips
- Create custom tooltip pages
- Show product details on hover

### Add Parameters
- Create "What-If" parameter for discount scenarios
- Add goal-setting parameters

---

## Deliverable Checklist

After completing this guide, you should have:

- [x] `.pbix` file with complete dashboard
- [x] 4 pages of visualizations
- [x] 8+ calculated measures
- [x] Proper relationships between tables
- [x] Synchronized slicers
- [x] Professional formatting
- [x] PDF export of dashboard
- [x] Tested and validated all visuals

---

## Time Estimate Breakdown

- Import Data: 5 min
- Create Relationships: 3 min
- Create Measures: 5 min
- Build Visuals: 7 min
- Add Slicers: 2 min
- Format: 3 min
- Test: 2 min
- **Total: ~20 minutes**

---

## For Interviews

When asked about Power BI:

**What you built**:
- "Complete sales intelligence dashboard with 4 pages"
- "Executive overview, customer analysis, product insights, time analysis"
- "8 DAX measures including YoY growth and customer lifetime value"
- "Star schema data model with proper relationships"

**Technical skills demonstrated**:
- Data modeling and relationships
- DAX measure creation
- Advanced visuals and formatting
- Slicer synchronization
- User experience design

**What you'd add next**:
- "Row-level security for multi-tenant access"
- "Predictive analytics using Power BI's ML features"
- "Mobile-optimized layout"
- "Scheduled refresh from live data source"

---

## Resources

**Power BI Desktop Download**: 
https://powerbi.microsoft.com/desktop

**DAX Reference**:
https://dax.guide

**Power BI Documentation**:
https://docs.microsoft.com/power-bi

---

**Created**: September 22, 2026  
**Last Updated**: September 22, 2026  
**Time to Complete**: 15-20 minutes  
**Difficulty**: ⭐⭐☆☆☆ (Beginner-friendly)
