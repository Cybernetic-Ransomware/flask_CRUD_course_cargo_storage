from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Bigga doopa and my choppa!</h1>'


@app.route('/about/<marine_id>')
def about_page(marine_id):
    return f'<h1>Brother {marine_id}! Avenge me!</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=80)
