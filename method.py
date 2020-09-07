import os
from email.mime.multipart import MIMEMultipart

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tinydb import TinyDB
import configparser

class Method():
    def __init__(self):
        self.content=""
        self.enclosure=""
    def getFile(self,text4,whoiswhat):
        if whoiswhat==1:
          fileName, filetype = QFileDialog.getOpenFileNames(None, "请选择要发送的文件",
                                                              "c:/",
                                                              "Text Files (*.txt)")
          self.content= self.get_contends(str(fileName[0]))
          text4.setText(str(fileName[0]))
        else:
          fileName, filetype = QFileDialog.getOpenFileNames(None, "请选择要发送的文件",
                                                              "c:/",
                                                              "Text Files (*.*)")
          self.enclosure=str(fileName[0])
          text4.setText(str(fileName[0]))
    def get_contends(self,path):
        with open(path,'r',encoding='utf-8') as file_object:
            contends = file_object.read()
        return contends
    def setEmail(self,email,text1,text2,text3,header,checkBox):
        self.saveConfig(checkBox,text1.text(),text2.text(),text1.text(),text3.text(),email.currentText())
        db = TinyDB('./db.json')
        db.table("logs")
        table = db.table('user')
        if email.currentText()=="QQ邮箱":
            host="smtp.qq.com"
            content=self.content
            issucce=self.sendEmail(host, text1.text(), text2.text(), text1.text(), text3.text(), header, content,  25)
            if issucce:
                db.insert({'QQ邮箱':{'发送邮箱':text1.text(),"发送口令":text2.text(),"发送人":text1.text(),"接受人":text3.text()}})
                QMessageBox.about(None, "提示!!!", "发送成功!")
        elif email.currentText()=="新浪邮箱":
            host = "smtp.sina.com"
            content = self.content
            issucce=self.sendEmail(host, text1.text(), text2.text(), text1.text(), text3.text(), header, content,  465)
            if issucce:
              db.insert({'新浪邮箱': {'发送邮箱': text1.text(), "发送口令": text2.text(), "发送人": text1.text(), "接受人": text3.text()}})
              QMessageBox.about(None, "提示!!!", "发送成功!")
        elif email.currentText()=="163邮箱":
            host = "smtp.163.com"
            content = self.content
            issucce=self.sendEmail(host, text1.text(), text2.text(), text1.text(), text3.text(), header, content,  465)
            if issucce:
              db.insert({'163邮箱': {'发送邮箱': text1.text(), "发送口令": text2.text(), "发送人": text1.text(), "接受人": text3.text()}})
              QMessageBox.about(None,  "提示!!!", "发送成功!")
    def sendEmail(self,host,user,passt,send,receiver,hearder,content,port):
        # 第三方 SMTP 服务
        mail_host = host  #"smtp.qq.com"  # 设置服务器
        mail_user =user   #"1848971636@qq.com"  # 用户名
        mail_pass = passt   #"jgdrritqlxfxdfgh"  # 口令
        sender = send          #'1848971636@qq.com'
        receivers = receiver #['827947062@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        # message = MIMEText(content, 'plain', 'utf-8')
        message =MIMEMultipart()
        message.attach(MIMEText(content, 'html', 'utf-8'))
        # 寄件者
        message["From"] = sender
        # 收件者
        message["To"] = receivers
        subject = hearder
        # 设置邮件主题
        message['Subject'] = Header(subject, 'utf-8')
        if self.enclosure:
            send_file = open(self.enclosure, 'rb').read()
            self.att = MIMEText(send_file,'base64','utf-8')  # 调用传送附件模块，传送附件
            self.att["Content-Type"] = 'application/octet-stream'
            self.att["Content-Disposition"] = 'attachment;filename='+str(os.path.basename(self.enclosure))
            message.attach(self.att)
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host,port,10)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            return True
        except Exception as e:
            print(str(e))

    def saveConfig(self,checkBox,user,passt,send,receiver,emailType):
        print(checkBox.isChecked())
        config = configparser.ConfigParser()
        if  checkBox.isChecked():
            config["DEFAULT"] = {
                "user": user,
                "passt": passt,
                "send": send,
                "receiver":receiver,
                "checkBox":True,
                "emailType":emailType
            }
        else:
            config["DEFAULT"] = {
                "user": "",
                "passt": "",
                "send": "",
                "receiver":"",
                "checkBox": False,
                "emailType": ""
            }
        with open('user.ini', 'w')as configfile:
            config.write((configfile))



