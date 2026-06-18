from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import FONT_PATH, TABLE_CONFIG, STAMP_PATH
from utils.relative_overlay import RelativeOverlay 

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
            firstLineIndent=11.522*cm,      # 首行缩进
            spaceBefore=0.192*cm,          # 段前距
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
            spaceBefore=0.22*cm,          # 段前距
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
            firstLineIndent=8.478*cm,      # 首行缩进
            spaceBefore=0.6498*cm,          # 段前距
            spaceAfter=0.1*cm,           # 段后距
            textColor=colors.black   # 字体颜色
    )
    text4 = Paragraph(text4_content, text4_style)
    elements.append(text4)

    # elements.append(Spacer(1, 20)) 

    return elements

def create_end():
    elements = []

    elements.append(Spacer(1, 100)) 

    text1_content = "特别提示:<br/>1. 本证明仅证明在用户选择的交易类型和时间段内，用户通过支付宝账户发生的历史交易记录情况。<br/>2. 因系统原因或通讯故障等偶发因素导致本回单与实际交易结果不符时，以实际交易情况为准。<br/>3. 支付宝快捷支付等非余额支付方式可能既产生支付宝交易也同步产生银行交易，因此请勿使用本回单进行重复记账。<br/>4. 本回单如经任何涂改、编造，均立即失去效力。<br/>5. 部分账单如：充值提现、账户转存或者个人设置收支等不计入为收入或者支出，记为不计收支类。<br/>6. 因统计逻辑不同，明细金额直接累加后，可能会和下方统计金额不一致，请以实际交易金额为准。<br/>7. 禁止将本回单用于非法用途。"
    text1_style = ParagraphStyle(
            name='Text1',
            fontName='MyFont',
            fontSize=8,   # 大号字
            leading=12,    # 行高
            alignment=0,   # 1=居中, 0=左对齐, 2=右对齐
            leftIndent=-10
        )
    text1 = Paragraph(text1_content, text1_style)
    elements.append(text1)


    text2_content = "支付宝支付科技有限公司"
    text2_style = ParagraphStyle(
            name='Text2',
            fontName='MyFont',
            fontSize=16,   # 大号字
            leading=19.2,    # 行高
            spaceAfter=0.719*cm, # 段落后间距
            alignment=2,   # 1=居中, 0=左对齐, 2=右对齐
            rightIndent=-0.5*cm,
        )
    text2 = Paragraph(text2_content, text2_style)
    elements.append(text2)

    stamp_text_content = "业务凭证专用章盖章处"
    stamp_text_style = ParagraphStyle(
            name='Text3',
            fontName='MyFont',
            fontSize=12,  
            leading=14.4,    # 行高
            alignment=2,   # 1=居中, 0=左对齐, 2=右对齐
            rightIndent=-0.5*cm,
        )
    stamp_text = Paragraph(stamp_text_content, stamp_text_style)

    stamp_img = Image(STAMP_PATH, width=4*cm, height=4*cm)

    overlay_stamp = RelativeOverlay(
        target_element=stamp_text,
        overlay_element=stamp_img,
        offset_x=11.5*cm, 
        offset_y=-2.5*cm
    )

    elements.append(overlay_stamp)
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

            # 合并第1行 (Row 0): 从第0列到最后一列 (-1)
            ('SPAN', (0, 0), (-1, 0)),
            # 合并第2行 (Row 1): 从第0列到最后一列 (-1)
            ('SPAN', (0, 1), (-1, 1)),

            # 全局样式
            ('FONTNAME', (0, 0), (-1, -1), 'MyFont'), # 全局使用注册的中文字体
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # 垂直居中
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),      # 水平左对齐

            ('TOPPADDING', (0, 0), (-1, -1), 2),      # 上内边距
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),   # 下内边距
            ('LEFTPADDING', (0, 0), (-1, -1), 2),   # 下内边距
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),   # 下内边距

            ('GRID', (0, 0), (-1, -1), 0.6, colors.black), # 网格线
        ])
        return style

    def generate(self, data, output_path):
        """生成 PDF 文件"""
        if not data:
            print("没有数据，无法生成 PDF")
            return

        full_data = [
                ["交易时间段：2026-01-01 00:00:00 至 2026-06-12 23:59:59"],  # 第1行
                ["交易类型：全部"],                                      # 第2行
            ] + data

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.72*cm,
            leftMargin=1.72*cm,
            topMargin=1.26*cm,
            bottomMargin=1.26*cm
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
        for i, row in enumerate(full_data):
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
        print(f"PDF 生成成功: {output_path}")