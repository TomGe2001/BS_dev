from flask import Flask, render_template

app = Flask(__name__)

# 呈现HTML模板
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
