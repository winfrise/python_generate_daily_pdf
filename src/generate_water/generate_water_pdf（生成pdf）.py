import os
from datetime import datetime
from tools.excel_reader import read_order_data
from tools.pdf_builder import PdfBuilder

def main(excel_path):
    print("--- 开始生成订单 PDF ---")

    # 1. 读取数据
    table_data = read_order_data(excel_path)
    
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y年%m月%d日%H时%M分%S秒")

    base_name, ext = os.path.splitext(excel_path)
    output_path = f"{base_name}_{formatted_time}.pdf"


    # 2. 生成 PDF
    if table_data:
        builder = PdfBuilder()
        builder.generate(table_data, output_path)
    else:
        print("任务终止。")

if __name__ == "__main__":
    excel_path = "/Users/teacher/Downloads/百度网盘下载/水/111.xlsx"
    main(excel_path)