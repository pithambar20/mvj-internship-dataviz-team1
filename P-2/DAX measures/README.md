# Namma Metro Power BI -- DAX Measures

## Team allocation

The 10 DAX measures are divided among the three members. Each member
should create, test, and verify the measures assigned to them in the
shared Power BI project.

  ------------------------------------------------------------------------
  Member                Assigned measures                            Count
  --------------------- --------------------- ----------------------------
  Nithin                Total Ridership,                                 3
                        Total Entries, Total  
                        Exits                 

  Pithambar             Average Ridership,                               3
                        Peak Hour Ridership,  
                        Peak Hour Share       

  Vimal                 Weekday Ridership,                               4
                        Weekend Ridership,    
                        Previous Month        
                        Ridership,            
                        Month-over-Month %    
                        Change                

  **Total**                                                         **10**
  ------------------------------------------------------------------------

> Create all measures in the existing `Metro_Ridership.pbix` file. For
> consistency, store the measures under `Fact_Ridership` where possible.
> Measures can technically be stored under another table, but keep them
> organized in one place.

------------------------------------------------------------------------

## Nithin -- Basic ridership measures

### 1. Total Ridership

``` dax
Total Ridership =
SUM(Fact_Ridership[Ridership])
```

Adds the ridership values in the fact table.

### 2. Total Entries

``` dax
Total Entries =
CALCULATE(
    [Total Ridership],
    Fact_Ridership[Measure] = "Entry"
)
```

Calculates total passenger entries.

### 3. Total Exits

``` dax
Total Exits =
CALCULATE(
    [Total Ridership],
    Fact_Ridership[Measure] = "Exit"
)
```

Calculates total passenger exits.

**Validation:** Check that the `Measure` column contains the exact
category values `"Entry"` and `"Exit"`. If the source uses different
spelling or capitalization, update the filter text to match.

------------------------------------------------------------------------

## Pithambar -- Average and peak-hour measures

### 4. Average Ridership

``` dax
Average Ridership =
AVERAGE(Fact_Ridership[Ridership])
```

Calculates the average ridership per fact-table row.

### 5. Peak Hour Ridership

``` dax
Peak Hour Ridership =
MAXX(
    ALL(Dim_Hour[Value]),
    CALCULATE([Total Ridership])
)
```

Finds the highest total ridership recorded across the 24 hours.

### 6. Peak Hour Share

``` dax
Peak Hour Share =
DIVIDE(
    [Peak Hour Ridership],
    [Total Ridership],
    0
)
```

Calculates the peak-hour ridership as a share of total ridership.

**Formatting:** Select this measure and set its format to
**Percentage**. Do not multiply the formula by 100 when using Percentage
formatting.

**Note:** `Peak Hour Ridership` returns one value. To display ridership
for every hour, use `Dim_Hour[Hour_Label]` on the chart X-axis and
`[Total Ridership]` on the Y-axis.

------------------------------------------------------------------------

## Vimal -- Day type and time-intelligence measures

### Prerequisite: Create a Day Type calculated column

This is a calculated column, not one of the 10 measures. In `Dim_Date`,
select **Modeling → New column** and create:

``` dax
Day Type =
IF(
    WEEKDAY(Dim_Date[Date], 2) <= 5,
    "Weekday",
    "Weekend"
)
```

This labels Monday--Friday as Weekday and Saturday--Sunday as Weekend.

### 7. Weekday Ridership

``` dax
Weekday Ridership =
CALCULATE(
    [Total Ridership],
    Dim_Date[Day Type] = "Weekday"
)
```

Calculates ridership on weekdays.

### 8. Weekend Ridership

``` dax
Weekend Ridership =
CALCULATE(
    [Total Ridership],
    Dim_Date[Day Type] = "Weekend"
)
```

Calculates ridership on weekends.

### 9. Previous Month Ridership

``` dax
Previous Month Ridership =
CALCULATE(
    [Total Ridership],
    DATEADD(
        Dim_Date[Date],
        -1,
        MONTH
    )
)
```

Calculates ridership for the previous month in the current date-filter
context.

### 10. Month-over-Month % Change

``` dax
MoM % Change =
DIVIDE(
    [Total Ridership] - [Previous Month Ridership],
    [Previous Month Ridership],
    0

