# Importación de módulos necesarios de Flask
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class formulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Mensaje = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()
# Configuración de Flask-Mail para el envío de correos

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'luisangelacu10@gmail.com'
app.config['MAIL_PASSWORD'] = 'cphz hzdt vafn zssu'
mail = Mail(app)
# Ruta principal que renderiza la página de inicio
@app.route('/')
def index():
    """Función que maneja la ruta principal y muestra la página de inicio.
    Returns:
        template: Renderiza la plantilla index.html
    """
    return render_template('index.html')

# Ruta para procesar los botones de habilidades
@app.route('/', methods=['POST'])
def process_form():
    """Función que procesa los clicks en los botones de habilidades.
    Obtiene el estado de cada botón y renderiza la plantilla con los proyectos correspondientes.
    
    Returns:
        template: Renderiza index.html con los estados de los botones actualizados
    """
    button_python = request.form.get('button_python')
    button_discord = request.form.get('button_discord')
    button_html = request.form.get('button_html')
    button_db = request.form.get('button_db')
    return render_template('index.html', 
                        button_python=button_python, 
                        button_discord=button_discord, 
                        button_html=button_html, 
                        button_db=button_db)

# Ruta para procesar el formulario de feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    """Función que procesa el envío del formulario de comentarios.
    Recibe el correo y mensaje del usuario y los muestra en una página de resultados.
    
    Returns:
        template: Renderiza formresult.html con los datos del formulario
    """
    correo = request.form['email']
    mensaje = request.form['text']
    return render_template('formresult.html', Correo=correo, Mensaje=mensaje)
@app.route('/gracias', methods=['POST'])
def gracias():
    try:
        if "button_emailsi" in request.form:
            correo = request.form['email']
            mensaje = request.form['text']

            try:
                msg = Message("Nuevo mensaje del portafolio", 
                            sender=correo, 
                            recipients=["luisangelacu10@gmail.com"])
                msg.body = f"De: {correo}\nMensaje: {mensaje}"
                mail.send(msg)
                NuevoFormulario = formulario(Mensaje=mensaje, email=correo)
                db.session.add(NuevoFormulario)
                db.session.commit()
                return render_template('gracias.html', )
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                return redirect("/")
        elif "button_emailno" in request.form:
            return redirect("/")

        return redirect("/")
    except KeyError:
        return redirect("/")
@app.route('/mensajes')
def mensajes():
    comentarios = formulario.query.all()
    return render_template('Ver-otros-comentarios.html', comentarios=comentarios)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
