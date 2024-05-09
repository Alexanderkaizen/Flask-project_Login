from flask import Flask, render_template ,request, jsonify, url_for, redirect
import sqlite3

app = Flask(__name__)

# Función para conectarse a la base de datos
def connect_db():
    conn = sqlite3.connect('app/static/db/appDB.db')
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
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY,
        nombre_admin TEXT,
        contraseña_admin TEXT
    )      
                   ''')
    
    
    conn.commit()
    conn.close()
    
    



@app.route("/") #Formulario para acceder al login y registro
def index():
    return render_template("admin.html")

@app.route('/admin', methods=['POST']) 
def admin():
    if request.method == 'POST':    
        nombre = request.form['name_admin']
        contraseña = request.form['password_admin']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE nombre_admin = ? AND contraseña_admin = ?', (nombre, contraseña))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect(url_for('mostrar_formulario_login'))
        else:
           return redirect(url_for('index', error='Credenciales incorrectas'))
       

    
    
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
        cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?', (nombre, contraseña))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect(url_for('exito'))
        else:
           
           return redirect(url_for('mostrar_formulario_login', error='Credenciales incorrectas'))





@app.route('/register') #Registor
def mostrar_formulario_registro():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def agregar_registro():
    if request.method == 'POST':
        nombre = request.form['fullname']
        email = request.form['email']
        contraseña = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
        validacion1 = cursor.fetchone()
        
        if validacion1:
            return redirect(url_for("mostrar_formulario_registro", error= "Este nombre ya esta registrado"))
        else:
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            validacion2 = cursor.fetchone()
            if validacion2:
                return redirect(url_for("mostrar_formulario_registro", error= "Este email ya esta registrado"))
            else:
                cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND email = ? AND contraseña = ?", (nombre, email, contraseña))
                validacion3 = cursor.fetchone()
                if validacion3:
                    return redirect(url_for("mostrar_formulario_registro", error= "Esta cuenta ya se encuentra"))

                else:
                    cursor.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES (?,?,?)", [nombre, email, contraseña])
                    conn.commit()
                    conn.close()           
                    return redirect(url_for('mostrar_formulario_login'))





        
@app.route('/exito')
def exito():
    return 'Inicio de sesión exitoso'


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
