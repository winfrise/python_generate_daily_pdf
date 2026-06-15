from src.excel_reader import read_order_data
from src.pdf_builder import PdfBuilder

def main():
    print("--- 开始生成订单 PDF ---")

    # 1. 读取数据
    table_data = read_order_data()

    # 2. 生成 PDF
    if table_data:
        builder = PdfBuilder()
        builder.generate(table_data)
    else:
        print("任务终止。")

if __name__ == "__main__":
    main()