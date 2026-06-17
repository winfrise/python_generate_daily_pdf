from spire.pdf.common import *
from spire.pdf import *

def add_invisible_signature(input_path):

    base_name, ext = os.path.splitext(input_path)
    output_path = f"{base_name}_signed{ext}"

    # 1. 加载 PDF 文档
    pdf = PdfDocument()
    pdf.LoadFromFile(input_path)
    
    # 2. 创建签名生成器（需要一个证书文件，如 .pfx 或 .p12）
    # 注意：这里必须提供真实的证书和密码，否则无法生成底层签名结构
    signatureMaker = PdfOrdinarySignatureMaker(pdf, "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/certificate.pfx", "123456")
    
    # 3. 设置签名元数据（这些信息会显示在 WPS/Acrobat 的签名面板中）
    signature = signatureMaker.Signature
    signature.Name = "张三"
    signature.Reason = "文档审批确认"
    signature.Location = "中国"
    
    # 4. 添加不可见签名（只传签名字段名称，不传页面坐标和外观）
    signatureMaker.MakeSignature("InvisibleSignatureField")
    
    # 5. 保存文档
    pdf.SaveToFile(output_path)
    pdf.Close()
    print(f"不可见签名已添加，保存至: {output_path}")

if __name__ == "__main__":
    input_path = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
    # 运行测试
    add_invisible_signature(input_path)