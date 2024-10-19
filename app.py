from flask import Flask, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'TUki777'  # Necesario para las sesiones

# Configuración de tu servidor de correo
EMAIL_ADDRESS = 'matriculas732@gmail.com'  # Tu correo
EMAIL_PASSWORD = 'qxff wkfi vtof xeop'  # Tu contraseña

# Simulando un usuario administrador para propósitos de ejemplo
ADMIN_USERNAME = 'WASON777'
ADMIN_PASSWORD = 'TUKI7776854'  # Cambia esto por una contraseña segura

def enviar_correo(destinatario):
    print(f"Enviando correo a: {destinatario}")  # Verifica el destinatario
    subject = "Confirmación de Matrícula"
    body = "¡Gracias por matricularte! Tu matrícula ha sido confirmada para el Instituto Tecnico Danlí."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario

    # Configuración del servidor SMTP
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()  # Iniciar TLS
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Inicia sesión con tus credenciales
        smtp.send_message(msg)  # Enviar el mensaje
        print("Correo enviado exitosamente.")  # Mensaje de éxito
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")  # Captura el error
    finally:
        smtp.quit()  # Cerrar la conexión SMTP

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matricula', methods=['GET', 'POST'])
def matricula():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        grado = request.form['grado']
        Nombre_del_Encargado = request.form['Nombre_del_Encargado']
        carrera = request.form['carrera']
        email = request.form['email']  # Agregar el campo de correo
        Numero_de_identidad = request.form['Numero_de_identidad']
        
        print(f"Datos recibidos: {nombre}, {telefono}, {grado}, {Nombre_del_Encargado}, {carrera}, {email}, {Numero_de_identidad}")  # Agrega esto

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO matriculas (nombre, Numero_de_identidad, telefono, grado, Nombre_del_Encargado, carrera, email) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (nombre, Numero_de_identidad, telefono, grado, Nombre_del_Encargado, carrera, email))
        connection.commit()
        cursor.close()
        connection.close()

        # Enviar el correo de confirmación
        print("Intentando enviar el correo...")  # Agrega esto
        enviar_correo(email)

        return redirect(url_for('index'))

    return render_template('matricula.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Guardar la sesión
            return redirect(url_for('ver_matriculados'))
        else:
            return "Credenciales incorrectas"

    return render_template('login.html')

@app.route('/ver_matriculados')
def ver_matriculados():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirigir si no está autenticado

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM matriculas")
    matriculados = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('ver_matriculados.html', matriculados=matriculados)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Cerrar sesión
    return redirect(url_for('index'))

@app.route('/historia')
def historia():
    return render_template('historia.html')

if __name__ == '__main__':
    app.run(debug=True)
