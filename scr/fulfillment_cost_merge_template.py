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


def standardize_columns(df):
    """
    Standardize column names:
    1. Apply specific replacements for known terms
    2. Convert to lowercase
    3. Remove all spaces
    4. Convert Chinese brackets to English brackets
    """
    # Define mapping of terms to replace
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

    new_columns = []
    for col in df.columns:
        # Convert to string
        col_str = str(col)
        original_col = col_str  # Save for debugging

        # Apply replacements (check all possible headers)
        for standardized_name, possible_headers in replacements.items():
            for header in possible_headers:
                if header in col_str:
                    col_str = col_str.replace(header, standardized_name)
                    print(f"Replaced '{original_col}' with '{standardized_name}'")
                    break  # Stop checking other headers once a match is found

        # Additional standardization
        col_str = col_str.lower()
        col_str = col_str.replace(" ", "_")  # Use underscore instead of removing spaces
        col_str = col_str.replace("（", "(").replace("）", ")")

        new_columns.append(col_str)

    return df.set_axis(new_columns, axis=1)


def merge_excel_sheets(input_folder, output_file):
    """Merge all Excel files in input folder to output file and add fulfillment summary"""
    all_data = {}
    print(f"\nProcessing folder: {input_folder}")
    print(f"Output file: {output_file}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Process all Excel files in folder
    file_count = 0
    for file in Path(input_folder).glob("*.xlsx"):
        file_count += 1
        print(f"  Processing file {file_count}: {file.name}...")

        # Read sheet names from Excel file
        try:
            sheet_names = pd.ExcelFile(file).sheet_names
        except Exception as e:
            print(f"    Error: Failed to read file {file.name}: {str(e)}")
            continue

        # Process each sheet in file
        for sheet in sheet_names:
            try:
                # Load current worksheet data
                df = pd.read_excel(file, sheet_name=sheet)

                # Standardize column names
                df = standardize_columns(df)

                # Add source file column
                df["Source_File"] = file.name

                # Standardize sheet names: convert all raw data sheets to "raw data"
                # This handles sheets named 0, Sheet1, or any other variation
                if sheet in ["0", "sheet1", "raw data", "Raw Data", "RAW DATA"]:
                    target_sheet_name = "raw data"
                else:
                    target_sheet_name = sheet

                # Store in dictionary
                if target_sheet_name not in all_data:
                    all_data[target_sheet_name] = []
                all_data[target_sheet_name].append(df)

                # Log sheet name conversion
                if sheet != target_sheet_name:
                    print(f"    Converted sheet '{sheet}' to '{target_sheet_name}'")
            except Exception as e:
                print(f"    Error: Failed to process sheet '{sheet}': {str(e)}")

    # Merge and save data if available
    if all_data:
        try:
            with pd.ExcelWriter(output_file) as writer:
                # Store all combined DataFrames for summary
                all_combined_dfs = []

                for sheet_name, data_list in all_data.items():
                    # Merge data from all files for this sheet
                    combined_df = pd.concat(data_list, ignore_index=True)

                    # === add adjusted_shipping_fee ===
                    if 'shipping_fee' in combined_df.columns and 'bill_type' in combined_df.columns:
                        # 1. 取运费绝对值
                        combined_df['adjusted_shipping_fee'] = combined_df['shipping_fee'].abs()

                        # 2. 当 bill_type = "退款成功" 时设为负值
                        refund_mask = combined_df['bill_status'].str.contains('退款成功', na=False)
                        combined_df.loc[refund_mask, 'adjusted_shipping_fee'] *= -1
                    else:
                        print(
                            f"    Warning: Missing required columns for adjusted shipping fee in sheet '{sheet_name}'")

                    all_combined_dfs.append(combined_df)  # Add to summary list

                    # Save to Excel
                    combined_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"  Merged sheet '{sheet_name}' with data from {len(data_list)} files")

                # Create fulfillment summary if data exists
                if all_combined_dfs:
                    # Combine data from all sheets
                    all_data_combined = pd.concat(all_combined_dfs, ignore_index=True)

                    # summary_cols = ['waybill_sn', 'carrier', 'currency', 'adjusted_shipping_fee']
                    summary_cols = ['pkg_sn', 'waybill_sn', 'carrier', 'currency', 'adjusted_shipping_fee']
                    missing_summary_cols = [col for col in summary_cols if col not in all_data_combined.columns]

                    if not missing_summary_cols:
                        # group by adjusted_shipping_fee
                        fulfillment_summary = all_data_combined.groupby(
                            #['pkg_sn', 'waybill_sn', 'carrier', 'currency'],
                            ['pkg_sn','waybill_sn', 'carrier', 'currency'],
                            as_index=False
                        )['adjusted_shipping_fee'].sum()

                        # save
                        fulfillment_summary.to_excel(writer, sheet_name="fulfillment_summary", index=False)
                        print(f"  Added fulfillment summary sheet with {len(fulfillment_summary)} records")
                    else:
                        print(
                            f"  Warning: Missing columns for fulfillment summary - {', '.join(missing_summary_cols)}. Skipping summary sheet.")

            print(f"Successfully saved merged file: {output_file}")
            return True
        except Exception as e:
            print(f"Error: Failed to save output file: {str(e)}")
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
        success = merge_excel_sheets(config["input_folder"], config["output_file"])
        if success:
            processed_count += 1

    print(f"\nProcessing completed! Successfully processed {processed_count}/{total_folders} folders")