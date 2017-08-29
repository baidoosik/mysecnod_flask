import os
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication


class Mail():
    def __init__(self,contents,email_address):
        self.contents =contents
        self.address =email_address

    def ready_to_send_mail(self):
        message = EmailMessage()

        message['Subject'] = '네이버 웹툰 리스트 업데이트 리스트'
        message['From'] = 'qoentlr37@naver.com'
        message['To'] = self.address

        message.set_content((self.contents))

        return message

    def naver_send_email(self):

        message= self.ready_to_send_mail()

        with smtplib.SMTP_SSL('smtp.naver.com',465) as server:
            server.ehlo()
            server.login('qoentlr37','Erunc837@@')
            server.send_message(message)




