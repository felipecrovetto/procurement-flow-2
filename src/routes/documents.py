from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from src.models.database import db
from src.models.models import Document
import os

documents_bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route('/', methods=['GET'])
def get_documents():
    process_id = request.args.get('process_id')
    supplier_id = request.args.get('supplier_id')
    
    query = Document.query
    
    if process_id:
        query = query.filter_by(process_id=process_id)
    if supplier_id:
        query = query.filter_by(supplier_id=supplier_id)
    
    documents = query.all()
    return jsonify([doc.to_dict() for doc in documents])

@documents_bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        document = Document(
            process_id=request.form.get('process_id') if request.form.get('process_id') else None,
            supplier_id=request.form.get('supplier_id') if request.form.get('supplier_id') else None,
            document_type=request.form.get('document_type'),
            file_name=filename,
            file_path=file_path,
            version=request.form.get('version'),
            notes=request.form.get('notes')
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify(document.to_dict()), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@documents_bp.route('/<int:document_id>/download', methods=['GET'])
def download_document(document_id):
    document = Document.query.get_or_404(document_id)
    return send_file(document.file_path, as_attachment=True, download_name=document.file_name)

@documents_bp.route('/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.session.delete(document)
    db.session.commit()
    
    return '', 204

