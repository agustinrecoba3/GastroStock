from src.models.user import db
from datetime import datetime

class Receta(db.Model):
    __tablename__ = 'receta'
    
    id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    rendimiento = db.Column(db.Float, nullable=False)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    instrucciones = db.Column(db.Text)
    tiempo_preparacion = db.Column(db.Integer)  # en minutos
    activo = db.Column(db.Boolean, default=True)
    
    ingredientes = db.relationship('RecetaIngrediente', backref='receta', lazy=True)
    productos = db.relationship('Producto', backref='receta', lazy=True)
    
    def __repr__(self):
        return f'<Receta {self.nombre}>'

class RecetaIngrediente(db.Model):
    __tablename__ = 'receta_ingrediente'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    
    def __repr__(self):
        return f'<RecetaIngrediente {self.id}>'
