# Temu Processor

Suitable for Temu accounts registered under Chinese companies

- [Bill Details Consolidation](#Bill-Details-Consolidation)
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

