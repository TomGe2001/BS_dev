from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)


# 呈现HTML模板
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 检查用户提供的登录凭据是否正确
        if request.form['username'] == 'your_username' and request.form['password'] == 'your_password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
