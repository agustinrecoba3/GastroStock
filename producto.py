from src.models.user import db
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    
    productos = db.relationship('Producto', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class UnidadMedida(db.Model):
    __tablename__ = 'unidad_medida'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # volumen, peso, unidad, etc.
    
    def __repr__(self):
        return f'<UnidadMedida {self.nombre}>'

class Producto(db.Model):
    __tablename__ = 'producto'
    
    id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio_venta = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float)
    imagen = db.Column(db.String(255))
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    atributos = db.Column(db.JSON)
    stock_minimo = db.Column(db.Float)
    stock_actual = db.Column(db.Float, default=0)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
