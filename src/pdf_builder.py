from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import FONT_PATH, TABLE_CONFIG, OUTPUT_PDF_PATH


def create_start():
    styles = {
        'Medium': ParagraphStyle(
            name='Medium',
            fontName='MyFont',
            fontSize=12,   # 大号字
            leading=20,    # 行高
            spaceAfter=12, # 段落后间距
            alignment=1,   # 1=居中, 0=左对齐, 2=右对齐
        ),
        'Small': ParagraphStyle(
            name='Small',
            fontName='MyFont',
            fontSize=8,    # 小号字
            leading=12,
            spaceAfter=6,
            textColor=colors.black, 
            alignment=2,
        )
    }

    header_texts = [
        ('编号: 2026061200085004702499331705700040431614', "Small"),
        ('支付宝支付科技有限公司 交易流水证明', "Medium"),
        ('兹证明:周杰伦(证件号码:21090219830118xxxx)在其支付宝账号15831490000中明细信息如下', "Small"),
        ('币种：人民币 / 单位：元', "Medium"),
    ]

    elements = []
    for text, style_name in header_texts:
        # 检查样式是否存在，不存在则使用默认 Body 样式
        para_style = styles.get(style_name, styles['Small'])
        para = Paragraph(text, para_style)
        elements.append(para)
    # 可以在头部文字和表格之间加一个大间距
    elements.append(Spacer(1, 20)) 

    return elements

def create_end():
    styles = {
        'Large': ParagraphStyle(
            name='Large',
            fontName='MyFont',
            fontSize=15,   # 大号字
            leading=20,    # 行高
            spaceAfter=12, # 段落后间距
            alignment=1,   # 1=居中, 0=左对齐, 2=右对齐
        ),
        'Medium': ParagraphStyle(
            name='Medium',
            fontName='MyFont',
            fontSize=12,   # 大号字
            leading=20,    # 行高
            spaceAfter=12, # 段落后间距
            alignment=1,   # 1=居中, 0=左对齐, 2=右对齐
        ),
        'Small': ParagraphStyle(
            name='Small',
            fontName='MyFont',
            fontSize=8,    # 小号字
            leading=12,
            spaceAfter=6,
            textColor=colors.black, 
            alignment=2,
        )
    }

    elements = []

    end_texts = [
        ("这是第一行文字。<br/>这是第二行文字。<br/>这是第三行。", "Small"),
        ("支付宝支付科技有限公司", "Large"),
        ("业务凭证专用章盖章处", "Medium")
    ]

    for text, style_name in end_texts:
        # 检查样式是否存在，不存在则使用默认 Body 样式
        para_style = styles.get(style_name)
        para = Paragraph(text, para_style)
        elements.append(para)
    # 可以在头部文字和表格之间加一个大间距
    elements.append(Spacer(1, 20)) 

    return elements

class PdfBuilder:
    def __init__(self):
        self._register_font()

    def _register_font(self):
        """注册中文字体"""
        try:
            # 这里的 'MyFont' 是我们在代码里引用的名字
            pdfmetrics.registerFont(TTFont('MyFont', FONT_PATH))
            print("字体注册成功")
        except Exception as e:
            print(f"字体注册失败: {e}")
            print("生成的 PDF 中文可能会乱码，请检查字体路径")

    def create_table_style(self):
        """定义表格样式"""
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'MyFont'), # 全局使用注册的中文字体
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),   # 垂直居中
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),      # 水平左对齐
            ('TOPPADDING', (0, 0), (-1, -1), 2),      # 上内边距
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),   # 下内边距
            ('GRID', (0, 0), (-1, -1), 0.6, colors.black), # 网格线
            # 表头样式
            # ('BACKGROUND', (0, 0), (-1, 0), TABLE_CONFIG['header_bg']),
            # ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            # ('FONTNAME', (0, 0), (-1, 0), 'MyFont'),
        ])
        return style

    def generate(self, data):
        """生成 PDF 文件"""
        if not data:
            print("没有数据，无法生成 PDF")
            return

        doc = SimpleDocTemplate(
            OUTPUT_PDF_PATH,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # 创建支持自动换行的段落样式
        p_style = ParagraphStyle(
            name='Normal',
            fontName='MyFont',
            fontSize=8,
            leading=8, # 行高
            wordWrap='CJK' # 关键：开启中日韩自动换行
        )

        # 处理数据：将长文本包裹在 Paragraph 中
        processed_data = []
        for i, row in enumerate(data):
            new_row = []
            for cell in row:
                # 第一行是表头，不需要 Paragraph，或者是单独处理
                if i == 0:
                    new_row.append(cell)
                else:
                    # 只有第二列（商品描述）需要强制换行，其他保持原样或也包裹
                    # 这里演示全部包裹，最稳妥
                    new_row.append(Paragraph(str(cell), p_style))
            processed_data.append(new_row)

        # 构建表格
        t = Table(processed_data, colWidths=TABLE_CONFIG['col_widths'])
        t.setStyle(self.create_table_style())

        # 构建文档内容
        elements = []

        # 添加开始的标题
        elements.extend(create_start())
        # B. 添加表格
        elements.append(t)
        # 添加结束
        elements.extend(create_end())

        # 开始生成
        doc.build(elements)
        print(f"PDF 生成成功: {OUTPUT_PDF_PATH}")