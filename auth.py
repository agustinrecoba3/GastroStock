from src.models.user import db, User
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'El usuario ya existe'}), 409
    
    # Crear nuevo usuario
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        negocio_id=data['negocio_id'],
        nombre=data['nombre'],
        email=data['email'],
        password=hashed_password,
        rol=data['rol'],
        activo=True
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario registrado correctamente'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401
    
    if not user.activo:
        return jsonify({'message': 'Usuario inactivo'}), 403
    
    # Actualizar último acceso
    user.ultimo_acceso = datetime.datetime.utcnow()
    db.session.commit()
    
    # Generar token
    token = jwt.encode({
        'user_id': user.id,
        'negocio_id': user.negocio_id,
        'rol': user.rol,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT'), algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'nombre': user.nombre,
            'email': user.email,
            'rol': user.rol,
            'negocio_id': user.negocio_id
        }
    }), 200

# Decorador para verificar token
def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401
        
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT'), algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token inválido'}), 401
        
        if not current_user.activo:
            return jsonify({'message': 'Usuario inactivo'}), 403
        
        return f(current_user, *args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated
