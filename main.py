import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.negocio import negocio_bp
from src.routes.producto import producto_bp
from src.routes.inventario import inventario_bp
from src.routes.venta import venta_bp
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(negocio_bp, url_prefix='/api/negocios')
app.register_blueprint(producto_bp, url_prefix='/api/productos')
app.register_blueprint(inventario_bp, url_prefix='/api/inventario')
app.register_blueprint(venta_bp, url_prefix='/api/ventas')

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Inicializar la base de datos y crear usuario admin
@app.before_first_request
def initialize_database():
    with app.app_context():
        db.create_all()
        
        # Verificar si ya existe un usuario admin
        admin = User.query.filter_by(email='admin@heladeria.com').first()
        if not admin:
            # Crear tipos de negocio predeterminados
            from src.models.negocio import TipoNegocio, Negocio
            
            # Tipo Heladería
            tipo_heladeria = TipoNegocio(
                nombre="Heladería",
                descripcion="Negocio especializado en la venta de helados y postres fríos",
                parametros_default={
                    "terminologia": {
                        "producto": "Sabor",
                        "categoria": "Tipo de helado"
                    },
                    "categorias_default": ["Cremas", "Frutas", "Especiales", "Postres"],
                    "atributos_producto": ["base", "alergenos", "temporada"]
                }
            )
            
            # Tipo Restaurante
            tipo_restaurante = TipoNegocio(
                nombre="Restaurante",
                descripcion="Negocio especializado en la venta de comidas y bebidas",
                parametros_default={
                    "terminologia": {
                        "producto": "Plato",
                        "categoria": "Sección"
                    },
                    "categorias_default": ["Entradas", "Platos principales", "Postres", "Bebidas"],
                    "atributos_producto": ["tiempo_preparacion", "calorias", "vegetariano", "vegano"]
                }
            )
            
            # Tipo Cafetería
            tipo_cafeteria = TipoNegocio(
                nombre="Cafetería",
                descripcion="Negocio especializado en la venta de café y productos relacionados",
                parametros_default={
                    "terminologia": {
                        "producto": "Bebida/Snack",
                        "categoria": "Tipo"
                    },
                    "categorias_default": ["Cafés", "Tés", "Pasteles", "Sándwiches"],
                    "atributos_producto": ["temperatura", "tamaño", "intensidad", "origen"]
                }
            )
            
            db.session.add(tipo_heladeria)
            db.session.add(tipo_restaurante)
            db.session.add(tipo_cafeteria)
            db.session.flush()
            
            # Crear negocio predeterminado
            negocio_default = Negocio(
                nombre="Mi Heladería",
                tipo_negocio_id=tipo_heladeria.id,
                configuracion=tipo_heladeria.parametros_default
            )
            
            db.session.add(negocio_default)
            db.session.flush()
            
            # Crear unidades de medida predeterminadas
            from src.models.producto import UnidadMedida
            
            unidades = [
                UnidadMedida(nombre="Kilogramo", abreviatura="kg", tipo="peso"),
                UnidadMedida(nombre="Gramo", abreviatura="g", tipo="peso"),
                UnidadMedida(nombre="Litro", abreviatura="l", tipo="volumen"),
                UnidadMedida(nombre="Mililitro", abreviatura="ml", tipo="volumen"),
                UnidadMedida(nombre="Unidad", abreviatura="u", tipo="unidad"),
                UnidadMedida(nombre="Porción", abreviatura="porc", tipo="unidad")
            ]
            
            for unidad in unidades:
                db.session.add(unidad)
            
            db.session.flush()
            
            # Crear usuario administrador
            hashed_password = generate_password_hash("admin123", method='sha256')
            admin_user = User(
                negocio_id=negocio_default.id,
                nombre="Administrador",
                email="admin@heladeria.com",
                password=hashed_password,
                rol="admin",
                activo=True
            )
            
            db.session.add(admin_user)
            db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
