import os
from reportlab.lib.units import cm
from reportlab.lib import colors

# 获取当前脚本所在的绝对路径，防止相对路径出错
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. 路径配置 ---
# 数据文件路径
# EXCEL_PATH = os.path.join(BASE_DIR, "assets","data", "11.xlsx")
EXCEL_PATH = "/Users/teacher/Downloads/百度网盘下载/水/111.xlsx"

# 输出文件路径
# OUTPUT_PDF_PATH = os.path.join(BASE_DIR, "output_report.pdf")
OUTPUT_PATH="/Users/teacher/Downloads/百度网盘下载/水/生成的文件.pdf"

# --- 2. 字体配置 ---
# 注意：macOS 系统自带字体通常不在项目目录下，建议直接使用系统绝对路径
# 如果一定要用项目里的字体，请确保 assets/fonts/SimSun.ttf 存在
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "SimSun.ttf")

STAMP_PATH = os.path.join(BASE_DIR, "assets", "images", "stamp.png")

# 备选方案：如果是 macOS 开发测试，可以直接用系统自带的黑体，避免找不到字体的报错
# FONT_PATH = "/System/Library/Fonts/PingFang.ttc"

# --- 3. 表格样式配置 ---
TABLE_CONFIG = {
    "col_widths": [1.13*cm, 2.26*cm, 2.26*cm, 1.7*cm, 3.957*cm, 3.957*cm, 2.26*cm],  # 列宽：序号、商品名、价格
    "header_bg": colors.HexColor('#4F81BD'), # 表头背景色
}