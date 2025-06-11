from flask import Blueprint, request, jsonify, send_file
from src.models.database import db
from src.models.models import ProcurementProcess, Supplier
from src.models.excel_models import *
import pandas as pd
import io
import os
from datetime import datetime
from werkzeug.utils import secure_filename

excel_bp = Blueprint('excel', __name__)

# Configuración para archivos Excel
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
UPLOAD_FOLDER = 'uploads/excel'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# ==================== PLANTILLAS EXCEL ====================

@excel_bp.route('/templates/process-tracking', methods=['GET'])
def download_process_tracking_template():
    """Descargar plantilla de seguimiento de procesos"""
    
    # Crear DataFrame con estructura de la plantilla
    data = {
        'N°': [1, 2, 3],
        'CÓDIGO': ['', '', ''],
        'NOMBRE DEL PROCESO': ['', '', ''],
        'TIPO': ['', '', ''],
        'ÁREA SOLICITANTE': ['', '', ''],
        'PRESUPUESTO': ['', '', ''],
        'FECHA INICIO': ['', '', ''],
        'FECHA CIERRE': ['', '', ''],
        'ESTADO': ['', '', ''],
        'PROVEEDORES': ['', '', ''],
        'PROVEEDOR ADJUDICADO': ['', '', ''],
        'OBSERVACIONES': ['', '', '']
    }
    
    df = pd.DataFrame(data)
    
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Agregar metadatos
        metadata_df = pd.DataFrame({
            'SEGUIMIENTO DE PROCESOS DE LICITACIÓN': [''],
            'Unnamed: 1': [''],
            'Unnamed: 2': [''],
            'Unnamed: 3': [''],
            'Unnamed: 4': [''],
            'Unnamed: 5': [''],
            'Unnamed: 6': [''],
            'Unnamed: 7': [''],
            'Unnamed: 8': [''],
            'Unnamed: 9': [''],
            'Unnamed: 10': [''],
            'Unnamed: 11': ['']
        })
        
        # Escribir metadatos
        metadata_df.to_excel(writer, sheet_name='Seguimiento', index=False, startrow=0)
        
        # Agregar campos de metadatos
        worksheet = writer.sheets['Seguimiento']
        worksheet['A3'] = 'Responsable:'
        worksheet['A4'] = 'Departamento:'
        worksheet['A5'] = 'Fecha de actualización:'
        
        # Escribir datos principales
        df.to_excel(writer, sheet_name='Seguimiento', index=False, startrow=6)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='Plantilla_Seguimiento_Procesos.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@excel_bp.route('/templates/technical-evaluation', methods=['GET'])
def download_technical_evaluation_template():
    """Descargar plantilla de evaluación técnica"""
    
    data = {
        'N°': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'CRITERIO': [
            'Experiencia', 'Capacidad Técnica', 'Metodología', 'Calidad',
            'Cumplimiento', 'Servicio Post-Venta', 'Innovación', 
            'Sostenibilidad', 'Capacidad Financiera', 'Referencias'
        ],
        'DESCRIPCIÓN': [''] * 10,
        'PESO %': [''] * 10,
        'PROVEEDOR 1': [''] * 10,
        'PONDERACIÓN 1': [''] * 10,
        'PROVEEDOR 2': [''] * 10,
        'PONDERACIÓN 2': [''] * 10,
        'PROVEEDOR 3': [''] * 10,
        'PONDERACIÓN 3': [''] * 10
    }
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Evaluación Técnica', index=False)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='Plantilla_Evaluacion_Tecnica.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@excel_bp.route('/templates/economic-comparison', methods=['GET'])
def download_economic_comparison_template():
    """Descargar plantilla de comparativo económico"""
    
    data = {
        'ÍTEM': [1, 2, 3, 4, 5],
        'DESCRIPCIÓN': ['', '', '', '', ''],
        'CANTIDAD': ['', '', '', '', ''],
        'UNIDAD': ['', '', '', '', ''],
        'PROVEEDOR 1': ['', '', '', '', ''],
        'PROVEEDOR 2': ['', '', '', '', ''],
        'PROVEEDOR 3': ['', '', '', '', ''],
        'MEJOR OFERTA': ['', '', '', '', '']
    }
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Agregar metadatos
        worksheet = writer.book.create_sheet('Comparativo Económico')
        worksheet['A1'] = 'COMPARATIVO DE PROPUESTAS ECONÓMICAS'
        worksheet['A3'] = 'Nombre Proceso:'
        worksheet['A4'] = 'Fecha:'
        worksheet['A5'] = 'Negociador:'
        worksheet['A6'] = 'Presupuesto Aprobado:'
        worksheet['A7'] = 'N° CAPEX/OPEX:'
        
        # Escribir datos principales
        df.to_excel(writer, sheet_name='Comparativo Económico', index=False, startrow=9)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='Plantilla_Comparativo_Economico.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@excel_bp.route('/templates/savings-analysis', methods=['GET'])
def download_savings_analysis_template():
    """Descargar plantilla de análisis de ahorros"""
    
    data = {
        'CONCEPTO': ['Bienes', 'Servicios', 'Otros', 'TOTAL'],
        'PRESUPUESTO': ['', '', '', ''],
        'PRECIO INICIAL': ['', '', '', ''],
        'PRECIO FINAL': ['', '', '', ''],
        'AHORRO VS PRESUPUESTO': ['', '', '', ''],
        '% AHORRO': ['', '', '', ''],
        'AHORRO VS PRECIO INICIAL': ['', '', '', ''],
        '% AHORRO INICIAL': ['', '', '', ''],
        'OBSERVACIONES': ['', '', '', '']
    }
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Análisis de Ahorros', index=False)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='Plantilla_Analisis_Ahorros.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@excel_bp.route('/templates/questions-answers', methods=['GET'])
def download_questions_answers_template():
    """Descargar plantilla de consultas y respuestas"""
    
    data = {
        'N° CONSULTA': [1, 2, 3, 4, 5],
        'FECHA CONSULTA': ['', '', '', '', ''],
        'PROVEEDOR': ['', '', '', '', ''],
        'DOCUMENTO REFERENCIA': ['', '', '', '', ''],
        'SECCIÓN/CLÁUSULA': ['', '', '', '', ''],
        'CONSULTA': ['', '', '', '', ''],
        'RESPUESTA': ['', '', '', '', ''],
        'FECHA RESPUESTA': ['', '', '', '', ''],
        'RESPONDIDO POR': ['', '', '', '', ''],
        'ESTADO': ['', '', '', '', '']
    }
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Consultas y Respuestas', index=False)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='Plantilla_Consultas_Respuestas.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ==================== EXPORTACIÓN DE DATOS ====================

@excel_bp.route('/export/suppliers', methods=['GET'])
def export_suppliers():
    """Exportar lista de proveedores a Excel"""
    
    suppliers = Supplier.query.all()
    
    data = []
    for supplier in suppliers:
        data.append({
            'ID': supplier.id,
            'Nombre': supplier.name,
            'Contacto': supplier.contact_person,
            'Email': supplier.email,
            'Teléfono': supplier.phone,
            'Dirección': supplier.address,
            'Fecha Registro': supplier.created_at.strftime('%Y-%m-%d') if supplier.created_at else '',
            'Notas': supplier.notes or ''
        })
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Proveedores', index=False)
        
        # Ajustar ancho de columnas
        worksheet = writer.sheets['Proveedores']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f'Lista_Proveedores_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@excel_bp.route('/export/processes', methods=['GET'])
def export_processes():
    """Exportar lista de procesos a Excel"""
    
    processes = ProcurementProcess.query.all()
    
    data = []
    for process in processes:
        data.append({
            'ID': process.id,
            'Título': process.title,
            'Tipo': process.process_type,
            'Estado': process.status,
            'Fecha Inicio': process.start_date.strftime('%Y-%m-%d') if process.start_date else '',
            'Fecha Fin': process.end_date.strftime('%Y-%m-%d') if process.end_date else '',
            'Descripción': process.description or '',
            'Notas': process.notes or '',
            'Fecha Creación': process.created_at.strftime('%Y-%m-%d') if process.created_at else ''
        })
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Procesos', index=False)
        
        # Ajustar ancho de columnas
        worksheet = writer.sheets['Procesos']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f'Lista_Procesos_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ==================== CARGA DE ARCHIVOS EXCEL ====================

@excel_bp.route('/upload/process-tracking', methods=['POST'])
def upload_process_tracking():
    """Cargar archivo de seguimiento de procesos"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400
    
    try:
        # Leer archivo Excel
        df = pd.read_excel(file, header=6)  # Los datos empiezan en la fila 7
        
        created_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            if pd.isna(row['N°']) or row['N°'] == '':
                continue
                
            # Buscar proceso existente por código o crear nuevo
            tracking = ProcessTracking.query.filter_by(code=row.get('CÓDIGO')).first()
            
            if not tracking:
                tracking = ProcessTracking()
                created_count += 1
            else:
                updated_count += 1
            
            # Actualizar datos
            tracking.code = row.get('CÓDIGO')
            tracking.process_name = row.get('NOMBRE DEL PROCESO')
            tracking.process_type = row.get('TIPO')
            tracking.requesting_area = row.get('ÁREA SOLICITANTE')
            tracking.budget = pd.to_numeric(row.get('PRESUPUESTO'), errors='ignore')
            
            # Convertir fechas
            if not pd.isna(row.get('FECHA INICIO')):
                tracking.start_date = pd.to_datetime(row.get('FECHA INICIO')).date()
            if not pd.isna(row.get('FECHA CIERRE')):
                tracking.close_date = pd.to_datetime(row.get('FECHA CIERRE')).date()
            
            tracking.status = row.get('ESTADO')
            tracking.suppliers_count = pd.to_numeric(row.get('PROVEEDORES'), errors='ignore')
            tracking.awarded_supplier = row.get('PROVEEDOR ADJUDICADO')
            tracking.observations = row.get('OBSERVACIONES')
            tracking.updated_at = datetime.utcnow()
            
            db.session.add(tracking)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Archivo procesado exitosamente',
            'created': created_count,
            'updated': updated_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error procesando archivo: {str(e)}'}), 500

@excel_bp.route('/upload/technical-evaluation', methods=['POST'])
def upload_technical_evaluation():
    """Cargar archivo de evaluación técnica"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400
    
    file = request.files['file']
    process_id = request.form.get('process_id')
    
    if not process_id:
        return jsonify({'error': 'ID de proceso requerido'}), 400
    
    try:
        # Leer archivo Excel
        df = pd.read_excel(file, header=0)
        
        created_count = 0
        
        for index, row in df.iterrows():
            if pd.isna(row['N°']) or row['N°'] == '':
                continue
            
            # Crear criterio de evaluación
            criteria = EvaluationCriteria(
                process_id=process_id,
                criterion_number=row['N°'],
                criterion_name=row['CRITERIO'],
                description=row.get('DESCRIPCIÓN'),
                weight_percentage=pd.to_numeric(row.get('PESO %'), errors='ignore'),
                evaluation_type='technical'
            )
            
            db.session.add(criteria)
            db.session.flush()  # Para obtener el ID
            
            # Crear puntuaciones para cada proveedor
            for i in range(1, 4):  # Proveedores 1, 2, 3
                score_col = f'PROVEEDOR {i}'
                weight_col = f'PONDERACIÓN {i}'
                
                if not pd.isna(row.get(score_col)):
                    # Buscar o crear proveedor
                    supplier_name = str(row.get(score_col, '')).strip()
                    if supplier_name:
                        supplier = Supplier.query.filter_by(name=supplier_name).first()
                        if not supplier:
                            supplier = Supplier(name=supplier_name)
                            db.session.add(supplier)
                            db.session.flush()
                        
                        # Crear puntuación
                        score = SupplierScore(
                            process_id=process_id,
                            supplier_id=supplier.id,
                            criteria_id=criteria.id,
                            score=pd.to_numeric(row.get(score_col), errors='ignore'),
                            weighted_score=pd.to_numeric(row.get(weight_col), errors='ignore')
                        )
                        
                        db.session.add(score)
            
            created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Evaluación técnica cargada exitosamente',
            'criteria_created': created_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error procesando archivo: {str(e)}'}), 500

# ==================== CONSULTA DE DATOS ====================

@excel_bp.route('/data/process-tracking', methods=['GET'])
def get_process_tracking_data():
    """Obtener datos de seguimiento de procesos"""
    
    tracking_data = ProcessTracking.query.all()
    
    return jsonify([item.to_dict() for item in tracking_data])

@excel_bp.route('/data/technical-evaluation/<int:process_id>', methods=['GET'])
def get_technical_evaluation_data(process_id):
    """Obtener datos de evaluación técnica por proceso"""
    
    criteria = EvaluationCriteria.query.filter_by(process_id=process_id).all()
    scores = SupplierScore.query.filter_by(process_id=process_id).all()
    
    return jsonify({
        'criteria': [item.to_dict() for item in criteria],
        'scores': [item.to_dict() for item in scores]
    })

@excel_bp.route('/data/economic-comparison/<int:process_id>', methods=['GET'])
def get_economic_comparison_data(process_id):
    """Obtener datos de comparativo económico por proceso"""
    
    comparisons = EconomicComparison.query.filter_by(process_id=process_id).all()
    
    return jsonify([item.to_dict() for item in comparisons])

@excel_bp.route('/data/savings-analysis/<int:process_id>', methods=['GET'])
def get_savings_analysis_data(process_id):
    """Obtener datos de análisis de ahorros por proceso"""
    
    savings = SavingsAnalysis.query.filter_by(process_id=process_id).all()
    
    return jsonify([item.to_dict() for item in savings])

