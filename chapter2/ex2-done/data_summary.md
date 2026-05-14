# Sales Data Summary

- Source: `chapter2/sales_data.csv`
- Rows: **10,000**
- Columns: **6**
- Date range: **2025-09-01** to **2026-04-30**
- Total revenue: **$6,103,927.75**

## Columns and data types
- `sales_person`: `str` (unique: 50, missing: 0)
- `product`: `str` (unique: 20, missing: 0)
- `category`: `str` (unique: 10, missing: 0)
- `price`: `float64` (unique: 9,552, missing: 0)
- `date`: `datetime64[us]` (unique: 242, missing: 0)
- `month`: `string` (unique: 8, missing: 0)

## Category distribution and revenue
```
             transactions     revenue  avg_price  revenue_share_pct
category                                                           
Computers             952  1551302.80    1629.52              25.41
Smartphones           986  1110034.87    1125.80              18.19
Cameras               959   819419.34     854.45              13.42
Tablets              1023   664764.50     649.82              10.89
Gaming               1065   601045.23     564.36               9.85
Monitors             1004   564493.60     562.24               9.25
Wearables             976   343239.44     351.68               5.62
Audio                1036   218384.12     210.80               3.58
Smart Home           1511   199687.85     132.16               3.27
Accessories           488    31556.00      64.66               0.52
```

## Monthly total revenue
```
           revenue
month             
2025-09  762268.81
2025-10  815299.15
2025-11  774461.61
2025-12  791661.88
2026-01  753457.02
2026-02  737188.70
2026-03  783187.64
2026-04  686402.94
```

## Monthly revenue by category (pivot)
```
category  Accessories     Audio    Cameras  Computers    Gaming  Monitors  Smart Home  Smartphones   Tablets  Wearables
month                                                                                                                  
2025-09       4371.99  28243.31  113060.46  214818.12  66966.91  67183.31    28956.32    128173.90  70225.31   40269.18
2025-10       3843.20  27658.77  103174.46  195202.68  83079.43  83964.92    24226.40    157504.36  93830.35   42814.58
2025-11       3381.92  25549.24  103258.02  193367.56  71942.30  71385.49    22531.59    150188.05  87864.65   44992.79
2025-12       3690.10  27287.74  104092.75  191896.94  70884.06  79128.85    24195.59    156414.83  86740.10   47330.92
2026-01       5042.53  28759.60   98100.94  176043.44  75052.61  69208.69    24434.50    152263.32  77267.34   47284.05
2026-02       3936.73  27099.63  101422.97  202027.80  67674.07  59363.35    25224.45    136744.92  70586.26   43108.52
2026-03       3826.62  28613.99   95147.67  217023.48  86500.38  70558.81    25196.65    121831.40  93794.29   40694.35
2026-04       3462.91  25171.84  101162.07  160922.78  78945.47  63700.18    24922.35    106914.09  84456.20   36745.05
```

## Top 10 salespeople by revenue
```
                  transactions    revenue  avg_sale
sales_person                                       
Atreus                     222  151039.28    680.36
Tony Stark                 223  140960.33    632.11
Ellen Ripley               212  136775.08    645.17
Mario                      222  136008.88    612.65
Luna Lovegood              194  135616.03    699.05
Link                       224  135293.24    603.99
Hermione Granger           212  135011.91    636.85
Samwise Gamgee             197  134451.78    682.50
Lara Croft                 212  133119.18    627.92
Din Djarin                 219  132971.54    607.18
```

## Top 10 products by revenue
```
                      transactions    revenue  avg_price
product                                                 
Titan Gaming Laptop            442  837868.32    1895.63
Nimbus Ultrabook               510  713434.48    1398.89
Photon DSLR Camera             495  670771.45    1355.09
Nebula Fold Phone              516  664258.18    1287.32
Aurora X1 Smartphone           470  445776.69     948.46
Orion Pro Tablet               499  429290.83     860.30
PixelView 34 Monitor           493  368049.46     746.55
Nova VR Headset                546  313775.70     574.68
Comet Game Console             519  287269.53     553.51
Pulse Mini Tablet              524  235473.67     449.38
```

## Key observations
- Unique values: 50 salespeople, 20 products, 10 categories.
- Highest revenue category: **Computers** ($1,551,302.80).
- Highest revenue month: **2025-10** ($815,299.15).
- Top salesperson: **Atreus** ($151,039.28).