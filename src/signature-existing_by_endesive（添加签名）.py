#!/usr/bin/env vpython3
# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

# from endesive.pdf import cmsn as cms

# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "signingdate": date,
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "signform": True,
        "sigfield": "Signature",
        "reason": "这里是描述",
        "password": "1234",
    }
    with open("/Users/teacher/Desktop/pdf_command/python_generate_daily_pdf/cert/cert_ca_signed.pfx", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"123456", backends.default_backend()
        )
    fname = "/Users/teacher/Downloads/百度网盘下载/水/生成的文件_page_seal.pdf"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    datau = open(fname, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-signature-existing-field222333.pdf")
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)


main()
