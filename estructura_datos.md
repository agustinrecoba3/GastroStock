# Diseño de la Estructura de Datos

## Modelo Entidad-Relación

### Entidades Principales

#### Negocio
- id: Identificador único
- nombre: Nombre del negocio
- tipo_negocio_id: Referencia al tipo de negocio (heladería, restaurante, cafetería, etc.)
- configuracion: Configuración específica del negocio (JSON)
- fecha_creacion: Fecha de creación del registro
- fecha_actualizacion: Fecha de última actualización

#### TipoNegocio
- id: Identificador único
- nombre: Nombre del tipo de negocio (heladería, restaurante, etc.)
- descripcion: Descripción del tipo de negocio
- parametros_default: Configuración predeterminada para este tipo (JSON)

#### Categoria
- id: Identificador único
- negocio_id: Referencia al negocio
- nombre: Nombre de la categoría (helados, postres, bebidas, etc.)
- descripcion: Descripción de la categoría
- activo: Estado de la categoría (activo/inactivo)

#### Producto
- id: Identificador único
- negocio_id: Referencia al negocio
- categoria_id: Referencia a la categoría
- codigo: Código único del producto
- nombre: Nombre del producto
- descripcion: Descripción detallada
- precio_venta: Precio de venta
- costo: Costo calculado
- imagen: Ruta a la imagen del producto
- receta_id: Referencia a la receta (opcional)
- atributos: Atributos específicos del producto (JSON)
- stock_minimo: Cantidad mínima recomendada
- stock_actual: Cantidad actual en inventario
- unidad_medida_id: Referencia a la unidad de medida
- activo: Estado del producto (activo/inactivo)
- fecha_creacion: Fecha de creación del registro
- fecha_actualizacion: Fecha de última actualización

#### UnidadMedida
- id: Identificador único
- nombre: Nombre de la unidad (litro, kilo, unidad, etc.)
- abreviatura: Abreviatura (l, kg, u, etc.)
- tipo: Tipo de medida (volumen, peso, unidad, etc.)

#### MateriaPrima
- id: Identificador único
- negocio_id: Referencia al negocio
- nombre: Nombre de la materia prima
- descripcion: Descripción detallada
- codigo: Código único
- stock_actual: Cantidad actual en inventario
- stock_minimo: Cantidad mínima recomendada
- unidad_medida_id: Referencia a la unidad de medida
- costo_unitario: Costo por unidad
- proveedor_id: Referencia al proveedor (opcional)
- fecha_ultima_compra: Fecha de última compra
- activo: Estado (activo/inactivo)

#### Receta
- id: Identificador único
- negocio_id: Referencia al negocio
- nombre: Nombre de la receta
- descripcion: Descripción detallada
- rendimiento: Cantidad que produce
- unidad_medida_id: Referencia a la unidad de medida del rendimiento
- instrucciones: Pasos de preparación
- tiempo_preparacion: Tiempo estimado de preparación (minutos)
- activo: Estado (activo/inactivo)

#### RecetaIngrediente
- id: Identificador único
- receta_id: Referencia a la receta
- materia_prima_id: Referencia a la materia prima
- cantidad: Cantidad requerida
- unidad_medida_id: Referencia a la unidad de medida

#### MovimientoInventario
- id: Identificador único
- negocio_id: Referencia al negocio
- fecha: Fecha y hora del movimiento
- tipo: Tipo de movimiento (entrada, salida, ajuste)
- referencia: Referencia al documento origen (venta, compra, etc.)
- usuario_id: Usuario que realizó el movimiento
- notas: Observaciones adicionales

#### DetalleMovimiento
- id: Identificador único
- movimiento_id: Referencia al movimiento
- item_id: Referencia al producto o materia prima
- tipo_item: Tipo de ítem (producto o materia prima)
- cantidad: Cantidad del movimiento
- unidad_medida_id: Referencia a la unidad de medida
- costo_unitario: Costo unitario al momento del movimiento

#### Venta
- id: Identificador único
- negocio_id: Referencia al negocio
- fecha: Fecha y hora de la venta
- total: Monto total
- metodo_pago: Método de pago utilizado
- estado: Estado de la venta (completada, cancelada, etc.)
- usuario_id: Usuario que registró la venta
- cliente_id: Referencia al cliente (opcional)
- notas: Observaciones adicionales

#### DetalleVenta
- id: Identificador único
- venta_id: Referencia a la venta
- producto_id: Referencia al producto
- cantidad: Cantidad vendida
- precio_unitario: Precio unitario al momento de la venta
- subtotal: Subtotal de la línea
- descuento: Descuento aplicado

#### Usuario
- id: Identificador único
- negocio_id: Referencia al negocio
- nombre: Nombre completo
- email: Correo electrónico
- password: Contraseña (hash)
- rol: Rol del usuario (administrador, empleado, etc.)
- activo: Estado (activo/inactivo)
- ultimo_acceso: Fecha y hora del último acceso

## Relaciones Principales

- Un Negocio pertenece a un TipoNegocio
- Un Negocio tiene muchas Categorías
- Un Negocio tiene muchos Productos
- Un Negocio tiene muchas MateriasPrimas
- Un Negocio tiene muchas Recetas
- Un Negocio tiene muchos MovimientosInventario
- Un Negocio tiene muchas Ventas
- Un Negocio tiene muchos Usuarios

- Una Categoría tiene muchos Productos
- Un Producto puede tener una Receta
- Una Receta tiene muchos RecetaIngredientes
- Un RecetaIngrediente se relaciona con una MateriaPrima
- Un MovimientoInventario tiene muchos DetalleMovimientos
- Una Venta tiene muchos DetalleVenta

## Índices Recomendados

- Negocio: id, tipo_negocio_id
- Producto: id, negocio_id, categoria_id, codigo
- MateriaPrima: id, negocio_id, codigo
- MovimientoInventario: id, negocio_id, fecha, tipo
- Venta: id, negocio_id, fecha
- Usuario: id, negocio_id, email
