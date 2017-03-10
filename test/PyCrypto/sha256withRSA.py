# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


if str(sys.version[0]) == "3":
 | from base64 import decodebytes, encodebytes
 | from urllib import parse as urlparse
else:
 | from base64 import decodestring as decodebytes
 | from base64 import encodestring as encodebytes
 | import urlparse
 | import urllib

private_key_file = 'private.pem'
public_key_file = 'public.pem'
ali_public_key_file = 'ali_public.pem'

unSigneddata = {
 | 'app_id': '2014072300007148',
 | 'method': 'alipay.mobile.public.menu.add',
 | 'charset': 'GBK',
 | 'sign_type': 'RSA2',
 | 'timestamp': '2014-07-24 03:07:50',
 | 'biz_content': {
 |  | "button":[
 |  |  | {
 |  |  |  | "actionParam":"ZFB_HFCZ",
 |  |  |  | "actionType":"out",
 |  |  |  | "name":"话费充值"
 |  |  | },
 |  |  | {
 |  |  |  | "name":"查询",
 |  |  |  | "subButton":[
 |  |  |  |  | {
 |  |  |  |  |  | "actionParam":"ZFB_YECX",
 |  |  |  |  |  | "actionType":"out",
 |  |  |  |  |  | "name":"余额查询"
 |  |  |  |  | },
 |  |  |  |  | {
 |  |  |  |  |  | "actionParam":"ZFB_LLCX",
 |  |  |  |  |  | "actionType":"out",
 |  |  |  |  |  | "name":"流量查询"
 |  |  |  |  | },
 |  |  |  |  | {
 |  |  |  |  |  | "actionParam":"ZFB_HFCX",
 |  |  |  |  |  | "actionType":"out",
 |  |  |  |  |  | "name":"话费查询"
 |  |  |  |  | }
 |  |  |  | ]
 |  |  | },
 |  |  | {
 |  |  |  | "actionParam":"http://m.alipay.com",
 |  |  |  | "actionType":"link",
 |  |  |  | "name":"最新优惠"
 |  |  | }
 |  | ]
 | },
 | 'sign': '',
 | 'version': '1.0',
}

def rsa_sign(sign_type="RSA2", unsigned_string=""):
 | with open(private_key_file) as fp:
 |  | key = RSA.importKey(fp.read())
 |  | signer = PKCS1_v1_5.new(key)
 |  | if sign_type == "RSA":
 |  |  | signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
 |  | else:
 |  |  | signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
 |  | # base64 编码，转换为unicode表示并移除回车
 |  | sign = encodebytes(signature).decode("utf8").replace("\n", "")
 |  | print(sign)
 |  | return sign


def __ordered_data(data):
 | complex_keys = []
 | for key, value in data.items():
 |  | if isinstance(value, dict):
 |  |  | complex_keys.append(key)

 | # 将字典类型的数据dump出来
 | for key in complex_keys:
 |  | # data[key] = json.dumps(data[key], separators=(',', ':'))
 |  | data[key] = json.dumps(data[key], separators=(',', ':'))

 | return sorted([(k, v) for k, v in data.items()])

def sign_str():
 | unSigneddata.pop("sign", None)
 | unsigned_items = __ordered_data(unSigneddata)
 | # print(unsigned_items)
 | unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
 | # print(type(unsigned_string))
 | # print("========")
 | # print(unsigned_string)
 | data = rsa_sign(unsigned_string=unsigned_string)


def mes2dict(message=''):
 | if not message:
 |  | message = 'https://api.xx.com/receive_notify.htm?gmt_payment=2015-06-11 22:33:59&notify_id=42af7baacd1d3746cf7b56752b91edcj34&seller_email=testyufabu07@alipay.com&notify_type=trade_status_sync&sign=kPbQIjX+xQc8F0/A6/AocELIjhhZnGbcBN6G4MM/HmfWL4ZiHM6fWl5NQhzXJusaklZ1LFuMo+lHQUELAYeugH8LYFvxnNajOvZhuxNFbN2LhF0l/KL8ANtj8oyPM4NN7Qft2kWJTDJUpQOzCzNnV9hDxh5AaT9FPqRS6ZKxnzM=&trade_no=2015061121001004400068549373&out_trade_no=21repl2ac2eOutTradeNo322&gmt_create=2015-06-11 22:33:46&seller_id=2088211521646673&notify_time=2015-06-11 22:34:03&subject=FACE_TO_FACE_PAYMENT_PRECREATE中文&trade_status=TRADE_SUCCESS&sign_type=RSA2'
 | # print(type(message), message)
 | message_date = dict(urlparse.parse_qsl(message.split('?', 1)[1]))
 | print(message_date)
 | return message_date

def verify_notify(data=None, signature='', sign_type='RSA2'):
 | response = {"code": 200, 'mes': ''}
 | res = mes2dict()
 | sign = res.pop("sign", None)
 | sign_type = res.pop("sign_type", None)
 | if not all([sign, sign_type]):
 |  | # 参数不合法
 |  | response['code'] = '401'
 |  | response['mes'] = '验签失败:关键参数缺少'
 |  | return response
 | unsigned_items = __ordered_data(res)
 | message = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
 | print(message)
 | return _verify(sign_type=sign_type, raw_content=message, signature=sign)

def _verify(sign_type="RSA2", raw_content="", signature=""):
 | # 开始计算签名
 | with open(ali_public_key_file) as fp:
 |  | key = RSA.importKey(fp.read())
 |  | signer = PKCS1_v1_5.new(key)
 |  | if sign_type == "RSA":
 |  |  | digest = SHA.new()
 |  | else:
 |  |  | digest = SHA256.new()
 |  | digest.update(raw_content.encode("utf8"))
 |  | print(digest)
 |  | print(digest.hexdigest())
 |  | if signer.verify(digest, decodebytes(signature.encode("utf8"))):
 |  |  | return True
 |  | return False


if '__main__' == __name__:
 | unsigned_string = 'app_id=2014072300007148&biz_content={"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"话费充值"},{"name":"查询","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"余额查询"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"流量查询"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"话费查询"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"最新优惠"}]}&charset=utf-8&method=alipay.mobile.public.menu.add&sign_type=RSA2&timestamp=2014-07-24 03:07:50&version=1.0'
 |  |  |  |  | # | app_id=2014072300007148&biz_content={"button":[{"actionParam":"ZFB_HFCZ","actionType":"out","name":"\u8bdd\u8d39\u5145\u503c"},{"name":"\u67e5\u8be2","subButton":[{"actionParam":"ZFB_YECX","actionType":"out","name":"\u4f59\u989d\u67e5\u8be2"},{"actionParam":"ZFB_LLCX","actionType":"out","name":"\u6d41\u91cf\u67e5\u8be2"},{"actionParam":"ZFB_HFCX","actionType":"out","name":"\u8bdd\u8d39\u67e5\u8be2"}]},{"actionParam":"http://m.alipay.com","actionType":"link","name":"\u6700\u65b0\u4f18\u60e0"}]}&charset=GBK&method=alipay.mobile.public.menu.add&sign_type=RSA2&timestamp=2014-07-24 03:07:50&version=1.0

 | # rsa_sign(unsigned_string=unsigned_string)
 | rsa_sign(unsigned_string='a=123')
 | # sign_str()
 | # verify_notify()
