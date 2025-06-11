# Guía de Instalación Rápida

## Sistema de Gestión de Compras y Licitaciones

### Requisitos Previos

- **Sistema Operativo:** Windows 10/11, Linux (Ubuntu 18.04+), o macOS 10.14+
- **Python:** Versión 3.8 o superior
- **Memoria RAM:** Mínimo 4 GB (recomendado 8 GB)
- **Espacio en Disco:** Mínimo 10 GB libres
- **Navegador:** Chrome 80+, Firefox 75+, Edge 80+, o Safari 13+

### Instalación Paso a Paso

#### 1. Verificar Python

```bash
# Verificar versión de Python
python --version
# o en Linux/macOS
python3 --version
```

Si Python no está instalado, descárgalo desde [python.org](https://python.org)

#### 2. Extraer el Sistema

Extrae el archivo del sistema en una carpeta de tu elección:
- **Windows:** `C:\procurement_system\`
- **Linux/macOS:** `/opt/procurement_system/` o `~/procurement_system/`

#### 3. Crear Entorno Virtual

```bash
# Navegar al directorio del sistema
cd procurement_system

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/macOS:
source venv/bin/activate
```

#### 4. Instalar Dependencias

```bash
# Con el entorno virtual activado
pip install -r requirements.txt
```

#### 5. Iniciar el Sistema

```bash
# Navegar al directorio src
cd src

# Ejecutar la aplicación
python main.py
```

#### 6. Acceder al Sistema

Abre tu navegador y ve a: `http://localhost:5000`

### Comandos de Inicio Rápido

#### Windows
```batch
cd C:\procurement_system
venv\Scripts\activate
cd src
python main.py
```

#### Linux/macOS
```bash
cd /path/to/procurement_system
source venv/bin/activate
cd src
python main.py
```

### Solución de Problemas Comunes

**Error: "python no se reconoce como comando"**
- Asegúrate de que Python esté instalado y agregado al PATH del sistema

**Error: "Puerto 5000 en uso"**
- Cierra otras aplicaciones que puedan estar usando el puerto 5000
- O modifica el puerto en el archivo `main.py`

**Error de permisos en Linux/macOS**
- Usa `sudo` solo si es necesario
- Verifica los permisos del directorio de instalación

### Configuración Inicial

1. **Primer Acceso:** Ve a `http://localhost:5000`
2. **Crear Datos de Prueba:** Usa la interfaz para crear proveedores y procesos de prueba
3. **Verificar Funcionalidades:** Prueba cargar documentos y generar reportes
4. **Configurar Respaldos:** Establece una rutina de respaldos del directorio completo

### Estructura de Archivos

```
procurement_system/
├── src/
│   ├── main.py              # Archivo principal
│   ├── models/              # Modelos de base de datos
│   ├── routes/              # Rutas de la API
│   ├── static/              # Archivos web (HTML, CSS, JS)
│   └── uploads/             # Documentos cargados
├── venv/                    # Entorno virtual de Python
├── requirements.txt         # Dependencias
├── MANUAL_USUARIO.md        # Manual completo
└── procurement.db           # Base de datos (se crea automáticamente)
```

### Respaldos

**Archivos importantes a respaldar:**
- `procurement.db` (base de datos)
- `src/uploads/` (documentos cargados)
- `src/` (código de la aplicación)

**Comando de respaldo simple:**
```bash
# Crear respaldo completo
tar -czf backup_$(date +%Y%m%d).tar.gz procurement_system/
```

### Soporte

Para problemas técnicos:
1. Consulta el manual completo (`MANUAL_USUARIO.md`)
2. Verifica los logs en la consola donde se ejecuta el sistema
3. Revisa que todos los requisitos estén cumplidos

### Detener el Sistema

Para detener el sistema:
- Presiona `Ctrl+C` en la terminal donde se está ejecutando
- O cierra la ventana de terminal

### Próximos Pasos

1. Lee el manual completo para entender todas las funcionalidades
2. Configura respaldos automáticos
3. Personaliza el sistema según las necesidades de tu organización
4. Capacita a los usuarios en el uso del sistema

---

**¡El sistema está listo para usar!**

Para acceso completo a todas las funcionalidades y configuraciones avanzadas, consulta el `MANUAL_USUARIO.md` incluido en el sistema.

