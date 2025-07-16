# Temu Processor

Suitable for Temu accounts registered under Chinese companies

- [Bill Details Consolidation](#Bill-Details-Consolidation)
- [Order Details Consolidation](#Order-Details-Consolidation)
- [Refund Cost Consolidation](#Refund-Cost-Consolidation)

## Bill Details Consolidation
This script merges multiple bill details Excel files from different folders into consolidated output files.

### Setup

1. Install requirements:
```bash
pip install pandas openpyxl
```

2. Create a copy of the template:
```bash
cp billdetails_merge_template.py billdetails_merge.py
```

3. Edit `billdetails_merge.py` and configure your paths:
```python
folder_config = [
    {
        "input_folder": "your/input/path1",
        "output_file": "your/output/path1.xlsx"
    },
    {
        "input_folder": "your/input/path2",
        "output_file": "your/output/path2.xlsx"
    }
]
```

### Usage
```bash
python billdetails_merge.py
```

### Features
- Processes multiple folders in one run
- Standardizes column names (lowercase, no spaces, English brackets)
- Maintains source file information
- Handles errors gracefully


## Order Details Consolidation
This script consolidates Excel and CSV files from multiple folders into standardized output files. It handles column name variations, filters to specific columns, and adds source tracking information.

### Setup

1. Create a copy of the template:
```bash
cp order_details_merge_template.py order_details_merge.py
```

2. Edit `order_details_merge.py` and configure your paths:
```python
folder_config = [
    {
        "input_folder": "your/input/path1",
        "output_file": "your/output/path1.xlsx"
    },
    {
        "input_folder": "your/input/path2",
        "output_file": "your/output/path2.xlsx"
    }
]

# Define final columns to keep
REQUIRED_COLUMNS = ['订单号', '子订单号', 'sku货号', '运单号', '物流商']

# Define column name aliases
COLUMN_ALIASES = {
    'sku货号': ['SKU货号', '货品', '产品编号', 'SKU', '货号', '商品编号'],
    '订单号': ['订单编号', '主订单号', 'OrderNumber'],
    # ... other column mappings
}

```

### Usage
```bash
python order_details_merge.py
```

#### Features
- Handles both Excel (.xlsx, .xls) and CSV files
- Standardizes column names (lowercase, no spaces, English brackets)
- Handles different naming variations through alias mapping
- Adds missing columns automatically
- Source Tracking: Maintains source file information in the last column
- Encoding Robustness: Special handling for Unicode variations and hidden characters


## Refund Cost Consolidation
This script merges multiple refund cost (退货面单) Excel files from different folders into consolidated output files.

### Setup

1. Create a copy of the template:
```bash
cp refund_cost_merge_template.py refund_cost_merge.py
```

2. Edit `refund_cost_merge.py` and configure your paths:
```python
folder_config = [
    {
        "input_folder": "your/input/path1",
        "output_file": "your/output/path1.xlsx"
    },
    {
        "input_folder": "your/input/path2",
        "output_file": "your/output/path2.xlsx"
    }
]
```

### Usage
```bash
python refund_cost_merge.py
```

#### Features
- Changes all sheet name to `raw data`
- Sum up freight charge based on waybill sn, parent order sn, and seller currency.

