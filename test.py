from flask import Flask, render_template
from flask import redirect
from flask import url_for
from flask import request
from model.check_login import is_existed, exist_user, is_null
from model.check_registe import add_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tom-ge-ge-ge-ge'


@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            return render_template('index.html', username=username)
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route("/regiser", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'])
            return render_template('index.html', username=username)
    return render_template('register.html')


if __name__ == "__main__":
    app.run()
