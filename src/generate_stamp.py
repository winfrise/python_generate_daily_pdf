from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def generate_stamp(output_path, text_content, stamp_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # 1. 绘制文字
    c.setFont("Helvetica", 12)
    c.drawString(5*cm, 25*cm, text_content)  # 文字位置
    
    # 2. 绘制印章（紧跟文字下方）
    stamp_x = 5*cm
    stamp_y = 23*cm  # 文字下方2cm处
    stamp_w = 3*cm
    stamp_h = 3*cm
    c.drawImage(stamp_path, stamp_x, stamp_y, width=stamp_w, height=stamp_h, mask='auto')
    
    c.save()
