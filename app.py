from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from models import Cliente, ClienteDuplicadoException, DatosInvalidosException

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes"

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'andvi3006',  
    'database': 'mi_base_de_datos' 
}

def obtener_conexion():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET'])
def inicio():
    return redirect(url_for('registrar_cliente'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo')
        dni = request.form.get('dni_ruc')
        correo = request.form.get('correo')
        fecha_nac = request.form.get('fecha_nacimiento')
        
        conexion = None
        cursor = None
        
        try:
            nuevo_cliente = Cliente(nombre, dni, correo, fecha_nac)
            nuevo_cliente.validar_datos()

            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # consulta de dni para evitar duplicidad
            cursor.execute("SELECT id_cliente FROM cliente WHERE dni_ruc = %s", (nuevo_cliente.dni_ruc,))
            if cursor.fetchone():
                raise ClienteDuplicadoException("El DNI/RUC ingresado ya está registrado.")

            # Insertar
            sql = "INSERT INTO cliente (nombre_completo, dni_ruc, correo, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nuevo_cliente.nombre_completo, nuevo_cliente.dni_ruc, nuevo_cliente.correo, nuevo_cliente.fecha_nacimiento))
            conexion.commit()

            flash("¡Cliente registrado exitosamente!", "exito")
            return redirect(url_for('registrar_cliente'))

        except (DatosInvalidosException, ClienteDuplicadoException) as e:
            flash(str(e), "error")
        except Exception as ex:
            flash(f"Error en la base de datos: {str(ex)}", "error")
        
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    # --- CONSULTA DE CLIENTES ---
    lista_clientes = []
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_cliente, nombre_completo, dni_ruc, correo, fecha_nacimiento, fecha_registro FROM cliente ORDER BY id_cliente DESC")
        lista_clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
    except Exception as ex:
        flash(f"Error al obtener la lista de clientes: {str(ex)}", "error")

    # Enviar la lista de clientes a la plantilla HTML
    return render_template('registrar.html', clientes=lista_clientes)

if __name__ == '__main__':
    app.run(debug=True)
