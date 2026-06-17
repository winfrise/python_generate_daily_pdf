import pandas as pd
import os

def filter_excel_files(folder_path, keyword, output_file):
    """
    遍历文件夹中所有Excel文件的所有Sheet，筛选包含指定关键字的行并汇总。
    :param folder_path: Excel文件所在的文件夹路径
    :param keyword: 需要筛选的关键字
    :param output_file: 结果保存的Excel文件路径
    """
    all_matched_rows = []  # 用于存储所有匹配的行
    
    # 1. 获取文件夹下所有的Excel文件
    excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print("指定文件夹下没有找到Excel文件。")
        return

    # 2. 遍历每一个Excel文件
    for file_name in excel_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            # 读取该Excel文件的所有Sheet名称
            xls = pd.ExcelFile(file_path)
            
            # 3. 遍历该文件中的每一个Sheet
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # 4. 检查每一列是否包含关键字（不区分大小写，处理空值）
                # 将整行数据转为字符串后进行关键字匹配
                mask = df.astype(str).apply(lambda col: col.str.contains(keyword, case=False, na=False)).any(axis=1)
                
                # 5. 提取匹配的行
                matched_df = df[mask].copy()
                
                # 如果找到了匹配的数据，添加来源信息并加入汇总列表
                if not matched_df.empty:
                    matched_df['来源文件'] = file_name
                    matched_df['来源Sheet'] = sheet_name
                    all_matched_rows.append(matched_df)
                    
        except Exception as e:
            print(f"处理文件 {file_name} 时发生错误: {e}")

    # 6. 合并所有结果并导出到新的Excel文件
    if all_matched_rows:
        result = pd.concat(all_matched_rows, ignore_index=True)
        result.to_excel(output_file, index=False)
        print(f"筛选完成！共找到 {len(result)} 条包含 '{keyword}' 的数据。")
        print(f"结果已保存至: {output_file}")
    else:
        print(f"未找到任何包含 '{keyword}' 的数据。")

# ================= 运行配置区 =================
if __name__ == "__main__":
    # 请修改为你存放Excel文件的实际文件夹路径
    target_folder = "/Users/teacher/Downloads/百度网盘下载/流水转excel"  
    # 需要查找的关键字
    search_keyword = "金铃狮"       
    # 输出的新Excel文件名
    output_excel = "/Users/teacher/Downloads/百度网盘下载/金铃狮筛选结果.xlsx" 
    
    # 确保目标文件夹存在
    if os.path.exists(target_folder):
        filter_excel_files(target_folder, search_keyword, output_excel)
    else:
        print(f"错误：找不到文件夹 '{target_folder}'，请检查路径是否正确。")