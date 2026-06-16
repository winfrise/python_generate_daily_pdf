from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import FONT_PATH, TABLE_CONFIG, OUTPUT_PDF_PATH

# 不换行文字
class NoWrapParagraph(Paragraph):
    def wrap(self, availWidth, availHeight):
        # 1. 获取单行所需的真实最小宽度
        w = self.minWidth()

        # 2. 调用父类 wrap，但传入一个极大的宽度（如 9999 inch）
        #    这样父类会认为空间无限，不会进行截断或换行计算，从而正确生成 blPara
        #    高度 h 会被正确计算出来
        _, h = Paragraph.wrap(self, 9999*inch, availHeight)

        # 3. 返回真实的宽度 w 和计算出的高度 h
        return w, h

def create_start():
    elements = []
    
    text1_content = '编号: 2026061200085004702499331705700040431614'
    text1_style = ParagraphStyle(
            name='Text1Style',      # 样式名称（必填）
            fontName='MyFont',    # 字体名称
            fontSize=8,             # 字体大小
            leading=9.6,            # 行距
            alignment=0,     # 对齐方式 1=居中, 0=左对齐, 2=右对齐
            firstLineIndent=11*cm,      # 首行缩进
            spaceBefore=0*cm,          # 段前距
            spaceAfter=0,           # 段后距
            textColor=colors.black   # 字体颜色
    )
    text1 = NoWrapParagraph(text1_content, text1_style)
    elements.append(text1)

    text2_content = '支付宝支付科技有限公司&nbsp;&nbsp;&nbsp;交易流水证明'
    text2_style = ParagraphStyle(
            name='Text2Style',      # 样式名称（必填）
            fontName='MyFont',    # 字体名称
            fontSize=12,             # 字体大小
            leading=14.4,            # 行距
            alignment=1,     # 对齐方式 1=居中, 0=左对齐, 2=右对齐
            firstLineIndent=0,      # 首行缩进
            spaceBefore=0.5843*cm,          # 段前距
            spaceAfter=0,           # 段后距
            textColor=colors.black,   # 字体颜色
            letterSpacing=2 # 字间距
    )
    text2 = Paragraph(text2_content, text2_style)
    elements.append(text2)

    text3_content = '兹证明:周杰伦(证件号码:21090219830118xxxx)在其支付宝账号15831490000中明细信息如下:'
    text3_style = ParagraphStyle(
            name='Text3Style',      # 样式名称（必填）
            fontName='MyFont',    # 字体名称
            fontSize=8,             # 字体大小
            leading=9.6,            # 行距
            alignment=0,     # 对齐方式 1=居中, 0=左对齐, 2=右对齐
            firstLineIndent=16,      # 首行缩进
            spaceBefore=0.756*cm,          # 段前距
            spaceAfter=0,           # 段后距
            textColor=colors.black   # 字体颜色
    )
    text3 = Paragraph(text3_content, text3_style)
    elements.append(text3)

    text4_content = '币种：人民币 / 单位：元'
    text4_style = ParagraphStyle(
            name='Text4Style',      # 样式名称（必填）
            fontName='MyFont',    # 字体名称
            fontSize=12,             # 字体大小
            leading=14.4,            # 行距
            alignment=0,     # 对齐方式 1=居中, 0=左对齐, 2=右对齐
            firstLineIndent=4.4628*cm,      # 首行缩进
            spaceBefore=0.6498*cm,          # 段前距
            spaceAfter=0,           # 段后距
            textColor=colors.black   # 字体颜色
    )
    text4 = Paragraph(text4_content, text4_style)
    elements.append(text4)

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
            rightMargin=2.2964*cm,
            leftMargin=2.2964*cm,
            topMargin=1.2585*cm,
            bottomMargin=1.6228*cm
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