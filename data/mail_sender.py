import smtplib
import mimetypes
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import traceback


def send_email(login, passwor, emailse=None, text=None, zagolovok=None, photo=None, register=False):
    # print(123)
    addr_from = login
    password = passwor

    try:
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        # server.starttls()
        # server.set_debuglevel(True)
        server.login(addr_from, password)
    except Exception as e:
        print(f'При авторизации произошла ошибка {e}')

    msg = MIMEMultipart()
    msg['FROM'] = addr_from
    msg['Subject'] = zagolovok
    msg.attach(MIMEText(text, 'plain'))
    if photo != None:
        img_data = open(photo, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(photo))
        msg.attach(image)
    # msg.attach(MIMEText(text, 'html' 'utf-8'))

    if not register:
        # print(1, emailse, len(emailse))
        if len(emailse) != 1:
            for i in emailse:
                try:
                    msg['To'] = i.email
                    server.send_message(msg)
                    # print(f"{email} Удачно доставлено")
                except Exception as e:
                    print(f"{emailse} При отправке произошла ошибка {e}")
        else:
            try:
                msg['To'] = emailse[0]
                server.send_message(msg)
                # print(f"{email} Удачно доставлено")
            except Exception as e:
                print(f"{emailse[0]} При отправке произошла ошибка {e}")
        # print('рассылка завершена')
    else:
        print(2)
        try:
            msg['To'] = emailse
            server.send_message(msg)
            # print(f"{email} Удачно доставлено")
        except Exception as e:
            print(f"{emailse} При отправке произошла ошибка {e}")
    server.quit()
