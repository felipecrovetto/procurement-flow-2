from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.models import Alert, ProcurementProcess
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

alerts_scheduler_bp = Blueprint('alerts_scheduler', __name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def check_process_deadlines():
    """Check for processes approaching deadlines and create alerts"""
    try:
        # Get processes that are active and have end dates
        processes = ProcurementProcess.query.filter(
            ProcurementProcess.status == 'active',
            ProcurementProcess.end_date.isnot(None)
        ).all()
        
        current_date = datetime.now().date()
        
        for process in processes:
            days_until_deadline = (process.end_date - current_date).days
            
            # Create alerts for processes approaching deadline
            if days_until_deadline <= 7 and days_until_deadline > 0:
                # Check if alert already exists
                existing_alert = Alert.query.filter(
                    Alert.process_id == process.id,
                    Alert.message.like(f'%{days_until_deadline} días%')
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        process_id=process.id,
                        alert_date=datetime.now(),
                        message=f'El proceso "{process.title}" vence en {days_until_deadline} días',
                        is_dismissed=False
                    )
                    db.session.add(alert)
            
            # Create alert for overdue processes
            elif days_until_deadline < 0:
                existing_alert = Alert.query.filter(
                    Alert.process_id == process.id,
                    Alert.message.like('%vencido%')
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        process_id=process.id,
                        alert_date=datetime.now(),
                        message=f'El proceso "{process.title}" está vencido por {abs(days_until_deadline)} días',
                        is_dismissed=False
                    )
                    db.session.add(alert)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error checking process deadlines: {e}")
        db.session.rollback()

def check_missing_documents():
    """Check for processes missing required documents"""
    try:
        # Get active processes
        processes = ProcurementProcess.query.filter(
            ProcurementProcess.status.in_(['active', 'evaluation'])
        ).all()
        
        for process in processes:
            # Check if process has required documents
            has_technical_base = any(doc.document_type == 'base_tecnica' for doc in process.documents)
            has_economic_base = any(doc.document_type == 'base_economica' for doc in process.documents)
            has_admin_base = any(doc.document_type == 'base_administrativa' for doc in process.documents)
            
            missing_docs = []
            if not has_technical_base:
                missing_docs.append('Base Técnica')
            if not has_economic_base:
                missing_docs.append('Base Económica')
            if not has_admin_base:
                missing_docs.append('Base Administrativa')
            
            if missing_docs:
                # Check if alert already exists
                existing_alert = Alert.query.filter(
                    Alert.process_id == process.id,
                    Alert.message.like('%documentos faltantes%')
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        process_id=process.id,
                        alert_date=datetime.now(),
                        message=f'El proceso "{process.title}" tiene documentos faltantes: {", ".join(missing_docs)}',
                        is_dismissed=False
                    )
                    db.session.add(alert)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error checking missing documents: {e}")
        db.session.rollback()

# Schedule jobs
scheduler.add_job(
    func=check_process_deadlines,
    trigger="interval",
    hours=24,  # Run daily
    id='check_deadlines'
)

scheduler.add_job(
    func=check_missing_documents,
    trigger="interval",
    hours=12,  # Run twice daily
    id='check_missing_docs'
)

@alerts_scheduler_bp.route('/manual-check', methods=['POST'])
def manual_check():
    """Manually trigger alert checks"""
    try:
        check_process_deadlines()
        check_missing_documents()
        return jsonify({'message': 'Verificación manual completada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

