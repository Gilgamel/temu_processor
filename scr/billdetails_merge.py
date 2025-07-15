import os
import pandas as pd
from pathlib import Path

# Configuration for multiple input folders and their corresponding output files
folder_config = [
    # Sixale
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\raw data global",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\processed\\temu_sixale_global_consolidated_output.xlsx"
    },
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\raw data us",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\processed\\temu_sixale_us_consolidated_output.xlsx"
    },
    # Edifier
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\raw data global",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\processed\\temu_edifier_global_consolidated_output.xlsx"
    },

    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\raw data us",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\processed\\temu_edifier_us_consolidated_output.xlsx"
    },

    # Broke and Happy
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\raw data us",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\processed\\temu_bnh_us_consolidated_output.xlsx"
    },

    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\raw data global",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\processed\\temu_bnh_global_consolidated_output.xlsx"
    }


]


def standardize_columns(df):
    """Standardize column names: lowercase, remove spaces, convert Chinese brackets to English"""
    new_columns = []
    for col in df.columns:
        # Convert to string in case of non-string column names
        col_str = str(col)
        # Convert to lowercase
        col_str = col_str.lower()
        # Remove all spaces
        col_str = col_str.replace(" ", "")
        # Convert Chinese brackets to English brackets
        col_str = col_str.replace("（", "(").replace("）", ")")
        new_columns.append(col_str)

    df.columns = new_columns
    return df


def merge_excel_sheets(input_folder, output_file):
    """Merge all Excel files in the specified input folder to the specified output file"""
    all_data = {}
    print(f"\nProcessing folder: {input_folder}")
    print(f"Output file: {output_file}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Process all Excel files in the folder
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

        # Process each sheet in the file
        for sheet in sheet_names:
            try:
                # Load current worksheet data
                df = pd.read_excel(file, sheet_name=sheet)

                # Standardize column names
                df = standardize_columns(df)

                # Add source file column
                df["Source_File"] = file.name

                # Store in dictionary
                if sheet not in all_data:
                    all_data[sheet] = []
                all_data[sheet].append(df)
            except Exception as e:
                print(f"    Error: Failed to process sheet '{sheet}': {str(e)}")

    # Merge and save data if available
    if all_data:
        try:
            with pd.ExcelWriter(output_file) as writer:
                for sheet_name, data_list in all_data.items():
                    # Merge data from all files for this sheet
                    combined_df = pd.concat(data_list, ignore_index=True)

                    # Save to Excel
                    combined_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"  Merged sheet '{sheet_name}' with data from {len(data_list)} files")

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