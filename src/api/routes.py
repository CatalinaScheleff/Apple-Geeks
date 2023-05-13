"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Proveedor, Categoria, Servicio, ImagenServicio
from api.utils import generate_sitemap, APIException
from flask_sqlalchemy import SQLAlchemy

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/proveedores", methods=["GET"])
def get_proveedores():
    proveedores = Proveedor.query.all()
    return jsonify([proveedor.serialize() for proveedor in proveedores])


@api.route("/proveedores/<int:id>", methods=["GET"])
def get_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    return jsonify(proveedor.serialize())


@api.route('/proveedor', methods=['POST'])
def create_proveedor():
    required_fields = ["rut", "nombre", "apellido", "region", "comuna",
                       "direccion", "telefono", "red_social", "correo", "contrasena"]

    data = request.get_json()
    print(data)
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': 'Missing fields in request body', 'missing_fields': missing_fields}), 400

    new_proveedor = Proveedor(
        rut=data['rut'],
        nombre=data['nombre'],
        apellido=data['apellido'],
        region=data['region'],
        comuna=data['comuna'],
        direccion=data['direccion'],
        correo=data['correo'],
        telefono=data['telefono'],
        red_social=data['red_social'],
        contrasena=data['contrasena']
    )

    db.session.add(new_proveedor)
    db.session.commit()

    return jsonify(new_proveedor.serialize()), 201


@api.route("/proveedores/<int:id>", methods=["PUT"])
def update_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    data = request.get_json()

    proveedor.rut = data.get("rut", proveedor.rut)
    proveedor.nombre = data.get("nombre", proveedor.nombre)
    proveedor.apellido = data.get("apellido", proveedor.apellido)
    proveedor.region = data.get("region", proveedor.region)
    proveedor.comuna = data.get("comuna", proveedor.comuna)
    proveedor.direccion = data.get("direccion", proveedor.direccion)
    proveedor.correo = data.get("correo", proveedor.correo)
    proveedor.telefono = data.get("telefono", proveedor.telefono)
    proveedor.red_social = data.get("red_social", proveedor.red_social)
    proveedor.contrasena = data.get("contrasena", proveedor.contrasena)

    db.session.commit()

    return jsonify(proveedor.serialize())


@api.route("/servicios", methods=["GET"])
def get_servicios():
    servicios = Servicio.query.all()
    return jsonify([servicio.serialize() for servicio in servicios])


@api.route("/servicios", methods=["POST"])
def create_servicio():
    data = request.get_json()

    nuevo_servicio = Servicio(
        titulo=data["titulo"],
        detalle=data["detalle"],
        precio=data["precio"],
        proveedor_id=data["proveedor_id"],
        categoria_id=data["categoria_id"],
        cobertura=data["cobertura"],
        estado=data["estado"],
    )

    db.session.add(nuevo_servicio)
    db.session.commit()

    return jsonify(nuevo_servicio.serialize()), 201


@api.route("/servicios/<int:id>", methods=["GET"])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    return jsonify(servicio.serialize())


@api.route("/servicios/<int:id>", methods=["PUT"])
def update_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    data = request.get_json()

    servicio.titulo = data.get("titulo", servicio.titulo)
    servicio.detalle = data.get("detalle", servicio.detalle)
    servicio.precio = data.get("precio", servicio.precio)
    servicio.proveedor_id = data.get("proveedor_id", servicio.proveedor_id)
    servicio.categoria_id = data.get("categoria_id", servicio.categoria_id)
    servicio.cobertura = data.get(
        "cobertura", servicio.cobertura)
    servicio.estado = data.get("estado", servicio.estado)

    db.session.commit()

    return jsonify(servicio.serialize())


@api.route("/servicios/<int:id>", methods=["DELETE"])
def delete_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    return jsonify({"message": "Servicio eliminado con éxito"}), 204


@api.route("/imagenes_servicio", methods=["GET"])
def get_imagenes_servicio():
    imagenes_servicio = ImagenServicio.query.all()
    return jsonify([imagen_servicio.serialize() for imagen_servicio in imagenes_servicio])


@api.route("/imagenes_servicio", methods=["POST"])
def create_imagen_servicio():
    data = request.get_json()

    nueva_imagen_servicio = ImagenServicio(
        ruta=data["ruta"],
        servicio_id=data["servicio_id"],
    )

    db.session.add(nueva_imagen_servicio)
    db.session.commit()

    return jsonify(nueva_imagen_servicio.serialize()), 201


@api.route("/imagenes_servicio/<int:id>", methods=["GET"])
def get_imagen_servicio(id):
    imagen_servicio = ImagenServicio.query.get_or_404(id)
    return jsonify(imagen_servicio.serialize())


@api.route("/imagenes_servicio/<int:id>", methods=["PUT"])
def update_imagen_servicio(id):
    imagen_servicio = ImagenServicio.query.get_or_404(id)
    data = request.get_json()

    imagen_servicio.ruta = data.get("ruta", imagen_servicio.ruta)
    imagen_servicio.servicio_id = data.get(
        "servicio_id", imagen_servicio.servicio_id)

    db.session.commit()

    return jsonify(imagen_servicio.serialize())


@api.route("/imagenes_servicio/<int:id>", methods=["DELETE"])
def delete_imagen_servicio(id):
    imagen_servicio = ImagenServicio.query.get_or_404(id)
    db.session.delete(imagen_servicio)
    db.session.commit()
    return jsonify({"message": "Imagen de servicio eliminada con éxito"}), 204


@api.route("/categorias", methods=["GET"])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([categoria.serialize() for categoria in categorias])


@api.route("/categorias", methods=["POST"])
def create_categoria():
    data = request.get_json()

    nueva_categoria = Categoria(
        nombre=data["nombre"]
    )

    db.session.add(nueva_categoria)
    db.session.commit()

    return jsonify(nueva_categoria.serialize()), 201


@api.route("/categorias/<int:id>", methods=["GET"])
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return jsonify(categoria.serialize())


@api.route("/categorias/<int:id>", methods=["PUT"])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.get_json()

    categoria.nombre = data.get("nombre", categoria.nombre)

    db.session.commit()

    return jsonify(categoria.serialize())


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    print(correo)
    print(contrasena)

    if not correo or not contrasena:
        return jsonify({'message': 'Correo y contraseña requeridos'}), 400

    proveedor = Proveedor.query.filter_by(correo=correo).first()

    if not proveedor:
        return jsonify({'message': 'Proveedor no encontrado'}), 404

    if proveedor.contrasena != contrasena:  # Compara la contraseña ingresada con la almacenada en la base de datos
        return jsonify({'message': 'Contraseña incorrecta'}), 401

    return jsonify({'message': 'Inicio de sesión exitoso'}), 200


@api.route('/sendPasswordResetEmail', methods=['POST'])
def send_password_reset_email():
    email = request.json['email']

    # Aquí deberías agregar la lógica para generar un token de recuperación de contraseña y guardarlo en tu base de datos

    msg = Message('Recuperación de contraseña',
                  sender='tu_correo@gmail.com', recipients=[email])
    msg.body = 'Aquí está tu enlace para restablecer tu contraseña: https://www.example.com/reset-password?token=tu_token'

    try:
        mail.send(msg)
        return jsonify(message='Correo electrónico de recuperación de contraseña enviado'), 200
    except Exception as e:
        print(str(e))
        return jsonify(message='Error al enviar el correo electrónico de recuperación de contraseña'), 500
