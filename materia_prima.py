from src.models.user import db
from datetime import datetime

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'
    
    id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    codigo = db.Column(db.String(20), nullable=False)
    stock_actual = db.Column(db.Float, default=0)
    stock_minimo = db.Column(db.Float)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    fecha_ultima_compra = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)
    
    receta_ingredientes = db.relationship('RecetaIngrediente', backref='materia_prima', lazy=True)
    
    def __repr__(self):
        return f'<MateriaPrima {self.nombre}>'

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    
    materias_primas = db.relationship('MateriaPrima', backref='proveedor', lazy=True)
    
    def __repr__(self):
        return f'<Proveedor {self.nombre}>'
