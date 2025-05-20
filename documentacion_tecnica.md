# Documentación Técnica - Sistema de Gestión para Heladería

## Arquitectura del Sistema

El sistema está desarrollado siguiendo una arquitectura de tres capas:

1. **Capa de Presentación (Frontend)**
   - Tecnologías: HTML5, CSS3, JavaScript
   - Frameworks: Bootstrap 5
   - Bibliotecas: Chart.js para visualizaciones

2. **Capa de Lógica de Negocio (Backend)**
   - Tecnología: Python
   - Framework: Flask
   - Autenticación: JWT (JSON Web Tokens)

3. **Capa de Datos**
   - Base de datos: MySQL
   - ORM: SQLAlchemy

## Estructura del Proyecto

```
heladeria_app/
├── venv/                  # Entorno virtual de Python
├── src/                   # Código fuente
│   ├── models/            # Modelos de datos
│   │   ├── user.py        # Modelo de usuarios
│   │   ├── negocio.py     # Modelo de negocios
│   │   ├── producto.py    # Modelo de productos
│   │   ├── inventario.py  # Modelo de inventario
│   │   ├── venta.py       # Modelo de ventas
│   │   ├── receta.py      # Modelo de recetas
│   │   └── materia_prima.py # Modelo de materias primas
│   ├── routes/            # Rutas de la API
│   │   ├── auth.py        # Rutas de autenticación
│   │   ├── user.py        # Rutas de usuarios
│   │   ├── negocio.py     # Rutas de negocios
│   │   ├── producto.py    # Rutas de productos
│   │   ├── inventario.py  # Rutas de inventario
│   │   └── venta.py       # Rutas de ventas
│   ├── static/            # Archivos estáticos
│   │   ├── css/           # Hojas de estilo
│   │   ├── js/            # Scripts de JavaScript
│   │   └── img/           # Imágenes
│   └── main.py            # Punto de entrada de la aplicación
└── requirements.txt       # Dependencias del proyecto
```

## Modelo de Datos

### Entidades Principales

1. **Negocio**: Representa el negocio que utiliza el sistema.
2. **TipoNegocio**: Define los diferentes tipos de negocios soportados.
3. **Categoria**: Categorías para clasificar productos.
4. **Producto**: Productos o sabores que se venden.
5. **UnidadMedida**: Unidades de medida para productos e ingredientes.
6. **MateriaPrima**: Ingredientes o insumos para la elaboración de productos.
7. **Receta**: Fórmulas para la elaboración de productos.
8. **MovimientoInventario**: Registros de entradas, salidas y ajustes de inventario.
9. **Venta**: Registros de ventas realizadas.
10. **Usuario**: Usuarios del sistema con diferentes roles.

## API REST

El sistema expone una API REST para la comunicación entre el frontend y el backend.

### Endpoints Principales

#### Autenticación
- `POST /api/auth/login`: Iniciar sesión
- `POST /api/auth/register`: Registrar nuevo usuario

#### Usuarios
- `GET /api/users`: Listar usuarios
- `GET /api/users/<id>`: Obtener usuario específico
- `PUT /api/users/<id>`: Actualizar usuario
- `DELETE /api/users/<id>`: Desactivar usuario

#### Negocios
- `GET /api/negocios`: Listar negocios
- `GET /api/negocios/<id>`: Obtener negocio específico
- `POST /api/negocios`: Crear nuevo negocio
- `PUT /api/negocios/<id>`: Actualizar negocio
- `GET /api/negocios/tipos`: Listar tipos de negocio

#### Productos
- `GET /api/productos`: Listar productos
- `GET /api/productos/<id>`: Obtener producto específico
- `POST /api/productos`: Crear nuevo producto
- `PUT /api/productos/<id>`: Actualizar producto
- `GET /api/productos/categorias`: Listar categorías
- `POST /api/productos/categorias`: Crear nueva categoría
- `GET /api/productos/unidades-medida`: Listar unidades de medida

#### Inventario
- `GET /api/inventario/movimientos`: Listar movimientos de inventario
- `GET /api/inventario/movimientos/<id>`: Obtener movimiento específico
- `POST /api/inventario/movimientos`: Crear nuevo movimiento
- `GET /api/inventario/stock/productos`: Listar stock de productos
- `GET /api/inventario/stock/materias-primas`: Listar stock de materias primas

#### Ventas
- `GET /api/ventas`: Listar ventas
- `GET /api/ventas/<id>`: Obtener venta específica
- `POST /api/ventas`: Crear nueva venta
- `PUT /api/ventas/<id>/estado`: Actualizar estado de venta
- `GET /api/ventas/clientes`: Listar clientes
- `GET /api/ventas/estadisticas`: Obtener estadísticas de ventas

## Seguridad

El sistema implementa las siguientes medidas de seguridad:

1. **Autenticación basada en tokens JWT**
   - Los tokens tienen una duración limitada (24 horas)
   - Se validan en cada petición a la API

2. **Control de acceso basado en roles**
   - Roles: admin, gerente, empleado
   - Cada rol tiene permisos específicos

3. **Protección de contraseñas**
   - Las contraseñas se almacenan hasheadas con SHA-256
   - No se guardan contraseñas en texto plano

4. **Validación de datos**
   - Todos los datos de entrada son validados antes de procesarse
   - Se previenen inyecciones SQL mediante el uso de ORM

## Adaptabilidad

El sistema está diseñado para ser adaptable a diferentes rubros gastronómicos mediante:

1. **Tipos de negocio configurables**
   - Cada tipo tiene parámetros predeterminados

2. **Terminología personalizable**
   - Se pueden cambiar términos como "producto", "categoría", etc.

3. **Atributos dinámicos**
   - Los productos pueden tener atributos específicos según el tipo de negocio

4. **Categorías flexibles**
   - Cada negocio puede definir sus propias categorías

## Requisitos del Sistema

### Servidor
- Python 3.8 o superior
- MySQL 5.7 o superior
- 2GB de RAM mínimo
- 10GB de espacio en disco

### Cliente
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexión a internet

## Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- MySQL
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```
   git clone https://github.com/usuario/heladeria_app.git
   cd heladeria_app
   ```

2. **Crear y activar entorno virtual**
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos MySQL
   - Actualizar credenciales en `src/main.py` si es necesario

5. **Iniciar la aplicación**
   ```
   python src/main.py
   ```

6. **Acceder a la aplicación**
   - Abrir navegador en http://localhost:5000
   - Usar credenciales por defecto:
     - Usuario: admin@heladeria.com
     - Contraseña: admin123

## Mantenimiento

### Copias de Seguridad
- Se recomienda realizar copias de seguridad diarias de la base de datos
- Comando para backup: `mysqldump -u [usuario] -p [contraseña] mydb > backup.sql`

### Actualizaciones
- Verificar regularmente si hay actualizaciones disponibles
- Para actualizar: `git pull && pip install -r requirements.txt`

### Monitoreo
- Revisar logs de la aplicación en caso de errores
- Verificar regularmente el uso de recursos del servidor

## Solución de Problemas Comunes

### Error de conexión a la base de datos
- Verificar que el servicio MySQL esté en ejecución
- Comprobar credenciales en la configuración
- Verificar que la base de datos exista

### Problemas de rendimiento
- Optimizar consultas a la base de datos
- Aumentar recursos del servidor si es necesario
- Implementar caché para operaciones frecuentes

### Errores de autenticación
- Verificar credenciales
- Comprobar que el token JWT no haya expirado
- Revisar permisos del usuario

## Contacto y Soporte

Para soporte técnico o consultas sobre el sistema:
- Email: soporte@heladeria-app.com
- Teléfono: (123) 456-7890
- Horario de atención: Lunes a Viernes, 9:00 - 18:00
