# # add_cert_endesive.py
# import os
# import hashlib
# import datetime


# def sign_pdf_with_endesive(input_pdf, output_pdf, cert_path, password):
#     """
#     使用 endesive 签名 PDF
#     """
#     try:
#         # 检查文件
#         input_pdf = os.path.abspath(input_pdf.strip())
#         cert_path = os.path.abspath(cert_path.strip())
#         output_pdf = os.path.abspath(output_pdf.strip())
        
#         if not os.path.exists(input_pdf):
#             raise FileNotFoundError(f"输入PDF不存在: {input_pdf}")
#         if not os.path.exists(cert_path):
#             raise FileNotFoundError(f"证书不存在: {cert_path}")
        
#         # 读取文件
#         with open(cert_path, 'rb') as f:
#             pfx_data = f.read()
        
#         with open(input_pdf, 'rb') as f:
#             pdf_data = f.read()
        
#         # 使用 endesive 签名
#         from endesive import pdf
        
#         # 配置签名
#         signature = {
#             'sig_name': 'Signature1',
#             'sig_subfilter': 'adbe.pkcs7.detached',
#             'sig_info': {
#                 'name': '张三',
#                 'reason': '文档审批确认',
#                 'location': '中国',
#                 'contact': 'zhangsan@company.com',
#                 'date': datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S+00\'00\''),
#             }
#         }
        
#         # 执行签名
#         signed_data = pdf.sign(
#             pdf_data,
#             pfx_data,
#             password,
#             signature,
#             hashlib.sha256()
#         )
        
#         # 保存
#         with open(output_pdf, 'wb') as f:
#             f.write(signed_data)
        
#         print(f"✅ 签名成功: {output_pdf}")
#         return output_pdf
        
#     except ImportError:
#         print("❌ endesive 未安装，请安装: pip install endesive")
#         return None
#     except Exception as e:
#         print(f"❌ 失败: {e}")
#         import traceback
#         traceback.print_exc()
#         return None

# if __name__ == "__main__":
#     input_pdf = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
#     cert_file = "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/cert_compatible.pfx"
#     password = "123456"
#     output_pdf = input_pdf.replace('.pdf', '_signed_endesive.pdf')
    
#     sign_pdf_with_endesive(input_pdf, output_pdf, cert_file, password)


# add_cert_compatible.py
from endesive import pdf
import hashlib
import datetime
import os

def sign_pdf(input_pdf_path, output_pdf_path, cert_path, cert_password):
    """
    使用 endesive 签名 PDF（兼容旧版本）
    """
    try:
        # 1. 读取证书文件
        with open(cert_path, 'rb') as f:
            pfx_data = f.read()
        
        # 2. 读取 PDF 文件
        with open(input_pdf_path, 'rb') as f:
            pdf_data = f.read()
        
        # 3. 配置签名
        # 注意：旧版本可能使用不同的参数格式
        signature = {
            'sig_name': 'Signature1',
            'sig_subfilter': 'adbe.pkcs7.detached',
            'sig_info': {
                'name': '张三',
                'reason': '文档审批确认',
                'location': '中国',
                'contact': 'zhangsan@company.com',
                'date': datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S+00\'00\''),
            }
        }
        
        # 4. 执行签名
        # 尝试不同的签名方法
        try:
            # 方法1: 使用 pdf.sign 直接传入证书数据
            signed_data = pdf.cms.sign(
                pdf_data,
                pfx_data,
                cert_password,
                signature,
                hashlib.sha256()
            )
        except TypeError:
            # 方法2: 如果上面的方法不行，尝试不带哈希参数
            signed_data = sign(
                pdf_data,
                pfx_data,
                cert_password,
                signature
            )
        
        # 5. 保存签名后的 PDF
        with open(output_pdf_path, 'wb') as f:
            f.write(signed_data)
        
        print(f"✅ PDF 签名成功！")
        print(f"📁 输出文件: {output_pdf_path}")
        print(f"\n📋 签名信息:")
        print(f"  - 签名者: 张三")
        print(f"  - 原因: 文档审批确认")
        print(f"  - 位置: 中国")
        
        return output_pdf_path
        
    except Exception as e:
        print(f"❌ 签名失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def verify_pdf(pdf_path):
    """
    验证 PDF 签名
    """
    try:
        with open(pdf_path, 'rb') as f:
            data = f.read()
        
        # 获取签名信息
        signatures = pdf.get_signatures(data)
        
        if not signatures:
            print("❌ PDF 没有签名")
            return False
        
        print(f"✅ 找到 {len(signatures)} 个签名")
        
        for i, sig in enumerate(signatures, 1):
            print(f"\n📋 签名 {i}:")
            print(f"  - 签名者: {sig.get('name', 'N/A')}")
            print(f"  - 原因: {sig.get('reason', 'N/A')}")
            print(f"  - 位置: {sig.get('location', 'N/A')}")
            print(f"  - 时间: {sig.get('date', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    # 配置路径
    input_pdf = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
    cert_file = "/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/wechat3_signed_by_ca.pfx"
    password = "123456"
    output_pdf = input_pdf.replace('.pdf', '_signed.pdf')
    
    # 执行签名
    sign_pdf(input_pdf, output_pdf, cert_file, password)
    
    # 验证签名
    # verify_pdf(output_pdf)