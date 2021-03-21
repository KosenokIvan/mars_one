from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import LoginForm, RegisterForm
from forms.job import JobForm

app = Flask(__name__)
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
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.team_leader.data).first():
            return render_template("job.html", title="Добавить работу",
                                   form=form, message="Тимлидер не найден")
        job = Jobs(team_leader=form.team_leader.data, job=form.title.data,
                   work_size=form.work_size.data, collaborators=form.collaborators.data,
                   is_finished=form.is_finished.data)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавить работу', form=form)


@app.route("/job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user == db_sess.query(User).filter(User.id == 1).first:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.user == current_user).first()
        if job:
            form.title.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user == db_sess.query(User).filter(User.id == 1).first:
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
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("job.html", form=form, title="Редактировать работу")


@app.errorhandler(401)
def unauthorized(error):
    return render_template("unauthorized.html", title="Нет авторизации")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
