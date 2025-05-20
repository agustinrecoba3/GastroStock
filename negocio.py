from src.models.user import db
from datetime import datetime

class TipoNegocio(db.Model):
    __tablename__ = 'tipo_negocio'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    parametros_default = db.Column(db.JSON)
    
    negocios = db.relationship('Negocio', backref='tipo_negocio', lazy=True)
    
    def __repr__(self):
        return f'<TipoNegocio {self.nombre}>'

class Negocio(db.Model):
    __tablename__ = 'negocio'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_negocio_id = db.Column(db.Integer, db.ForeignKey('tipo_negocio.id'), nullable=False)
    configuracion = db.Column(db.JSON)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    categorias = db.relationship('Categoria', backref='negocio', lazy=True)
    productos = db.relationship('Producto', backref='negocio', lazy=True)
    materias_primas = db.relationship('MateriaPrima', backref='negocio', lazy=True)
    recetas = db.relationship('Receta', backref='negocio', lazy=True)
    movimientos_inventario = db.relationship('MovimientoInventario', backref='negocio', lazy=True)
    ventas = db.relationship('Venta', backref='negocio', lazy=True)
    
    def __repr__(self):
        return f'<Negocio {self.nombre}>'
