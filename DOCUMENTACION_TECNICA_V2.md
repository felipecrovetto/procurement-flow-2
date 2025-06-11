# Sistema de Gestión de Compras y Licitaciones - Versión 2.0
## Documentación Técnica Completa

### Tabla de Contenidos

1. [Introducción y Características](#introducción-y-características)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Nuevas Funcionalidades](#nuevas-funcionalidades)
4. [Integración con Tablas Excel](#integración-con-tablas-excel)
5. [Sistema de Análisis Avanzado](#sistema-de-análisis-avanzado)
6. [Mejoras de Robustez](#mejoras-de-robustez)
7. [Instalación y Configuración](#instalación-y-configuración)
8. [Guía de Usuario](#guía-de-usuario)
9. [API Reference](#api-reference)
10. [Mantenimiento y Troubleshooting](#mantenimiento-y-troubleshooting)

---

## Introducción y Características

El Sistema de Gestión de Compras y Licitaciones versión 2.0 es una aplicación web completa diseñada para automatizar y optimizar los procesos de adquisición en organizaciones. Esta versión incorpora análisis avanzados basados en tablas Excel, mejoras significativas de robustez y nuevas funcionalidades de visualización de datos.

### Características Principales

**Gestión Integral de Procesos:**
- Administración completa de procesos de compra simples y licitaciones grandes
- Seguimiento detallado del ciclo de vida de cada proceso
- Gestión de documentos con carga, descarga y versionado
- Sistema de alertas automáticas e inteligentes
- Control de tiempos y vencimientos

**Análisis Avanzado con Excel:**
- Integración completa con tablas Excel especializadas
- Carga y procesamiento automático de datos desde archivos Excel
- Generación de plantillas descargables para diferentes tipos de análisis
- Validación automática de datos con reportes de errores y advertencias
- Exportación de datos del sistema a formatos Excel

**Visualización y Reportes:**
- Dashboard interactivo con métricas en tiempo real
- Gráficos avanzados: radar, barras, líneas, dispersión, cascada
- Análisis comparativo de propuestas técnicas y económicas
- Reportes de ahorros y valor agregado
- Tendencias históricas y proyecciones

**Gestión de Proveedores:**
- Base de datos completa de proveedores con historial
- Evaluación técnica y comercial automatizada
- Análisis de rendimiento y recomendaciones
- Seguimiento de cumplimiento y calidad

**Robustez y Seguridad:**
- Sistema de respaldos automáticos
- Validación exhaustiva de datos
- Manejo robusto de errores
- Logging detallado para auditoría
- Monitoreo del estado del sistema

---

## Arquitectura del Sistema

### Componentes Principales

**Backend (Flask):**
- Framework Flask con arquitectura modular
- Base de datos SQLite para simplicidad de instalación
- APIs RESTful para comunicación frontend-backend
- Sistema de blueprints para organización del código

**Frontend (HTML/CSS/JavaScript):**
- Interfaz responsiva compatible con dispositivos móviles
- Framework Bootstrap para diseño moderno
- Chart.js para visualizaciones interactivas
- JavaScript vanilla para máximo rendimiento

**Base de Datos:**
- SQLite para facilidad de instalación y portabilidad
- Esquema normalizado con relaciones bien definidas
- Soporte para datos de Excel con tablas especializadas
- Índices optimizados para consultas rápidas

**Sistema de Archivos:**
- Gestión segura de archivos subidos
- Validación de tipos y tamaños de archivo
- Organización jerárquica de documentos
- Sistema de respaldos automáticos

### Estructura de Directorios

```
procurement_app/
├── src/
│   ├── main.py                 # Aplicación principal
│   ├── models/
│   │   ├── database.py         # Configuración de base de datos
│   │   ├── models.py           # Modelos principales
│   │   └── excel_models.py     # Modelos para datos Excel
│   ├── routes/
│   │   ├── suppliers.py        # APIs de proveedores
│   │   ├── processes.py        # APIs de procesos
│   │   ├── documents.py        # APIs de documentos
│   │   ├── bids.py            # APIs de ofertas
│   │   ├── alerts.py          # APIs de alertas
│   │   ├── reports.py         # APIs de reportes
│   │   └── excel_routes.py    # APIs para Excel
│   └── static/
│       ├── index.html         # Interfaz principal
│       ├── style.css          # Estilos
│       └── app.js            # Lógica frontend
├── robustness_improvements.py  # Mejoras de robustez
├── requirements.txt           # Dependencias
├── README.md                 # Documentación básica
├── MANUAL_USUARIO.md         # Manual de usuario
└── INSTALACION_RAPIDA.md     # Guía de instalación
```

---

## Nuevas Funcionalidades

### 1. Integración Completa con Excel

**Carga de Archivos Excel:**
- Soporte para múltiples tipos de tablas especializadas
- Validación automática de estructura y datos
- Procesamiento inteligente con detección de encabezados
- Manejo de errores con reportes detallados

**Tipos de Tablas Soportadas:**
- Seguimiento de Procesos de Licitación
- Matriz de Evaluación Técnico-Comercial
- Evaluación Técnica de Proveedores
- Evaluación General de Proveedores
- Consultas y Respuestas
- Comparativo de Propuestas Económicas
- Análisis de Ahorro y Valor Agregado

**Descarga de Plantillas:**
- Plantillas pre-configuradas para cada tipo de análisis
- Formato estándar con validaciones incorporadas
- Instrucciones detalladas en cada plantilla
- Compatibilidad con Excel 2016 y versiones posteriores

### 2. Sistema de Análisis Avanzado

**Análisis Técnico:**
- Gráficos radar para comparación multidimensional
- Análisis de criterios ponderados
- Ranking automático de proveedores
- Identificación de fortalezas y debilidades

**Análisis Económico:**
- Comparativos de precios por ítem
- Análisis de distribución de precios
- Identificación de ofertas atípicas
- Cálculo automático de mejores ofertas

**Análisis de Ahorros:**
- Gráficos de cascada para visualizar ahorros
- Comparación presupuesto vs. precio final
- Análisis por categorías de gasto
- Cálculo de porcentajes de ahorro

**Análisis de Tendencias:**
- Tendencias mensuales de procesos
- Evolución de presupuestos
- Análisis de rendimiento de proveedores
- Proyecciones basadas en datos históricos

### 3. Dashboard Mejorado

**Métricas en Tiempo Real:**
- Contadores dinámicos de procesos, proveedores y ofertas
- Estado actual del sistema
- Alertas activas y vencimientos próximos
- Resumen de actividad reciente

**Visualizaciones Interactivas:**
- Gráficos de distribución por estado
- Tendencias temporales
- Análisis de rendimiento
- Mapas de calor para identificar patrones

### 4. Gestión Avanzada de Documentos

**Organización Mejorada:**
- Categorización automática por tipo de proceso
- Versionado de documentos
- Búsqueda avanzada con filtros
- Previsualización de archivos

**Integración con Análisis:**
- Vinculación automática con datos de Excel
- Generación de reportes consolidados
- Exportación de análisis completos
- Trazabilidad de cambios

---

## Integración con Tablas Excel

### Proceso de Carga

**1. Selección de Tipo de Tabla:**
El sistema permite seleccionar entre diferentes tipos de tablas especializadas, cada una con su propio esquema de validación y procesamiento.

**2. Validación Automática:**
- Verificación de estructura de columnas
- Validación de tipos de datos
- Comprobación de rangos y valores permitidos
- Detección de inconsistencias

**3. Procesamiento Inteligente:**
- Detección automática de filas de encabezado
- Limpieza de datos automática
- Conversión de tipos de datos
- Manejo de valores faltantes

**4. Integración con Base de Datos:**
- Creación automática de registros relacionados
- Actualización de datos existentes
- Mantenimiento de integridad referencial
- Logging de cambios para auditoría

### Validaciones Implementadas

**Seguimiento de Procesos:**
- Validación de números de proceso únicos
- Verificación de fechas coherentes
- Validación de tipos de proceso estándar
- Comprobación de presupuestos válidos

**Evaluación Técnica:**
- Verificación de suma de pesos (100%)
- Validación de rangos de puntuación (0-5)
- Comprobación de criterios obligatorios
- Validación de coherencia entre criterios

**Comparativo Económico:**
- Validación de precios positivos
- Verificación de cantidades válidas
- Comprobación de coherencia entre ofertas
- Detección de valores atípicos

**Análisis de Ahorros:**
- Validación de coherencia presupuesto vs. precio final
- Verificación de cálculos de porcentajes
- Comprobación de categorías estándar
- Validación de totales

### Exportación de Datos

**Listas de Proveedores:**
- Exportación completa con todos los campos
- Filtros por estado, tipo, evaluación
- Formato Excel con formato profesional
- Inclusión de métricas de rendimiento

**Listas de Procesos:**
- Exportación por período, estado, tipo
- Inclusión de datos financieros
- Métricas de participación
- Análisis de duración

**Análisis Consolidados:**
- Reportes completos por proceso
- Análisis comparativo multi-proceso
- Tendencias históricas
- Proyecciones y recomendaciones

---

## Sistema de Análisis Avanzado

### Tipos de Gráficos Implementados

**1. Gráficos Radar (Spider Charts):**
- Comparación multidimensional de proveedores
- Visualización de criterios técnicos
- Identificación rápida de fortalezas y debilidades
- Soporte para múltiples proveedores simultáneamente

**2. Gráficos de Barras Agrupadas:**
- Comparación de precios por ítem
- Análisis de puntuaciones técnicas
- Distribución de procesos por tipo
- Evolución temporal de métricas

**3. Gráficos de Cascada (Waterfall):**
- Visualización de ahorros acumulados
- Análisis de variaciones presupuestarias
- Desglose de costos por categoría
- Impacto de decisiones de compra

**4. Gráficos de Dispersión:**
- Análisis de correlación precio-calidad
- Identificación de proveedores óptimos
- Detección de valores atípicos
- Análisis de rendimiento vs. costo

**5. Gráficos de Líneas Temporales:**
- Tendencias de procesos mensuales
- Evolución de presupuestos
- Análisis de estacionalidad
- Proyecciones futuras

**6. Gráficos Circulares (Pie Charts):**
- Distribución por categorías
- Análisis de participación de mercado
- Desglose de ahorros por concepto
- Estado de procesos

### Análisis Estadísticos

**Métricas Descriptivas:**
- Promedios, medianas, modas
- Desviaciones estándar
- Rangos y percentiles
- Coeficientes de variación

**Análisis Comparativo:**
- Benchmarking entre proveedores
- Comparación histórica
- Análisis de mejores prácticas
- Identificación de oportunidades

**Análisis Predictivo:**
- Tendencias futuras basadas en datos históricos
- Proyección de presupuestos
- Estimación de ahorros potenciales
- Análisis de riesgos

### Reportes Automatizados

**Reportes por Proceso:**
- Análisis completo de un proceso específico
- Comparación de ofertas técnicas y económicas
- Recomendaciones de adjudicación
- Análisis de ahorros logrados

**Reportes de Proveedores:**
- Evaluación integral de rendimiento
- Historial de participación
- Análisis de cumplimiento
- Recomendaciones de calificación

**Reportes Ejecutivos:**
- Resumen de actividad del período
- Métricas clave de rendimiento
- Análisis de tendencias
- Recomendaciones estratégicas

---

## Mejoras de Robustez

### Sistema de Validación

**Validación de Archivos:**
- Verificación de tipos de archivo permitidos
- Validación de tamaños máximos (16MB)
- Detección de archivos maliciosos
- Sanitización de nombres de archivo

**Validación de Datos:**
- Esquemas de validación por tipo de tabla
- Verificación de integridad referencial
- Validación de rangos y formatos
- Detección de inconsistencias

**Validación de Entrada:**
- Sanitización de inputs del usuario
- Prevención de inyección SQL
- Validación de parámetros de API
- Manejo seguro de archivos subidos

### Sistema de Logging

**Niveles de Log:**
- ERROR: Errores críticos del sistema
- WARNING: Situaciones que requieren atención
- INFO: Información general de operaciones
- DEBUG: Información detallada para desarrollo

**Categorías de Log:**
- Operaciones de base de datos
- Procesamiento de archivos
- Autenticación y autorización
- Errores de validación
- Operaciones del sistema

**Rotación de Logs:**
- Archivos diarios con timestamp
- Compresión automática de logs antiguos
- Limpieza automática después de 30 días
- Configuración de tamaños máximos

### Sistema de Respaldos

**Respaldos Automáticos:**
- Respaldo diario de base de datos
- Respaldo semanal de archivos
- Compresión automática
- Verificación de integridad

**Respaldos Manuales:**
- Endpoint para crear respaldos bajo demanda
- Respaldos antes de operaciones críticas
- Exportación de datos completos
- Respaldos incrementales

**Restauración:**
- Proceso automatizado de restauración
- Verificación de integridad antes de restaurar
- Respaldo de seguridad antes de restaurar
- Logging detallado del proceso

### Monitoreo del Sistema

**Verificaciones de Salud:**
- Estado de la base de datos
- Espacio en disco disponible
- Integridad de directorios
- Conectividad de servicios

**Métricas de Rendimiento:**
- Tiempo de respuesta de APIs
- Uso de memoria
- Carga de CPU
- Throughput de operaciones

**Alertas Automáticas:**
- Notificaciones de errores críticos
- Alertas de espacio en disco bajo
- Notificaciones de fallos de respaldo
- Alertas de rendimiento degradado

### Manejo de Errores

**Captura Exhaustiva:**
- Try-catch en todas las operaciones críticas
- Logging detallado de errores
- Información de contexto para debugging
- Stack traces para desarrollo

**Recuperación Automática:**
- Reintentos automáticos para operaciones fallidas
- Fallback a operaciones alternativas
- Degradación elegante de funcionalidades
- Mantenimiento de estado consistente

**Comunicación de Errores:**
- Mensajes de error amigables para usuarios
- Códigos de error específicos para APIs
- Documentación de errores comunes
- Guías de resolución de problemas

---

## Instalación y Configuración

### Requisitos del Sistema

**Requisitos Mínimos:**
- Sistema Operativo: Windows 10, macOS 10.14, Ubuntu 18.04 o superior
- Python: 3.8 o superior
- RAM: 4 GB mínimo, 8 GB recomendado
- Espacio en Disco: 2 GB para instalación, 10 GB para datos
- Navegador: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Dependencias Python:**
- Flask 2.3.0+
- SQLAlchemy 2.0+
- Pandas 2.0+
- Matplotlib 3.7+
- Openpyxl 3.1+
- APScheduler 3.10+

### Proceso de Instalación

**1. Preparación del Entorno:**
```bash
# Crear directorio del proyecto
mkdir procurement_system
cd procurement_system

# Extraer archivos del sistema
tar -xzf sistema_compras_licitaciones.tar.gz
cd procurement_app
```

**2. Configuración de Python:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

**3. Configuración de la Base de Datos:**
```bash
# La base de datos se crea automáticamente al iniciar
# No se requiere configuración adicional para SQLite
```

**4. Configuración de Directorios:**
```bash
# Crear directorios necesarios
mkdir -p uploads/documents
mkdir -p uploads/excel
mkdir -p backups
mkdir -p logs
```

**5. Inicio del Sistema:**
```bash
# Navegar al directorio src
cd src

# Iniciar la aplicación
python main.py
```

**6. Verificación de la Instalación:**
- Abrir navegador en `http://localhost:5000`
- Verificar que la interfaz carga correctamente
- Probar funcionalidades básicas
- Revisar logs en caso de errores

### Configuración Avanzada

**Variables de Entorno:**
```bash
# Configuración opcional
export FLASK_ENV=production
export DATABASE_URL=sqlite:///procurement.db
export UPLOAD_FOLDER=uploads
export MAX_FILE_SIZE=16777216
export BACKUP_RETENTION_DAYS=30
```

**Configuración de Logging:**
```python
# En robustness_improvements.py
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_ROTATION = 'daily'  # daily, weekly, monthly
MAX_LOG_SIZE = '10MB'
```

**Configuración de Respaldos:**
```python
# Configuración de respaldos automáticos
BACKUP_SCHEDULE = '0 2 * * *'  # Diario a las 2 AM
BACKUP_RETENTION = 30  # Días
BACKUP_COMPRESSION = True
```

### Configuración de Producción

**Servidor Web:**
Para entornos de producción, se recomienda usar un servidor web como Nginx con Gunicorn:

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

**Base de Datos:**
Para mayor rendimiento en producción, considerar migrar a PostgreSQL:

```python
# Configuración para PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/procurement'
```

**Seguridad:**
```python
# Configuraciones de seguridad adicionales
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
```

---

## Guía de Usuario

### Navegación Principal

**Dashboard:**
El dashboard proporciona una vista general del sistema con métricas clave, gráficos de estado y actividad reciente. Incluye:
- Contadores de procesos, proveedores y ofertas
- Gráficos de distribución por estado
- Lista de procesos recientes
- Alertas activas y próximos vencimientos

**Gestión de Procesos:**
Permite crear, editar y gestionar procesos de compra y licitaciones:
- Crear nuevo proceso con información básica
- Definir tipo de proceso (Simple, Licitación Pequeña, Licitación Grande)
- Establecer fechas de inicio y cierre
- Asignar presupuesto y área solicitante
- Gestionar documentos asociados

**Gestión de Proveedores:**
Administra la base de datos de proveedores:
- Registrar nuevos proveedores con información completa
- Mantener historial de participación
- Evaluar rendimiento y calidad
- Generar reportes de cumplimiento

**Gestión de Documentos:**
Organiza todos los documentos del sistema:
- Subir documentos por categoría
- Organizar por proceso o proveedor
- Descargar documentos individuales o en lote
- Mantener versionado de documentos

**Tablas Excel:**
Nueva funcionalidad para integración con análisis avanzados:
- Descargar plantillas especializadas
- Cargar archivos Excel con validación automática
- Exportar datos del sistema a Excel
- Generar análisis gráficos avanzados

**Reportes y Análisis:**
Genera reportes detallados y análisis visuales:
- Dashboard ejecutivo con métricas clave
- Análisis por proceso individual
- Reportes de rendimiento de proveedores
- Análisis de tendencias temporales

### Flujo de Trabajo Típico

**1. Creación de Proceso:**
- Acceder a la sección "Procesos"
- Hacer clic en "Nuevo Proceso"
- Completar información básica (título, tipo, fechas, presupuesto)
- Guardar el proceso

**2. Carga de Documentos:**
- Seleccionar el proceso creado
- Ir a la sección "Documentos"
- Subir bases de licitación, especificaciones técnicas
- Organizar documentos por categoría

**3. Gestión de Proveedores:**
- Registrar proveedores participantes
- Cargar información de contacto y capacidades
- Mantener historial de evaluaciones

**4. Carga de Ofertas:**
- Recibir ofertas técnicas y económicas
- Cargar documentos de ofertas
- Registrar información básica de cada oferta

**5. Evaluación con Excel:**
- Descargar plantillas de evaluación técnica
- Completar evaluación de criterios técnicos
- Cargar archivo Excel con evaluaciones
- Descargar plantilla de comparativo económico
- Completar análisis de precios
- Cargar archivo Excel con comparativo

**6. Análisis y Reportes:**
- Generar análisis gráfico del proceso
- Revisar comparativos técnicos y económicos
- Analizar ahorros logrados
- Generar reporte ejecutivo

**7. Adjudicación:**
- Revisar recomendaciones del sistema
- Documentar decisión de adjudicación
- Generar documentos finales
- Archivar proceso completado

### Funcionalidades Avanzadas

**Análisis Comparativo:**
- Gráficos radar para evaluación técnica
- Comparativos de precios por ítem
- Análisis de distribución de ofertas
- Identificación de mejores ofertas

**Análisis de Ahorros:**
- Cálculo automático de ahorros vs. presupuesto
- Análisis por categorías de gasto
- Visualización de cascada de ahorros
- Reportes de valor agregado

**Gestión de Alertas:**
- Configuración de recordatorios automáticos
- Alertas de vencimientos próximos
- Notificaciones de documentos faltantes
- Seguimiento de hitos del proceso

**Exportación de Datos:**
- Exportar listas de proveedores a Excel
- Exportar procesos por período
- Generar reportes consolidados
- Crear respaldos de datos

### Consejos y Mejores Prácticas

**Organización de Datos:**
- Mantener nomenclatura consistente en nombres de procesos
- Usar categorías estándar para documentos
- Completar toda la información requerida
- Revisar datos antes de cargar archivos Excel

**Gestión de Archivos:**
- Usar nombres descriptivos para archivos
- Mantener versiones actualizadas de documentos
- Organizar archivos por proceso y fecha
- Realizar respaldos regulares

**Análisis Efectivo:**
- Completar evaluaciones técnicas antes que económicas
- Usar criterios de evaluación consistentes
- Documentar decisiones y justificaciones
- Revisar análisis automáticos antes de tomar decisiones

**Mantenimiento del Sistema:**
- Realizar respaldos semanales
- Limpiar archivos temporales regularmente
- Monitorear espacio en disco
- Actualizar información de proveedores

---

## API Reference

### Endpoints Principales

**Procesos (`/api/processes`):**
```
GET    /api/processes              # Listar todos los procesos
POST   /api/processes              # Crear nuevo proceso
GET    /api/processes/{id}         # Obtener proceso específico
PUT    /api/processes/{id}         # Actualizar proceso
DELETE /api/processes/{id}         # Eliminar proceso
```

**Proveedores (`/api/suppliers`):**
```
GET    /api/suppliers              # Listar todos los proveedores
POST   /api/suppliers              # Crear nuevo proveedor
GET    /api/suppliers/{id}         # Obtener proveedor específico
PUT    /api/suppliers/{id}         # Actualizar proveedor
DELETE /api/suppliers/{id}         # Eliminar proveedor
```

**Documentos (`/api/documents`):**
```
GET    /api/documents              # Listar documentos
POST   /api/documents              # Subir nuevo documento
GET    /api/documents/{id}         # Descargar documento
DELETE /api/documents/{id}         # Eliminar documento
```

**Excel (`/api/excel`):**
```
GET    /api/excel/templates/{type}           # Descargar plantilla
POST   /api/excel/upload/{type}              # Cargar archivo Excel
GET    /api/excel/export/{type}              # Exportar datos
GET    /api/excel/data/{type}/{process_id}   # Obtener datos para análisis
```

**Reportes (`/api/reports`):**
```
GET    /api/reports/dashboard                    # Dashboard principal
GET    /api/reports/advanced-analysis/{id}       # Análisis avanzado de proceso
GET    /api/reports/supplier-performance-advanced # Rendimiento de proveedores
GET    /api/reports/trends-analysis              # Análisis de tendencias
GET    /api/reports/comprehensive-dashboard      # Dashboard completo
```

### Formatos de Datos

**Proceso:**
```json
{
  "id": 1,
  "title": "Adquisición de Equipos de Oficina",
  "process_type": "Compra Simple",
  "description": "Proceso para adquirir equipos de oficina",
  "start_date": "2024-01-15",
  "end_date": "2024-02-15",
  "budget": 50000,
  "status": "active",
  "requesting_area": "Administración",
  "created_at": "2024-01-10T10:00:00Z"
}
```

**Proveedor:**
```json
{
  "id": 1,
  "name": "TechSupply SA",
  "contact_person": "Juan Pérez",
  "email": "juan.perez@techsupply.com",
  "phone": "+1234567890",
  "address": "Av. Principal 123",
  "tax_id": "12345678-9",
  "category": "Tecnología",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Análisis de Proceso:**
```json
{
  "process": {...},
  "technical_evaluations": [...],
  "economic_comparisons": [...],
  "savings_analysis": [...],
  "charts": {
    "technical_radar": "data:image/png;base64,...",
    "economic_comparison": "data:image/png;base64,...",
    "savings_waterfall": "data:image/png;base64,..."
  },
  "summary_stats": {
    "technical": {...},
    "economic": {...},
    "savings": {...}
  }
}
```

### Códigos de Respuesta

**Códigos de Éxito:**
- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Operación exitosa sin contenido de respuesta

**Códigos de Error:**
- `400 Bad Request`: Datos de entrada inválidos
- `401 Unauthorized`: Autenticación requerida
- `403 Forbidden`: Acceso denegado
- `404 Not Found`: Recurso no encontrado
- `413 Payload Too Large`: Archivo muy grande
- `422 Unprocessable Entity`: Error de validación
- `500 Internal Server Error`: Error interno del servidor

### Autenticación y Autorización

Actualmente el sistema opera sin autenticación para simplicidad de uso local. Para implementaciones en producción, se recomienda agregar:

**JWT Authentication:**
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/api/auth/login', methods=['POST'])
def login():
    # Validar credenciales
    access_token = create_access_token(identity=user_id)
    return {'access_token': access_token}

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    # Endpoint protegido
    return {'message': 'Access granted'}
```

---

## Mantenimiento y Troubleshooting

### Tareas de Mantenimiento Regular

**Diario:**
- Verificar logs de errores
- Monitorear espacio en disco
- Revisar alertas del sistema
- Verificar respaldos automáticos

**Semanal:**
- Limpiar archivos temporales
- Revisar rendimiento del sistema
- Actualizar datos de proveedores
- Verificar integridad de base de datos

**Mensual:**
- Analizar tendencias de uso
- Optimizar consultas de base de datos
- Revisar y actualizar documentación
- Planificar actualizaciones del sistema

**Trimestral:**
- Revisar y actualizar dependencias
- Realizar pruebas de recuperación
- Analizar métricas de rendimiento
- Planificar mejoras del sistema

### Problemas Comunes y Soluciones

**Error: "Base de datos bloqueada"**
```
Causa: Múltiples procesos accediendo a SQLite simultáneamente
Solución: 
1. Reiniciar la aplicación
2. Verificar que no hay múltiples instancias ejecutándose
3. Considerar migrar a PostgreSQL para alta concurrencia
```

**Error: "Archivo muy grande"**
```
Causa: Archivo excede el límite de 16MB
Solución:
1. Comprimir el archivo antes de subirlo
2. Dividir archivos grandes en partes más pequeñas
3. Ajustar MAX_CONTENT_LENGTH en configuración si es necesario
```

**Error: "Plantilla Excel no válida"**
```
Causa: Estructura del archivo Excel no coincide con la esperada
Solución:
1. Descargar plantilla actualizada del sistema
2. Verificar que los encabezados coinciden exactamente
3. Revisar que no hay filas o columnas adicionales
4. Verificar formato de datos (fechas, números)
```

**Error: "Espacio en disco insuficiente"**
```
Causa: Disco lleno o casi lleno
Solución:
1. Limpiar archivos temporales y logs antiguos
2. Mover respaldos antiguos a almacenamiento externo
3. Comprimir archivos grandes
4. Considerar expandir almacenamiento
```

**Rendimiento Lento:**
```
Causas posibles:
- Base de datos muy grande sin índices
- Muchos archivos en directorio de uploads
- Memoria insuficiente
- Consultas no optimizadas

Soluciones:
1. Agregar índices a tablas grandes
2. Organizar archivos en subdirectorios por fecha
3. Aumentar memoria RAM disponible
4. Optimizar consultas SQL
5. Implementar cache para consultas frecuentes
```

### Herramientas de Diagnóstico

**Verificación del Estado del Sistema:**
```bash
# Acceder al endpoint de salud
curl http://localhost:5000/health

# Verificar estado detallado
curl http://localhost:5000/api/system/status
```

**Análisis de Logs:**
```bash
# Ver logs recientes
tail -f logs/procurement_$(date +%Y%m%d).log

# Buscar errores específicos
grep "ERROR" logs/procurement_*.log

# Analizar patrones de uso
grep "INFO" logs/procurement_*.log | grep "API"
```

**Verificación de Base de Datos:**
```python
# Script de verificación
import sqlite3

conn = sqlite3.connect('procurement.db')
cursor = conn.cursor()

# Verificar integridad
cursor.execute('PRAGMA integrity_check')
result = cursor.fetchone()
print(f"Database integrity: {result[0]}")

# Estadísticas de tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"Table {table[0]}: {count} records")

conn.close()
```

### Procedimientos de Recuperación

**Recuperación de Base de Datos:**
```bash
# 1. Detener la aplicación
pkill -f "python main.py"

# 2. Crear respaldo de la base actual
cp procurement.db procurement_backup_$(date +%Y%m%d_%H%M%S).db

# 3. Restaurar desde respaldo
cp backups/database_backup_YYYYMMDD_HHMMSS.db procurement.db

# 4. Verificar integridad
sqlite3 procurement.db "PRAGMA integrity_check;"

# 5. Reiniciar aplicación
cd src && python main.py
```

**Recuperación de Archivos:**
```bash
# 1. Crear respaldo de archivos actuales
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# 2. Restaurar desde respaldo
tar -xzf backups/files_backup_YYYYMMDD_HHMMSS.tar.gz

# 3. Verificar permisos
chmod -R 755 uploads/
```

**Recuperación Completa del Sistema:**
```bash
# 1. Detener todos los servicios
pkill -f "python main.py"

# 2. Crear respaldo completo actual
tar -czf system_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    procurement.db uploads/ logs/ backups/

# 3. Restaurar código de aplicación
tar -xzf sistema_compras_licitaciones.tar.gz

# 4. Restaurar datos
cp backups/database_backup_latest.db procurement.db
tar -xzf backups/files_backup_latest.tar.gz

# 5. Verificar configuración
python -c "import src.main; print('Configuration OK')"

# 6. Reiniciar sistema
cd src && python main.py
```

### Monitoreo Continuo

**Script de Monitoreo:**
```python
#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime

def monitor_system():
    """Monitor system health continuously"""
    
    while True:
        try:
            # Check health endpoint
            response = requests.get('http://localhost:5000/health', timeout=10)
            
            if response.status_code == 200:
                status = response.json()
                if status.get('overall_status') != 'healthy':
                    logging.warning(f"System health issues: {status}")
                else:
                    logging.info("System healthy")
            else:
                logging.error(f"Health check failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Health check request failed: {e}")
            
        except Exception as e:
            logging.error(f"Unexpected error in monitoring: {e}")
            
        # Wait 5 minutes before next check
        time.sleep(300)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    monitor_system()
```

**Alertas Automáticas:**
```python
def send_alert(message, severity='INFO'):
    """Send alert notification"""
    
    # Log the alert
    logging.log(getattr(logging, severity), f"ALERT: {message}")
    
    # Send email notification (if configured)
    if EMAIL_ALERTS_ENABLED:
        send_email_alert(message, severity)
    
    # Write to alert file
    with open('alerts.log', 'a') as f:
        f.write(f"{datetime.now().isoformat()} - {severity} - {message}\n")

# Usage examples
send_alert("Disk space below 10%", "WARNING")
send_alert("Database backup failed", "ERROR")
send_alert("System started successfully", "INFO")
```

Este sistema de gestión de compras y licitaciones versión 2.0 proporciona una solución completa y robusta para la automatización de procesos de adquisición, con capacidades avanzadas de análisis y una arquitectura diseñada para facilidad de uso y mantenimiento.

