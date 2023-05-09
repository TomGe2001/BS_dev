from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
import pymysql
from model.check_login import is_null, is_existed, exist_user
from model.check_registe import add_user
from myClass.loginForm import LoginForm
from myClass.registrationForm import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bs_db'

db = SQLAlchemy(app)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jump_in')
def jump_in():
    return render_template('jump_in.html')


# old_version login
# @app.route('/user_login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':  # 注册发送的请求为POST请求
#         username = request.form['username']
#         password = request.form['password']
#         if is_null(username, password):
#             login_massage = "温馨提示：账号和密码是必填"
#             return render_template('test_templates/login.html', message=login_massage)
#         elif is_existed(username, password):
#             return render_template('index.html', username=username)
#         elif exist_user(username):
#             login_massage = "温馨提示：密码错误，请输入正确密码"
#             return render_template('test_templates/login.html', message=login_massage)
#         else:
#             login_massage = "温馨提示：不存在该用户，请先注册"
#             return render_template('test_templates/login.html', message=login_massage)
#     return render_template('test_templates/login.html')


# old version register
# @app.route("/regiser", methods=["GET", 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if is_null(username, password):
#             login_massage = "温馨提示：账号和密码是必填"
#             return render_template('test_templates/register.html', message=login_massage)
#         elif exist_user(username):
#             login_massage = "温馨提示：用户已存在，请直接登录"
#             # return redirect(url_for('user_login'))
#             return render_template('test_templates/register.html', message=login_massage)
#         else:
#             add_user(request.form['username'], request.form['password'])
#             return render_template('index.html', username=username)
#     return render_template('test_templates/register.html')//

# new version register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Username already taken. Please choose another one.')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash('Email address already in use. Please try another one.')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# new version login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email address or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
