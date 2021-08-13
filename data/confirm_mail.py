# from dotenv import load_dotenv
from data.mail_sender import send_email
from threading import Thread
import os
# import urllib.parse

from data.users import User

from . import db_session

# load_dotenv()


def start_massage(massage='test', zagolovok='test', photo=None, register=False, email=None):
    # pass
    # mail = ['vlados.tuzov2017ass@yandex.ru']
    db_sess = db_session.create_session()

    if register:
        user = db_sess.query(User).filter(User.email == email).first()
        zagolovok = 'Вы зарегистрированы в RedFish'
        massage = f'''\
            Спасибо за регистрацию в RedFish
                подтвердите почту по ссылке http://178.64.227.74:6785/mail/auth/{user.secret_key_cokies}
                Подтверждая почты вы автоматически соглашаетесь на рассылку сообщений
                Отказаться от расылки http://178.64.227.74:6785/mail/not_auth/{user.secret_key_cokies}'''
        # massage = urllib.parse.quote(massage)
        mail = email
    else:
        if email == None:
            mail = [i.email for i in db_sess.query(
                User).filter(User.auth_mail == True)]
            # mail = db_sess.query(User).filter(User.auth_mail == True)
        else:
            mail = [email]

    # login = os.getenv("FROM")
    login = 'redfish35che@yandex.ru'
    # password = str(os.getenv("PASSWORD"))
    password = 'txesmakiesrlrunl'
    th = Thread(target=send_email, args=(
        login, password, mail, massage, zagolovok, photo, register))
    th.start()
    print('Поток запущен')
