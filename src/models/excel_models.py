from src.models.database import db
from datetime import datetime


class ProcessTracking(db.Model):
    __tablename__ = 'process_tracking'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    code = db.Column(db.String(50))
    process_name = db.Column(db.String(200), nullable=False)
    process_type = db.Column(db.String(100))
    requesting_area = db.Column(db.String(100))
    budget = db.Column(db.Float)
    start_date = db.Column(db.Date)
    close_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    suppliers_count = db.Column(db.Integer)
    awarded_supplier = db.Column(db.String(200))
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='tracking_data')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'code': self.code,
            'process_name': self.process_name,
            'process_type': self.process_type,
            'requesting_area': self.requesting_area,
            'budget': self.budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'close_date': self.close_date.isoformat() if self.close_date else None,
            'status': self.status,
            'suppliers_count': self.suppliers_count,
            'awarded_supplier': self.awarded_supplier,
            'observations': self.observations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class EvaluationCriteria(db.Model):
    __tablename__ = 'evaluation_criteria'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    criterion_number = db.Column(db.Integer, nullable=False)
    criterion_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    weight_percentage = db.Column(db.Float)
    evaluation_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='evaluation_criteria')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'criterion_number': self.criterion_number,
            'criterion_name': self.criterion_name,
            'description': self.description,
            'weight_percentage': self.weight_percentage,
            'evaluation_type': self.evaluation_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SupplierScore(db.Model):
    __tablename__ = 'supplier_scores'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('evaluation_criteria.id'), nullable=False)
    score = db.Column(db.Float)
    weighted_score = db.Column(db.Float)
    comments = db.Column(db.Text)
    evaluator = db.Column(db.String(100))
    evaluation_date = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='supplier_scores')
    supplier = db.relationship('Supplier', backref='scores')
    criteria = db.relationship('EvaluationCriteria', backref='scores')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'supplier_id': self.supplier_id,
            'criteria_id': self.criteria_id,
            'score': self.score,
            'weighted_score': self.weighted_score,
            'comments': self.comments,
            'evaluator': self.evaluator,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None,
            'supplier_name': self.supplier.name if self.supplier else None,
            'criteria_name': self.criteria.criterion_name if self.criteria else None
        }


class EconomicComparison(db.Model):
    __tablename__ = 'economic_comparison'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    item_number = db.Column(db.Integer, nullable=False)
    item_description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))
    supplier1_price = db.Column(db.Float)
    supplier2_price = db.Column(db.Float)
    supplier3_price = db.Column(db.Float)
    best_offer_supplier = db.Column(db.String(200))
    best_offer_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='economic_comparisons')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'item_number': self.item_number,
            'item_description': self.item_description,
            'quantity': self.quantity,
            'unit': self.unit,
            'supplier1_price': self.supplier1_price,
            'supplier2_price': self.supplier2_price,
            'supplier3_price': self.supplier3_price,
            'best_offer_supplier': self.best_offer_supplier,
            'best_offer_price': self.best_offer_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavingsAnalysis(db.Model):
    __tablename__ = 'savings_analysis'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float)
    initial_price = db.Column(db.Float)
    final_price = db.Column(db.Float)
    savings_vs_budget = db.Column(db.Float)
    savings_percentage_budget = db.Column(db.Float)
    savings_vs_initial = db.Column(db.Float)
    savings_percentage_initial = db.Column(db.Float)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='savings_analysis')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'concept': self.concept,
            'budget': self.budget,
            'initial_price': self.initial_price,
            'final_price': self.final_price,
            'savings_vs_budget': self.savings_vs_budget,
            'savings_percentage_budget': self.savings_percentage_budget,
            'savings_vs_initial': self.savings_vs_initial,
            'savings_percentage_initial': self.savings_percentage_initial,
            'observations': self.observations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class QuestionsAnswers(db.Model):
    __tablename__ = 'questions_answers'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_date = db.Column(db.Date)
    supplier_name = db.Column(db.String(200))
    reference_document = db.Column(db.String(200))
    section_clause = db.Column(db.String(200))
    question_text = db.Column(db.Text)
    answer_text = db.Column(db.Text)
    answer_date = db.Column(db.Date)
    answered_by = db.Column(db.String(100))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='questions_answers')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'question_number': self.question_number,
            'question_date': self.question_date.isoformat() if self.question_date else None,
            'supplier_name': self.supplier_name,
            'reference_document': self.reference_document,
            'section_clause': self.section_clause,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'answer_date': self.answer_date.isoformat() if self.answer_date else None,
            'answered_by': self.answered_by,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TechnicalEvaluationMatrix(db.Model):
    __tablename__ = 'technical_evaluation_matrix'

    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=False)
    process_name = db.Column(db.String(200))
    evaluation_date = db.Column(db.Date)
    requesting_department = db.Column(db.String(100))
    negotiator = db.Column(db.String(100))
    budget_amount = db.Column(db.Float)
    capex_opex_number = db.Column(db.String(50))
    compliance_scale = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    process = db.relationship('ProcurementProcess', backref='technical_evaluation_matrix')

    def to_dict(self):
        return {
            'id': self.id,
            'process_id': self.process_id,
            'process_name': self.process_name,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None,
            'requesting_department': self.requesting_department,
            'negotiator': self.negotiator,
            'budget_amount': self.budget_amount,
            'capex_opex_number': self.capex_opex_number,
            'compliance_scale': self.compliance_scale,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SupplierEvaluation(db.Model):
    __tablename__ = 'supplier_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('procurement_processes.id'), nullable=True)
    evaluation_date = db.Column(db.Date)
    overall_score = db.Column(db.Float)
    quality_score = db.Column(db.Float)
    delivery_score = db.Column(db.Float)
    service_score = db.Column(db.Float)
    price_competitiveness = db.Column(db.Float)
    technical_capability = db.Column(db.Float)
    financial_stability = db.Column(db.Float)
    compliance_score = db.Column(db.Float)
    innovation_score = db.Column(db.Float)
    sustainability_score = db.Column(db.Float)
    evaluator = db.Column(db.String(100))
    comments = db.Column(db.Text)
    recommendation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier = db.relationship('Supplier', backref='evaluations')
    process = db.relationship('ProcurementProcess', backref='supplier_evaluations')

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'process_id': self.process_id,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None,
            'overall_score': self.overall_score,
            'quality_score': self.quality_score,
            'delivery_score': self.delivery_score,
            'service_score': self.service_score,
            'price_competitiveness': self.price_competitiveness,
            'technical_capability': self.technical_capability,
            'financial_stability': self.financial_stability,
            'compliance_score': self.compliance_score,
            'innovation_score': self.innovation_score,
            'sustainability_score': self.sustainability_score,
            'evaluator': self.evaluator,
            'comments': self.comments,
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'supplier_name': self.supplier.name if self.supplier else None
        }
