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
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Trusted Authority"), # <--- 这里改成你想要的颁发机构名称
        x509.NameAttribute(NameOID.COMMON_NAME, u"My Trusted Authority Root CA"),
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
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"WeChat User Dept"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"微信3"), # <--- 这是签名者的名字
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

    print(">>> 成功生成 wechat3_signed_by_ca.pfx")
    print(">>> 请使用此文件进行 PDF 签名，'Issued by' 将会显示为 'My Trusted Authority'")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y年%m月%d日%H时%M分%S秒")

    cert_path = os.path.join(BASE_DIR, "../cert", f"cert_self_signed_{formatted_time}.pfx")

    generate_ca_cert(cert_path)