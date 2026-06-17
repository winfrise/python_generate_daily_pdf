from spire.pdf.common import *
from spire.pdf import *
import os
import subprocess

def validate_certificate(cert_path, password):
    """验证证书是否可读"""
    try:
        # 使用 openssl 验证
        cmd = [
            "openssl", "pkcs12",
            "-in", cert_path,
            "-info", "-noout",
            "-passin", f"pass:{password}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 证书验证通过")
            return True
        else:
            print(f"❌ 证书验证失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return False

def add_invisible_signature(input_path):
    try:
        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_signed{ext}"
        
        # 1. 加载 PDF 文档
        pdf = PdfDocument()
        pdf.LoadFromFile(input_path)
        
        # 2. 证书信息
        cert_path = "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/wechat3_signed_by_ca.pfx"
        password = "123456"
        
        # 3. 验证证书
        if not validate_certificate(cert_path, password):
            print("⚠️  证书验证失败，尝试使用备用证书...")
            # 尝试其他可能的证书路径
            alt_paths = [
                "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/cert.p12",
                "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/certificate.p12",
            ]
            for alt in alt_paths:
                if os.path.exists(alt) and validate_certificate(alt, password):
                    cert_path = alt
                    print(f"✅ 使用备用证书: {alt}")
                    break
        
        # 4. 创建签名生成器
        signatureMaker = PdfOrdinarySignatureMaker(pdf, cert_path, password)
        
        # 5. 设置签名元数据
        signature = signatureMaker.Signature
        signature.Name = "支付宝贝"
        signature.Reason = "文档审批确认111"
        signature.Location = "CN"


        
        
        # 6. 添加不可见签名
        signatureMaker.MakeSignature("InvisibleSignatureField")
        
        # 7. 保存文档
        pdf.SaveToFile(output_path)
        pdf.Close()
        print(f"✅ 不可见签名已添加，保存至: {output_path}")
        
    except Exception as e:
        print(f"❌ 签名失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    input_path = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
    add_invisible_signature(input_path)