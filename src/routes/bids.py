from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.models import Bid

bids_bp = Blueprint('bids', __name__)

@bids_bp.route('/', methods=['GET'])
def get_bids():
    process_id = request.args.get('process_id')
    supplier_id = request.args.get('supplier_id')
    
    query = Bid.query
    
    if process_id:
        query = query.filter_by(process_id=process_id)
    if supplier_id:
        query = query.filter_by(supplier_id=supplier_id)
    
    bids = query.all()
    return jsonify([bid.to_dict() for bid in bids])

@bids_bp.route('/', methods=['POST'])
def create_bid():
    data = request.get_json()
    
    bid = Bid(
        process_id=data.get('process_id'),
        supplier_id=data.get('supplier_id'),
        technical_proposal_path=data.get('technical_proposal_path'),
        economic_proposal_path=data.get('economic_proposal_path'),
        status=data.get('status', 'submitted'),
        notes=data.get('notes')
    )
    
    db.session.add(bid)
    db.session.commit()
    
    return jsonify(bid.to_dict()), 201

@bids_bp.route('/<int:bid_id>', methods=['GET'])
def get_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    return jsonify(bid.to_dict())

@bids_bp.route('/<int:bid_id>', methods=['PUT'])
def update_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    data = request.get_json()
    
    bid.technical_proposal_path = data.get('technical_proposal_path', bid.technical_proposal_path)
    bid.economic_proposal_path = data.get('economic_proposal_path', bid.economic_proposal_path)
    bid.status = data.get('status', bid.status)
    bid.notes = data.get('notes', bid.notes)
    
    db.session.commit()
    
    return jsonify(bid.to_dict())

@bids_bp.route('/<int:bid_id>', methods=['DELETE'])
def delete_bid(bid_id):
    bid = Bid.query.get_or_404(bid_id)
    db.session.delete(bid)
    db.session.commit()
    
    return '', 204

