# Mejoras de Robustez y Validaciones

## Validaciones de Datos para Archivos Excel

import pandas as pd
from datetime import datetime
import re

class ExcelDataValidator:
    """Clase para validar datos de archivos Excel antes de procesarlos"""
    
    @staticmethod
    def validate_process_tracking_data(df):
        """Validar datos de seguimiento de procesos"""
        errors = []
        warnings = []
        
        # Verificar columnas requeridas
        required_columns = ['N°', 'CÓDIGO', 'NOMBRE DEL PROCESO', 'TIPO', 'ÁREA SOLICITANTE']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        # Validar datos por fila
        for index, row in df.iterrows():
            if pd.isna(row.get('N°')) or row.get('N°') == '':
                continue  # Saltar filas vacías
            
            # Validar número de proceso
            if not isinstance(row.get('N°'), (int, float)) or row.get('N°') <= 0:
                errors.append(f"Fila {index + 1}: Número de proceso inválido")
            
            # Validar nombre del proceso
            if pd.isna(row.get('NOMBRE DEL PROCESO')) or len(str(row.get('NOMBRE DEL PROCESO')).strip()) < 3:
                errors.append(f"Fila {index + 1}: Nombre del proceso muy corto o vacío")
            
            # Validar tipo de proceso
            valid_types = ['Compra Simple', 'Licitación Pequeña', 'Licitación Grande', 'Contratación Directa']
            if row.get('TIPO') not in valid_types:
                warnings.append(f"Fila {index + 1}: Tipo de proceso no estándar: {row.get('TIPO')}")
            
            # Validar presupuesto
            if not pd.isna(row.get('PRESUPUESTO')):
                try:
                    budget = float(row.get('PRESUPUESTO'))
                    if budget < 0:
                        errors.append(f"Fila {index + 1}: Presupuesto no puede ser negativo")
                except (ValueError, TypeError):
                    errors.append(f"Fila {index + 1}: Presupuesto debe ser un número")
            
            # Validar fechas
            for date_col in ['FECHA INICIO', 'FECHA CIERRE']:
                if not pd.isna(row.get(date_col)):
                    try:
                        pd.to_datetime(row.get(date_col))
                    except:
                        errors.append(f"Fila {index + 1}: Formato de fecha inválido en {date_col}")
        
        return {'errors': errors, 'warnings': warnings, 'is_valid': len(errors) == 0}
    
    @staticmethod
    def validate_technical_evaluation_data(df):
        """Validar datos de evaluación técnica"""
        errors = []
        warnings = []
        
        # Verificar columnas requeridas
        required_columns = ['N°', 'CRITERIO', 'PESO %']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        total_weight = 0
        
        for index, row in df.iterrows():
            if pd.isna(row.get('N°')) or row.get('N°') == '':
                continue
            
            # Validar criterio
            if pd.isna(row.get('CRITERIO')) or len(str(row.get('CRITERIO')).strip()) < 2:
                errors.append(f"Fila {index + 1}: Criterio vacío o muy corto")
            
            # Validar peso
            if not pd.isna(row.get('PESO %')):
                try:
                    weight = float(row.get('PESO %'))
                    if weight < 0 or weight > 100:
                        errors.append(f"Fila {index + 1}: Peso debe estar entre 0 y 100")
                    total_weight += weight
                except (ValueError, TypeError):
                    errors.append(f"Fila {index + 1}: Peso debe ser un número")
            
            # Validar puntuaciones de proveedores
            for i in range(1, 4):
                score_col = f'PROVEEDOR {i}'
                if not pd.isna(row.get(score_col)):
                    try:
                        score = float(row.get(score_col))
                        if score < 0 or score > 5:
                            warnings.append(f"Fila {index + 1}: Puntuación de {score_col} fuera del rango 0-5")
                    except (ValueError, TypeError):
                        errors.append(f"Fila {index + 1}: Puntuación de {score_col} debe ser un número")
        
        # Verificar que los pesos sumen 100%
        if abs(total_weight - 100) > 0.1 and total_weight > 0:
            warnings.append(f"Los pesos totales suman {total_weight}% en lugar de 100%")
        
        return {'errors': errors, 'warnings': warnings, 'is_valid': len(errors) == 0}
    
    @staticmethod
    def validate_economic_comparison_data(df):
        """Validar datos de comparativo económico"""
        errors = []
        warnings = []
        
        # Verificar columnas requeridas
        required_columns = ['ÍTEM', 'DESCRIPCIÓN', 'CANTIDAD']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        for index, row in df.iterrows():
            if pd.isna(row.get('ÍTEM')) or row.get('ÍTEM') == '':
                continue
            
            # Validar descripción
            if pd.isna(row.get('DESCRIPCIÓN')) or len(str(row.get('DESCRIPCIÓN')).strip()) < 3:
                errors.append(f"Fila {index + 1}: Descripción muy corta o vacía")
            
            # Validar cantidad
            if not pd.isna(row.get('CANTIDAD')):
                try:
                    quantity = float(row.get('CANTIDAD'))
                    if quantity <= 0:
                        errors.append(f"Fila {index + 1}: Cantidad debe ser mayor a 0")
                except (ValueError, TypeError):
                    errors.append(f"Fila {index + 1}: Cantidad debe ser un número")
            
            # Validar precios de proveedores
            for i in range(1, 4):
                price_col = f'PROVEEDOR {i}'
                if not pd.isna(row.get(price_col)):
                    try:
                        price = float(row.get(price_col))
                        if price < 0:
                            errors.append(f"Fila {index + 1}: Precio de {price_col} no puede ser negativo")
                    except (ValueError, TypeError):
                        errors.append(f"Fila {index + 1}: Precio de {price_col} debe ser un número")
        
        return {'errors': errors, 'warnings': warnings, 'is_valid': len(errors) == 0}
    
    @staticmethod
    def validate_savings_analysis_data(df):
        """Validar datos de análisis de ahorros"""
        errors = []
        warnings = []
        
        # Verificar columnas requeridas
        required_columns = ['CONCEPTO', 'PRESUPUESTO', 'PRECIO FINAL']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        for index, row in df.iterrows():
            if pd.isna(row.get('CONCEPTO')) or row.get('CONCEPTO') == '':
                continue
            
            # Validar concepto
            valid_concepts = ['Bienes', 'Servicios', 'Otros', 'TOTAL']
            if row.get('CONCEPTO') not in valid_concepts:
                warnings.append(f"Fila {index + 1}: Concepto no estándar: {row.get('CONCEPTO')}")
            
            # Validar presupuesto
            if not pd.isna(row.get('PRESUPUESTO')):
                try:
                    budget = float(row.get('PRESUPUESTO'))
                    if budget < 0:
                        errors.append(f"Fila {index + 1}: Presupuesto no puede ser negativo")
                except (ValueError, TypeError):
                    errors.append(f"Fila {index + 1}: Presupuesto debe ser un número")
            
            # Validar precio final
            if not pd.isna(row.get('PRECIO FINAL')):
                try:
                    final_price = float(row.get('PRECIO FINAL'))
                    if final_price < 0:
                        errors.append(f"Fila {index + 1}: Precio final no puede ser negativo")
                except (ValueError, TypeError):
                    errors.append(f"Fila {index + 1}: Precio final debe ser un número")
            
            # Validar coherencia entre presupuesto y precio final
            if (not pd.isna(row.get('PRESUPUESTO')) and not pd.isna(row.get('PRECIO FINAL'))):
                try:
                    budget = float(row.get('PRESUPUESTO'))
                    final_price = float(row.get('PRECIO FINAL'))
                    if final_price > budget * 1.5:  # Permitir hasta 50% de exceso
                        warnings.append(f"Fila {index + 1}: Precio final significativamente mayor al presupuesto")
                except (ValueError, TypeError):
                    pass  # Ya se validó arriba
        
        return {'errors': errors, 'warnings': warnings, 'is_valid': len(errors) == 0}

## Manejo de Errores Mejorado

class ProcurementException(Exception):
    """Excepción base para errores del sistema de procurement"""
    pass

class ValidationError(ProcurementException):
    """Error de validación de datos"""
    pass

class FileProcessingError(ProcurementException):
    """Error en el procesamiento de archivos"""
    pass

class DatabaseError(ProcurementException):
    """Error de base de datos"""
    pass

## Logging Mejorado

import logging
import os
from datetime import datetime

def setup_logging():
    """Configurar sistema de logging"""
    
    # Crear directorio de logs si no existe
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formato de logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurar logging para archivo
    log_filename = os.path.join(log_dir, f'procurement_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # También mostrar en consola
        ]
    )
    
    return logging.getLogger('procurement_system')

## Configuración de Seguridad

class SecurityConfig:
    """Configuración de seguridad para el sistema"""
    
    # Tamaños máximos de archivo
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_FILENAME_LENGTH = 255
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.pdf', '.doc', '.docx', '.txt'}
    
    # Patrones de nombres de archivo peligrosos
    DANGEROUS_PATTERNS = [
        r'\.\./',  # Path traversal
        r'[<>:"|?*]',  # Caracteres peligrosos en Windows
        r'^\.',  # Archivos ocultos
        r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)',  # Nombres reservados Windows
    ]
    
    @classmethod
    def validate_filename(cls, filename):
        """Validar nombre de archivo por seguridad"""
        if not filename or len(filename) > cls.MAX_FILENAME_LENGTH:
            return False, "Nombre de archivo inválido o muy largo"
        
        # Verificar patrones peligrosos
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, filename, re.IGNORECASE):
                return False, f"Nombre de archivo contiene caracteres no permitidos"
        
        # Verificar extensión
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            return False, f"Extensión de archivo no permitida: {file_ext}"
        
        return True, "Archivo válido"
    
    @classmethod
    def validate_file_size(cls, file_size):
        """Validar tamaño de archivo"""
        if file_size > cls.MAX_FILE_SIZE:
            return False, f"Archivo muy grande. Máximo permitido: {cls.MAX_FILE_SIZE / (1024*1024):.1f} MB"
        
        return True, "Tamaño válido"

## Backup y Recuperación

import shutil
import json
from datetime import datetime, timedelta

class BackupManager:
    """Gestor de respaldos del sistema"""
    
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def create_database_backup(self):
        """Crear respaldo de la base de datos"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'database_backup_{timestamp}.db'
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copiar archivo de base de datos SQLite
            db_path = 'procurement.db'
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path)
                return backup_path
            else:
                raise FileNotFoundError("Archivo de base de datos no encontrado")
                
        except Exception as e:
            raise DatabaseError(f"Error creando respaldo de base de datos: {str(e)}")
    
    def create_files_backup(self):
        """Crear respaldo de archivos subidos"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'files_backup_{timestamp}.tar.gz'
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Crear archivo tar.gz con todos los archivos
            uploads_dir = 'uploads'
            if os.path.exists(uploads_dir):
                shutil.make_archive(
                    backup_path.replace('.tar.gz', ''),
                    'gztar',
                    uploads_dir
                )
                return backup_path
            else:
                raise FileNotFoundError("Directorio de uploads no encontrado")
                
        except Exception as e:
            raise FileProcessingError(f"Error creando respaldo de archivos: {str(e)}")
    
    def cleanup_old_backups(self, days_to_keep=30):
        """Limpiar respaldos antiguos"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        
        except Exception as e:
            logging.warning(f"Error limpiando respaldos antiguos: {str(e)}")
    
    def restore_database(self, backup_path):
        """Restaurar base de datos desde respaldo"""
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError("Archivo de respaldo no encontrado")
            
            # Crear respaldo de la base actual antes de restaurar
            current_backup = self.create_database_backup()
            
            # Restaurar desde respaldo
            shutil.copy2(backup_path, 'procurement.db')
            
            return True, f"Base de datos restaurada. Respaldo actual guardado en: {current_backup}"
            
        except Exception as e:
            return False, f"Error restaurando base de datos: {str(e)}"

## Monitoreo del Sistema

class SystemMonitor:
    """Monitor del sistema para detectar problemas"""
    
    @staticmethod
    def check_disk_space(min_free_gb=1):
        """Verificar espacio en disco disponible"""
        try:
            statvfs = os.statvfs('.')
            free_bytes = statvfs.f_frsize * statvfs.f_bavail
            free_gb = free_bytes / (1024**3)
            
            if free_gb < min_free_gb:
                return False, f"Espacio en disco bajo: {free_gb:.2f} GB disponibles"
            
            return True, f"Espacio en disco suficiente: {free_gb:.2f} GB disponibles"
            
        except Exception as e:
            return False, f"Error verificando espacio en disco: {str(e)}"
    
    @staticmethod
    def check_database_integrity():
        """Verificar integridad de la base de datos"""
        try:
            from src.models.database import db
            
            # Intentar una consulta simple
            result = db.session.execute('SELECT 1').fetchone()
            
            if result:
                return True, "Base de datos funcionando correctamente"
            else:
                return False, "Error en consulta de prueba"
                
        except Exception as e:
            return False, f"Error verificando base de datos: {str(e)}"
    
    @staticmethod
    def check_upload_directory():
        """Verificar directorio de uploads"""
        upload_dirs = ['uploads', 'uploads/documents', 'uploads/excel']
        
        for dir_path in upload_dirs:
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except Exception as e:
                    return False, f"Error creando directorio {dir_path}: {str(e)}"
        
        return True, "Directorios de upload verificados"
    
    @staticmethod
    def get_system_status():
        """Obtener estado general del sistema"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # Verificar espacio en disco
        disk_ok, disk_msg = SystemMonitor.check_disk_space()
        status['checks']['disk_space'] = {'status': 'ok' if disk_ok else 'warning', 'message': disk_msg}
        
        # Verificar base de datos
        db_ok, db_msg = SystemMonitor.check_database_integrity()
        status['checks']['database'] = {'status': 'ok' if db_ok else 'error', 'message': db_msg}
        
        # Verificar directorios
        dir_ok, dir_msg = SystemMonitor.check_upload_directory()
        status['checks']['directories'] = {'status': 'ok' if dir_ok else 'error', 'message': dir_msg}
        
        # Estado general
        all_ok = disk_ok and db_ok and dir_ok
        status['overall_status'] = 'healthy' if all_ok else 'issues_detected'
        
        return status

## Configuración de Performance

class PerformanceConfig:
    """Configuración para optimizar rendimiento"""
    
    # Configuración de cache
    CACHE_TIMEOUT = 300  # 5 minutos
    MAX_CACHE_SIZE = 100  # Máximo 100 elementos en cache
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Configuración de archivos
    CHUNK_SIZE = 8192  # Tamaño de chunk para lectura de archivos
    
    @staticmethod
    def optimize_database_queries():
        """Optimizar consultas de base de datos"""
        # Aquí se pueden agregar índices y optimizaciones específicas
        pass

## Utilidades de Desarrollo y Testing

class TestDataGenerator:
    """Generador de datos de prueba"""
    
    @staticmethod
    def generate_sample_process_tracking():
        """Generar datos de muestra para seguimiento de procesos"""
        sample_data = {
            'N°': [1, 2, 3, 4, 5],
            'CÓDIGO': ['PROC-2024-001', 'PROC-2024-002', 'PROC-2024-003', 'PROC-2024-004', 'PROC-2024-005'],
            'NOMBRE DEL PROCESO': [
                'Adquisición de Equipos de Oficina',
                'Contratación de Servicios de Limpieza',
                'Compra de Material de Construcción',
                'Licitación de Vehículos',
                'Servicios de Consultoría IT'
            ],
            'TIPO': ['Compra Simple', 'Licitación Pequeña', 'Licitación Grande', 'Licitación Grande', 'Compra Simple'],
            'ÁREA SOLICITANTE': ['Administración', 'Servicios Generales', 'Obras', 'Transporte', 'IT'],
            'PRESUPUESTO': [50000, 120000, 500000, 800000, 75000],
            'FECHA INICIO': ['2024-01-15', '2024-02-01', '2024-02-15', '2024-03-01', '2024-03-15'],
            'FECHA CIERRE': ['2024-02-15', '2024-03-15', '2024-04-30', '2024-05-30', '2024-04-15'],
            'ESTADO': ['Completado', 'En Evaluación', 'Activo', 'Borrador', 'Completado'],
            'PROVEEDORES': [3, 5, 8, 6, 2],
            'PROVEEDOR ADJUDICADO': ['OfficeMax SA', 'CleanPro Ltda', '', '', 'TechConsult SRL'],
            'OBSERVACIONES': ['Proceso exitoso', 'Pendiente evaluación técnica', 'En proceso', 'Esperando aprobación', 'Adjudicado']
        }
        
        return pd.DataFrame(sample_data)
    
    @staticmethod
    def generate_sample_technical_evaluation():
        """Generar datos de muestra para evaluación técnica"""
        sample_data = {
            'N°': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'CRITERIO': [
                'Experiencia', 'Capacidad Técnica', 'Metodología', 'Calidad',
                'Cumplimiento', 'Servicio Post-Venta', 'Innovación', 
                'Sostenibilidad', 'Capacidad Financiera', 'Referencias'
            ],
            'DESCRIPCIÓN': [
                'Años de experiencia en el rubro',
                'Capacidad técnica del equipo',
                'Metodología de trabajo propuesta',
                'Calidad de productos/servicios',
                'Historial de cumplimiento',
                'Calidad del servicio post-venta',
                'Nivel de innovación propuesto',
                'Prácticas sostenibles',
                'Solidez financiera',
                'Referencias de trabajos anteriores'
            ],
            'PESO %': [15, 20, 15, 20, 10, 5, 5, 5, 3, 2],
            'PROVEEDOR 1': [4.2, 4.5, 4.0, 4.3, 4.1, 3.8, 3.5, 4.0, 4.2, 4.1],
            'PONDERACIÓN 1': [63, 90, 60, 86, 41, 19, 17.5, 20, 12.6, 8.2],
            'PROVEEDOR 2': [3.8, 4.0, 4.2, 3.9, 4.3, 4.1, 4.0, 3.7, 3.9, 4.0],
            'PONDERACIÓN 2': [57, 80, 63, 78, 43, 20.5, 20, 18.5, 11.7, 8.0],
            'PROVEEDOR 3': [4.0, 3.7, 3.8, 4.1, 3.9, 3.9, 3.8, 4.2, 4.0, 3.8],
            'PONDERACIÓN 3': [60, 74, 57, 82, 39, 19.5, 19, 21, 12, 7.6]
        }
        
        return pd.DataFrame(sample_data)
    
    @staticmethod
    def generate_sample_economic_comparison():
        """Generar datos de muestra para comparativo económico"""
        sample_data = {
            'ÍTEM': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'DESCRIPCIÓN': [
                'Computadoras de escritorio',
                'Monitores LED 24"',
                'Teclados inalámbricos',
                'Mouse ópticos',
                'Impresoras multifunción',
                'Papel bond A4',
                'Cartuchos de tinta',
                'Sillas ergonómicas',
                'Escritorios modulares',
                'Archivadores metálicos'
            ],
            'CANTIDAD': [25, 25, 30, 30, 5, 100, 20, 25, 15, 10],
            'UNIDAD': ['Unidad', 'Unidad', 'Unidad', 'Unidad', 'Unidad', 'Resma', 'Unidad', 'Unidad', 'Unidad', 'Unidad'],
            'PROVEEDOR 1': [850, 320, 45, 25, 450, 8.5, 35, 280, 650, 180],
            'PROVEEDOR 2': [820, 310, 42, 23, 420, 8.0, 32, 270, 620, 175],
            'PROVEEDOR 3': [880, 330, 48, 27, 480, 9.0, 38, 290, 680, 185],
            'MEJOR OFERTA': ['Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2', 'Proveedor 2']
        }
        
        return pd.DataFrame(sample_data)
    
    @staticmethod
    def generate_sample_savings_analysis():
        """Generar datos de muestra para análisis de ahorros"""
        sample_data = {
            'CONCEPTO': ['Bienes', 'Servicios', 'Otros', 'TOTAL'],
            'PRESUPUESTO': [300000, 150000, 50000, 500000],
            'PRECIO INICIAL': [320000, 160000, 55000, 535000],
            'PRECIO FINAL': [280000, 140000, 45000, 465000],
            'AHORRO VS PRESUPUESTO': [20000, 10000, 5000, 35000],
            '% AHORRO': [6.67, 6.67, 10.0, 7.0],
            'AHORRO VS PRECIO INICIAL': [40000, 20000, 10000, 70000],
            '% AHORRO INICIAL': [12.5, 12.5, 18.18, 13.08],
            'OBSERVACIONES': [
                'Ahorro por negociación de volumen',
                'Optimización de especificaciones',
                'Eliminación de items innecesarios',
                'Ahorro total del proceso'
            ]
        }
        
        return pd.DataFrame(sample_data)

