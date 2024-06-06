from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('datos_Form.html')


@app.route('/img/<path:filename>')
def custom_static(filename):
    return send_from_directory('img', filename)


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f"<h1>Buen dia: {name} :3.</h1> \n <a href='/'>Volver</a>"


if __name__ == '__main__':
    app.run(debug=True)