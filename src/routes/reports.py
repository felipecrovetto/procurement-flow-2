from flask import Blueprint, request, jsonify
from src.models.database import db
from src.models.models import ProcurementProcess, Bid, Supplier, ComparativeAnalysis, Document
from sqlalchemy import func, extract
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    # Count of processes by status
    process_counts = db.session.query(
        ProcurementProcess.status,
        func.count(ProcurementProcess.id)
    ).group_by(ProcurementProcess.status).all()
    
    # Count of processes by type
    type_counts = db.session.query(
        ProcurementProcess.process_type,
        func.count(ProcurementProcess.id)
    ).group_by(ProcurementProcess.process_type).all()
    
    # Recent processes
    recent_processes = ProcurementProcess.query.order_by(
        ProcurementProcess.start_date.desc()
    ).limit(5).all()
    
    # Total counts
    total_processes = ProcurementProcess.query.count()
    total_suppliers = Supplier.query.count()
    total_bids = Bid.query.count()
    
    return jsonify({
        'process_counts': [{'status': status, 'count': count} for status, count in process_counts],
        'type_counts': [{'type': ptype, 'count': count} for ptype, count in type_counts],
        'recent_processes': [process.to_dict() for process in recent_processes],
        'totals': {
            'processes': total_processes,
            'suppliers': total_suppliers,
            'bids': total_bids
        }
    })

@reports_bp.route('/process/<int:process_id>/comparison', methods=['GET'])
def get_process_comparison(process_id):
    # Get all bids for the process with supplier information
    bids = db.session.query(Bid, Supplier).join(
        Supplier, Bid.supplier_id == Supplier.id
    ).filter(Bid.process_id == process_id).all()
    
    comparison_data = []
    for bid, supplier in bids:
        comparison_data.append({
            'bid_id': bid.id,
            'supplier_name': supplier.name,
            'supplier_id': supplier.id,
            'technical_proposal': bid.technical_proposal_path,
            'economic_proposal': bid.economic_proposal_path,
            'submission_date': bid.submission_date.isoformat() if bid.submission_date else None,
            'status': bid.status,
            'notes': bid.notes
        })
    
    return jsonify(comparison_data)

@reports_bp.route('/supplier/<int:supplier_id>/history', methods=['GET'])
def get_supplier_history(supplier_id):
    # Get all bids by supplier with process information
    bids = db.session.query(Bid, ProcurementProcess).join(
        ProcurementProcess, Bid.process_id == ProcurementProcess.id
    ).filter(Bid.supplier_id == supplier_id).all()
    
    history_data = []
    for bid, process in bids:
        history_data.append({
            'bid_id': bid.id,
            'process_title': process.title,
            'process_id': process.id,
            'process_type': process.process_type,
            'submission_date': bid.submission_date.isoformat() if bid.submission_date else None,
            'status': bid.status,
            'process_status': process.status
        })
    
    return jsonify(history_data)

@reports_bp.route('/analytics/monthly', methods=['GET'])
def get_monthly_analytics():
    # Get processes created by month
    monthly_data = db.session.query(
        func.strftime('%Y-%m', ProcurementProcess.start_date).label('month'),
        func.count(ProcurementProcess.id).label('count')
    ).filter(
        ProcurementProcess.start_date.isnot(None)
    ).group_by('month').order_by('month').all()
    
    return jsonify([{'month': month, 'count': count} for month, count in monthly_data])

@reports_bp.route('/analytics/supplier-performance', methods=['GET'])
def get_supplier_performance():
    # Get supplier performance metrics
    supplier_stats = db.session.query(
        Supplier.name,
        func.count(Bid.id).label('total_bids'),
        func.count(func.nullif(Bid.status, 'rejected')).label('successful_bids')
    ).outerjoin(Bid).group_by(Supplier.id, Supplier.name).all()
    
    performance_data = []
    for name, total_bids, successful_bids in supplier_stats:
        success_rate = (successful_bids / total_bids * 100) if total_bids > 0 else 0
        performance_data.append({
            'supplier_name': name,
            'total_bids': total_bids,
            'successful_bids': successful_bids,
            'success_rate': round(success_rate, 2)
        })
    
    return jsonify(performance_data)

@reports_bp.route('/analytics/process-duration', methods=['GET'])
def get_process_duration():
    # Get average process duration by type
    processes_with_duration = db.session.query(
        ProcurementProcess.process_type,
        ProcurementProcess.start_date,
        ProcurementProcess.end_date
    ).filter(
        ProcurementProcess.start_date.isnot(None),
        ProcurementProcess.end_date.isnot(None)
    ).all()
    
    duration_data = {}
    for process_type, start_date, end_date in processes_with_duration:
        duration = (end_date - start_date).days
        if process_type not in duration_data:
            duration_data[process_type] = []
        duration_data[process_type].append(duration)
    
    # Calculate averages
    avg_durations = []
    for process_type, durations in duration_data.items():
        avg_duration = sum(durations) / len(durations)
        avg_durations.append({
            'process_type': process_type,
            'avg_duration_days': round(avg_duration, 1),
            'total_processes': len(durations)
        })
    
    return jsonify(avg_durations)

@reports_bp.route('/export/process-summary/<int:process_id>', methods=['GET'])
def export_process_summary(process_id):
    # Get process details
    process = ProcurementProcess.query.get_or_404(process_id)
    
    # Get related data
    bids = Bid.query.filter_by(process_id=process_id).all()
    documents = Document.query.filter_by(process_id=process_id).all()
    
    # Create summary data
    summary = {
        'process': process.to_dict(),
        'bids_count': len(bids),
        'documents_count': len(documents),
        'bids': [bid.to_dict() for bid in bids],
        'documents': [doc.to_dict() for doc in documents]
    }
    
    return jsonify(summary)

@reports_bp.route('/charts/process-status', methods=['GET'])
def get_process_status_chart():
    # Generate process status chart
    process_counts = db.session.query(
        ProcurementProcess.status,
        func.count(ProcurementProcess.id)
    ).group_by(ProcurementProcess.status).all()
    
    if not process_counts:
        return jsonify({'error': 'No data available'}), 404
    
    # Create chart
    plt.figure(figsize=(10, 6))
    statuses = [item[0] for item in process_counts]
    counts = [item[1] for item in process_counts]
    
    colors = ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#6c757d']
    plt.pie(counts, labels=statuses, autopct='%1.1f%%', colors=colors[:len(statuses)])
    plt.title('Distribución de Procesos por Estado')
    
    # Save to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'chart_data': img_base64,
        'data': [{'status': status, 'count': count} for status, count in process_counts]
    })

@reports_bp.route('/charts/monthly-trends', methods=['GET'])
def get_monthly_trends_chart():
    # Generate monthly trends chart
    monthly_data = db.session.query(
        func.strftime('%Y-%m', ProcurementProcess.start_date).label('month'),
        func.count(ProcurementProcess.id).label('count')
    ).filter(
        ProcurementProcess.start_date.isnot(None)
    ).group_by('month').order_by('month').all()
    
    if not monthly_data:
        return jsonify({'error': 'No data available'}), 404
    
    # Create chart
    plt.figure(figsize=(12, 6))
    months = [item[0] for item in monthly_data]
    counts = [item[1] for item in monthly_data]
    
    plt.plot(months, counts, marker='o', linewidth=2, markersize=6, color='#0d6efd')
    plt.title('Tendencia Mensual de Procesos')
    plt.xlabel('Mes')
    plt.ylabel('Número de Procesos')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'chart_data': img_base64,
        'data': [{'month': month, 'count': count} for month, count in monthly_data]
    })


# ==================== ADVANCED EXCEL-BASED ANALYTICS ====================

from src.models.excel_models import *
import seaborn as sns
import pandas as pd
import numpy as np

# Set matplotlib to use a font that supports Spanish characters
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100

def create_chart_base64(fig):
    """Convert matplotlib figure to base64 string"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"

@reports_bp.route('/advanced-analysis/<int:process_id>', methods=['GET'])
def get_advanced_process_analysis(process_id):
    """Get comprehensive analysis for a specific process with Excel data"""
    
    process = ProcurementProcess.query.get_or_404(process_id)
    
    # Get all related Excel data
    tracking_data = ProcessTracking.query.filter_by(process_id=process_id).first()
    technical_evaluations = SupplierScore.query.filter_by(process_id=process_id).all()
    economic_comparisons = EconomicComparison.query.filter_by(process_id=process_id).all()
    savings_analysis = SavingsAnalysis.query.filter_by(process_id=process_id).all()
    questions_answers = QuestionsAnswers.query.filter_by(process_id=process_id).all()
    
    # Generate advanced charts
    charts = {}
    
    # Technical evaluation radar chart
    if technical_evaluations:
        charts['technical_radar'] = generate_technical_radar_chart(technical_evaluations)
        charts['technical_comparison'] = generate_technical_comparison_chart(technical_evaluations)
    
    # Economic comparison charts
    if economic_comparisons:
        charts['economic_comparison'] = generate_economic_comparison_chart(economic_comparisons)
        charts['price_distribution'] = generate_price_distribution_chart(economic_comparisons)
    
    # Savings analysis charts
    if savings_analysis:
        charts['savings_waterfall'] = generate_savings_waterfall_chart(savings_analysis)
        charts['savings_breakdown'] = generate_savings_breakdown_chart(savings_analysis)
    
    # Process timeline
    charts['timeline'] = generate_process_timeline_chart(process, tracking_data)
    
    # Questions and answers analysis
    if questions_answers:
        charts['qa_analysis'] = generate_qa_analysis_chart(questions_answers)
    
    return jsonify({
        'process': process.to_dict(),
        'tracking': tracking_data.to_dict() if tracking_data else None,
        'technical_evaluations': [te.to_dict() for te in technical_evaluations],
        'economic_comparisons': [ec.to_dict() for ec in economic_comparisons],
        'savings_analysis': [sa.to_dict() for sa in savings_analysis],
        'questions_answers': [qa.to_dict() for qa in questions_answers],
        'charts': charts,
        'summary_stats': calculate_process_summary_stats(process_id)
    })

def calculate_process_summary_stats(process_id):
    """Calculate summary statistics for a process"""
    
    # Technical evaluation stats
    tech_scores = SupplierScore.query.filter_by(process_id=process_id).all()
    tech_stats = {}
    if tech_scores:
        scores = [score.score for score in tech_scores if score.score]
        if scores:
            tech_stats = {
                'avg_score': np.mean(scores),
                'max_score': np.max(scores),
                'min_score': np.min(scores),
                'std_score': np.std(scores)
            }
    
    # Economic comparison stats
    econ_comparisons = EconomicComparison.query.filter_by(process_id=process_id).all()
    econ_stats = {}
    if econ_comparisons:
        prices = []
        for comp in econ_comparisons:
            if comp.supplier1_price: prices.append(comp.supplier1_price)
            if comp.supplier2_price: prices.append(comp.supplier2_price)
            if comp.supplier3_price: prices.append(comp.supplier3_price)
        
        if prices:
            econ_stats = {
                'avg_price': np.mean(prices),
                'total_value': sum(prices),
                'price_variance': np.var(prices),
                'items_count': len(econ_comparisons)
            }
    
    # Savings stats
    savings = SavingsAnalysis.query.filter_by(process_id=process_id).all()
    savings_stats = {}
    if savings:
        total_budget = sum([s.budget for s in savings if s.budget])
        total_final = sum([s.final_price for s in savings if s.final_price])
        total_savings = total_budget - total_final if total_budget and total_final else 0
        
        savings_stats = {
            'total_budget': total_budget,
            'total_final_price': total_final,
            'total_savings': total_savings,
            'savings_percentage': (total_savings / total_budget * 100) if total_budget > 0 else 0
        }
    
    return {
        'technical': tech_stats,
        'economic': econ_stats,
        'savings': savings_stats
    }

def generate_technical_radar_chart(evaluations):
    """Generate radar chart for technical evaluations"""
    
    # Group evaluations by supplier and criteria
    suppliers_data = {}
    criteria_names = []
    
    for eval in evaluations:
        supplier_name = eval.supplier.name if eval.supplier else f"Supplier {eval.supplier_id}"
        criteria_name = eval.criteria.criterion_name if eval.criteria else f"Criteria {eval.criteria_id}"
        
        if supplier_name not in suppliers_data:
            suppliers_data[supplier_name] = {}
        
        suppliers_data[supplier_name][criteria_name] = eval.score or 0
        
        if criteria_name not in criteria_names:
            criteria_names.append(criteria_name)
    
    if not suppliers_data or not criteria_names:
        return None
    
    # Create radar chart
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    # Number of criteria
    N = len(criteria_names)
    
    # Angles for each criteria
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Colors for suppliers
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, (supplier, scores) in enumerate(suppliers_data.items()):
        values = [scores.get(criteria, 0) for criteria in criteria_names]
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, 
                label=supplier, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    # Add criteria labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(criteria_names)
    ax.set_ylim(0, 5)
    ax.set_title('Evaluación Técnica por Proveedor', size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    return create_chart_base64(fig)

def generate_technical_comparison_chart(evaluations):
    """Generate bar chart comparing technical scores"""
    
    # Prepare data for comparison
    suppliers = {}
    criteria = set()
    
    for eval in evaluations:
        supplier_name = eval.supplier.name if eval.supplier else f"Supplier {eval.supplier_id}"
        criteria_name = eval.criteria.criterion_name if eval.criteria else f"Criteria {eval.criteria_id}"
        
        if supplier_name not in suppliers:
            suppliers[supplier_name] = {}
        
        suppliers[supplier_name][criteria_name] = eval.score or 0
        criteria.add(criteria_name)
    
    if not suppliers:
        return None
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    criteria_list = sorted(list(criteria))
    supplier_names = list(suppliers.keys())
    
    x = np.arange(len(criteria_list))
    width = 0.8 / len(supplier_names)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, supplier in enumerate(supplier_names):
        scores = [suppliers[supplier].get(criterion, 0) for criterion in criteria_list]
        bars = ax.bar(x + i * width, scores, width, label=supplier, 
                     color=colors[i % len(colors)], alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Criterios de Evaluación')
    ax.set_ylabel('Puntuación')
    ax.set_title('Comparativo de Evaluación Técnica', fontweight='bold', fontsize=16)
    ax.set_xticks(x + width * (len(supplier_names) - 1) / 2)
    ax.set_xticklabels(criteria_list, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 5.5)
    
    plt.tight_layout()
    return create_chart_base64(fig)

def generate_economic_comparison_chart(comparisons):
    """Generate bar chart for economic comparisons"""
    
    # Prepare data
    items = []
    supplier1_prices = []
    supplier2_prices = []
    supplier3_prices = []
    
    for comp in comparisons[:10]:  # Limit to first 10 items
        items.append(f"Ítem {comp.item_number}")
        supplier1_prices.append(comp.supplier1_price or 0)
        supplier2_prices.append(comp.supplier2_price or 0)
        supplier3_prices.append(comp.supplier3_price or 0)
    
    if not items:
        return None
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(items))
    width = 0.25
    
    bars1 = ax.bar(x - width, supplier1_prices, width, label='Proveedor 1', color='#FF6B6B', alpha=0.8)
    bars2 = ax.bar(x, supplier2_prices, width, label='Proveedor 2', color='#4ECDC4', alpha=0.8)
    bars3 = ax.bar(x + width, supplier3_prices, width, label='Proveedor 3', color='#45B7D1', alpha=0.8)
    
    ax.set_xlabel('Ítems')
    ax.set_ylabel('Precio ($)')
    ax.set_title('Comparativo de Propuestas Económicas', fontweight='bold', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(items, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'${height:,.0f}', ha='center', va='bottom', fontsize=8)
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    plt.tight_layout()
    return create_chart_base64(fig)

def generate_price_distribution_chart(comparisons):
    """Generate price distribution histogram"""
    
    all_prices = []
    for comp in comparisons:
        if comp.supplier1_price: all_prices.append(comp.supplier1_price)
        if comp.supplier2_price: all_prices.append(comp.supplier2_price)
        if comp.supplier3_price: all_prices.append(comp.supplier3_price)
    
    if not all_prices:
        return None
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histogram
    ax1.hist(all_prices, bins=20, color='#4ECDC4', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Precio ($)')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución de Precios', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(all_prices, vert=True, patch_artist=True,
                boxprops=dict(facecolor='#4ECDC4', alpha=0.7))
    ax2.set_ylabel('Precio ($)')
    ax2.set_title('Análisis de Dispersión de Precios', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return create_chart_base64(fig)

def generate_savings_waterfall_chart(savings_data):
    """Generate waterfall chart for savings analysis"""
    
    if not savings_data:
        return None
    
    # Prepare data
    categories = []
    budget_values = []
    final_values = []
    savings_values = []
    
    total_budget = 0
    total_final = 0
    
    for saving in savings_data:
        if saving.concept != 'TOTAL':
            categories.append(saving.concept)
            budget = saving.budget or 0
            final = saving.final_price or 0
            
            budget_values.append(budget)
            final_values.append(final)
            savings_values.append(budget - final)
            
            total_budget += budget
            total_final += final
    
    if not categories:
        return None
    
    # Create chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Savings by category (bar chart)
    colors = ['#2ECC71' if s >= 0 else '#E74C3C' for s in savings_values]
    bars = ax1.bar(categories, savings_values, color=colors, alpha=0.8)
    
    ax1.set_title('Ahorros por Categoría', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Ahorro ($)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars, savings_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${value:,.0f}', ha='center', 
                va='bottom' if height >= 0 else 'top', fontweight='bold')
    
    # Budget vs Final comparison (grouped bar chart)
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, budget_values, width, label='Presupuesto', color='#3498DB', alpha=0.8)
    bars2 = ax2.bar(x + width/2, final_values, width, label='Precio Final', color='#E67E22', alpha=0.8)
    
    ax2.set_title('Presupuesto vs Precio Final', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Monto ($)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return create_chart_base64(fig)

def generate_savings_breakdown_chart(savings_data):
    """Generate pie chart for savings breakdown"""
    
    if not savings_data:
        return None
    
    # Prepare data for pie chart
    categories = []
    savings_amounts = []
    
    for saving in savings_data:
        if saving.concept != 'TOTAL' and saving.savings_vs_budget:
            categories.append(saving.concept)
            savings_amounts.append(abs(saving.savings_vs_budget))
    
    if not categories:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    wedges, texts, autotexts = ax.pie(savings_amounts, labels=categories, autopct='%1.1f%%',
                                     colors=colors[:len(categories)], startangle=90)
    
    ax.set_title('Distribución de Ahorros por Categoría', fontweight='bold', fontsize=16)
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    return create_chart_base64(fig)

def generate_qa_analysis_chart(questions_answers):
    """Generate analysis chart for questions and answers"""
    
    if not questions_answers:
        return None
    
    # Analyze questions by status and supplier
    status_counts = {}
    supplier_counts = {}
    
    for qa in questions_answers:
        # Count by status
        status = qa.status or 'pending'
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count by supplier
        supplier = qa.supplier_name or 'Unknown'
        supplier_counts[supplier] = supplier_counts.get(supplier, 0) + 1
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Status distribution
    if status_counts:
        statuses = list(status_counts.keys())
        counts = list(status_counts.values())
        colors = ['#2ECC71', '#F39C12', '#E74C3C']
        
        ax1.pie(counts, labels=statuses, autopct='%1.1f%%', colors=colors[:len(statuses)])
        ax1.set_title('Estado de Consultas', fontweight='bold')
    
    # Supplier distribution
    if supplier_counts:
        suppliers = list(supplier_counts.keys())
        counts = list(supplier_counts.values())
        
        ax2.bar(suppliers, counts, color='#4ECDC4', alpha=0.8)
        ax2.set_title('Consultas por Proveedor', fontweight='bold')
        ax2.set_xlabel('Proveedor')
        ax2.set_ylabel('Número de Consultas')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return create_chart_base64(fig)

@reports_bp.route('/supplier-performance-advanced', methods=['GET'])
def get_advanced_supplier_performance():
    """Get advanced supplier performance analysis"""
    
    # Get supplier evaluations
    evaluations = SupplierEvaluation.query.all()
    
    if not evaluations:
        return jsonify({'message': 'No hay datos de evaluación de proveedores'})
    
    # Generate performance charts
    charts = {
        'performance_scatter': generate_supplier_performance_scatter(evaluations),
        'performance_radar': generate_supplier_performance_radar(evaluations),
        'performance_trends': generate_supplier_performance_trends(evaluations)
    }
    
    # Calculate performance metrics
    performance_data = []
    for eval in evaluations:
        performance_data.append({
            'supplier_name': eval.supplier.name if eval.supplier else 'Unknown',
            'overall_score': eval.overall_score or 0,
            'quality_score': eval.quality_score or 0,
            'delivery_score': eval.delivery_score or 0,
            'service_score': eval.service_score or 0,
            'technical_capability': eval.technical_capability or 0,
            'financial_stability': eval.financial_stability or 0,
            'recommendation': eval.recommendation,
            'evaluation_date': eval.evaluation_date.isoformat() if eval.evaluation_date else None
        })
    
    return jsonify({
        'performance_data': performance_data,
        'charts': charts,
        'summary_stats': calculate_supplier_summary_stats(evaluations)
    })

def calculate_supplier_summary_stats(evaluations):
    """Calculate summary statistics for supplier performance"""
    
    if not evaluations:
        return {}
    
    # Overall statistics
    overall_scores = [e.overall_score for e in evaluations if e.overall_score]
    quality_scores = [e.quality_score for e in evaluations if e.quality_score]
    
    # Recommendation distribution
    recommendations = {}
    for eval in evaluations:
        rec = eval.recommendation or 'unknown'
        recommendations[rec] = recommendations.get(rec, 0) + 1
    
    return {
        'total_evaluations': len(evaluations),
        'avg_overall_score': np.mean(overall_scores) if overall_scores else 0,
        'avg_quality_score': np.mean(quality_scores) if quality_scores else 0,
        'recommendations': recommendations,
        'top_performers': len([e for e in evaluations if e.overall_score and e.overall_score >= 4.0]),
        'needs_improvement': len([e for e in evaluations if e.overall_score and e.overall_score < 3.0])
    }

def generate_supplier_performance_scatter(evaluations):
    """Generate supplier performance scatter plot"""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Prepare data
    suppliers = []
    overall_scores = []
    quality_scores = []
    colors = []
    
    color_map = {'approved': '#2ECC71', 'conditional': '#F39C12', 'rejected': '#E74C3C'}
    
    for eval in evaluations:
        suppliers.append(eval.supplier.name if eval.supplier else f'Supplier {eval.supplier_id}')
        overall_scores.append(eval.overall_score or 0)
        quality_scores.append(eval.quality_score or 0)
        colors.append(color_map.get(eval.recommendation, '#95A5A6'))
    
    # Create scatter plot
    scatter = ax.scatter(overall_scores, quality_scores, c=colors, s=100, alpha=0.7)
    
    # Add supplier labels
    for i, supplier in enumerate(suppliers):
        ax.annotate(supplier, (overall_scores[i], quality_scores[i]), 
                   xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    ax.set_xlabel('Puntuación General')
    ax.set_ylabel('Puntuación de Calidad')
    ax.set_title('Rendimiento de Proveedores', fontweight='bold', fontsize=16)
    ax.grid(True, alpha=0.3)
    
    # Add legend
    legend_elements = [plt.scatter([], [], c=color, s=100, alpha=0.7, label=status.title()) 
                      for status, color in color_map.items()]
    ax.legend(handles=legend_elements)
    
    return create_chart_base64(fig)

def generate_supplier_performance_radar(evaluations):
    """Generate radar chart for supplier performance comparison"""
    
    if len(evaluations) == 0:
        return None
    
    # Take top 5 suppliers for comparison
    top_suppliers = sorted(evaluations, key=lambda x: x.overall_score or 0, reverse=True)[:5]
    
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    # Criteria
    criteria = ['Calidad', 'Entrega', 'Servicio', 'Técnica', 'Financiera', 'Cumplimiento']
    N = len(criteria)
    
    # Angles for each criteria
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, eval in enumerate(top_suppliers):
        values = [
            eval.quality_score or 0,
            eval.delivery_score or 0,
            eval.service_score or 0,
            eval.technical_capability or 0,
            eval.financial_stability or 0,
            eval.compliance_score or 0
        ]
        values += values[:1]
        
        supplier_name = eval.supplier.name if eval.supplier else f'Supplier {eval.supplier_id}'
        
        ax.plot(angles, values, 'o-', linewidth=2, 
                label=supplier_name, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(criteria)
    ax.set_ylim(0, 5)
    ax.set_title('Comparativo de Rendimiento de Proveedores', size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    return create_chart_base64(fig)

def generate_supplier_performance_trends(evaluations):
    """Generate supplier performance trends over time"""
    
    # Group evaluations by month
    monthly_performance = {}
    
    for eval in evaluations:
        if eval.evaluation_date:
            month_key = eval.evaluation_date.strftime('%Y-%m')
            if month_key not in monthly_performance:
                monthly_performance[month_key] = []
            monthly_performance[month_key].append(eval.overall_score or 0)
    
    if not monthly_performance:
        return None
    
    # Calculate monthly averages
    months = sorted(monthly_performance.keys())
    avg_scores = [np.mean(monthly_performance[month]) for month in months]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(months, avg_scores, marker='o', linewidth=2, markersize=6, color='#3498DB')
    ax.set_title('Tendencia de Rendimiento de Proveedores', fontweight='bold', fontsize=16)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Puntuación Promedio')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    # Add trend line
    if len(months) > 1:
        z = np.polyfit(range(len(months)), avg_scores, 1)
        p = np.poly1d(z)
        ax.plot(months, p(range(len(months))), "--", color='#E74C3C', alpha=0.8, label='Tendencia')
        ax.legend()
    
    plt.tight_layout()
    return create_chart_base64(fig)

@reports_bp.route('/comprehensive-dashboard', methods=['GET'])
def get_comprehensive_dashboard():
    """Get comprehensive dashboard with all analytics"""
    
    # Basic statistics
    basic_stats = {
        'total_processes': ProcurementProcess.query.count(),
        'total_suppliers': Supplier.query.count(),
        'total_bids': Bid.query.count(),
        'total_evaluations': SupplierEvaluation.query.count(),
        'total_savings_records': SavingsAnalysis.query.count()
    }
    
    # Recent activity
    recent_processes = ProcurementProcess.query.order_by(
        ProcurementProcess.created_at.desc()
    ).limit(5).all()
    
    # Generate summary charts
    charts = {
        'process_status_distribution': get_process_status_chart_data(),
        'monthly_trends': get_monthly_trends_chart_data(),
        'supplier_performance_summary': get_supplier_performance_summary_chart(),
        'savings_overview': get_savings_overview_chart()
    }
    
    return jsonify({
        'basic_stats': basic_stats,
        'recent_processes': [p.to_dict() for p in recent_processes],
        'charts': charts
    })

def get_process_status_chart_data():
    """Get process status distribution chart"""
    process_counts = db.session.query(
        ProcurementProcess.status,
        func.count(ProcurementProcess.id)
    ).group_by(ProcurementProcess.status).all()
    
    if not process_counts:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    statuses = [item[0] for item in process_counts]
    counts = [item[1] for item in process_counts]
    
    colors = ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#6c757d']
    wedges, texts, autotexts = ax.pie(counts, labels=statuses, autopct='%1.1f%%', 
                                     colors=colors[:len(statuses)])
    ax.set_title('Distribución de Procesos por Estado', fontweight='bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    return create_chart_base64(fig)

def get_monthly_trends_chart_data():
    """Get monthly trends chart"""
    monthly_data = db.session.query(
        func.strftime('%Y-%m', ProcurementProcess.start_date).label('month'),
        func.count(ProcurementProcess.id).label('count')
    ).filter(
        ProcurementProcess.start_date.isnot(None)
    ).group_by('month').order_by('month').all()
    
    if not monthly_data:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    months = [item[0] for item in monthly_data]
    counts = [item[1] for item in monthly_data]
    
    ax.plot(months, counts, marker='o', linewidth=2, markersize=6, color='#0d6efd')
    ax.set_title('Tendencia Mensual de Procesos', fontweight='bold')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Número de Procesos')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return create_chart_base64(fig)

def get_supplier_performance_summary_chart():
    """Get supplier performance summary chart"""
    evaluations = SupplierEvaluation.query.all()
    
    if not evaluations:
        return None
    
    # Count by recommendation
    recommendations = {}
    for eval in evaluations:
        rec = eval.recommendation or 'unknown'
        recommendations[rec] = recommendations.get(rec, 0) + 1
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    recs = list(recommendations.keys())
    counts = list(recommendations.values())
    colors = ['#2ECC71', '#F39C12', '#E74C3C', '#95A5A6']
    
    bars = ax.bar(recs, counts, color=colors[:len(recs)], alpha=0.8)
    ax.set_title('Distribución de Recomendaciones de Proveedores', fontweight='bold')
    ax.set_ylabel('Número de Proveedores')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    return create_chart_base64(fig)

def get_savings_overview_chart():
    """Get savings overview chart"""
    savings_data = SavingsAnalysis.query.all()
    
    if not savings_data:
        return None
    
    # Calculate total savings by concept
    concept_savings = {}
    for saving in savings_data:
        if saving.concept and saving.concept != 'TOTAL':
            concept = saving.concept
            amount = saving.savings_vs_budget or 0
            concept_savings[concept] = concept_savings.get(concept, 0) + amount
    
    if not concept_savings:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    concepts = list(concept_savings.keys())
    amounts = list(concept_savings.values())
    colors = ['#2ECC71', '#3498DB', '#F39C12']
    
    bars = ax.bar(concepts, amounts, color=colors[:len(concepts)], alpha=0.8)
    ax.set_title('Ahorros Totales por Concepto', fontweight='bold')
    ax.set_ylabel('Ahorros ($)')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height != 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    return create_chart_base64(fig)

