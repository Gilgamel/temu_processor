import os
import pandas as pd
from pathlib import Path
import unicodedata

# Configuration for multiple input folders and corresponding output files
folder_config = [
    {
        "input_folder": "PATH/TO/YOUR/INPUT/FOLDER1",
        "output_file": "PATH/TO/YOUR/OUTPUT/FILE1.xlsx"
    },
    {
        "input_folder": "PATH/TO/YOUR/INPUT/FOLDER2",
        "output_file": "PATH/TO/YOUR/OUTPUT/FILE2.xlsx"
    },
    # Add more configurations as needed
]

# Define final columns to keep
REQUIRED_COLUMNS = ['订单号', '子订单号', 'sku货号', '运单号', '物流商']

# Define column name aliases
COLUMN_ALIASES = {
    'sku货号': ['SKU货号', '货品', '产品编号', 'SKU', '货号', '商品编号'],
    '订单号': ['订单编号', '主订单号', 'OrderNumber'],
    '子订单号': ['子订单编号', '子单号', 'SubOrder'],
    '运单号': ['物流单号', '快递单号', 'Waybill'],
    '物流商': ['物流公司', '快递公司', 'Carrier']
}


def clean_column_name(name):
    """Thoroughly clean column names"""
    # Convert to string
    name = str(name)

    # Remove non-printable characters
    name = ''.join(c for c in name if c.isprintable())

    # Normalize Unicode characters (e.g., full-width to half-width)
    name = unicodedata.normalize('NFKC', name)

    # Replace special spaces
    name = name.replace('\u3000', ' ').replace('\u00A0', ' ')

    # Remove leading/trailing whitespace
    return name.strip()


def find_column(df, possible_names):
    """Find column among multiple possible names"""
    cleaned_df_columns = [clean_column_name(col).lower().replace(" ", "")
                          for col in df.columns]

    for name in possible_names:
        clean_name = clean_column_name(name).lower().replace(" ", "")
        if clean_name in cleaned_df_columns:
            idx = cleaned_df_columns.index(clean_name)
            return df.columns[idx]

    return None


def standardize_columns(df):
    """Create standardized column name mapping"""
    column_mapping = {}
    for col in df.columns:
        clean_col = clean_column_name(col)
        column_mapping[col] = clean_col

    return df.rename(columns=column_mapping)


def filter_columns(df):
    """Filter columns to keep only required ones"""
    filtered_df = pd.DataFrame()

    # Process each required column
    for col in REQUIRED_COLUMNS:
        # Get all possible column names (including aliases)
        possible_names = [col] + COLUMN_ALIASES.get(col, [])

        # Find actual existing column
        actual_col = find_column(df, possible_names)

        if actual_col:
            # Ensure column name is standardized
            clean_col_name = clean_column_name(actual_col)
            filtered_df[col] = df[actual_col]
            print(f"        Found column: '{actual_col}' -> mapped to '{col}'")
        else:
            # Add empty column if missing
            filtered_df[col] = None
            print(f"        Added missing column: '{col}'")

    # Add source_file column as the last column
    if 'source_file' in df.columns:
        filtered_df['source_file'] = df['source_file']
    else:
        filtered_df['source_file'] = None
        print("        Added source_file column")

    return filtered_df


def merge_files(input_folder, output_file):
    """Merge all Excel and CSV files in input folder to output file"""
    all_data = []
    print(f"\nProcessing folder: {input_folder}")
    print(f"Output file: {output_file}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Process all files
    for file in Path(input_folder).glob("*.*"):
        if file.suffix.lower() not in ['.xlsx', '.xls', '.csv']:
            continue

        print(f"  Processing file: {file.name}...")

        try:
            # Read file based on extension
            if file.suffix.lower() == '.csv':
                df = pd.read_csv(file)
                sheet_name = "CSV"
            else:
                # Get first sheet (all sheets will be merged)
                df = pd.read_excel(file, sheet_name=0)
                sheet_name = "Sheet0"

            # Add source information
            df["source_file"] = f"{file.name} - {sheet_name}"

            # Standardize column names
            df = standardize_columns(df)

            # Debug: print standardized column names
            print(f"    Standardized columns: {list(df.columns)}")

            # Filter columns
            filtered_df = filter_columns(df)

            # Add to dataset
            all_data.append(filtered_df)
            print(f"    Successfully processed: {file.name}")

        except Exception as e:
            print(f"    Error processing file {file.name}: {str(e)}")
            import traceback
            traceback.print_exc()

    # Merge and save data
    if all_data:
        try:
            combined_df = pd.concat(all_data, ignore_index=True)

            with pd.ExcelWriter(output_file) as writer:
                combined_df.to_excel(writer, sheet_name="raw data", index=False)

            print(f"Successfully saved merged file: {output_file} (Records: {len(combined_df)})")
            return True
        except Exception as e:
            print(f"Error saving output file: {str(e)}")
            return False
    else:
        print("Warning: No data found for merging")
        return False


if __name__ == "__main__":
    # Process all configured folders
    total_folders = len(folder_config)
    processed_count = 0

    print(f"Starting batch processing of {total_folders} folders...")

    for idx, config in enumerate(folder_config, 1):
        print(f"\n=== Processing folder {idx}/{total_folders} ===")
        success = merge_files(config["input_folder"], config["output_file"])
        if success:
            processed_count += 1

    print(f"\nProcessing completed! Successfully processed {processed_count}/{total_folders} folders")