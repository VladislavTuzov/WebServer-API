import flask
from flask import request, jsonify
from pickle import loads

from . import db_session
from data.klass import Klass
from data.users_profile import UsersProfile

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/sheduele', methods=['POST'])
def post_shedule():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name_klass', 'shool_id', 'date']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    klass = db_sess.query(Klass).filter(
        Klass.name_klass == request.json['name_klass'] and Klass.shool_id == request.json['shool_id']).first()
    usrprf = db_sess.query(UsersProfile).filter(
        UsersProfile.id_users == klass.id).first()

    jsn = loads(usrprf.zipfiles)
    if request.json['date'] != 'all':
        ret_date = jsn[request.json['date']]
    else:
        ret_date = jsn

    # print(request.json['name_klass'],
    #       request.json['shool_id'], request.json['date'])
    return jsonify(
        {
            request.json['date']: ret_date
        })
