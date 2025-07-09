# Temu Processor

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction
项目介绍...

## Temu Merge Script
This script merges multiple Excel files from different folders into consolidated output files.

### Setup

1. Install requirements:
```bash
pip install pandas openpyxl
```

2. Create a copy of the template:
```bash
cp temu_merge_template.py temu_merge.py
```

3. Edit `merge_excel.py` and configure your paths:
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
python temu_merge.py
```

### Features
- Processes multiple folders in one run
- Standardizes column names (lowercase, no spaces, English brackets)
- Maintains source file information
- Handles errors gracefully
