# Sistema de Gestión de Compras y Licitaciones

## Descripción

Sistema web completo para la gestión de procesos de compra y licitaciones, diseñado para uso local en organizaciones que necesitan administrar adquisiciones de manera eficiente, transparente y profesional.

## Características Principales

### ✅ Gestión Integral de Procesos
- Creación y administración de procesos de compra simple y licitaciones grandes
- Control de estados (borrador, activo, evaluación, completado, cancelado)
- Gestión de fechas y plazos con alertas automáticas
- Seguimiento completo del ciclo de vida de cada proceso

### ✅ Administración de Proveedores
- Base de datos completa de proveedores
- Información de contacto y historial de participación
- Evaluación de desempeño y trazabilidad
- Gestión de declaraciones juradas y documentos legales

### ✅ Gestión Documental Avanzada
- Repositorio centralizado para todos los documentos
- Soporte para múltiples formatos (PDF, Word, Excel, imágenes)
- Control de versiones y trazabilidad de cambios
- Clasificación por tipos: bases de licitación, propuestas técnicas/económicas, contratos
- Descarga segura y organizada de documentos

### ✅ Sistema de Alertas Inteligente
- Alertas automáticas por proximidad de vencimientos
- Notificaciones de documentos faltantes
- Monitoreo de procesos vencidos
- Dashboard de alertas activas con gestión de estados

### ✅ Reportes y Análisis
- Dashboard ejecutivo con métricas clave
- Gráficos de distribución por estado y tipo de proceso
- Análisis de tendencias temporales
- Reportes de desempeño de proveedores
- Comparativos técnicos y económicos
- Exportación de datos en múltiples formatos

### ✅ Interfaz Moderna y Responsiva
- Diseño limpio y profesional con Bootstrap
- Navegación intuitiva y accesible
- Responsive design para desktop y móvil
- Experiencia de usuario optimizada

## Tecnologías Utilizadas

- **Backend:** Python 3.8+ con Flask
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de Datos:** SQLite (fácil instalación) con soporte para MySQL
- **Gráficos:** Chart.js para visualizaciones interactivas
- **Alertas:** APScheduler para notificaciones automáticas

## Instalación Rápida

### Requisitos
- Python 3.8 o superior
- 4 GB RAM mínimo (8 GB recomendado)
- 10 GB espacio en disco
- Navegador web moderno

### Pasos de Instalación

1. **Extraer el sistema** en una carpeta de tu elección
2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```
3. **Activar entorno virtual:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```
4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Iniciar el sistema:**
   ```bash
   cd src
   python main.py
   ```
6. **Acceder al sistema:** `http://localhost:5000`

## Estructura del Proyecto

```
procurement_app/
├── src/
│   ├── main.py                 # Aplicación principal
│   ├── models/
│   │   ├── database.py         # Configuración de base de datos
│   │   └── models.py           # Modelos de datos
│   ├── routes/
│   │   ├── suppliers.py        # API de proveedores
│   │   ├── processes.py        # API de procesos
│   │   ├── documents.py        # API de documentos
│   │   ├── bids.py            # API de ofertas
│   │   ├── alerts.py          # API de alertas
│   │   ├── alerts_scheduler.py # Sistema de alertas automáticas
│   │   └── reports.py         # API de reportes
│   ├── static/
│   │   ├── index.html         # Interfaz principal
│   │   ├── style.css          # Estilos personalizados
│   │   └── app.js             # Lógica del frontend
│   └── uploads/               # Documentos cargados
├── venv/                      # Entorno virtual
├── requirements.txt           # Dependencias
├── MANUAL_USUARIO.md          # Manual completo
├── INSTALACION_RAPIDA.md      # Guía de instalación
└── README.md                  # Este archivo
```

## Funcionalidades Detalladas

### Dashboard Principal
- Contadores de procesos, proveedores, ofertas y alertas
- Gráficos de distribución por estado y tipo
- Lista de procesos recientes
- Panel de alertas activas

### Gestión de Procesos
- Formulario completo para creación de procesos
- Tipos: Compra Simple y Licitación Grande
- Estados controlados con flujo de trabajo
- Fechas de inicio y fin con validaciones
- Campo de notas para información adicional

### Gestión de Proveedores
- Registro completo de información de contacto
- Historial de participación en procesos
- Evaluaciones de desempeño
- Gestión de documentos asociados

### Gestión de Documentos
- Carga de archivos con validación de tipos
- Clasificación automática por categorías
- Asociación con procesos y proveedores
- Control de versiones básico
- Descarga segura de archivos

### Sistema de Alertas
- Verificación automática de vencimientos
- Alertas de documentos faltantes
- Notificaciones configurables
- Gestión de estados (activa/descartada)

### Reportes y Análisis
- Métricas de rendimiento en tiempo real
- Gráficos interactivos con Chart.js
- Análisis de tendencias temporales
- Comparativos de proveedores
- Exportación de datos

## Seguridad y Respaldos

### Características de Seguridad
- Validación de tipos de archivo
- Sanitización de nombres de archivo
- Control de acceso a documentos
- Logs de actividad del sistema

### Respaldos Recomendados
- Base de datos SQLite (`procurement.db`)
- Directorio de documentos (`src/uploads/`)
- Archivos de configuración
- Respaldos automáticos programados

## Casos de Uso

### Organizaciones Pequeñas y Medianas
- Gestión centralizada de compras
- Control de proveedores locales
- Documentación organizada
- Reportes básicos de gestión

### Instituciones Gubernamentales
- Transparencia en procesos de licitación
- Trazabilidad completa de documentos
- Cumplimiento de plazos legales
- Auditoría de procesos

### Empresas Corporativas
- Gestión de múltiples procesos simultáneos
- Evaluación de proveedores estratégicos
- Análisis de tendencias de compra
- Optimización de procesos

## Ventajas del Sistema

### ✅ **Instalación Simple**
- Sin servidores complejos
- Base de datos embebida
- Configuración mínima requerida

### ✅ **Uso Local y Seguro**
- No requiere conexión a Internet
- Datos almacenados localmente
- Control total sobre la información

### ✅ **Interfaz Intuitiva**
- Diseño moderno y profesional
- Navegación clara y lógica
- Responsive para todos los dispositivos

### ✅ **Funcionalidad Completa**
- Cubre todo el ciclo de compras
- Alertas automáticas inteligentes
- Reportes y análisis avanzados

### ✅ **Escalable y Personalizable**
- Arquitectura modular
- Fácil de extender
- Adaptable a necesidades específicas

## Soporte y Documentación

- **Manual Completo:** `MANUAL_USUARIO.md` (50+ páginas)
- **Guía de Instalación:** `INSTALACION_RAPIDA.md`
- **Código Documentado:** Comentarios en español
- **Arquitectura Clara:** Separación de responsabilidades

## Requisitos Técnicos Detallados

### Hardware Mínimo
- **CPU:** 2 núcleos, 2.0 GHz
- **RAM:** 4 GB
- **Disco:** 10 GB libres
- **Red:** No requerida (uso local)

### Hardware Recomendado
- **CPU:** 4 núcleos, 2.5 GHz
- **RAM:** 8 GB o más
- **Disco:** SSD con 50 GB libres
- **Red:** LAN para acceso multi-usuario

### Software Compatible
- **Windows:** 10, 11, Server 2016+
- **Linux:** Ubuntu 18.04+, CentOS 7+, Debian 9+
- **macOS:** 10.14 (Mojave) o superior
- **Python:** 3.8, 3.9, 3.10, 3.11
- **Navegadores:** Chrome 80+, Firefox 75+, Edge 80+, Safari 13+

## Licencia y Uso

Este sistema ha sido desarrollado para uso organizacional interno. Incluye todas las funcionalidades necesarias para la gestión profesional de procesos de compra y licitaciones.

## Contacto

Para soporte técnico, consultas sobre personalización, o asistencia en la implementación, contacta al equipo de desarrollo a través de los canales establecidos por tu organización.

---

**¡Sistema listo para producción!** 🚀

Consulta el `MANUAL_USUARIO.md` para información detallada sobre todas las funcionalidades y mejores prácticas de uso.

