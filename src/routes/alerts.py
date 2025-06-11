from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.models import Alert
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
def get_alerts():
    process_id = request.args.get('process_id')
    dismissed = request.args.get('dismissed', 'false').lower() == 'true'
    
    query = Alert.query
    
    if process_id:
        query = query.filter_by(process_id=process_id)
    
    query = query.filter_by(is_dismissed=dismissed)
    
    alerts = query.order_by(Alert.alert_date.desc()).all()
    return jsonify([alert.to_dict() for alert in alerts])

@alerts_bp.route('/', methods=['POST'])
def create_alert():
    data = request.get_json()
    
    alert_date = datetime.utcnow()
    if data.get('alert_date'):
        alert_date = datetime.fromisoformat(data.get('alert_date'))
    
    alert = Alert(
        process_id=data.get('process_id'),
        alert_date=alert_date,
        message=data.get('message'),
        is_dismissed=data.get('is_dismissed', False)
    )
    
    db.session.add(alert)
    db.session.commit()
    
    return jsonify(alert.to_dict()), 201

@alerts_bp.route('/<int:alert_id>/dismiss', methods=['PUT'])
def dismiss_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.is_dismissed = True
    db.session.commit()
    
    return jsonify(alert.to_dict())

@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    db.session.delete(alert)
    db.session.commit()
    
    return '', 204

