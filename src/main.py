import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.database import db
from src.models.models import *
from src.models.excel_models import *
from src.routes.suppliers import suppliers_bp
from src.routes.processes import processes_bp
from src.routes.documents import documents_bp
from src.routes.bids import bids_bp
from src.routes.alerts import alerts_bp
from src.routes.reports import reports_bp
from src.routes.alerts_scheduler import alerts_scheduler_bp
from src.routes.excel_routes import excel_bp

# Robustness setup
try:
    from robustness_improvements import setup_logging, SystemMonitor, BackupManager
    logger = setup_logging()
    ROBUSTNESS_ENABLED = True
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('procurement_system')
    ROBUSTNESS_ENABLED = False
    logger.warning("Robustness improvements not available")

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'procurement_secret_key_2024'

# Configuración de conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://procure_user:238923Fc.@localhost:3306/procurement_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# CORS
CORS(app)

# Registrar blueprints
app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
app.register_blueprint(processes_bp, url_prefix='/api/processes')
app.register_blueprint(documents_bp, url_prefix='/api/documents')
app.register_blueprint(bids_bp, url_prefix='/api/bids')
app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(alerts_scheduler_bp, url_prefix='/api/alerts-scheduler')
app.register_blueprint(excel_bp, url_prefix='/api/excel')

# Inicializar DB
db.init_app(app)

# Inicializar backups si aplica
if ROBUSTNESS_ENABLED:
    backup_manager = BackupManager()

@app.route('/health')
def health_check():
    try:
        if ROBUSTNESS_ENABLED:
            status = SystemMonitor.get_system_status()
            return jsonify(status), 200 if status['overall_status'] == 'healthy' else 503
        else:
            return jsonify({'status': 'ok', 'message': 'Basic health check passed'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/backup', methods=['POST'])
def create_backup():
    try:
        if not ROBUSTNESS_ENABLED:
            return jsonify({'success': False, 'message': 'Backup functionality not available'}), 503

        db_backup = backup_manager.create_database_backup()
        files_backup = backup_manager.create_files_backup()
        logger.info(f"Backup created successfully: DB={db_backup}, Files={files_backup}")

        return jsonify({
            'success': True,
            'message': 'Backup creado exitosamente',
            'database_backup': db_backup,
            'files_backup': files_backup
        })
    except Exception as e:
        logger.error(f"Backup creation failed: {str(e)}")
        return jsonify({'success': False, 'message': f'Error creando backup: {str(e)}'}), 500

@app.route('/api/system/status')
def system_status():
    try:
        if ROBUSTNESS_ENABLED:
            status = SystemMonitor.get_system_status()
        else:
            status = {
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'basic',
                'message': 'Sistema funcionando en modo básico'
            }
        return jsonify(status)
    except Exception as e:
        logger.error(f"System status check failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {error}")
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(413)
def file_too_large(error):
    logger.warning(f"File too large: {error}")
    return jsonify({'error': 'Archivo muy grande. Máximo 16MB permitido'}), 413

with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")

        if ROBUSTNESS_ENABLED:
            status = SystemMonitor.get_system_status()
            if status['overall_status'] != 'healthy':
                logger.warning(f"System health issues detected: {status}")
            backup_manager.cleanup_old_backups()
    except Exception as e:
        logger.error(f"Application initialization failed: {str(e)}")
        raise

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# 🔥 Esta es la sección modificada para Heroku:
if __name__ == '__main__':
    try:
        logger.info("Starting Procurement Management System...")
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
