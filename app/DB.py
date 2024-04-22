from flask import Flask, render_template ,request, jsonify, url_for, redirect
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos
def connect_db():
    conn = sqlite3.connect('static/db/appDB.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función para crear la base de datos
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT,
                        email TEXT,
                        contraseña TEXT
                    )''')
    conn.commit()
    conn.close()

# Ruta para mostrar el formulario de registro
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register')
def mostrar_formulario_registro():
    return render_template('registro.html')

# Función para enviar el registro a la base de datos
@app.route('/registro', methods=['POST'])
def agregar_registro():
    if request.method == 'POST':
        nombre = request.form['fullname']
        email = request.form['email']
        contraseña = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO usuarios (nombre, email, contraseña) 
                        VALUES (?, ?, ?)''', (nombre, email, contraseña))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': 'Registro agregado exitosamente'}), 201
    
    
# Ruta para mostrar el formulario de login
@app.route('/acceso')
def mostrar_formulario_login():
    return render_template('login.html')

# Función para logiarte
@app.route('/login', methods=['POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre = request.form['fullname']
        contraseña = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?''', (nombre, contraseña))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect(url_for('exito'))
        else:
            return redirect(url_for('mostrar_formulario_login', error='Nombre de usuario o contraseña incorrectos'))
@app.route('/exito')
def exito():
    return 'Inicio de sesión exitoso'


if __name__ == '__main__':
    create_table()
    app.run(debug=True, port=5000)

