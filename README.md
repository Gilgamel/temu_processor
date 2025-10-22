# Temu Processor

- [File_Management](#File-Management)

Suitable for Temu accounts registered under Chinese companies

- [Bill Details Consolidation](#Bill-Details-Consolidation)
- [Order Details Consolidation](#Order-Details-Consolidation)
- [Fulfillment Cost Consolidation](#Fulfillment-Cost-Consolidation)
- [Refund Cost Consolidation](#Refund-Cost-Consolidation)

## File Management
This script automatically organizes files into their corresponding folders


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


## Fulfillment Cost Consolidation
This script merges multiple fulfillment cost (发货面单) Excel files from different folders into consolidated output files.

### Setup 

1. Create a copy of the template:
```bash
cp fulfillment_cost_merge_template.py fulfillment_cost_merge.py
```

2. Edit `fulfillment_cost_merge.py` and configure your paths:
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

    replacements = {
        "pkg_sn": ["包裹号", "Package Number", "包裹编号"],
        "waybill_sn": ["运单号", "Waybill Number"],
        "carrier": ["服务商code", "Service Provider Code"],
        "bill_type": ["账单类型", "Bill Type"],
        "shipping_fee": ["运费(单位元)", "Shipping Fee (Unit: Yuan)"],
        "currency": ["币种", "Currency"],
        "bill_status": ["对账单状态", "Reconciliation Bill Status"],
        "date": ["支出/退款时间(时区：GMT+8)", "Expense/Refund Time (Time Zone: GMT+8)"]
    }
```

### Usage
```bash
python fulfillment_cost_merge.py
```

#### Features
- Changes all sheet name to `raw data`
- Calculates adjusted shipping fee based on bill status (支出成功/退款成功)
- Sum up shipping fee based on pkg_sn, waybill_sn, carrier, and currency

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
- Sum up freight charge based on waybill sn, parent order sn, and seller currency

