# src/generate_compatible_cert.py
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime
import os
from cryptography.hazmat.primitives.serialization import pkcs12

def generate_self_cert(cert_path):
    """生成 macOS 兼容的 PKCS#12 证书"""
    
    # 1. 生成 RSA 私钥（使用 2048 位）
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # 2. 创建自签名证书
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"微信3"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Test Org3"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"33"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).sign(private_key, hashes.SHA256())
    
    # 3. 序列化为 PKCS#12 格式
    # 使用较新的加密算法（AES-256-CBC）
    p12_data = serialization.pkcs12.serialize_key_and_certificates(
        name=b"test_cert",
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(b"123456")
    )
    
    # 4. 保存证书
    with open(cert_path, "wb") as f:
        f.write(p12_data)
    
    print(f"✅ 兼容证书已生成: {cert_path}")
    print(f"📄 密码: 123456")
    print(f"🔑 算法: RSA 2048 + SHA256 + AES-256-CBC")
    
    return cert_path

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y年%m月%d日%H时%M分%S秒")

    cert_path = os.path.join(BASE_DIR, "../cert", f"cert_self_signed_{formatted_time}.pfx")
    generate_self_cert(cert_path)