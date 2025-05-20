from src.models.user import db
from datetime import datetime

class MovimientoInventario(db.Model):
    __tablename__ = 'movimiento_inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.String(20), nullable=False)  # entrada, salida, ajuste
    referencia = db.Column(db.String(50))  # referencia al documento origen
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notas = db.Column(db.Text)
    
    detalles = db.relationship('DetalleMovimiento', backref='movimiento', lazy=True)
    
    def __repr__(self):
        return f'<MovimientoInventario {self.id}>'

class DetalleMovimiento(db.Model):
    __tablename__ = 'detalle_movimiento'
    
    id = db.Column(db.Integer, primary_key=True)
    movimiento_id = db.Column(db.Integer, db.ForeignKey('movimiento_inventario.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    tipo_item = db.Column(db.String(20), nullable=False)  # producto o materia_prima
    cantidad = db.Column(db.Float, nullable=False)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<DetalleMovimiento {self.id}>'
