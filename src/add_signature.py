import endesive.pdf.cms as cms
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from datetime import datetime

# ==============================
# 1. 配置参数
# ==============================

# 你通过 generate_ca_cert.py 生成的 PFX 文件路径
PFX_PATH = '/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/cert/cert_ca_signed.pfx'  # <-- 请替换为你的实际文件路径

# PFX 文件的密码 (在 generate_ca_cert.py 中设置为 "123456")
PFX_PASSWORD = '123456'

# 待签名的原始 PDF 文件路径
INPUT_PDF = '/Users/teacher/Downloads/百度网盘下载/水/111_2026年06月18日08时15分06秒.pdf'  # <-- 请替换为你要签名的PDF文件路径

# 签名后输出的 PDF 文件路径
OUTPUT_PDF = '/Users/teacher/Downloads/百度网盘下载/水/111_2026年06月18日08时15分06秒_NEWSSS.pdf'

# ==============================
# 2. 加载证书和私钥
# ==============================
with open(PFX_PATH, 'rb') as f:
    pfx_data = f.read()

private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
    pfx_data, PFX_PASSWORD.encode(), backend=default_backend()
)

# ==============================
# 3. 读取原始PDF文件
# ==============================
with open(INPUT_PDF, 'rb') as f:
    pdf_data = f.read()

# ==============================
# 4. 准备签名元数据 (关键修复点)
# ==============================
# 这里的 udct 就是报错提示缺少的参数
sig_metadata = {
    "sigflags": 3,           # 签名标志，3表示文档签名后不允许修改
    "contact": "teacher@example.com", # 联系方式
    "location": "Beijing, China",     # 签署地点
    "signingdate": datetime.now().strftime("D:%Y%m%d%H%M%S+08'00'"), # 签署时间
    "reason": "Document Approval",    # 签署原因
}

# ==============================
# 5. 执行签名
# ==============================
try:
    # 注意：不同版本的 endesive 参数顺序可能略有不同
    # 常见顺序：(data, private_key, certificate_chain, hash_algorithm, sig_metadata)
    signed_pdf_data = cms.sign(
        pdf_data,               # 1. PDF 二进制数据
        private_key,            # 2. 私钥对象
        [certificate],          # 3. 证书链列表
        "sha256",               # 4. 哈希算法
        sig_metadata            # 5. 签名字典 (即报错缺少的 udct)
    )

    # ==============================
    # 6. 保存签名后的文件
    # ==============================
    with open(OUTPUT_PDF, 'wb') as f:
        f.write(signed_pdf_data)

    print(f"✅ 签名成功！文件已保存为: {OUTPUT_PDF}")

except Exception as e:
    print(f"❌ 签名失败: {e}")