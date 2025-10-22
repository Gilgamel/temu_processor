import os
import pandas as pd
from pathlib import Path
import unicodedata

# Configuration for multiple input folders and corresponding output files
folder_config = [
    # Sixale
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\sixale outfitters account\\processed\\temu_sixale_fulfillment_consolidated_output.xlsx"
    },

    # Edifier
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Edifier Official Shop\\processed\\temu_edifier_fulfillment_consolidated_output.xlsx"
    },

    # Broke and Happy
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Broke n Happy account\\processed\\temu_bnh_fulfillment_consolidated_output.xlsx"
    },

    # Canadian Wheels
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Canadian Wheel account\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Canadian Wheel account\\processed\\temu_cw_fulfillment_consolidated_output.xlsx"
    },

    # Edifier REF
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\EDIFIER Refurbished Official Shop\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\EDIFIER Refurbished Official Shop\\processed\\temu_edifier_ref_fulfillment_consolidated_output.xlsx"
    },

    # Juicy Penny
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\JuicyPenny account\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\JuicyPenny account\\processed\\temu_jp_fulfillment_consolidated_output.xlsx"
    },

    # Good Basics
    {
        "input_folder": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Good Basics account\\raw data fulfillment cost",
        "output_file": "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\Good Basics account\\processed\\temu_gb_fulfillment_consolidated_output.xlsx"
    },

]

# 新增：全局输出文件配置
GLOBAL_OUTPUT_FILE = "C:\\Users\\vuser\\Documents\\Monthly Report\\Monthly Channel Profit\\Temu Ventchoice\\all_accounts_fulfillment_consolidated_output.xlsx"


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


def merge_excel_sheets(input_folder, output_file, account_name=None):
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
                df["source_file"] = file.name

                # 新增：添加账户名称列
                if account_name:
                    df["account_name"] = account_name

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

                    summary_cols = ['pkg_sn', 'waybill_sn', 'carrier', 'currency', 'adjusted_shipping_fee']
                    missing_summary_cols = [col for col in summary_cols if col not in all_data_combined.columns]

                    if not missing_summary_cols:
                        # group by adjusted_shipping_fee
                        fulfillment_summary = all_data_combined.groupby(
                            ['pkg_sn', 'waybill_sn', 'carrier', 'currency'],
                            as_index=False
                        )['adjusted_shipping_fee'].sum()

                        # 新增：在 fulfillment_summary 上添加 source_file
                        # 通过合并操作将 source_file 信息添加到汇总表中
                        source_mapping = all_data_combined[['pkg_sn', 'waybill_sn', 'source_file']].drop_duplicates()
                        fulfillment_summary = fulfillment_summary.merge(source_mapping, on=['pkg_sn', 'waybill_sn'],
                                                                        how='left')

                        # 新增：如果存在 account_name，也添加到汇总表
                        if 'account_name' in all_data_combined.columns:
                            account_mapping = all_data_combined[
                                ['pkg_sn', 'waybill_sn', 'account_name']].drop_duplicates()
                            fulfillment_summary = fulfillment_summary.merge(account_mapping,
                                                                            on=['pkg_sn', 'waybill_sn'], how='left')

                        # save
                        fulfillment_summary.to_excel(writer, sheet_name="fulfillment_summary", index=False)
                        print(f"  Added fulfillment summary sheet with {len(fulfillment_summary)} records")
                    else:
                        print(
                            f"  Warning: Missing columns for fulfillment summary - {', '.join(missing_summary_cols)}. Skipping summary sheet.")

            print(f"Successfully saved merged file: {output_file}")
            return all_data  # 返回处理的数据用于全局合并
        except Exception as e:
            print(f"Error: Failed to save output file: {str(e)}")
            return None
    else:
        print("Warning: No data found for merging")
        return None


def create_global_output(all_accounts_data):
    """创建包含所有账户数据的全局Excel文件"""
    if not all_accounts_data:
        print("No data available for global output")
        return

    print(f"\n=== Creating global output file: {GLOBAL_OUTPUT_FILE} ===")

    # 确保输出目录存在
    output_dir = os.path.dirname(GLOBAL_OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created global output directory: {output_dir}")

    try:
        with pd.ExcelWriter(GLOBAL_OUTPUT_FILE) as writer:
            # 用于存储所有账户的汇总数据
            all_fulfillment_summaries = []

            # 处理每个账户的数据
            for account_name, account_data in all_accounts_data.items():
                print(f"Processing account: {account_name}")

                # 合并该账户的所有工作表数据
                for sheet_name, data_list in account_data.items():
                    if data_list:
                        combined_df = pd.concat(data_list, ignore_index=True)

                        # 为每个工作表添加账户标识
                        combined_df['global_account_name'] = account_name

                        # 保存到全局文件，工作表名格式：账户名_原工作表名
                        safe_sheet_name = f"{account_name}_{sheet_name}"[:31]  # Excel工作表名最大31字符
                        combined_df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                        print(f"  Added sheet: {safe_sheet_name}")

                        # 如果是raw data工作表，收集数据用于全局汇总
                        if sheet_name == "raw data":
                            all_fulfillment_summaries.append(combined_df)

            # 创建全局fulfillment_summary
            if all_fulfillment_summaries:
                global_all_data = pd.concat(all_fulfillment_summaries, ignore_index=True)

                summary_cols = ['pkg_sn', 'waybill_sn', 'carrier', 'currency', 'adjusted_shipping_fee']
                missing_summary_cols = [col for col in summary_cols if col not in global_all_data.columns]

                if not missing_summary_cols:
                    # 分组汇总
                    global_fulfillment_summary = global_all_data.groupby(
                        ['pkg_sn', 'waybill_sn', 'carrier', 'currency'],
                        as_index=False
                    )['adjusted_shipping_fee'].sum()

                    # 添加source_file信息
                    source_mapping = global_all_data[['pkg_sn', 'waybill_sn', 'source_file']].drop_duplicates()
                    global_fulfillment_summary = global_fulfillment_summary.merge(source_mapping,
                                                                                  on=['pkg_sn', 'waybill_sn'],
                                                                                  how='left')

                    # 添加account_name信息
                    if 'global_account_name' in global_all_data.columns:
                        account_mapping = global_all_data[
                            ['pkg_sn', 'waybill_sn', 'global_account_name']].drop_duplicates()
                        global_fulfillment_summary = global_fulfillment_summary.merge(account_mapping,
                                                                                      on=['pkg_sn', 'waybill_sn'],
                                                                                      how='left')

                    global_fulfillment_summary.to_excel(writer, sheet_name="global_fulfillment_summary", index=False)
                    print(f"Added global fulfillment summary with {len(global_fulfillment_summary)} records")
                else:
                    print(f"Warning: Missing columns for global summary - {', '.join(missing_summary_cols)}")

            print(f"Successfully created global output file: {GLOBAL_OUTPUT_FILE}")

    except Exception as e:
        print(f"Error creating global output file: {str(e)}")


if __name__ == "__main__":
    # Process all configured folders
    total_folders = len(folder_config)
    processed_count = 0

    # 新增：存储所有账户数据的字典
    all_accounts_data = {}

    print(f"Starting batch processing of {total_folders} folders...")

    for idx, config in enumerate(folder_config, 1):
        print(f"\n=== Processing folder {idx}/{total_folders} ===")

        # 从文件夹路径提取账户名称
        account_name = os.path.basename(os.path.dirname(config["input_folder"]))

        # 处理单个账户，并收集数据
        account_data = merge_excel_sheets(config["input_folder"], config["output_file"], account_name)
        if account_data:
            processed_count += 1
            # 存储账户数据用于全局输出
            all_accounts_data[account_name] = account_data

    print(f"\nIndividual processing completed! Successfully processed {processed_count}/{total_folders} folders")

    # 新增：创建全局输出文件
    if all_accounts_data:
        create_global_output(all_accounts_data)
        print(f"\nGlobal output file created: {GLOBAL_OUTPUT_FILE}")
    else:
        print("\nNo data available to create global output file")