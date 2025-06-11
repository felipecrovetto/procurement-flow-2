from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.models import ProcurementProcess
from datetime import datetime

processes_bp = Blueprint('processes', __name__)

@processes_bp.route('/', methods=['GET'])
def get_processes():
    processes = ProcurementProcess.query.all()
    return jsonify([process.to_dict() for process in processes])

@processes_bp.route('/', methods=['POST'])
def create_process():
    data = request.get_json()
    
    start_date = None
    end_date = None
    
    if data.get('start_date'):
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    if data.get('end_date'):
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    
    process = ProcurementProcess(
        title=data.get('title'),
        description=data.get('description'),
        process_type=data.get('process_type'),
        start_date=start_date,
        end_date=end_date,
        status=data.get('status', 'draft'),
        notes=data.get('notes')
    )
    
    db.session.add(process)
    db.session.commit()
    
    return jsonify(process.to_dict()), 201

@processes_bp.route('/<int:process_id>', methods=['GET'])
def get_process(process_id):
    process = ProcurementProcess.query.get_or_404(process_id)
    return jsonify(process.to_dict())

@processes_bp.route('/<int:process_id>', methods=['PUT'])
def update_process(process_id):
    process = ProcurementProcess.query.get_or_404(process_id)
    data = request.get_json()
    
    process.title = data.get('title', process.title)
    process.description = data.get('description', process.description)
    process.process_type = data.get('process_type', process.process_type)
    process.status = data.get('status', process.status)
    process.notes = data.get('notes', process.notes)
    
    if data.get('start_date'):
        process.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    if data.get('end_date'):
        process.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify(process.to_dict())

@processes_bp.route('/<int:process_id>', methods=['DELETE'])
def delete_process(process_id):
    process = ProcurementProcess.query.get_or_404(process_id)
    db.session.delete(process)
    db.session.commit()
    
    return '', 204

