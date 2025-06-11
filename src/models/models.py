from src.models.database import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Relationships
    bids = db.relationship('Bid', backref='supplier', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='supplier', lazy=True, cascade='all, delete-orphan')
    sworn_declarations = db.relationship('SwornDeclaration', backref='supplier', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'notes': self.notes
        }

class ProcurementProcess(db.Model):
    __tablename__ = 'procurement_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    process_type = db.Column(db.Enum('simple', 'licitacion_grande'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    # Relationships
    documents = db.relationship('Document', backref='process', lazy=True, cascade='all, delete-orphan')
    bids = db.relationship('Bid', backref='process', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='process', lazy=True, cascade='all, delete-orphan')
    comparative_analyses = db.relationship('ComparativeAnalysis', backref='process', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'process_type': self.process_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'notes': self.notes
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    document_type = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'supplier_id': self.supplier_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'version': self.version,
            'notes': self.notes
        }

class Bid(db.Model):
    __tablename__ = 'bids'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    technical_proposal_path = db.Column(db.String(255))
    economic_proposal_path = db.Column(db.String(255))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'supplier_id': self.supplier_id,
            'technical_proposal_path': self.technical_proposal_path,
            'economic_proposal_path': self.economic_proposal_path,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'status': self.status,
            'notes': self.notes
        }

class ComparativeAnalysis(db.Model):
    __tablename__ = 'comparative_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    technical_score = db.Column(db.Numeric(5, 2))
    economic_score = db.Column(db.Numeric(5, 2))
    overall_score = db.Column(db.Numeric(5, 2))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'technical_score': float(self.technical_score) if self.technical_score else None,
            'economic_score': float(self.economic_score) if self.economic_score else None,
            'overall_score': float(self.overall_score) if self.overall_score else None,
            'notes': self.notes
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=True)
    alert_date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_dismissed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'alert_date': self.alert_date.isoformat() if self.alert_date else None,
            'message': self.message,
            'is_dismissed': self.is_dismissed
        }

class SwornDeclaration(db.Model):
    __tablename__ = 'sworn_declarations'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    declaration_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'file_path': self.file_path,
            'declaration_date': self.declaration_date.isoformat() if self.declaration_date else None,
            'notes': self.notes
        }

