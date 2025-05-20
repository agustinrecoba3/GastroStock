// Funcionalidad principal de la aplicación
document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let token = localStorage.getItem('token');
    let userData = JSON.parse(localStorage.getItem('userData'));
    
    // Elementos DOM
    const loginContainer = document.getElementById('login-container');
    const dashboardContainer = document.getElementById('dashboard-container');
    const productosContainer = document.getElementById('productos-container');
    const inventarioContainer = document.getElementById('inventario-container');
    const ventasContainer = document.getElementById('ventas-container');
    const reportesContainer = document.getElementById('reportes-container');
    const configuracionContainer = document.getElementById('configuracion-container');
    
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    // Inicialización
    init();
    
    // Función de inicialización
    function init() {
        // Verificar si el usuario está autenticado
        if (!token) {
            showLoginForm();
        } else {
            setupUserInterface();
            loadDashboardData();
        }
        
        // Event listeners para navegación
        setupNavigationListeners();
        
        // Event listeners para formularios
        setupFormListeners();
        
        // Event listener para toggle sidebar en móviles
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
        }
    }
    
    // Mostrar formulario de login
    function showLoginForm() {
        // Ocultar todos los contenedores
        hideAllContainers();
        
        // Mostrar formulario de login
        loginContainer.classList.remove('d-none');
        
        // Event listener para formulario de login
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                // Llamada a la API para login
                fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Credenciales inválidas');
                    }
                    return response.json();
                })
                .then(data => {
                    // Guardar token y datos de usuario
                    token = data.token;
                    userData = data.user;
                    
                    localStorage.setItem('token', token);
                    localStorage.setItem('userData', JSON.stringify(userData));
                    
                    // Configurar interfaz de usuario
                    setupUserInterface();
                    loadDashboardData();
                })
                .catch(error => {
                    alert('Error de inicio de sesión: ' + error.message);
                });
            });
        }
    }
    
    // Configurar interfaz de usuario según rol y datos
    function setupUserInterface() {
        // Ocultar login y mostrar dashboard
        loginContainer.classList.add('d-none');
        dashboardContainer.classList.remove('d-none');
        
        // Actualizar nombre de usuario y negocio
        const usuarioNombre = document.getElementById('usuario-nombre');
        const negocioNombre = document.getElementById('negocio-nombre');
        
        if (usuarioNombre && userData) {
            usuarioNombre.textContent = userData.nombre;
        }
        
        // Cargar nombre del negocio
        if (negocioNombre && userData) {
            fetch(`/api/negocios/${userData.negocio_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(data => {
                negocioNombre.textContent = data.nombre;
            })
            .catch(error => console.error('Error al cargar datos del negocio:', error));
        }
        
        // Configurar permisos según rol
        if (userData && userData.rol !== 'admin') {
            // Ocultar opciones solo para administradores
            const adminElements = document.querySelectorAll('.admin-only');
            adminElements.forEach(el => el.classList.add('d-none'));
        }
    }
    
    // Cargar datos del dashboard
    function loadDashboardData() {
        // Cargar estadísticas de ventas
        fetch('/api/ventas/estadisticas', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            // Actualizar tarjetas de estadísticas
            const ventasHoy = document.getElementById('ventas-hoy');
            if (ventasHoy) {
                ventasHoy.textContent = `$${data.monto_total.toFixed(2)}`;
            }
            
            // Crear gráfico de productos más vendidos
            if (data.productos_mas_vendidos && data.productos_mas_vendidos.length > 0) {
                createProductosChart(data.productos_mas_vendidos);
            }
        })
        .catch(error => console.error('Error al cargar estadísticas:', error));
        
        // Cargar total de productos
        fetch('/api/productos', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            const totalProductos = document.getElementById('total-productos');
            if (totalProductos) {
                totalProductos.textContent = data.length;
            }
        })
        .catch(error => console.error('Error al cargar productos:', error));
        
        // Cargar alertas de stock
        fetch('/api/inventario/stock/productos?bajo_minimo=true', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            const alertasStock = document.getElementById('alertas-stock');
            if (alertasStock) {
                alertasStock.textContent = data.length;
            }
        })
        .catch(error => console.error('Error al cargar alertas de stock:', error));
    }
    
    // Crear gráfico de productos más vendidos
    function createProductosChart(productos) {
        const ctx = document.getElementById('productosChart');
        if (!ctx) return;
        
        const labels = productos.slice(0, 5).map(p => p.nombre);
        const data = productos.slice(0, 5).map(p => p.cantidad_total);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Unidades vendidas',
                    data: data,
                    backgroundColor: 'rgba(78, 115, 223, 0.8)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Configurar listeners para navegación
    function setupNavigationListeners() {
        // Dashboard
        const dashboardLink = document.getElementById('dashboard-link');
        if (dashboardLink) {
            dashboardLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                dashboardContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Dashboard';
                loadDashboardData();
            });
        }
        
        // Productos
        const productosLink = document.getElementById('productos-link');
        if (productosLink) {
            productosLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                productosContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Productos';
                loadProductos();
            });
        }
        
        // Inventario
        const inventarioLink = document.getElementById('inventario-link');
        if (inventarioLink) {
            inventarioLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                inventarioContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Inventario';
                loadInventario();
            });
        }
        
        // Ventas
        const ventasLink = document.getElementById('ventas-link');
        if (ventasLink) {
            ventasLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                ventasContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Ventas';
                loadVentas();
            });
        }
        
        // Reportes
        const reportesLink = document.getElementById('reportes-link');
        if (reportesLink) {
            reportesLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                reportesContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Reportes';
            });
        }
        
        // Configuración
        const configuracionLink = document.getElementById('configuracion-link');
        if (configuracionLink) {
            configuracionLink.addEventListener('click', function(e) {
                e.preventDefault();
                hideAllContainers();
                configuracionContainer.classList.remove('d-none');
                setActiveLink(this);
                document.getElementById('page-title').textContent = 'Configuración';
                loadConfiguracion();
            });
        }
        
        // Cerrar sesión
        const logoutLink = document.getElementById('logout-link');
        if (logoutLink) {
            logoutLink.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Limpiar localStorage
                localStorage.removeItem('token');
                localStorage.removeItem('userData');
                
                // Resetear variables
                token = null;
                userData = null;
                
                // Mostrar login
                showLoginForm();
            });
        }
    }
    
    // Configurar listeners para formularios y acciones
    function setupFormListeners() {
        // Formulario de producto
        const guardarProductoBtn = document.getElementById('guardar-producto');
        if (guardarProductoBtn) {
            guardarProductoBtn.addEventListener('click', function() {
                saveProducto();
            });
        }
        
        // Formulario de movimiento
        const guardarMovimientoBtn = document.getElementById('guardar-movimiento');
        if (guardarMovimientoBtn) {
            guardarMovimientoBtn.addEventListener('click', function() {
                saveMovimiento();
            });
        }
        
        // Formulario de venta
        const guardarVentaBtn = document.getElementById('guardar-venta');
        if (guardarVentaBtn) {
            guardarVentaBtn.addEventListener('click', function() {
                saveVenta();
            });
        }
        
        // Botón nuevo producto
        const nuevoProductoBtn = document.getElementById('nuevo-producto-btn');
        if (nuevoProductoBtn) {
            nuevoProductoBtn.addEventListener('click', function() {
                showProductoModal();
            });
        }
        
        // Botón nuevo movimiento
        const nuevoMovimientoBtn = document.getElementById('nuevo-movimiento-btn');
        const nuevoMovimientoBtn2 = document.getElementById('nuevo-movimiento-btn-2');
        
        if (nuevoMovimientoBtn) {
            nuevoMovimientoBtn.addEventListener('click', function() {
                showMovimientoModal();
            });
        }
        
        if (nuevoMovimientoBtn2) {
            nuevoMovimientoBtn2.addEventListener('click', function() {
                showMovimientoModal();
            });
        }
        
        // Botón nueva venta
        const nuevaVentaBtn = document.getElementById('nueva-venta-btn');
        if (nuevaVentaBtn) {
            nuevaVentaBtn.addEventListener('click', function() {
                showVentaModal();
            });
        }
        
        // Tabs de inventario
        const tabStock = document.getElementById('tab-stock');
        const tabMovimientos = document.getElementById('tab-movimientos');
        const tabMateriasPrimas = document.getElementById('tab-materias-primas');
        
        if (tabStock) {
            tabStock.addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('stock-container').classList.remove('d-none');
                document.getElementById('movimientos-container').classList.add('d-none');
                document.getElementById('materias-primas-container').classList.add('d-none');
                setActiveTab(this);
            });
        }
        
        if (tabMovimientos) {
            tabMovimientos.addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('stock-container').classList.add('d-none');
                document.getElementById('movimientos-container').classList.remove('d-none');
                document.getElementById('materias-primas-container').classList.add('d-none');
                setActiveTab(this);
                loadMovimientos();
            });
        }
        
        if (tabMateriasPrimas) {
            tabMateriasPrimas.addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('stock-container').classList.add('d-none');
                document.getElementById('movimientos-container').classList.add('d-none');
                document.getElementById('materias-primas-container').classList.remove('d-none');
                setActiveTab(this);
                loadMateriasPrimas();
            });
        }
        
        // Tabs de configuración
        const tabNegocio = document.getElementById('tab-negocio');
        const tabUsuarios = document.getElementById('tab-usuarios');
        const tabCategorias = document.getElementById('tab-categorias');
        const tabUnidades = document.getElementById('tab-unidades');
        
        if (tabNegocio) {
            tabNegocio.addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('negocio-config-container').classList.re
(Content truncated due to size limit. Use line ranges to read in chunks)