from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from pickle import loads, dumps
import json
import uuid
# import base64
import os

# from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from forms.addschools import AddSchoolsForm, AddKlass
from forms.upload import UploadAvatar
from data.users import User
from data.inquiry import Inquiry
from data.klass import Klass
from data.director import Director
from data.schools import Schools
from data.student import Student
from data.users_profile import UsersProfile
from data.homework import Homework

from data import db_session, news_api

# роли пользователей:
# 1) admin
# 2) director
# 3) student
# 4) guest - простой пользователь, который может запросить получение прав директора

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
UPLOAD_FOLDER = 'static/user_folder'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SECRET_KEY'] = ':d;SFDFjeF32-=36nsvcD654W'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024


class File_manag:
    def read(self, id):
        db_sess = db_session.create_session()
        file = db_sess.query(UsersProfile).filter(
            UsersProfile.id == id).first()
        json_edit = loads(file.zipfiles)
        return json_edit

    def save(self, id, event={}):
        db_sess = db_session.create_session()
        usersprofile = UsersProfile(
            id_users=id,
            zipfiles=dumps(event)
        )
        db_sess.add(usersprofile)
        db_sess.commit()

    def edit(self, id, new):
        db_sess = db_session.create_session()
        f = db_sess.query(UsersProfile).filter(
            UsersProfile.id_users == id).first()
        f.zipfiles = dumps(new)
        db_sess.commit()
        print(f.zipfiles)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.run(debug=True)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    schools = db_sess.query(Schools)
    directors = db_sess.query(User)
    return render_template("index.html", schools=schools)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            apprentice=form.apprentice.data,
            patronymic=form.patronymic.data,
            email=form.email.data,
            roles='guest'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile')
@login_required
def profile():
    if current_user.roles == 'admin':
        return render_template('profile_admin.html')
    elif current_user.roles == 'director':
        db_sess = db_session.create_session()
        school = db_sess.query(Schools).filter(
            Schools.director == current_user.id).first()
        print(school.name_schools)
        return render_template('profile_director.html', school=school)
    elif current_user.roles == 'student':
        db_sess = db_session.create_session()
        student = db_sess.query(Student).filter(
            Student.id == current_user.id).first()
        return render_template('profile_student.html', student=student)
    elif current_user.roles == 'guest':
        return render_template('profile.html')


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.roles == 'director' or current_user.roles == 'student':
        if request.method == 'POST':
            file = request.files['file']
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.id == current_user.id).first()
            if not user.photo:
                user.photo = str(uuid.uuid4())
            db_sess.commit()

            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(
                User.id == current_user.id).first()
            if os.path.exists(f"{UPLOAD_FOLDER}/{user.photo}"):
                file.save(os.path.join(f"{UPLOAD_FOLDER}/{user.photo}", 'profile_image.jpg'))
            else:
                print('create folder', user.photo)
                os.mkdir(f"{UPLOAD_FOLDER}/{user.photo}")
                file.save(os.path.join(f"{UPLOAD_FOLDER}/{user.photo}", 'profile_image.jpg'))

        return render_template('edit_profile_director.html')


@app.route('/add-director')
@login_required
def add_director():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        inquiry = db_sess.query(Inquiry).all()
        user_list = []
        for i in inquiry:
            user_list.append(i.user_id)
        users = db_sess.query(User).filter(User.id.in_(user_list))
        return render_template('add-director.html', inquiry=users)
    else:
        return render_template('authorization_error.html')


@app.route('/del-director')
@login_required
def del_director():
    if current_user.roles == 'admin':
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.roles == 'director')
        return render_template('del-director.html', inquiry=users)
    else:
        return render_template('authorization_error.html')


@app.route('/iniquary', methods=['GET', 'POST'])
@login_required
def iniquary():
    if current_user.roles == 'guest':
        db_sess = db_session.create_session()
        user = db_sess.query(Inquiry).filter(
            Inquiry.id == current_user.id).first()
        if not user:
            form = AddSchoolsForm()
            if form.validate_on_submit():
                db_sess = db_session.create_session()
                inquiry = Inquiry(
                    name_school=form.name.data,
                    id=int(current_user.id),
                    user_id=int(current_user.id)
                )
                db_sess.add(inquiry)
                db_sess.commit()
                return redirect('/profile')
            return render_template('iniquary.html', form=form)
        else:
            return redirect('/profile')


@app.route('/control-director/<int:id>/<act>')
@login_required
def control_director(id, act):
    if act == 'add':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        user.roles = 'director'
        db_sess.commit()
        inquiry = db_sess.query(Inquiry).filter(Inquiry.id == id).first()
        school = db_sess.query(Schools).filter(
            Schools.name_schools == inquiry.name_school).first()
        if school:
            school.director = id
        else:
            school = Schools(
                name_schools=inquiry.name_school,
                director=id
            )
            db_sess.add(school)
        db_sess.commit()
        school_id = db_sess.query(Schools).filter(
            Schools.director == id).first()
        director = Director(
            id_dir=id,
            school_id=school_id.id
        )
        db_sess.add(director)
        db_sess.commit()
        try:
            db_sess.delete(inquiry)
            db_sess.commit()
        except:
            print('error delete inquiry')
        return redirect('/add-director')
    elif act == 'del':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        user.roles = 'guest'
        db_sess.commit()
        return redirect('/del-director')


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.roles == 'director':
        db_sess = db_session.create_session()

        schoo_id = db_sess.query(Schools).filter(
            Schools.director == current_user.id).first()

        klass = db_sess.query(Klass).filter(Klass.shool_id == schoo_id.id)

        if request.method == 'POST':
            klas = request.form['klass']
            id_st = request.form['id']
            std = db_sess.query(Student).filter(
                Student.id == id_st).first()
            user = db_sess.query(User).filter(User.id == id_st).first()
            if not std and user:
                klass_id = db_sess.query(Klass).filter(
                    Klass.shool_id == schoo_id.id and name_klass == klas).first()
                student = Student(
                    id=id_st,
                    school_id=schoo_id.id,
                    klass_id=klass_id.id,
                    name_klass=klas
                )
                db_sess.add(student)
                user.roles = 'student'
                db_sess.commit()
            else:
                return render_template('add-student.html', message='Такой ученик уже добавлен или такого пользователя не существует', klass=klass)
        return render_template('add-student.html', klass=klass)
    else:
        return render_template('authorization_error.html')


@app.route('/add-klass', methods=['GET', 'POST'])
@login_required
def add_klass():
    if current_user.roles == 'director':
        form = AddKlass()
        if form.validate_on_submit():
            ranom_id = uuid.uuid4()
            db_sess = db_session.create_session()
            id_shool = db_sess.query(Schools).filter(
                Schools.director == current_user.id).first()
            klass = Klass(
                name_klass=form.name.data,
                shool_id=id_shool.id,
                schedule_url=f"{ranom_id}"
            )
            db_sess.add(klass)
            db_sess.commit()
            id_klass = db_sess.query(Klass).filter(
                Klass.schedule_url == f"{ranom_id}").first()
            file_manag = File_manag()
            file_manag.save(id=id_klass.id)
            return redirect('/profile')
        return render_template('add-klass.html', form=form)
    else:
        return render_template('authorization_error.html')


@app.route("/school/<int:id>")
@login_required
def school_info(id):
    db_sess = db_session.create_session()
    school = db_sess.query(Schools).filter(Schools.id == id).first()
    director = db_sess.query(User).filter(User.id == school.director).first()
    klass = db_sess.query(Klass).filter(Klass.shool_id == id)
    # print(klass[0].name_klass)
    return render_template("school.html", school=school, director=director, klass=klass)


@app.route("/request-schedule", methods=['GET', 'POST'])
@login_required
def request_schedule():
    if current_user.roles == 'director':
        if request.method == 'POST':
            s = request.get_json()[0]
            db_sess = db_session.create_session()
            schoo_id = db_sess.query(Schools).filter(
                Schools.director == current_user.id).first()

            klass = db_sess.query(Klass).filter(
                Klass.shool_id == schoo_id.id and Klass.name_klass == request.get_json()[0]['klass']).first()

            usersprofile = db_sess.query(UsersProfile).filter(
                UsersProfile.id_users == klass.id).first()

            ss = loads(usersprofile.zipfiles)
            if s['date'] not in ss:
                print('расписание добавлено')
                ss[s['date']] = s['changes']
            else:
                print('расписание изменено')
                ss[s['date']] = s['changes']
            s_save = dumps(ss)
            usersprofile.zipfiles = s_save
            db_sess.commit()
            # print(request.get_json())
            return redirect('/edit-schedule')


@app.route("/edit-schedule", methods=['GET', 'POST'])
@login_required
def edit_schedule():
    if current_user.roles == 'director':

        db_sess = db_session.create_session()
        schoo_id = db_sess.query(Schools).filter(
            Schools.director == current_user.id).first()

        klass = db_sess.query(Klass).filter(Klass.shool_id == schoo_id.id)

        if request.method == 'POST':
            klass = db_sess.query(Klass).filter(
                Klass.shool_id == schoo_id.id and Klass.name_klass == request.get_json()['klass']).first()

            usersprofile = db_sess.query(UsersProfile).filter(
                UsersProfile.id_users == klass.id).first()
            ss = loads(usersprofile.zipfiles)

            d = request.get_json()['date']
            # print(ss)
            if d in ss:
                print(ss, 'in')
                return ss
            else:
                print('not in')
                return {}
        return render_template("edit-schedule.html", klass=klass)
    else:
        return render_template("authorization_error.html")


@app.route("/homework")
@login_required
def students_homework():
    return render_template("homework.html")


@app.route("/schedule", methods=['GET', 'POST'])
@login_required
def stundents_schedule():
    if current_user.roles == 'director':
        db_sess = db_session.create_session()

        schoo_id = db_sess.query(Schools).filter(
            Schools.director == current_user.id).first()

        klass = db_sess.query(Klass).filter(Klass.shool_id == schoo_id.id)
        if request.method == 'POST':
            klass_s = db_sess.query(Klass).filter(
                Klass.shool_id == schoo_id.id and Klass.name_klass == request.get_json()['klass']).first()
            # print(klass_s.id, schoo_id.id)
            usersprofile = db_sess.query(UsersProfile).filter(
                UsersProfile.id_users == klass_s.id).first()
            ss = loads(usersprofile.zipfiles)
            # print(ss)

            return ss
        return render_template("schedule.html", klass=klass)
    elif current_user.roles == 'student':
        db_sess = db_session.create_session()
        if request.method == 'POST':
            student = db_sess.query(Student).filter(
                Student.id == current_user.id).first()
            # print(student.klass_id)
            usersprofile = db_sess.query(UsersProfile).filter(
                UsersProfile.id_users == student.klass_id).first()
            ss = loads(usersprofile.zipfiles)
            # print(ss)
            return ss
        return render_template("shedule_student.html")


@app.route("/api/documentation")
def api_documentation():
    return render_template("api_documentation.html")


# @app.route('/class-list', methods=['GET', 'POST'])
# @login_required
# def class_list():
#     if request.method == 'POST':
#         db_sess = db_session.create_session()
#         schoo_id = db_sess.query(Schools).filter(
#                 Schools.director == current_user.id).first()
#         student = db_sess.query(Student).filter(
#                     Student.school_id == schoo_id.id and Student.name_klass == request.get_json()['klass'])
#         s = []
#         for i in student:
#             s.append(i.id)
#     return render_template('class_list.html')


if __name__ == '__main__':
    main()
