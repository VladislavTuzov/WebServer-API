import flask
from flask import request, jsonify, redirect
from pickle import loads
from flask_login import login_required, current_user
import datetime
# from werkzeug.utils import secure_filename
# from random import choice
# from string import ascii_letters
import os
import uuid
import traceback

from random import choice
from string import digits

from data.coupons import Coupon
from data.orders import Orders
from data.history import History
from data.positions import Positions
from data.users import User
from data.def_actions import CheckGoodMassage
from data.mass_act import Action__mass
from data.confirm_mail import start_massage

from forms.upload import UpLoadForm, AddCupons

from . import db_session

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)

UPLOAD_FOLDER = 'static/Image_positions'


def secure_filename(file_name):
    name = uuid.uuid4()
    return f"{name}.{file_name.split('.')[1]}"


# {'positions': [
#         ['id_positions', 'quantity'],
#         ['id_positions', 'quantity']],
#     'address': 'победа 171 кв 16',
#     'email': 'vlados.tuzov2017ass@yandex.ru'
#     'name': 'Владислав',
#     'phone': '89997911240',
#     'applied_coupons': 'id_coupons',
#     'order_note': 'домофон не работает',
#     'time_pin': 'fast or к 15:00',
#     'payment_method': 'card or cash',
#       'delivery_method': ''}


# {1:{'id_positions': 1, 'quantity': 2}, 2:{'id_positions': 1, 'quantity': 2}}

@blueprint.route('/orders/no_auth', methods=['POST'])
def order_not_auth():
    if not request.json:
        # print(1)
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['goods', 'address', 'email', 'name', 'phone', 'applied_coupons', 'order_note', 'time_pin', 'payment_method', 'execution_time', 'count', 'sum', 'delivery_method', 'scores']):
        # print(2)
        # print(request.json)
        return jsonify({'error': 'Bad request'})
    # mailing(img=request.json['img'], text=request.json['text'])
    else:
        goods = {}
        # print(request.json)
        for i in request.json['goods']:
            if i['id'] != 'action_product':
                rst = {'id': int(i['id'].split('_')[1]), 'count': i['count']}
                goods[int(request.json['goods'].index(i))] = rst
            # print(request.json['goods'].index(i))
        # print(3, goods)
        # print(request.json)
        db_sess = db_session.create_session()
        summ = 0
        for i in request.json['goods']:
            if i['id'] != 'action_product':
                position = db_sess.query(Positions).filter(
                    Positions.id == int(i['id'].split('_')[1])).first()
                # print(i['id'].split('_')[1])
                summ += int(position.price) * int(i['count'])
        if request.json['applied_coupons'] != '':
            cup = db_sess.query(Coupon).filter(
                Coupon.coupon == request.json['applied_coupons']).first()
            if cup.discount != '':
                summ *= (1 - (cup.discount * 0.01))

        if request.json['delivery_method'] == 'paid_100':
            summ += 100
        elif request.json['delivery_method'] == 'paid_150':
            summ += 150

        au = current_user.is_authenticated
        if current_user.is_authenticated:
            back_id = current_user.id
        else:
            back_id = None
        if au:
            user_scores = db_sess.query(User).filter(
                User.id == current_user.id).first()
            if request.json['scores'] <= user_scores.scores:
                scor = request.json['scores']
            else:
                return jsonify({'error': 'not enough points'})
        else:
            scor = request.json['scores']

        if au:
            print('ddddddddddddddd', request.json['scores'])
            sc = db_sess.query(User).filter(User.id == current_user.id).first()
            sc.scores_freez = scor
            sc.scores = sc.scores - scor
            db_sess.add(sc)

        summ -= scor
        if au:
            bal = db_sess.query(User).filter(
                User.id == current_user.id).first()
            bal.scores += summ // 10
            db_sess.add(bal)

        if request.json['execution_time'] == 'fast':
            orde = Orders(
                name_klient=request.json['name'],
                adress=request.json['address'],
                email=request.json['email'],
                phone_number=request.json['phone'],
                applied_coupons=request.json['applied_coupons'],
                order_note=request.json['order_note'],
                execution_speed='fast',
                payment_method=request.json['payment_method'],
                structure=goods,
                summ=summ,
                back_id=back_id,
                status=True,
                scores=scor
            )
        else:
            orde = Orders(
                name_klient=request.json['name'],
                adress=request.json['address'],
                email=request.json['email'],
                phone_number=request.json['phone'],
                applied_coupons=request.json['applied_coupons'],
                order_note=request.json['order_note'],
                execution_speed=request.json['time_pin'],
                payment_method=request.json['payment_method'],
                summ=summ,
                structure=goods,
                back_id=back_id,
                status=True,
                scores=scor
            )
        goods_mail = []
        for j in goods:
            print(j)
            name = db_sess.query(Positions).filter(
                Positions.id == goods[j]['id']).first().name
            coun = goods[j]['count']
            dr = f'Наименование: {name}, количество: {coun}'
            # i.structure[j]['id']
            goods_mail.append(dr)
        coup_pri = db_sess.query(Coupon).filter(
            Coupon.id == request.json['applied_coupons']).first()
        if coup_pri:
            coup_re = f'скидка: {coup_pri.discount}, описание: {coup_pri.description}, купон: {coup_pri.coupon}'
        else:
            coup_re = 'Купон не применён'
        # ['понедельник', 'вторник', 'среда', 'четверг', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 0, 1, 2, 3]
        today = datetime.datetime(datetime.date)
        b = today.get_weekday()
        if b in ['понедельник', 'вторник', 'среда', 'четверг', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 0, 1, 2, 3]:
            if request.json['execution_time'] == 'fast':
                mass = f'''\
                Имя: {request.json['name']}
                адресс: {request.json['address']}
                почта: {request.json['email']}
                номер телефона: {request.json['phone']}
                Применённый купон: {coup_re}
                Примечание к заказу: {request.json['order_note']}
                Время доставки: {'быстрее'}
                Способ оплаты: {request.json['payment_method']}
                сумма заказа: {summ - scor}руб
                Состав заказа: {goods_mail}
                Использование баллов: {scor}
                скидка 25% в день рождения
                    '''
            else:
                mass = f'''\
                Имя: {request.json['name']}
                адресс: {request.json['address']}
                почта: {request.json['email']}
                номер телефона: {request.json['phone']}
                Применённый купон: {coup_re}
                Примечание к заказу: {request.json['order_note']}
                Время доставки: {request.json['time_pin']}
                Способ оплаты: {request.json['payment_method']}
                сумма заказа: {summ - scor}руб
                Состав заказа: {goods_mail}
                Использование баллов: {scor}
                скидка 25% в день рождения
                '''
        zak = 'Новый заказ из RedFish'
        start_massage(massage=mass, zagolovok=zak,
                      email='redfish35che@yandex.ru')
        try:
            # print(0000)
            db_sess.add(orde)
            db_sess.commit()
            return jsonify({'good': 'orders create'})
        except Exception as e:
            # print(f'1111111111111111 ----{e}')
            return jsonify({'error': 'errore write'})


@blueprint.route('/orders/coupon_check', methods=['POST'])
def coupon_check():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['coupons']):
        return jsonify({'error': 'Bad request'})
    else:
        db_sess = db_session.create_session()
        cup = db_sess.query(Coupon).filter(
            Coupon.coupon == request.json['coupons']).first()
        if cup:
            if cup.description == None:
                if cup.discount == None:
                    ret = jsonify({'status': cup.status, 'discount': '', 'description': '', 'coup_id': f'{cup.id}'})
                else:
                    ret = jsonify({'status': cup.status, 'discount': f'{cup.discount}', 'description': '', 'coup_id': f'{cup.id}'})
            else:
                if cup.discount == None:
                    ret = jsonify({'status': cup.status, 'discount': '', 'description': f'{cup.description}', 'coup_id': f'{cup.id}'})
                else:
                    ret = jsonify({'status': cup.status, 'discount': f'{cup.discount}', 'description': f'{cup.description}', 'coup_id': f'{cup.id}'})
            if cup.status == True:
                cup.status = False
                db_sess.commit()
            return ret
        else:
            return jsonify({'error': 'coupon not found'})


@blueprint.route('/control/add-posit', methods=['POST'])
def add_postit():
    formAdd = UpLoadForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        filename = secure_filename(formAdd.image.data.filename)
        try:
            image_url = os.path.join(UPLOAD_FOLDER, filename)
            formAdd.image.data.save(image_url)
        except Exception as e:
            return e
        position = Positions(
            name=formAdd.name.data,
            photo=filename,
            price=formAdd.price.data,
            structure=formAdd.description.data,
            weight=formAdd.weight.data,
            kategory=request.form['kategori'])
        try:
            db_sess.add(position)
            db_sess.commit()
            return redirect('/admins-cont')
        except Exception as e:
            return jsonify({'error': f'{e}'})


@blueprint.route('/control/del-posit/<id>', methods=['GET'])
def del_postit(id):
    db_sess = db_session.create_session()
    try:
        dl = db_sess.query(Positions).filter(Positions.id == id).first()
        db_sess.delete(dl)
        db_sess.commit()
    except Exception as e:
        return jsonify({'error': f'{e}'})
    return redirect('/Positions')


@blueprint.route('/control/random_coup', methods=['POST'])
def rand_coup():
    db_sess = db_session.create_session()
    a = True
    while a:
        cod = ''.join(choice(digits) for i in range(6))
        if db_sess.query(Coupon).filter(Coupon.coupon == cod).first():
            a = True
        else:
            a = False
    return jsonify({'cod': cod})


@blueprint.route('/control/add-coupon', methods=['POST'])
@login_required
def add_coup():
    if current_user.roles == 'admin':
        if request.method == 'POST':
            form = AddCupons()
            db_sess = db_session.create_session()
            try:
                coupon = Coupon(
                    coupon=form.coupon.data,
                    description=form.description.data,
                    discount=form.discount.data,
                    status=1,
                    id_klient=form.id_klient.data
                )
                db_sess.add(coupon)
                db_sess.commit()
                # return jsonify({'good': 'coupon append'})
                return redirect('/Cupons')
            except Exception as e:
                return jsonify({'error': f'{e}'})


@blueprint.route('/control/del-coupon/<id>', methods=['GET'])
@login_required
def del_coup(id):
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        a = db_sess.query(Coupon).filter(Coupon.id == id).first()
        try:
            if a:
                db_sess.delete(a)
                db_sess.commit()
                return redirect('/Cupons')
            else:
                return jsonify({'error': f'not faund'})
        except Exception as e:
            return jsonify({'error': f'{e}'})


@blueprint.route('/mail/auth/<id>', methods=['GET'])
def mail_auth(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.secret_key_cokies == id).first()
    if user:
        if user.auth_mail != True:
            try:
                user.auth_mail = True
                db_sess.add(user)
                db_sess.commit()
                return 'Почта подтверждена <a href="/">на главную</a>'
            except Exception as e:
                return jsonify({'error': f'{e}'})
        else:
            return 'Почта уже подтверждена <a href="/">на главную</a>'


@blueprint.route('/mail/not_auth/<id>', methods=['GET'])
def mail_not_auth(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.secret_key_cokies == id).first()
    if user:
        if user.auth_mail != False:
            try:
                user.auth_mail = False
                db_sess.add(user)
                db_sess.commit()
                return 'Рассылка отключена <a href="/">на главную</a>'
            except Exception as e:
                return jsonify({'error': f'{e}'})
        else:
            return 'Рассылка для этой почты уже отключена <a href="/">на главную</a>'


@blueprint.route('/control/form_cont', methods=['POST'])
def control_form_cont():
    pass


# {
    # 'sps':[1, 2, 3],
    # 'pos': [1]
# }


@blueprint.route('/control/check_action', methods=['POST'])
def check_actio():
    if not request.json:
        # print(1)
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['arr']):
        # print(2)
        # print(request.json)
        return jsonify({'error': 'Bad request'})
    # mailing(img=request.json['img'], text=request.json['text'])
    else:
        db_sess = db_session.create_session()
        arrds = db_sess.query(Action__mass)
        # print(request.json['arr'])
        flag = True
        for i in arrds:
            if i.mass_el['sps'] == request.json['arr']:
                ret = db_sess.query(Positions).filter(
                    Positions.id == i.mass_el['pos'][0]).first()
                # return jsonify(ret)
                return jsonify({'name': ret.name, 'photo': f'static/Image_positions/{ret.photo}', 'price': ret.price, 'structure': ret.structure, 'weight': ret.weight, 'status': True})
        return jsonify({'status': False})


@blueprint.route('/control/del-order/<id>', methods=['GET'])
@login_required
def del_order_id(id):
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        try:
            order = db_sess.query(Orders).filter(Orders.id == id).first()
            order.status = False
            if order.back_id != None:
                scr = db_sess.query(User).filter(
                    User.id == order.back_id).first()
                scr.scores_freez = 0
                db_sess.add(scr)
            db_sess.add(order)
            db_sess.commit()
            return redirect('/orders')
        except Exception as e:
            return redirect('/orders', massage=f'При удалении произошла ошибка: {e}')


@blueprint.route('/control/pos_posit', methods=['POST'])
# @login_required
def pos_posit():
    db_sess = db_session.create_session()
    pos = db_sess.query(Positions)
    res = []
    for i in pos:
        # res[i.id] = i.name
        res.append({'id': i.id, 'name': i.name,
                    'price': int(i.price), 'photo': f'/static/Image_positions/{i.photo}', 'weight': int(i.weight)})
    return jsonify(res)


@blueprint.route('/control/add_comb_act', methods=['POST'])
# @login_required
def add_comb_act():
    if not request.json:
        # print(1)
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['sps', 'pos']):
        # print(2)
        # print(request.json)
        return jsonify({'error': 'Bad request'})
    # mailing(img=request.json['img'], text=request.json['text'])
    else:
        db_sess = db_session.create_session()
        try:
            act = Action__mass(
                mass_el=request.json)
            db_sess.add(act)
            db_sess.commit()
            return redirect('/admins-cont')
        except Exception as e:
            return jsonify({'error': e})


@blueprint.route('/control/check_scores', methods=['POST'])
def shech_scores():
    au = current_user.is_authenticated
    # au = True
    if au:
        db_sess = db_session.create_session()
        pos = db_sess.query(User).filter(User.id == current_user.id).first()
        return jsonify({'auth': au, 'scores': pos.scores})
        # return jsonify({'auth': au, 'scores': 50})
    else:
        return jsonify({'auth': au})
