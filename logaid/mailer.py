import smtplib
from email.mime.text import MIMEText

class Mail:
    REQUIRED_FIELDS = ("host", "token", "sender", "nickname", "receivers", "subject")

    def __init__(self, email):
        if not isinstance(email, dict):
            raise TypeError('mailer config must be a dict.')
        missing_fields = [field for field in self.REQUIRED_FIELDS if field not in email]
        if missing_fields:
            raise ValueError(f'mailer config missing fields: {", ".join(missing_fields)}')
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
