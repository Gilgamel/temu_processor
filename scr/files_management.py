import os
import shutil
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 定义业务规则 - 支持多种文件格式
business_rules = {
    "Anotherpologies account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Anotherpologies account"
    },

    "Broke n Happy account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Broke n Happy account"
    },

    "Canadian Wheel account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Canadian Wheel account"
    },

    "DealDepot account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\DealDepot account"
    },

    "Edifier Official Shop": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Edifier Official Shop"
    },

    "EDIFIER Refurbished Official Shop": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\EDIFIER Refurbished Official Shop"
    },

    "Emptybay Traders account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Emptybay Traders account"
    },

    "Good Basics account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Good Basics account"
    },

    "Jackery Official Shop account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Jackery Official Shop account"
    },

    "JuicyPenny account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\JuicyPenny account"
    },

    "sixale outfitters account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\sixale outfitters account"
    },

    "Ventchoice Account": {
        "file_patterns": {
            r".*发货面单.*\.(csv|xlsx|xls)": "raw data fulfillment cost",
            r".*退货面单.*\.(csv|xlsx|xls)": "raw data refund cost",
            r".*订单明细.*\.(csv|xlsx|xls)": "raw data order details",
            r"^(?=.*BillDetails)(?=.*美国)(?!.*全球).*\.(csv|xlsx|xls)": ["raw data us", "raw data us and global"],
            r"^(?=.*BillDetails)(?=.*全球)(?!.*美国).*\.(csv|xlsx|xls)": ["raw data global", "raw data us and global"],
        },
        "base_target": r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice\Ventchoice Account"
    }

}


class TemuFileHandler(FileSystemEventHandler):
    def __init__(self):
        # 收集所有目标文件夹路径，用于过滤
        self.target_folders = set()
        for account_rules in business_rules.values():
            base_target = account_rules["base_target"]
            # 处理单个文件夹和多个文件夹的情况
            for pattern_value in account_rules["file_patterns"].values():
                if isinstance(pattern_value, list):
                    # 如果是列表，遍历每个文件夹名
                    for folder_name in pattern_value:
                        target_folder = os.path.join(base_target, folder_name)
                        self.target_folders.add(target_folder.lower())
                else:
                    # 如果是字符串，直接使用
                    target_folder = os.path.join(base_target, pattern_value)
                    self.target_folders.add(target_folder.lower())

        print(f"📋 目标文件夹列表: {list(self.target_folders)}")

    def is_target_folder_file(self, file_path):
        """检查文件是否在目标文件夹中"""
        file_path_lower = file_path.lower()
        for target_folder in self.target_folders:
            if file_path_lower.startswith(target_folder):
                return True
        return False

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            # 跳过目标文件夹中的文件，避免循环复制
            if self.is_target_folder_file(file_path):
                print(f"⏭️  跳过目标文件夹中的文件: {os.path.basename(file_path)}")
                return
            print(f"🎯 检测到新文件: {file_path}")
            self.process_file(file_path)

    def on_moved(self, event):
        if not event.is_directory:
            file_path = event.dest_path
            # 跳过目标文件夹中的文件，避免循环复制
            if self.is_target_folder_file(file_path):
                print(f"⏭️  跳过目标文件夹中的文件: {os.path.basename(file_path)}")
                return
            print(f"🎯 检测到文件移动: {file_path}")
            self.process_file(file_path)

    def copy_file_with_retry(self, src_path, dst_path, max_retries=3, retry_delay=2):
        """带重试机制的文件复制"""
        for attempt in range(max_retries):
            try:
                # 首先检查源文件是否存在
                if not os.path.exists(src_path):
                    print(f"   ❌ 源文件不存在: {src_path}")
                    return False

                # 检查源文件是否可读
                try:
                    with open(src_path, 'rb'):
                        pass
                except IOError:
                    print(f"   ⚠️ 源文件不可读，等待 {retry_delay} 秒... (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue

                # 执行复制
                shutil.copy2(src_path, dst_path)
                return True

            except PermissionError as e:
                if attempt < max_retries - 1:
                    print(f"   ⏳ 文件被占用，等待 {retry_delay} 秒后重试... (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(f"   ❌ 复制失败: 文件被占用，已达到最大重试次数")
                    return False
            except FileNotFoundError:
                print(f"   ❌ 源文件在复制过程中消失: {src_path}")
                return False
            except Exception as e:
                print(f"   ❌ 复制失败: {e}")
                return False
        return False

    def safe_delete_file(self, file_path, max_retries=2):
        """安全删除文件，带重试机制"""
        for attempt in range(max_retries):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return True
            except PermissionError:
                if attempt < max_retries - 1:
                    print(f"   ⏳ 文件被占用，等待删除... (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    print(f"   ⚠️ 无法删除文件，可能正在被使用")
                    return False
            except Exception as e:
                print(f"   ⚠️ 删除文件时出错: {e}")
                return False
        return False

    def copy_to_target_folders(self, file_path, file_name, base_target, target_folders):
        """复制文件到多个目标文件夹"""
        success_count = 0
        total_count = len(target_folders)

        for folder_name in target_folders:
            print(f"   📁 处理目标文件夹: {folder_name}")

            # 构建目标路径
            target_dir = os.path.join(base_target, folder_name)
            print(f"   📂 目标目录: {target_dir}")

            # 自动创建目标目录
            try:
                if not os.path.exists(target_dir):
                    print(f"   📂 创建目标目录: {target_dir}")
                    os.makedirs(target_dir, exist_ok=True)
                else:
                    print(f"   ✅ 目标目录已存在")
            except Exception as e:
                print(f"   ❌ 创建目录时出错: {e}")
                continue

            # 复制文件
            target_path = os.path.join(target_dir, file_name)
            print(f"   📋 准备复制到: {target_path}")

            # 再次检查源文件是否存在
            if not os.path.exists(file_path):
                print(f"❌ 源文件在处理过程中消失: {file_path}")
                break

            # 检查目标文件是否已存在
            if os.path.exists(target_path):
                print(f"   ⚠️  目标文件已存在，将覆盖: {file_name}")

                # 安全删除已存在的文件
                if self.safe_delete_file(target_path):
                    print(f"   ✅ 已删除旧文件")
                else:
                    print(f"   ⚠️  无法删除旧文件，尝试直接覆盖")

            # 使用带重试机制的复制
            print(f"   🔄 开始复制文件...")
            success = self.copy_file_with_retry(file_path, target_path)

            if success:
                print(f"   ✅ 复制完成: {file_name} → {target_path}")
                success_count += 1
                # 验证复制成功
                if os.path.exists(target_path):
                    print(f"   ✅ 文件复制验证成功")
                else:
                    print(f"   ❌ 文件复制验证失败")
            else:
                print(f"   ❌ 复制失败")

        return success_count, total_count

    def process_file(self, file_path):
        """处理新创建或移动的文件"""
        try:
            print(f"🔔 开始处理文件: {file_path}")

            # 再次检查是否为目标文件夹文件（双重保险）
            if self.is_target_folder_file(file_path):
                print(f"⏭️  跳过目标文件夹中的文件: {os.path.basename(file_path)}")
                return

            # 立即检查文件是否存在
            if not os.path.exists(file_path):
                print(f"❌ 文件不存在，可能已被移动或删除: {file_path}")
                return

            # 检查文件是否可访问
            try:
                file_size = os.path.getsize(file_path)
                print(f"   📏 文件大小: {file_size} 字节")
            except OSError:
                print(f"❌ 无法访问文件: {file_path}")
                return

            # 解析文件路径结构
            path_parts = file_path.split(os.sep)
            print(f"📂 完整路径解析: {path_parts}")

            # 查找账号名
            base_folder_name = "Temu Ventchoice"
            account_name = None

            try:
                base_index = path_parts.index(base_folder_name)
                if len(path_parts) > base_index + 1:
                    account_name = path_parts[base_index + 1]
                    print(f"   🔍 从路径解析账号名: {account_name}")
            except ValueError:
                print("   ⚠️  无法找到基础文件夹 'Temu Ventchoice'")

            if not account_name:
                account_name = path_parts[-3] if len(path_parts) >= 3 else None
                print(f"   🔍 使用备用方法解析账号名: {account_name}")

            file_name = path_parts[-1]
            file_ext = os.path.splitext(file_name)[1].lower()

            print(f"📁 文件名: {file_name}")
            print(f"   📝 最终确定的账号: {account_name}")

            if not account_name or account_name not in business_rules:
                print(f"⚠️  未知账号: '{account_name}'，跳过处理")
                return

            # 获取该账号的规则
            account_rules = business_rules[account_name]
            file_patterns = account_rules["file_patterns"]
            base_target = account_rules["base_target"]

            # 匹配文件类型
            matched_folders = self.classify_file(file_name, file_patterns)

            if matched_folders:
                # 统一处理：将单个文件夹转为列表
                if isinstance(matched_folders, str):
                    target_folders = [matched_folders]
                else:
                    target_folders = matched_folders

                print(f"   ✅ 文件分类: {target_folders}")
                print(f"   📊 将复制到 {len(target_folders)} 个文件夹")

                # 复制到多个目标文件夹
                success_count, total_count = self.copy_to_target_folders(
                    file_path, file_name, base_target, target_folders
                )

                print(f"   📈 复制结果: {success_count}/{total_count} 个文件夹成功")

                print("=" * 60)
            else:
                print(f"   ❓ 未匹配到规则的文件: {file_name}")
                print("=" * 60)

        except Exception as e:
            print(f"❌ 处理文件时出错: {e}")
            import traceback
            traceback.print_exc()
            print("=" * 60)

    def classify_file(self, file_name, patterns):
        """根据文件名模式分类文件"""
        file_name_lower = file_name.lower()

        for pattern, target_folders in patterns.items():
            if re.search(pattern, file_name_lower, re.IGNORECASE):
                return target_folders

        return None


def start_temu_monitoring(base_folder):
    """启动监控"""
    if not os.path.exists(base_folder):
        print(f"❌ 监控文件夹不存在: {base_folder}")
        return

    print(f"🔍 监控文件夹: {base_folder}")

    event_handler = TemuFileHandler()
    observer = Observer()
    observer.schedule(event_handler, base_folder, recursive=True)
    observer.start()

    print(f"✅ 开始监控TEMU数据文件夹: {base_folder}")
    print("📋 监控的账号:", list(business_rules.keys()))
    print("💾 新增功能: 多目标复制 + 防止循环复制")
    print("=" * 60)

    try:
        while True:
            time.sleep(10)
            print("💓 监控运行中...")
    except KeyboardInterrupt:
        print("🛑 停止监控")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    base_monitor_path = r"C:\Users\vuser\Documents\Monthly Report\Monthly Channel Profit\Temu Ventchoice"

    print("🚀 启动TEMU文件监控系统...")
    print("=" * 60)
    print("🔄 多目标复制规则:")
    print("   📁 BillDetails 美国 → raw data us + raw data us and global")
    print("   📁 BillDetails 全球 → raw data global + raw data us and global")
    print("   📁 BillDetails → raw data us and global")
    print("   ✅ 其他文件类型保持单目标复制")
    print("=" * 60)

    start_temu_monitoring(base_monitor_path)