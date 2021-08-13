from flask import Flask, render_template, redirect, make_response, request
# from flask_socketio import send, emit
# from flask_socketio import SocketIO

from sqlalchemy import asc, desc

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from flask_cors import CORS

import os
import uuid
from flask import send_from_directory
from random import choice
from string import digits

from forms.users import RegisterForm, LoginForm
from forms.upload import UpLoadForm
from forms.upload import AddCupons
from data.users import User
from data.positions import Positions
from data.coupons import Coupon
from data.orders import Orders
from data.history import History
from data.main_info_site import MainInfo
from data.kategory import Kategory
from data.def_actions import CheckGoodMassage
from data.confirm_mail import start_massage

from data import db_session, bluepr
from data.bluepr import secure_filename
# from data.db_session import SqlAlchemyBase

application = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(application)
application.config['SECRET_KEY'] = 'KFend932y*#rjndfs322wdsfs'
application.config['UPLOAD_FOLDER'] = 'static/Image_positions'
application.config['MAIN_EMAIL'] = 'redfish35che@yandex.ru'

# CORS(app)
# socketio = SocketIO(app)
# cors = CORS(resources={
#     r"/*": {"origins": "http://178.57.98.87"}
# })


# @socketio.on('json')
# def handle_json(json):
#     print(json)
#     jso = {'name': 'lol'}
#     send(jso, json=True)


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/db_kafe.db")
    application.register_blueprint(bluepr.blueprint)
    # app.run(debug=True, port='6784', threaded=True)
    # socketio.run(app)
    application.run(debug=True, host='0.0.0.0', port='6784', threaded=True)


@application.route('/admins-cont')
@login_required
def admins():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        user = db_sess.query(User).count()
        zakaz = db_sess.query(Orders).count()
        return render_template('admin.html', user=user, zakaz=zakaz)
    else:
        return redirect('/')


@application.route('/list-user')
@login_required
def list_user():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        user = db_sess.query(User)
        return render_template('list_user.html', user=user)
    else:
        return redirect('/')


@application.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico')


@application.route("/")
def index():
    db_sess = db_session.create_session()
    positions = db_sess.query(Positions)
    return render_template('index.html', positions=positions)


@application.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # res = make_response("Setting a cookie")
            # res.set_cookie('key_sekr_aut', f'{user.secret_key_cokies}', max_age=60 * 60 * 24 * 31)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        secret_key_cokies = f'{uuid.uuid4()}'
        user = User(
            name=form.name.data,
            email=form.email.data,
            roles='klient',
            secret_key_cokies=secret_key_cokies,
            auth_mail=False,
            scores=0,
            scores_freez=0
        )
        user.set_password(form.password.data)
        user.set_personal_code()
        try:
            db_sess.add(user)
            db_sess.commit()
        except Exception as e:
            return jsonify({'errore': e})
        utr = db_sess.query(User).filter(User.email == form.email.data).first()
        a = True
        while a:
            cod = ''.join(choice(digits) for i in range(6))
            if db_sess.query(Coupon).filter(Coupon.coupon == cod).first():
                a = True
            else:
                a = False
        coupon = Coupon(
            coupon=cod,
            discount=10,
            status=1,
            id_klient=utr.id
        )
        try:
            db_sess.add(coupon)
            db_sess.commit()
        except Exception as e:
            return jsonify({'errore': e})
        start_massage(register=True, email=form.email.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@application.route('/personal-area')
@login_required
def personal_area():
    db_sess = db_session.create_session()
    pes_cod = db_sess.query(Coupon).filter(Coupon.id_klient == current_user.id)
    scores = db_sess.query(User).filter(
        User.id == current_user.id).first().scores
    return render_template('personal_area.html', pes_cod=pes_cod, scores=scores)


# корзина заказов
@application.route('/basket')
def basket():
    return render_template('basket.html')


# Добавление позиций для заказов
@application.route('/Positions')
@login_required
def addPositions():
    if current_user.roles == 'admin':
        FormAddPos = UpLoadForm()
        db_sess = db_session.create_session()
        kateg = db_sess.query(Kategory)
        posit = db_sess.query(Positions)
        return render_template('addPositions.html', formAdd=FormAddPos, kateg=kateg, formdel=posit)
    else:
        return redirect('/')


# Добавление купонов
@application.route('/Cupons')
@login_required
def addCupons():
    if current_user.roles == 'admin':
        form = AddCupons()
        db_sess = db_session.create_session()
        coup = db_sess.query(Coupon)
        return render_template('addCupons.html', form=form, coup=coup)
    else:
        return redirect('/')


# истории заказов клиентов
@application.route('/historyOreders')
@login_required
def historyOreders():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        orders = db_sess.query(Orders).order_by(desc('id'))
        res_orders = []
        for i in orders:
            # name = db_sess.query(Orders).filter(Orders.id==)
            d = {}
            d['id'] = i.id
            d['name_klient'] = i.name_klient
            d['adress'] = i.adress
            d['email'] = i.email
            d['phone_number'] = i.phone_number
            d['times_orders'] = i.times_orders
            d['applied_coupons'] = i.applied_coupons
            d['order_note'] = i.order_note
            d['execution_speed'] = i.execution_speed
            d['payment_method'] = i.payment_method
            d['back_id'] = i.back_id
            d['summ'] = i.summ
            d['status'] = i.status
            d['structure'] = []
            for j in i.structure:
                name = db_sess.query(Positions).filter(
                    Positions.id == i.structure[j]['id']).first().name
                coun = i.structure[j]['count']
                dr = f'Наименование: {name}, количество: {coun}'
                # i.structure[j]['id']
                d['structure'].append(dr)
            res_orders.append(d)
        return render_template('historyOreders.html', orders=res_orders)
    else:
        return redirect('/')


@application.route('/historyOredersCrope/<id>')
@login_required
def historyOredersCrope(id):
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        orders = db_sess.query(Orders).filter(Orders.id == id).first()
        return render_template('historyOredersCrope.html', orders=orders)
    else:
        return redirect('/')


# история заказов клиента
@application.route('/history')
@login_required
def history():
    return render_template('history.html')


# заказы которые отображаются на кухне
@application.route('/orders')
@login_required
def orders_klients():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        orders = db_sess.query(Orders).order_by(
            desc('id')).filter(Orders.status == True)
        res_orders = []
        for i in orders:
            # name = db_sess.query(Orders).filter(Orders.id==)
            d = {}
            d['id'] = i.id
            d['name_klient'] = i.name_klient
            d['adress'] = i.adress
            d['email'] = i.email
            d['phone_number'] = i.phone_number
            d['times_orders'] = i.times_orders
            d['applied_coupons'] = i.applied_coupons
            d['order_note'] = i.order_note
            d['execution_speed'] = i.execution_speed
            d['payment_method'] = i.payment_method
            d['back_id'] = i.back_id
            d['summ'] = i.summ
            d['status'] = i.status
            d['scores'] = i.scores
            d['structure'] = []
            for j in i.structure:
                name = db_sess.query(Positions).filter(
                    Positions.id == i.structure[j]['id']).first().name
                coun = i.structure[j]['count']
                dr = f'Наименование: {name}, количество: {coun}'
                # i.structure[j]['id']
                d['structure'].append(dr)
            res_orders.append(d)
        return render_template('orders_klients.html', orders=res_orders)
    else:
        return redirect('/')


@application.route('/combin_act')
@login_required
def combin_act():
    if current_user.roles == 'admin':
        return render_template('combin_act.html')
    else:
        return redirect('/')


@application.route('/control', methods=['POST', 'GET'])
def control():
    if request.method == 'POST':
        # print('==============================')
        file = request.files['file']
        if file:
            if file.filename.split('.')[1] in ['jpg', 'png', 'jpeg']:
                try:
                    filenames = secure_filename(file.filename)
                    image_url = os.path.join('static/form_photos', filenames)
                    file.save(image_url)
                except Exception as e:
                    return render_template('control.html', message=f'{e}')
                    # return jsonify({'error': f'{e}'})
            else:
                print('данный тип файла не подходит')
                return render_template('control.html', message='данный тип файла не подходит')
        else:
            print('Файла нет')

        thems = request.form['thems']
        name = request.form['name']
        tel = request.form['tel']
        massage = request.form['massage']
        zak = 'Новое сообщение со страницы контроль качества'
        mass = f'''\
        Имя: {name}
        Телефон: {tel}
        Тема: {thems}
        Сообщение: {massage}'''
        check_good_massage = CheckGoodMassage()
        if file:
            if check_good_massage.check_good_massage(massage):
                start_massage(massage=mass, zagolovok=zak,
                              photo=image_url, email=application.config['MAIN_EMAIL'])
            else:
                return render_template('control.html', message="в вашем сообщении обнаружены не цензурные высказывания, убедительная прозьба писать без цензурных высказываний")
        else:
            if check_good_massage.check_good_massage(massage):
                start_massage(massage=mass, zagolovok=zak,
                              email=application.config['MAIN_EMAIL'])
            else:
                return render_template('control.html', message="в вашем сообщении обнаружены не цензурные высказывания, убедительная прозьба писать без цензурных высказываний")
        # print(app.config['MAIN_EMAIL'], '+++++++')
        return redirect('/control')
    else:
        return render_template('control.html')


@application.route('/job', methods=['POST', 'GET'])
def jobs():
    if request.method == 'POST':
        position = request.form['position']
        name = request.form['name']
        big_name = request.form['big_name']
        marital_status = request.form['marital_status']
        age = request.form['age']
        children = request.form['children']
        experience = request.form['experience']
        tel = request.form['tel']
        # massage = request.form['massage']
        zak = 'Новый отзыв на вакансию'
        mass = f'''\
        Должность: {position}
        Имя: {name}
        Фамилия: {big_name}
        Семейное положение: {marital_status}
        Возраст: {age}
        Дети: {children}
        Опыт: {experience}
        Телефон: {tel}'''
        check_good_massage = CheckGoodMassage()
        if check_good_massage.check_good_massage(massage):
            start_massage(massage=mass, zagolovok=zak,
                          email=application.config['MAIN_EMAIL'])
        else:
            return render_template('job.html', message="в вашем сообщении обнаружены не цензурные высказывания, убедительная прозьба писать без цензурных высказываний")
        # print(app.config['MAIN_EMAIL'], '+++++++')
        return redirect('/job')
    else:
        return render_template('job.html')


@application.route('/contacts', methods=['POST', 'GET'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        tel = request.form['tel']
        massage = request.form['massage']
        # massage = request.form['massage']
        zak = 'Новый запрос на связь с нами'
        mass = f'''\
        Имя: {name}
        Телефон: {tel}
        Почта: {mail}
        Сообщение: {massage}'''
        check_good_massage = CheckGoodMassage()
        if check_good_massage.check_good_massage(massage):
            start_massage(massage=mass, zagolovok=zak,
                          email=application.config['MAIN_EMAIL'])
        else:
            return render_template('contacts.html', message="в вашем сообщении обнаружены не цензурные высказывания, убедительная прозьба писать без цензурных высказываний")
        # print(app.config['MAIN_EMAIL'], '+++++++')
        return redirect('/contacts')
    else:
        return render_template('contacts.html')


@application.route('/kategor/<id>')
def kategor(id):
    db_sess = db_session.create_session()
    # if id != 2 or id !=3 or id != 4:
    name_kateg = db_sess.query(Kategory).filter(Kategory.id == int(id)).first()
    positions = db_sess.query(Positions).filter(Positions.kategory == int(id))
    return render_template('kategory.html', name_kateg=name_kateg, positions=positions)
    # else:
    # pass


@application.route('/delivery')
def delivery():
    return render_template('delivery.html')


@application.route('/specials')
def specials():
    return render_template('specials.html')


@application.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@application.route('/order')
def order():
    return render_template('order.html')


@application.route('/tankyou')
def tankyou():
    return render_template('tankyou.html')


# if __name__ == "__main__":
main()

# db_session.global_init("db/db_kafe.db")
# app.register_blueprint(bluepr.blueprint)
# app.run()
