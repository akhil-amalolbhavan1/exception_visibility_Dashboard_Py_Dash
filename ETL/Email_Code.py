# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:30:28 2019

@author: 300068051
"""
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase 
from email import encoders 
import os

# class email_myntra:
    #base_path = "D:/Automation/Python/Q2_Automation/"
    # def __init__(self, Base_Path):
    #     self.base_path = Base_Path
    #     os.chdir(self.base_path)
    #Base_Path="D:/To/Training/To_Nitin/" #Give the path details where you have to save the data
    
    
    ##########################################################################################################################
    ############ Mail Generation                                                                             #################
    ##########################################################################################################################  
def send_mail(to_mailid, from_mailid, password, subject, html, fileName = None):
    #attachment=attachments
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_mailid
    #msgRoot['CC'] = ', '.join(to_mailid)
    #msgRoot['To'] = ", ".join(to_mailid)
    msgRoot['To'] = to_mailid
    msgRoot['Recepients'] = ", ".join(to_mailid)
    msgHtml = MIMEText(html, 'html')
    msgRoot.attach(msgHtml)
    #filename = "File_name_with_extension"
    #fileName=['Q2 Dump_2019-11-18.csv', 'Q2_Missing_Brand_Tag_2019-11-18.xlsx']
    if fileName is not None:
        for file in fileName:
            #print(file)
            attachment = open(str(file), "rb")
            p = MIMEBase('application', 'octet-stream')   
            # To change the payload into encoded form 
            p.set_payload((attachment).read())
            # encode into base64 
            encoders.encode_base64(p)
            # p.add_header('Content-Disposition', "attachment; filename= %s" % file[str.index(file,'-',41)+1:len(file)])
            p.add_header('Content-Disposition', "attachment; filename= %s" % file)
            msgRoot.attach(p)
            attachment.close()
    
    #msgRoot.attach(msgdf)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(from_mailid, password)
    smtp.sendmail(msgRoot['From'], msgRoot['To'].split(","),  msgRoot.as_string())
    smtp.quit()
#############################################################

def exception_html(exception=[]):
    print("Inside exception html method")
    html=""
    body = ''
    html_header = """<html>
                <head>
                </head>
                <body><h2>Data ingestion failed with below Error</h2>"""
                
    for ex in exception:
        print(ex)
        body = body + "<p>" + str(ex) + "</p>"
    html_footer = """</body>
                    </html>"""
    
    html = html_header + body + html_footer
    
    return html
