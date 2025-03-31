# Importación de módulos necesarios de Flask
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
# Inicialización de la aplicación Flask
app = Flask(__name__)

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
                            sender="luisangelacu10@gmail.com", 
                            recipients=["luisangelacu10@gmail.com"])
                msg.body = f"De: {correo}\nMensaje: {mensaje}"
                mail.send(msg)
                return render_template('gracias.html')
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                return redirect("/")
        elif "button_emailno" in request.form:
            return redirect("/")

        return redirect("/")
    except KeyError:
        return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
