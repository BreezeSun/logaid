import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64

class Mail:
    def __init__(self,host,token,sender,receivers):
        self.host = host
        self.token = token
        self.sender = sender
        self.receivers = receivers

    def send(self,subject, content):
        content = str(content)
        message = MIMEText(content, 'plain', 'utf-8')
        message["From"] = self.sender
        message["To"] = "LogAid Notice"
        message["Subject"] = subject

        if 'qq.com' in self.host:
            message['From'] = Header(
                f'=?utf-8?B?{base64.b64encode("LogAid Notice".encode()).decode()}=?= <{self.sender}>')
            message['To'] = Header("LogAid Notice", 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.host, 465)
            smtpObj.login(self.sender, self.token)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
        except Exception as e:
            raise e

if __name__ == '__main__':
    mail = Mail()
    mail.send('subject','test')
    email = {
        'host': 'smtp.qq.com',
        'token': 'xxxxxx',
        'sender': 'xxxxx@qq.com',
        'receivers': ['xxxxx@qq.com'],
        'subject': 'LogAid Notice'
    }
