#!/usr/bin/env vpython3
# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from cryptography.hazmat.primitives.serialization import pkcs12
import os



def generate_ca_cert(cert_path):
    # ==============================
    # 第一步：生成根 CA 证书 (颁发者)
    # 这个证书将作为 "Issued by" 的来源
    # ==============================

    # 1. 生成根 CA 私钥
    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. 构建根 CA 证书主体信息 (这就是以后显示的 "Issued by")
    ca_subject = ca_issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "天威诚信CA"),
    ])

    # 3. 创建自签名的根证书
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_subject)
        .issuer_name(ca_issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650)) # 有效期10年
        .sign(ca_key, hashes.SHA256())
    )

    print(">>> 根 CA 证书已生成 (内存中)")


    # ==============================
    # 第二步：生成用户证书 (签名者)
    # 这个证书将作为 "Signed by" 的来源
    # ==============================

    # 1. 生成用户私钥
    user_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. 构建用户证书主体信息 (这就是以后显示的 "Signed by")
    user_subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "北京天威诚信电子商务服务有限公司"),
        x509.NameAttribute(NameOID.COMMON_NAME, "支付宝支付科技有限公司"), # <--- 这是签名者的名字
    ])

    # 3. 创建由根 CA 签发的用户证书
    # 注意：这里的 issuer_name 使用的是上面生成的 ca_cert.subject
    user_cert = (
        x509.CertificateBuilder()
        .subject_name(user_subject)       # 使用者：微信3
        .issuer_name(ca_cert.subject)     # 颁发者：My Trusted Authority (关键区别在这里！)
        .public_key(user_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) # 有效期1年
        .sign(ca_key, hashes.SHA256())    # 使用 CA 的私钥进行签名
    )

    print(">>> 用户证书已生成 (内存中)")


    # ==============================
    # 第三步：导出为 PFX 文件供 PDF 签名使用
    # ==============================

    # 导出用户证书（包含私钥和证书链）
    # 为了让 PDF 阅读器能验证信任链，最好把 CA 证书也打包进 pfx 的附加证书列表中
    pfx_data = serialization.pkcs12.serialize_key_and_certificates(
        name=b"wechat3_cert",
        key=user_key,
        cert=user_cert,
        cas=[ca_cert],  # 【重要】将 CA 证书放入此处，帮助建立信任链
        encryption_algorithm=serialization.BestAvailableEncryption(b"123456") # 设置密码
    )

    with open(cert_path, "wb") as f:
        f.write(pfx_data)

    print(">>> 成功生成 CA 证书")

    return cert_path


def add_cert_sign(input_path, output_path,  cert_path):

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "signingdate": date,
        "aligned": 0,
        "sigflags": 3,  # 签名标志，3表示文档签名后不允许修
        "sigflagsft": 132,
        "sigpage": 0,
        "signform": True,
        "sigfield": "Signature",
        "reason": "电子合同签约",
        "password": "1234",
    }


    with open(cert_path, "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"123456", backends.default_backend()
        )


    datau = open(input_path, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

    with open(output_path, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    print('添加签名成功')


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y年%m月%d日%H时%M分%S秒")


    # 一、生成证书
    cert_path = os.path.join(BASE_DIR, "../cert", f"cert_ca_signed_{formatted_time}.pfx")
    generate_ca_cert(cert_path = cert_path)


    # 二、添加签名
    input_path = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
    
    base_name, ext = os.path.splitext(input_path)
    output_path = f"{base_name}_signature-existing{ext}"


    add_cert_sign(
        input_path = input_path, 
        output_path = output_path, 
        cert_path = cert_path
    )