from src.models.user import User, db
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.routes.auth import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@token_required
def get_users(current_user):
    # Verificar si el usuario es administrador
    if current_user.rol != 'admin':
        return jsonify({'message': 'No autorizado'}), 403
    
    users = User.query.all()
    
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'nombre': user.nombre,
            'email': user.email,
            'rol': user.rol,
            'negocio_id': user.negocio_id,
            'activo': user.activo,
            'ultimo_acceso': user.ultimo_acceso
        }
        output.append(user_data)
    
    return jsonify(output), 200

@user_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    # Verificar si el usuario es administrador o es el mismo usuario
    if current_user.rol != 'admin' and current_user.id != id:
        return jsonify({'message': 'No autorizado'}), 403
    
    user = User.query.get_or_404(id)
    
    user_data = {
        'id': user.id,
        'nombre': user.nombre,
        'email': user.email,
        'rol': user.rol,
        'negocio_id': user.negocio_id,
        'activo': user.activo,
        'ultimo_acceso': user.ultimo_acceso
    }
    
    return jsonify(user_data), 200

@user_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    # Verificar si el usuario es administrador o es el mismo usuario
    if current_user.rol != 'admin' and current_user.id != id:
        return jsonify({'message': 'No autorizado'}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    # Actualizar campos
    if 'nombre' in data:
        user.nombre = data['nombre']
    
    # Solo el administrador puede cambiar estos campos
    if current_user.rol == 'admin':
        if 'rol' in data:
            user.rol = data['rol']
        
        if 'activo' in data:
            user.activo = data['activo']
        
        if 'negocio_id' in data:
            user.negocio_id = data['negocio_id']
    
    # Cambiar contraseña
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='sha256')
    
    db.session.commit()
    
    return jsonify({'message': 'Usuario actualizado correctamente'}), 200

@user_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    # Verificar si el usuario es administrador
    if current_user.rol != 'admin':
        return jsonify({'message': 'No autorizado'}), 403
    
    # No permitir eliminar al propio usuario
    if current_user.id == id:
        return jsonify({'message': 'No puede eliminar su propio usuario'}), 400
    
    user = User.query.get_or_404(id)
    
    # En lugar de eliminar, desactivar
    user.activo = False
    db.session.commit()
    
    return jsonify({'message': 'Usuario desactivado correctamente'}), 200
