import smtplib
from email.mime.text import MIMEText

class Mail:
    def __init__(self, email):
        self.host = email['host']
        self.token = email['token']
        self.sender = email['sender']
        self.nickname = email['nickname']
        self.receivers = email['receivers']
        self.subject = email['subject']

    def send(self,content):
        content = str(content)
        message = MIMEText(content, 'plain', 'utf-8')
        message["From"] = f"{self.nickname} <{self.sender}>"
        message["To"] = ""
        message["Subject"] = self.subject

        try:
            smtpObj = smtplib.SMTP_SSL(self.host, 465, timeout=3)
            smtpObj.login(self.sender, self.token)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            return True,'success'
        except Exception as e:
            return False,e


if __name__ == '__main__':
    email = {
        'host': 'smtp.qq.com',
        'token': 'skyfhpajuwjtcjhb',
        'nickname':'CSDN',
        'sender': '1774479405@qq.com',
        'receivers': ['python1966@qq.com'],
        'subject': 'LogAid Notice'
    }
    mail = Mail(email)
    mail.send('LogAid test.\n\n\n\n123456719')
