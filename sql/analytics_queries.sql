-- ============================================================================
-- SALES ANALYTICS - BUSINESS INTELLIGENCE QUERIES
-- ============================================================================
-- Comprehensive SQL queries for sales analysis
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. REVENUE OVERVIEW
-- ----------------------------------------------------------------------------

-- Total revenue summary
SELECT 
    COUNT(DISTINCT OrderID) as TotalOrders,
    COUNT(DISTINCT CustomerID) as UniqueCustomers,
    SUM(TotalAmount) as TotalRevenue,
    AVG(TotalAmount) as AvgOrderValue,
    SUM(Discount) as TotalDiscounts,
    SUM(ShippingCost) as TotalShipping
FROM orders
WHERE OrderStatus = 'Completed';


-- ----------------------------------------------------------------------------
-- 2. MONTHLY REVENUE TREND
-- ----------------------------------------------------------------------------

SELECT 
    strftime('%Y-%m', OrderDate) as Month,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue,
    SUM(Quantity) as UnitsSold
FROM orders
WHERE OrderStatus IN ('Completed', 'Shipped')
GROUP BY Month
ORDER BY Month;


-- ----------------------------------------------------------------------------
-- 3. YEAR-OVER-YEAR GROWTH
-- ----------------------------------------------------------------------------

WITH MonthlyRevenue AS (
    SELECT 
        strftime('%Y', OrderDate) as Year,
        strftime('%m', OrderDate) as Month,
        SUM(TotalAmount) as Revenue
    FROM orders
    WHERE OrderStatus = 'Completed'
    GROUP BY Year, Month
)
SELECT 
    Year,
    Month,
    Revenue as CurrentRevenue,
    LAG(Revenue, 12) OVER (ORDER BY Year, Month) as PriorYearRevenue,
    ROUND(((Revenue - LAG(Revenue, 12) OVER (ORDER BY Year, Month)) / 
           LAG(Revenue, 12) OVER (ORDER BY Year, Month)) * 100, 2) as YoYGrowthPct
FROM MonthlyRevenue
ORDER BY Year, Month;


-- ----------------------------------------------------------------------------
-- 4. TOP 10 PRODUCTS BY REVENUE
-- ----------------------------------------------------------------------------

SELECT 
    p.ProductName,
    p.Category,
    COUNT(DISTINCT o.OrderID) as TimesSold,
    SUM(o.Quantity) as TotalUnitsSold,
    SUM(o.TotalAmount) as TotalRevenue,
    AVG(o.TotalAmount) as AvgOrderValue
FROM orders o
JOIN products p ON o.ProductID = p.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.ProductID, p.ProductName, p.Category
ORDER BY TotalRevenue DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 5. CATEGORY PERFORMANCE
-- ----------------------------------------------------------------------------

SELECT 
    Category,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    SUM(Quantity) as UnitsSold,
    AVG(TotalAmount) as AvgOrderValue,
    ROUND(SUM(TotalAmount) * 100.0 / (SELECT SUM(TotalAmount) FROM orders WHERE OrderStatus = 'Completed'), 2) as RevenuePct
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY Category
ORDER BY Revenue DESC;


-- ----------------------------------------------------------------------------
-- 6. CUSTOMER LIFETIME VALUE (CLV)
-- ----------------------------------------------------------------------------

SELECT 
    c.CustomerID,
    c.FirstName || ' ' || c.LastName as CustomerName,
    c.CustomerSegment,
    COUNT(DISTINCT o.OrderID) as TotalOrders,
    SUM(o.TotalAmount) as LifetimeValue,
    AVG(o.TotalAmount) as AvgOrderValue,
    MIN(o.OrderDate) as FirstPurchase,
    MAX(o.OrderDate) as LastPurchase,
    ROUND(julianday(MAX(o.OrderDate)) - julianday(MIN(o.OrderDate)), 0) as DaysSinceFirst
FROM customers c
JOIN orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.CustomerID
ORDER BY LifetimeValue DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 7. CUSTOMER SEGMENTATION (RFM Analysis)
-- ----------------------------------------------------------------------------

WITH RFM AS (
    SELECT 
        CustomerID,
        -- Use dataset's max date as reference instead of current date
        CAST(julianday((SELECT MAX(OrderDate) FROM orders WHERE OrderStatus = 'Completed')) - julianday(MAX(OrderDate)) AS INTEGER) as Recency,
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
    COUNT(*) as Customers,
    ROUND(AVG(Monetary), 2) as AvgLifetimeValue,
    ROUND(AVG(Frequency), 1) as AvgOrderCount
FROM RFM_Scores
GROUP BY Segment
ORDER BY Customers DESC;


-- ----------------------------------------------------------------------------
-- 8. REPEAT CUSTOMER ANALYSIS
-- ----------------------------------------------------------------------------

WITH CustomerOrderCounts AS (
    SELECT 
        CustomerID,
        COUNT(DISTINCT OrderID) as OrderCount
    FROM orders
    WHERE OrderStatus = 'Completed'
    GROUP BY CustomerID
)
SELECT 
    CASE 
        WHEN OrderCount = 1 THEN 'One-Time'
        WHEN OrderCount BETWEEN 2 AND 5 THEN 'Repeat (2-5)'
        WHEN OrderCount BETWEEN 6 AND 10 THEN 'Frequent (6-10)'
        ELSE 'VIP (11+)'
    END as CustomerType,
    COUNT(*) as Customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM CustomerOrderCounts), 2) as Percentage
FROM CustomerOrderCounts
GROUP BY CustomerType
ORDER BY 
    CASE CustomerType
        WHEN 'One-Time' THEN 1
        WHEN 'Repeat (2-5)' THEN 2
        WHEN 'Frequent (6-10)' THEN 3
        ELSE 4
    END;


-- ----------------------------------------------------------------------------
-- 9. REGIONAL SALES PERFORMANCE
-- ----------------------------------------------------------------------------

SELECT 
    Region,
    COUNT(DISTINCT OrderID) as Orders,
    COUNT(DISTINCT CustomerID) as Customers,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue,
    SUM(Quantity) as UnitsSold,
    ROUND(SUM(TotalAmount) * 100.0 / (SELECT SUM(TotalAmount) FROM orders WHERE OrderStatus = 'Completed'), 2) as RevenuePct
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY Region
ORDER BY Revenue DESC;


-- ----------------------------------------------------------------------------
-- 10. STATE-LEVEL SALES BREAKDOWN
-- ----------------------------------------------------------------------------

SELECT 
    State,
    Region,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue,
    RANK() OVER (ORDER BY SUM(TotalAmount) DESC) as RevenueRank
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY State, Region
ORDER BY Revenue DESC
LIMIT 15;


-- ----------------------------------------------------------------------------
-- 11. SALES CHANNEL PERFORMANCE
-- ----------------------------------------------------------------------------

SELECT 
    SalesChannel,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue,
    ROUND(SUM(TotalAmount) * 100.0 / (SELECT SUM(TotalAmount) FROM orders WHERE OrderStatus = 'Completed'), 2) as RevenuePct,
    ROUND(AVG(Discount), 2) as AvgDiscount
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY SalesChannel
ORDER BY Revenue DESC;


-- ----------------------------------------------------------------------------
-- 12. PAYMENT METHOD ANALYSIS
-- ----------------------------------------------------------------------------

SELECT 
    PaymentMethod,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue,
    ROUND(AVG(Discount), 2) as AvgDiscount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders WHERE OrderStatus = 'Completed'), 2) as UsagePct
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY PaymentMethod
ORDER BY Orders DESC;


-- ----------------------------------------------------------------------------
-- 13. MONTHLY CUSTOMER ACQUISITION
-- ----------------------------------------------------------------------------

SELECT 
    strftime('%Y-%m', RegistrationDate) as Month,
    COUNT(*) as NewCustomers,
    SUM(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', RegistrationDate)) as CumulativeCustomers
FROM customers
GROUP BY Month
ORDER BY Month;


-- ----------------------------------------------------------------------------
-- 14. COHORT ANALYSIS (Monthly Registration)
-- ----------------------------------------------------------------------------

WITH FirstPurchase AS (
    SELECT 
        CustomerID,
        DATE(MIN(OrderDate)) as FirstOrderDate,
        strftime('%Y-%m', MIN(OrderDate)) as Cohort
    FROM orders
    WHERE OrderStatus = 'Completed'
    GROUP BY CustomerID
),
CohortActivity AS (
    SELECT 
        fp.Cohort,
        strftime('%Y-%m', o.OrderDate) as ActivityMonth,
        COUNT(DISTINCT o.CustomerID) as ActiveCustomers
    FROM FirstPurchase fp
    JOIN orders o ON fp.CustomerID = o.CustomerID
    WHERE o.OrderStatus = 'Completed'
    GROUP BY fp.Cohort, ActivityMonth
)
SELECT 
    Cohort,
    COUNT(DISTINCT ActiveCustomers) as CohortSize,
    ActivityMonth,
    ActiveCustomers,
    ROUND(ActiveCustomers * 100.0 / (
        SELECT COUNT(DISTINCT CustomerID) 
        FROM FirstPurchase 
        WHERE Cohort = ca.Cohort
    ), 2) as RetentionRate
FROM CohortActivity ca
WHERE Cohort >= '2023-01'
ORDER BY Cohort, ActivityMonth;


-- ----------------------------------------------------------------------------
-- 15. AVERAGE ORDER VALUE BY CUSTOMER SEGMENT
-- ----------------------------------------------------------------------------

SELECT 
    c.CustomerSegment,
    COUNT(DISTINCT o.OrderID) as Orders,
    COUNT(DISTINCT o.CustomerID) as Customers,
    SUM(o.TotalAmount) as Revenue,
    AVG(o.TotalAmount) as AvgOrderValue,
    ROUND(AVG(o.Discount), 2) as AvgDiscount,
    ROUND(AVG(o.Quantity), 1) as AvgQuantity
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderStatus = 'Completed'
GROUP BY c.CustomerSegment
ORDER BY Revenue DESC;


-- ----------------------------------------------------------------------------
-- 16. PRODUCT PROFITABILITY ANALYSIS
-- ----------------------------------------------------------------------------

SELECT 
    p.ProductName,
    p.Category,
    p.ListPrice,
    p.UnitCost,
    p.ProfitMargin as ProductMargin,
    COUNT(DISTINCT o.OrderID) as TimesSold,
    SUM(o.Quantity) as UnitsSold,
    SUM(o.TotalAmount) as Revenue,
    SUM(o.Quantity * p.UnitCost) as TotalCost,
    SUM(o.TotalAmount) - SUM(o.Quantity * p.UnitCost) as GrossProfit,
    ROUND((SUM(o.TotalAmount) - SUM(o.Quantity * p.UnitCost)) / SUM(o.TotalAmount) * 100, 2) as ActualMargin
FROM orders o
JOIN products p ON o.ProductID = p.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.ProductID
HAVING UnitsSold > 10
ORDER BY GrossProfit DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 17. SLOW-MOVING INVENTORY
-- ----------------------------------------------------------------------------

SELECT 
    p.ProductID,
    p.ProductName,
    p.Category,
    p.StockQuantity,
    COALESCE(SUM(o.Quantity), 0) as UnitsSoldLast90Days,
    ROUND(p.StockQuantity * 1.0 / NULLIF(SUM(o.Quantity), 0), 2) as DaysOfInventory
FROM products p
LEFT JOIN orders o ON p.ProductID = o.ProductID 
    AND o.OrderDate >= date('now', '-90 days')
    AND o.OrderStatus = 'Completed'
WHERE p.IsActive = 1
GROUP BY p.ProductID
HAVING UnitsSoldLast90Days < 10 AND p.StockQuantity > 50
ORDER BY DaysOfInventory DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 18. SALES TRENDS BY DAY OF WEEK
-- ----------------------------------------------------------------------------

SELECT 
    CASE CAST(strftime('%w', OrderDate) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as DayOfWeek,
    CAST(strftime('%w', OrderDate) AS INTEGER) as DayNum,
    COUNT(DISTINCT OrderID) as Orders,
    SUM(TotalAmount) as Revenue,
    AVG(TotalAmount) as AvgOrderValue
FROM orders
WHERE OrderStatus = 'Completed'
GROUP BY DayOfWeek, DayNum
ORDER BY DayNum;


-- ----------------------------------------------------------------------------
-- 19. CROSS-SELL OPPORTUNITIES (Products Bought Together)
-- ----------------------------------------------------------------------------

WITH ProductPairs AS (
    SELECT 
        o1.ProductID as Product1,
        o2.ProductID as Product2,
        COUNT(DISTINCT o1.CustomerID) as Customers
    FROM orders o1
    JOIN orders o2 
        ON o1.CustomerID = o2.CustomerID 
        AND o1.ProductID < o2.ProductID
    WHERE o1.OrderStatus = 'Completed' 
        AND o2.OrderStatus = 'Completed'
    GROUP BY Product1, Product2
    HAVING Customers >= 5
)
SELECT 
    p1.ProductName as Product1,
    p2.ProductName as Product2,
    pp.Customers,
    p1.Category as Category1,
    p2.Category as Category2
FROM ProductPairs pp
JOIN products p1 ON pp.Product1 = p1.ProductID
JOIN products p2 ON pp.Product2 = p2.ProductID
ORDER BY pp.Customers DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 20. DISCOUNT EFFECTIVENESS ANALYSIS
-- ----------------------------------------------------------------------------

WITH DiscountBrackets AS (
    SELECT 
        OrderID,
        TotalAmount,
        Discount,
        CASE 
            WHEN Discount = 0 THEN 'No Discount'
            WHEN Discount > 0 AND Discount <= 10 THEN '1-10'
            WHEN Discount > 10 AND Discount <= 25 THEN '11-25'
            WHEN Discount > 25 AND Discount <= 50 THEN '26-50'
            ELSE '50+'
        END as DiscountRange
    FROM orders
    WHERE OrderStatus = 'Completed'
)
SELECT 
    DiscountRange,
    COUNT(*) as Orders,
    ROUND(AVG(TotalAmount), 2) as AvgOrderValue,
    ROUND(AVG(Discount), 2) as AvgDiscount,
    ROUND(SUM(TotalAmount), 2) as TotalRevenue
FROM DiscountBrackets
GROUP BY DiscountRange
ORDER BY 
    CASE DiscountRange
        WHEN 'No Discount' THEN 1
        WHEN '1-10' THEN 2
        WHEN '11-25' THEN 3
        WHEN '26-50' THEN 4
        ELSE 5
    END;
