from django.http import HttpResponse
from django.core.mail import send_mail
from users.models import EmailVertifyRecord
from random import Random
from jyteaches.settings import EMAIL_FROM
def random_str(default_length=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'
    random = Random()
    for i in range(default_length):
        str+=chars[random.randint(0,len(chars)-1)]  #索引
    return str

def register_send_mail(email,send_type='register'):
    email_record = EmailVertifyRecord()
    code = random_str(9)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == 'register':
        email_title = "在线教育网在线激活"
        email_body = "请点击下面的链接进行激活：http://127.0.0.1:8000/active/{0}".format(code)
        email_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if email_status:
            pass
        else:
            return HttpResponse('糟糕短信发送失败')
    if send_type == 'forget':
        email_title = "在线教育网重置密码"
        email_body = "请点击下面的链接进行密码重置：http://127.0.0.1:8000/reset/{0}".format(code)
        email_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if email_status:
            pass
        else:
            return HttpResponse('糟糕短信发送失败')