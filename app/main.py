from flask import Flask, redirect, request, session, render_template, url_for,jsonify,flash
from werkzeug.utils import secure_filename
from helpers.user import *
from helpers.citas import *
from helpers.barbero import *
from helpers.servicios import *
from helpers.producto import *
from helpers.venta import *
import os



app = Flask(__name__, static_folder='static')
app.secret_key = 'tu_clave_secreta_segura'  

#-------------------------------------------------------#
#--------------Rutas de pagina de barberia--------------#
#-------------------------------------------------------#


#Ruta principal del index 
@app.route('/', methods=['GET', 'POST'])
def index():
    user = session.get('user')
    form_id = None
    barberos = select_barbers()
    productos = select_productos()


    if request.method == "POST":
        form_id = request.form.get("form_id")        
        if form_id == "loginForm":
            return login()
        elif form_id == "signupForm":
            return register()
        elif form_id == "bookingForm":
            return new_reserv()
        elif form_id == "editUserForm":
            return edit_user()

    #return render_template('index.html', user=user,barberos = barberos,paquetes = paquetes,productos = productos)
    return render_template('index.html',barberos = barberos,productos= productos,user=user)

#Ruta  de inicio de seesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password", "").strip()

        error = None

        if not email or not password:
            error = 'Todos los campos son obligatorios'
            return render_template('loginUser.html', error=error)

        user = select_user_email(email)

        if user:
            stored_password = str(user.password).strip()
            if stored_password == password:
                session['user'] = user.to_dict()
                return redirect('/')
            else:
                error = 'Correo electrónico o contraseña inválidos'
        else:
            error = 'Usuario no encontrado'

        print("Error:", error)

        return render_template('loginUser.html', error=error)

    return render_template('loginUser.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")
    email = request.form.get("correo_electronico")
    password = request.form.get("password")

    # Validación de campos vacíos (opcional pero recomendado)
    if not nombre or not telefono or not email or not password:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/registro')

    # Verificar si el usuario ya existe
    if select_user_email(email):
        flash("Este correo ya está registrado. Intenta con otro.", "danger")
        return redirect(url_for('index'))     
    
    # Registrar nuevo usuario
    new_user(nombre, telefono, email, password)

    # Obtener el usuario recién creado (puedes usar select_user_email)
    user = select_user_email(email)
    user_dict = user.to_dict()

    # Iniciar sesión
    session['user_id'] = user_dict['id']  # Asegúrate de que 'id' esté en la consulta
    session['user_name'] = user_dict['name']

    flash("Registro exitoso. ¡Bienvenido!", "success")
    return redirect(url_for('index')) 

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index')) 


@app.route('/horarios_disponibles', methods=['GET'])
def horarios_disponibles():
    barbero = request.args.get("barbero")
    fecha = request.args.get("fecha")

    if not barbero or not fecha:
        return jsonify({"error": "Faltan parámetros"}), 400

    id_barbero = select_barbero_id(barbero)

    if id_barbero is None:
        return jsonify({"error": "Barbero no encontrado"}), 404  # Evita consultas incorrectas

    horarios = obtener_horarios_disponibles(id_barbero, fecha)

    return jsonify(horarios)


#-------------------------------------------------------#
#-----------------Funciones de barberia-----------------#
#-------------------------------------------------------#

#Funcion de reservacion nueva
def new_reserv():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")
    fecha = request.form.get("fecha")
    hora = request.form.get("hora")
    barbero = request.form.get("barbero")
    servicio = request.form.get("servicio")

    # Validar si hay sesión iniciada
    user = session.get('user')
    if not user:
        flash("Por favor inicia sesión para hacer una reserva.", "danger")
        return redirect(url_for('login'))
    else:  # Asegúrate de que esta ruta exista
        user_id = user.get('id')
        barber_id = select_barbero_id(barbero)
        id_servicio = get_servicio_id(servicio)

        new_cita(barber_id, user_id, fecha, hora, id_servicio)
        flash("¡Reserva creada exitosamente!", "success")

    return redirect(url_for('index'))

#Funcion para editar valores de usuario
def edit_user():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")

    user = session.get('user')
    user_id = user.get('id')
    modify_user(user_id,nombre,telefono)

    return jsonify({
        "status":"succes",
        "message":"Modificacion de datos correcta",
        "datos": {
            "user_id":user_id,
            "nombre":nombre,
            "telefono":telefono
        }
    }),2000




#-------------------------------------------------------#
#----------------Rutas de administrador-----------------#
#-------------------------------------------------------#

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    usuario_correcto = 'admin'
    contraseña_correcta = 'admin27'

    if request.method == 'POST':
        user = request.form.get("usuario")
        password = request.form.get("contraseña", "").strip()

        if user == usuario_correcto and password == contraseña_correcta:
            session['admin'] = True  # Marcar al usuario como autenticado
            return redirect(url_for('adminManager'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('admin'))

    return render_template('loginAdmin.html')       

#Funcion principal del administrador 
@app.route('/adminManager')
def adminManager():
    if not session.get('admin'):
        return redirect(url_for('admin'))

    citas = select_citas_pendientes()
    barberos = select_barbers()
    productos = select_productos()

    return render_template('AdminManager.html', citas=citas, barberos=barberos,productos = productos)

@app.route('/barber', methods= ['GET','POST'])
def barber():

    barberos = select_barbers()

    return render_template('barberPage.html', barberos = barberos)


@app.route('/productos',methods = ['GET','POST'])
def productos():

    productos = select_productos()
    return render_template('/productos.html', productos = productos)


@app.route('/agregar_barbero', methods=['POST'])
def agregar_barbero():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    imagen = request.files['imagen']
    
    if imagen:
        filename = secure_filename(imagen.filename)
        ruta_imagen = os.path.join('static', 'imges', filename)
        
        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)
        
        imagen.save(ruta_imagen)

        # Insertar en base de datos
        insert_barbero(nombre, telefono, filename)  # solo guardamos el nombre del archivo

    return redirect(url_for('barber'))

@app.route('/reportes',methods = ['GET','POST'])
def reportes():
    ventas = select_all_ventas()

    return render_template('venta.html',ventas  = ventas)

from datetime import datetime

@app.route('/crear_venta', methods=['POST'])
def crear_venta():
    data = request.get_json()
    
    id_cita = data.get('id_cita')
    tipo_pago = data.get('tipo_pago')
    monto_final = data.get('monto_final')

    if not id_cita or not tipo_pago or monto_final is None:
        return jsonify({'error': 'Datos incompletos'}), 400

    # Insertar la venta
    insert_venta(id_cita=id_cita, tipo_pago=tipo_pago, monto_final=monto_final)

    return redirect('adminManager')



@app.route('/precio_producto', methods=['GET'])
def obtener_precio_producto():
    producto_id = request.args.get('id', type=int)
    monto_servicio = request.args.get('monto', type=float)

    # Suponemos que el nombre del producto es lo que se envía en el 'id'
    producto_nombre = request.args.get('nombre_producto', type=str)
    
    # Consulta el precio del producto usando la función de tu CRUD
    precio_producto = select_producto_precio(producto_nombre)
    
    if precio_producto is None:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    # Calcula el monto final
    monto_final = monto_servicio + precio_producto
    return jsonify({
        'precio_producto': precio_producto,
        'monto_final': round(monto_final, 2)
    })





if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5050, debug=True)
    except KeyboardInterrupt:
        session.pop('user', None)
