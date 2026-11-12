# (1) Chart Collection and Review

We collected both good and bad chart examples for this project. The [`good_chart/`](good_chart/) folder contains six examples of effective data visualization, while [`bad_chart/`](bad_chart/) contains six charts that can be difficult to read or compare. Each member is assigned two good-chart examples and two bad-chart examples:

## Team Assignments

### Nithin — Images 1 and 2

**Bad charts**

- [Image 1: Department satisfaction](bad_chart/bad%20image%201.png) uses nearly identical tall bars for values in the 90s, a tall y-axis range, and no clear chart title, making small differences hard to see.
- [Image 2: Weekly website traffic](bad_chart/bad%20chart%202.png) overlays six traffic-source lines, so it is difficult to follow each series.

**Good charts**

- [Image 1: Temperature anomalies](good_chart/good%20image%201.jpg) uses a line chart to show changes over time, with a clear title, subtitle, direct series labels, units, and source.
- [Image 2: Internet use by age](good_chart/good%20image%202.jpg) uses a 100% stacked horizontal bar chart with percentage labels to compare internet use across age groups.

### Pithambar — Images 3 and 4

**Bad charts**

- [Image 3: Vote shares](bad_chart/bad%20img%203.png) uses a 3D cone-style chart, which distorts the values and makes comparisons less accurate.
- [Image 4: Fertility rates](bad_chart/bad%20img%204.png) combines many colored bars across several survey periods and adds India reference markers, making the comparison visually busy.

**Good charts**

- [Image 3: Pre-monsoon rainfall](good_chart/good_img_3.jpg) uses a time-series line chart, clear units, and direct labels to compare three rainfall measures over time.
- [Image 4: Life expectancy](good_chart/good_img_4.jpg) uses directly labeled lines to compare long-term trends for India and the United Kingdom.

### Vimal — Images 5 and 6

**Bad charts**

- [Image 5: Country/region shares](bad_chart/bad%20chart%20img5.png) uses many pie slices, which makes it hard to compare categories with similar values.
- [Image 6: Mortality rates](bad_chart/bad%20chart%20img%206.png) uses a 3D grouped-column chart with perspective and crowded labels, making the values harder to compare.

**Good charts**

- [Image 5: Tobacco use by age group](good_chart/good%20chart%205.jpg) uses a horizontal bar chart with a common scale and value labels for straightforward comparisons.
- [Image 6: Weekly food consumption](good_chart/good%20chart%206.jpg) uses horizontal bars to compare food consumption across income groups, with clear labels and values.

# (2) Chart Choice

In [`chart_choices.md`](chart_choices.md), we matched common data questions with chart types that make the answers easier to understand. The choice depends on what we want to communicate and the data available:

- Use a **line chart** to show how values change over time.
- Use a **bar chart** to compare categories or groups.
- Use a **histogram** to show the distribution of numerical values.
- Use a **scatter plot** to explore the relationship between two numerical variables.
- Use a **heatmap** to reveal patterns across two dimensions, such as month and year.
- Use a **pie chart** only for a small number of categories when showing parts of a whole; use a bar chart when precise comparisons are more important.

We should start with the question, then choose a chart that presents the data accurately and clearly. Labels, units, and scales should be easy to read, and the chart should avoid unnecessary visual effects. For example, a rainfall-and-temperature scatter plot is appropriate only when the dataset includes both variables.




# (3) Chart Makeover

We created Excel makeovers to make selected charts easier to read and compare. The workbooks are saved in [`chart_make_over/`](chart_make_over/):

- **Pithambar:** [Country/region shares](chart_make_over/make_over_1/pithambar_chart_make_over.xlsx) changes a pie chart into a bar chart so category sizes are easier to compare. The values are estimates read from the original image, not the underlying source data.

- **Vimal:** [Fertility rates](chart_make_over/maker_over_2/vimal%20chart%20make%20over.xlsx) presents values across survey periods in a flat bar chart, avoiding the perspective distortion of the original 3D chart.

- **Nithin:** [Website traffic](chart_make_over/make_over_3/nithin%20chart%20makeover.xlsx) recreates the weekly traffic-source series as a line chart. The values are approximate estimates reconstructed from the image. Since six lines can still be difficult to distinguish, highlighting fewer series at a time could improve readability further.

The makeover workbooks currently cover selected examples and do not correspond to every member's two assigned bad charts. Estimated values should be treated as approximations, not exact source data.


# (4) Bangalore Rainfall Data

For this project, **Vimal collected** the Bangalore rainfall data, **Nithin analysed** it to explore monthly and yearly patterns and the relationship with El Niño and La Niña conditions, and **Pithambar modified** the dataset. The workbook includes monthly rainfall values, annual totals, and El Niño/La Niña indicators.

- [Original rainfall workbook](banglore_rain_fall/banglore_rainfall_data.xlsx) contains records for 2024 and 2025.
- [Modified rainfall workbook](banglore_rain_fall/modified_banglore_rainfall_data.xlsx) contains a longer historical series, with year-labeled records from 1902 to 2025.

The data can be used to compare annual totals, identify seasonal patterns, and examine rainfall during El Niño and La Niña years. Before drawing conclusions, confirm the rainfall units and review the modified workbook's first data row, which has no year recorded.