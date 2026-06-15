import pandas as pd
from config import EXCEL_PATH

def read_order_data():
    """
    读取 Excel 数据并转换为 ReportLab 需要的格式
    """
    try:
        df = pd.read_excel(EXCEL_PATH)
        print(f"成功读取 {len(df)} 条数据")

        # 定义表头
        headers = ["序号", "商品描述", "单价"]
        table_data = [headers]

        # 遍历数据行
        for index, row in df.iterrows():
            # 将每一行转换为列表，index+1 作为序号
            table_data.append([
                str(index + 1),
                str(row.get('商品名称', '')), # 假设Excel列名叫'商品名称'
                f"¥{row.get('价格', 0):.2f}"
            ])

        return table_data

    except FileNotFoundError:
        print(f"错误：找不到文件 {EXCEL_PATH}")
        print("请检查 config.py 中的 EXCEL_PATH 是否正确")
        return []
    except Exception as e:
        print(f"读取 Excel 发生未知错误: {e}")
        return []