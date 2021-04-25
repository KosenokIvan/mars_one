import json
import os
from string import ascii_letters, digits
from random import choices
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session, jobs_api, users_api, users_resource, jobs_resource
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.categories import Category
from forms.user import LoginForm, RegisterForm
from forms.job import JobForm
from forms.department import DepartmentForm
from forms.gallery import GalleryForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, surname=form.surname.data,
                    email=form.email.data, age=form.age.data,
                    position=form.position.data, speciality=form.speciality.data,
                    address=form.address.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", works_list=jobs, title="Список работ")


@app.route("/job", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobForm()
    db_sess = db_session.create_session()
    form.categories.choices = [(category.id, category.name)
                               for category in db_sess.query(Category).all()]
    if form.validate_on_submit():
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template("job.html", title="Добавить работу",
                                   form=form, message="Тимлидер не найден")
        job = Jobs(team_leader=form.team_leader.data, job=form.title.data,
                   work_size=form.work_size.data, collaborators=form.collaborators.data,
                   is_finished=form.is_finished.data,
                   categories=[db_sess.query(Category).get(category_id)
                               for category_id in form.categories.data])
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавить работу', form=form)


@app.route("/job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = JobForm()
    db_sess = db_session.create_session()
    form.categories.choices = [(category.id, category.name)
                               for category in db_sess.query(Category).all()]
    if request.method == "GET":
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.user == current_user).first()
        if job:
            form.title.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            form.categories.data = [category.id for category in job.categories]
        else:
            abort(404)
    if form.validate_on_submit():
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.user == current_user).first()
        if job:
            if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
                return render_template("job.html", title="Добавить работу",
                                       form=form, message="Тимлидер не найден")
            job.job = form.title.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            job.categories = [db_sess.query(Category).get(category_id)
                              for category_id in form.categories.data]
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("job.html", form=form, title="Редактировать работу")


@app.route("/delete_job/<int:job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.user == current_user).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/departments")
def departments_list():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("departments_list.html", departments_list=departments,
                           title="Список департаментов")


@app.route("/department", methods=["GET", "POST"])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.chief.data).first():
            return render_template("department.html", title="Добавить департамент",
                                   form=form, message="Шеф не найден")
        department = Department(
            title=form.title.data, chief=form.chief.data,
            members=form.members.data, email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавить департамент', form=form)


@app.route("/department/<int:department_id>", methods=["GET", "POST"])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == department_id).first()
        else:
            department = db_sess.query(Department).filter(Department.id == department_id,
                                                          Department.user == current_user).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == department_id).first()
        else:
            department = db_sess.query(Department).filter(Department.id == department_id,
                                                          Department.user == current_user).first()
        if department:
            if not db_sess.query(User).filter(User.id == form.chief.data).first():
                return render_template("department.html", title="Добавить департамент",
                                       form=form, message="Шеф не найден")
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("department.html", form=form, title="Редактировать департамент")


@app.route("/delete_department/<int:department_id>", methods=["GET", "POST"])
@login_required
def delete_department(department_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        department = db_sess.query(Department).filter(Department.id == department_id).first()
    else:
        department = db_sess.query(Department).filter(Department.id == department_id,
                                                      Department.user == current_user).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/departments")


@app.route("/member")
def member():
    with open("templates/members.json", "r", encoding="utf-8") as json_file:
        astronauts_list = json.load(json_file)["members"]
    return render_template("member.html", title="member", astronauts_list=astronauts_list)


@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    form = GalleryForm()
    if form.validate_on_submit():
        image = Image.open(BytesIO(form.image.data.read()))
        while True:
            filename = f"{''.join(choices(ascii_letters + digits, k=64))}.png"
            if not os.path.exists(f"static/img/mars_images/{filename}"):
                break
        image.save(f"static/img/mars_images/{filename}")
        return redirect("/gallery")
    images_list = os.listdir("static/img/mars_images")
    return render_template("gallery.html", title="Галерея с загрузкой",
                           images_list=images_list, form=form)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(render_template("unauthorized.html", title="Нет авторизации"), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(users_resource.UsersListResource, "/api/v2/users")
    api.add_resource(users_resource.UsersResource, "/api/v2/users/<int:user_id>")
    api.add_resource(jobs_resource.JobsListResource, "/api/v2/jobs")
    api.add_resource(jobs_resource.JobsResource, "/api/v2/jobs/<int:job_id>")
    app.run()


if __name__ == '__main__':
    main()
