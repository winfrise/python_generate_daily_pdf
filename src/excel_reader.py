import pandas as pd
from config import EXCEL_PATH

def read_order_data():
    """
    读取 Excel 数据并转换为 ReportLab 需要的格式
    """
    try:
        # header=None 确保第一行被当作数据处理
        df = pd.read_excel(EXCEL_PATH, header=None)

        # 【关键】axis=1 表示按列操作，how='all' 表示整列都是 NaN 才删除
        # 这样可以去除 Excel 中那些看不见的空白列
        df = df.dropna(axis=1, how='all')

        table_data = df.values.tolist()

        # 清洗剩余的单元格内的 NaN 为空字符串
        cleaned_data = []
        for row in table_data:
            new_row = ["" if pd.isna(cell) else str(cell) for cell in row]
            cleaned_data.append(new_row)

        return cleaned_data

    except FileNotFoundError:
        print(f"错误：找不到文件 {EXCEL_PATH}")
        print("请检查 config.py 中的 EXCEL_PATH 是否正确")
        return []
    except Exception as e:
        print(f"读取 Excel 发生未知错误: {e}")
        return []