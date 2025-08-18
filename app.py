from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template(f'usuario/{nombre}.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
