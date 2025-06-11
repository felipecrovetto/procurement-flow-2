// Procurement Management System JavaScript

const API_BASE_URL = 'http://localhost:5000/api';

// Global variables
let currentProcesses = [];
let currentSuppliers = [];
let currentDocuments = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function () {
    loadDashboard();
    loadProcesses();
    loadSuppliers();
    // Mostrar sección por defecto
    showSection('dashboard');
});

// Show section function (MODIFICADA)
function showSection(sectionName) {
    const sections = document.querySelectorAll('.content-section'); // Corregido aquí
    sections.forEach(s => s.style.display = 'none');

    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    const activeLink = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    switch (sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'processes':
            loadProcesses();
            break;
        case 'suppliers':
            loadSuppliers();
            break;
        case 'documents':
            loadDocuments();
            break;
        case 'excel-tables':
            loadExcelProcesses();
            break;
        case 'reports':
            loadReports();
            break;
    }
}


async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports/dashboard`);
        const data = await response.json();
        
        // Update stats cards
        document.getElementById('total-processes').textContent = data.totals.processes;
        document.getElementById('total-suppliers').textContent = data.totals.suppliers;
        document.getElementById('total-bids').textContent = data.totals.bids;
        
        // Load recent processes
        const recentProcessesHtml = data.recent_processes.map(process => `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2 border-bottom">
                <div>
                    <strong>${process.title}</strong>
                    <br>
                    <small class="text-muted">${process.process_type}</small>
                </div>
                <span class="badge status-${process.status}">${process.status}</span>
            </div>
        `).join('');
        
        document.getElementById('recent-processes').innerHTML = recentProcessesHtml;
        
        // Load alerts
        loadRecentAlerts();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error al cargar el dashboard', 'danger');
    }
}

async function loadRecentAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/alerts/?dismissed=false`);
        const alerts = await response.json();
        
        const alertsHtml = alerts.slice(0, 5).map(alert => `
            <div class="alert alert-warning alert-sm mb-2">
                <small>${alert.message}</small>
                <button class="btn btn-sm btn-outline-warning float-end" onclick="dismissAlert(${alert.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
        document.getElementById('recent-alerts').innerHTML = alertsHtml || '<p class="text-muted">No hay alertas activas</p>';
        document.getElementById('active-alerts').textContent = alerts.length;
        
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

// Process functions
async function loadProcesses() {
    try {
        const response = await fetch(`${API_BASE_URL}/processes/`);
        currentProcesses = await response.json();
        
        const tableHtml = currentProcesses.map(process => `
            <tr>
                <td>${process.id}</td>
                <td>${process.title}</td>
                <td><span class="badge bg-info">${process.process_type}</span></td>
                <td><span class="badge status-${process.status}">${process.status}</span></td>
                <td>${process.start_date || '-'}</td>
                <td>${process.end_date || '-'}</td>
                <td>
                    <div class="btn-group">
                        <button class="btn btn-sm btn-outline-primary" onclick="editProcess(${process.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteProcess(${process.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
        
        document.getElementById('processes-table').innerHTML = tableHtml;
        
    } catch (error) {
        console.error('Error loading processes:', error);
        showAlert('Error al cargar los procesos', 'danger');
    }
}

function showProcessModal(processId = null) {
    const modal = new bootstrap.Modal(document.getElementById('processModal'));
    const form = document.getElementById('processForm');
    
    if (processId) {
        // Edit mode
        const process = currentProcesses.find(p => p.id === processId);
        if (process) {
            form.title.value = process.title;
            form.description.value = process.description || '';
            form.process_type.value = process.process_type;
            form.start_date.value = process.start_date || '';
            form.end_date.value = process.end_date || '';
            form.status.value = process.status;
            form.notes.value = process.notes || '';
        }
        form.dataset.processId = processId;
    } else {
        // Create mode
        form.reset();
        delete form.dataset.processId;
    }
    
    modal.show();
}

async function saveProcess() {
    const form = document.getElementById('processForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const isEdit = form.dataset.processId;
        const url = isEdit ? 
            `${API_BASE_URL}/processes/${form.dataset.processId}` : 
            `${API_BASE_URL}/processes/`;
        const method = isEdit ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert(isEdit ? 'Proceso actualizado exitosamente' : 'Proceso creado exitosamente', 'success');
            bootstrap.Modal.getInstance(document.getElementById('processModal')).hide();
            loadProcesses();
            loadDashboard();
        } else {
            throw new Error('Error al guardar el proceso');
        }
        
    } catch (error) {
        console.error('Error saving process:', error);
        showAlert('Error al guardar el proceso', 'danger');
    }
}

function editProcess(processId) {
    showProcessModal(processId);
}

async function deleteProcess(processId) {
    if (confirm('¿Está seguro de que desea eliminar este proceso?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/processes/${processId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Proceso eliminado exitosamente', 'success');
                loadProcesses();
                loadDashboard();
            } else {
                throw new Error('Error al eliminar el proceso');
            }
            
        } catch (error) {
            console.error('Error deleting process:', error);
            showAlert('Error al eliminar el proceso', 'danger');
        }
    }
}

// Supplier functions
async function loadSuppliers() {
    try {
        const response = await fetch(`${API_BASE_URL}/suppliers/`);
        currentSuppliers = await response.json();
        
        const tableHtml = currentSuppliers.map(supplier => `
            <tr>
                <td>${supplier.id}</td>
                <td>${supplier.name}</td>
                <td>${supplier.contact_person || '-'}</td>
                <td>${supplier.email || '-'}</td>
                <td>${supplier.phone || '-'}</td>
                <td>
                    <div class="btn-group">
                        <button class="btn btn-sm btn-outline-primary" onclick="editSupplier(${supplier.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteSupplier(${supplier.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
        
        document.getElementById('suppliers-table').innerHTML = tableHtml;
        
        // Update supplier select options
        updateSupplierSelects();
        
    } catch (error) {
        console.error('Error loading suppliers:', error);
        showAlert('Error al cargar los proveedores', 'danger');
    }
}

function updateSupplierSelects() {
    const selects = document.querySelectorAll('#document-supplier-select');
    selects.forEach(select => {
        const options = currentSuppliers.map(supplier => 
            `<option value="${supplier.id}">${supplier.name}</option>`
        ).join('');
        select.innerHTML = '<option value="">Seleccionar proveedor...</option>' + options;
    });
}

function showSupplierModal(supplierId = null) {
    const modal = new bootstrap.Modal(document.getElementById('supplierModal'));
    const form = document.getElementById('supplierForm');
    
    if (supplierId) {
        // Edit mode
        const supplier = currentSuppliers.find(s => s.id === supplierId);
        if (supplier) {
            form.name.value = supplier.name;
            form.contact_person.value = supplier.contact_person || '';
            form.email.value = supplier.email || '';
            form.phone.value = supplier.phone || '';
            form.address.value = supplier.address || '';
            form.notes.value = supplier.notes || '';
        }
        form.dataset.supplierId = supplierId;
    } else {
        // Create mode
        form.reset();
        delete form.dataset.supplierId;
    }
    
    modal.show();
}

async function saveSupplier() {
    const form = document.getElementById('supplierForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const isEdit = form.dataset.supplierId;
        const url = isEdit ? 
            `${API_BASE_URL}/suppliers/${form.dataset.supplierId}` : 
            `${API_BASE_URL}/suppliers/`;
        const method = isEdit ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert(isEdit ? 'Proveedor actualizado exitosamente' : 'Proveedor creado exitosamente', 'success');
            bootstrap.Modal.getInstance(document.getElementById('supplierModal')).hide();
            loadSuppliers();
            loadDashboard();
        } else {
            throw new Error('Error al guardar el proveedor');
        }
        
    } catch (error) {
        console.error('Error saving supplier:', error);
        showAlert('Error al guardar el proveedor', 'danger');
    }
}

function editSupplier(supplierId) {
    showSupplierModal(supplierId);
}

async function deleteSupplier(supplierId) {
    if (confirm('¿Está seguro de que desea eliminar este proveedor?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/suppliers/${supplierId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Proveedor eliminado exitosamente', 'success');
                loadSuppliers();
                loadDashboard();
            } else {
                throw new Error('Error al eliminar el proveedor');
            }
            
        } catch (error) {
            console.error('Error deleting supplier:', error);
            showAlert('Error al eliminar el proveedor', 'danger');
        }
    }
}

// Document functions
async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/`);
        currentDocuments = await response.json();
        
        const tableHtml = currentDocuments.map(doc => {
            const process = currentProcesses.find(p => p.id === doc.process_id);
            const supplier = currentSuppliers.find(s => s.id === doc.supplier_id);
            
            return `
                <tr>
                    <td>${doc.id}</td>
                    <td>${doc.file_name}</td>
                    <td><span class="badge bg-secondary">${doc.document_type}</span></td>
                    <td>${process ? process.title : '-'}</td>
                    <td>${supplier ? supplier.name : '-'}</td>
                    <td>${new Date(doc.upload_date).toLocaleDateString()}</td>
                    <td>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-success" onclick="downloadDocument(${doc.id})">
                                <i class="fas fa-download"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteDocument(${doc.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
        
        document.getElementById('documents-table').innerHTML = tableHtml;
        
    } catch (error) {
        console.error('Error loading documents:', error);
        showAlert('Error al cargar los documentos', 'danger');
    }
}

function showDocumentModal() {
    const modal = new bootstrap.Modal(document.getElementById('documentModal'));
    const form = document.getElementById('documentForm');
    
    form.reset();
    
    // Update process select options
    const processSelect = document.getElementById('document-process-select');
    const processOptions = currentProcesses.map(process => 
        `<option value="${process.id}">${process.title}</option>`
    ).join('');
    processSelect.innerHTML = '<option value="">Seleccionar proceso...</option>' + processOptions;
    
    modal.show();
}

async function uploadDocument() {
    const form = document.getElementById('documentForm');
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Documento subido exitosamente', 'success');
            bootstrap.Modal.getInstance(document.getElementById('documentModal')).hide();
            loadDocuments();
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Error al subir el documento');
        }
        
    } catch (error) {
        console.error('Error uploading document:', error);
        showAlert('Error al subir el documento: ' + error.message, 'danger');
    }
}

async function downloadDocument(documentId) {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${documentId}/download`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = ''; // The filename will be set by the server
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            throw new Error('Error al descargar el documento');
        }
        
    } catch (error) {
        console.error('Error downloading document:', error);
        showAlert('Error al descargar el documento', 'danger');
    }
}

async function deleteDocument(documentId) {
    if (confirm('¿Está seguro de que desea eliminar este documento?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showAlert('Documento eliminado exitosamente', 'success');
                loadDocuments();
            } else {
                throw new Error('Error al eliminar el documento');
            }
            
        } catch (error) {
            console.error('Error deleting document:', error);
            showAlert('Error al eliminar el documento', 'danger');
        }
    }
}

// Reports functions
async function loadReports() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports/dashboard`);
        const data = await response.json();
        
        // Process Status Chart
        const statusCtx = document.getElementById('processStatusChart').getContext('2d');
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: data.process_counts.map(item => item.status),
                datasets: [{
                    data: data.process_counts.map(item => item.count),
                    backgroundColor: [
                        '#0d6efd',
                        '#198754',
                        '#ffc107',
                        '#dc3545',
                        '#6c757d'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        
        // Process Type Chart
        const typeCtx = document.getElementById('processTypeChart').getContext('2d');
        new Chart(typeCtx, {
            type: 'bar',
            data: {
                labels: data.type_counts.map(item => item.type),
                datasets: [{
                    label: 'Cantidad',
                    data: data.type_counts.map(item => item.count),
                    backgroundColor: '#0d6efd'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading reports:', error);
        showAlert('Error al cargar los reportes', 'danger');
    }
}

// Alert functions
async function dismissAlert(alertId) {
    try {
        const response = await fetch(`${API_BASE_URL}/alerts/${alertId}/dismiss`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            loadRecentAlerts();
        } else {
            throw new Error('Error al descartar la alerta');
        }
        
    } catch (error) {
        console.error('Error dismissing alert:', error);
        showAlert('Error al descartar la alerta', 'danger');
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('es-ES');
}

// Format currency
function formatCurrency(amount) {
    if (!amount) return '-';
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}



// ==================== EXCEL TABLES FUNCTIONALITY ====================

// Download Excel templates
function downloadTemplate(templateType) {
    const url = `/api/excel/templates/${templateType}`;
    
    // Create a temporary link to trigger download
    const link = document.createElement('a');
    link.href = url;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert('Descargando plantilla...', 'info');
}

// Handle table type selection for upload
document.addEventListener('DOMContentLoaded', function() {
    const tableTypeSelect = document.getElementById('tableType');
    const processSelectDiv = document.getElementById('processSelectDiv');
    
    if (tableTypeSelect) {
        tableTypeSelect.addEventListener('change', function() {
            const selectedType = this.value;
            
            // Show process selection for certain table types
            if (['technical-evaluation', 'economic-comparison', 'savings-analysis', 'questions-answers'].includes(selectedType)) {
                processSelectDiv.style.display = 'block';
                loadProcessesForSelect('processSelect');
            } else {
                processSelectDiv.style.display = 'none';
            }
        });
    }
});

// Load processes for select dropdown
function loadProcessesForSelect(selectId) {
    fetch('/api/processes')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Seleccionar proceso...</option>';
            
            data.forEach(process => {
                const option = document.createElement('option');
                option.value = process.id;
                option.textContent = `${process.title} (${process.process_type})`;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading processes:', error);
            showAlert('Error cargando procesos', 'error');
        });
}

// Upload Excel file
function uploadExcelFile() {
    const tableType = document.getElementById('tableType').value;
    const excelFile = document.getElementById('excelFile').files[0];
    const processId = document.getElementById('processSelect').value;
    
    if (!tableType) {
        showAlert('Selecciona el tipo de tabla', 'error');
        return;
    }
    
    if (!excelFile) {
        showAlert('Selecciona un archivo Excel', 'error');
        return;
    }
    
    // Check if process is required for this table type
    const requiresProcess = ['technical-evaluation', 'economic-comparison', 'savings-analysis', 'questions-answers'].includes(tableType);
    if (requiresProcess && !processId) {
        showAlert('Selecciona un proceso para este tipo de tabla', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', excelFile);
    if (processId) {
        formData.append('process_id', processId);
    }
    
    // Show progress
    const progressDiv = document.getElementById('uploadProgress');
    const progressBar = progressDiv.querySelector('.progress-bar');
    const resultDiv = document.getElementById('uploadResult');
    
    progressDiv.style.display = 'block';
    progressBar.style.width = '0%';
    resultDiv.innerHTML = '';
    
    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + '%';
        if (progress >= 90) {
            clearInterval(progressInterval);
        }
    }, 200);
    
    fetch(`/api/excel/upload/${tableType}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        
        setTimeout(() => {
            progressDiv.style.display = 'none';
            
            if (data.error) {
                resultDiv.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle me-2"></i>${data.error}</div>`;
            } else {
                let message = `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i>${data.message}`;
                if (data.created) {
                    message += `<br><small>Registros creados: ${data.created}</small>`;
                }
                if (data.updated) {
                    message += `<br><small>Registros actualizados: ${data.updated}</small>`;
                }
                if (data.criteria_created) {
                    message += `<br><small>Criterios creados: ${data.criteria_created}</small>`;
                }
                message += '</div>';
                resultDiv.innerHTML = message;
                
                // Reset form
                document.getElementById('excelUploadForm').reset();
                document.getElementById('processSelectDiv').style.display = 'none';
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        progressDiv.style.display = 'none';
        console.error('Error uploading file:', error);
        resultDiv.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle me-2"></i>Error cargando archivo</div>`;
    });
}

// Export data functions
function exportData(dataType) {
    const url = `/api/excel/export/${dataType}`;
    
    // Create a temporary link to trigger download
    const link = document.createElement('a');
    link.href = url;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert(`Exportando ${dataType}...`, 'info');
}

function exportProcessAnalysis() {
    const processId = document.getElementById('exportProcessSelect').value;
    
    if (!processId) {
        showAlert('Selecciona un proceso', 'error');
        return;
    }
    
    const url = `/api/excel/export/process-analysis/${processId}`;
    
    const link = document.createElement('a');
    link.href = url;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert('Exportando análisis del proceso...', 'info');
}

function exportByPeriod() {
    const dateFrom = document.getElementById('exportDateFrom').value;
    const dateTo = document.getElementById('exportDateTo').value;
    
    if (!dateFrom || !dateTo) {
        showAlert('Selecciona ambas fechas', 'error');
        return;
    }
    
    const url = `/api/excel/export/period?from=${dateFrom}&to=${dateTo}`;
    
    const link = document.createElement('a');
    link.href = url;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert('Exportando datos del período...', 'info');
}

// Generate analysis
function generateAnalysis() {
    const processId = document.getElementById('analysisProcessSelect').value;
    const analysisType = document.getElementById('analysisType').value;
    
    if (!processId) {
        showAlert('Selecciona un proceso', 'error');
        return;
    }
    
    if (!analysisType) {
        showAlert('Selecciona un tipo de análisis', 'error');
        return;
    }
    
    const resultsDiv = document.getElementById('analysisResults');
    resultsDiv.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p class="mt-2">Generando análisis...</p></div>';
    
    // Fetch analysis data based on type
    let dataUrl = '';
    switch (analysisType) {
        case 'technical-scores':
            dataUrl = `/api/excel/data/technical-evaluation/${processId}`;
            break;
        case 'economic-comparison':
            dataUrl = `/api/excel/data/economic-comparison/${processId}`;
            break;
        case 'savings-analysis':
            dataUrl = `/api/excel/data/savings-analysis/${processId}`;
            break;
        default:
            dataUrl = `/api/excel/data/process-tracking`;
    }
    
    fetch(dataUrl)
        .then(response => response.json())
        .then(data => {
            generateAnalysisCharts(analysisType, data, resultsDiv);
        })
        .catch(error => {
            console.error('Error generating analysis:', error);
            resultsDiv.innerHTML = '<div class="alert alert-danger">Error generando análisis</div>';
        });
}

// Generate analysis charts
function generateAnalysisCharts(analysisType, data, container) {
    let chartHtml = '';
    
    switch (analysisType) {
        case 'technical-scores':
            chartHtml = generateTechnicalScoresChart(data);
            break;
        case 'economic-comparison':
            chartHtml = generateEconomicComparisonChart(data);
            break;
        case 'savings-analysis':
            chartHtml = generateSavingsAnalysisChart(data);
            break;
        case 'supplier-performance':
            chartHtml = generateSupplierPerformanceChart(data);
            break;
        case 'process-timeline':
            chartHtml = generateProcessTimelineChart(data);
            break;
        default:
            chartHtml = '<div class="alert alert-info">Tipo de análisis no implementado</div>';
    }
    
    container.innerHTML = chartHtml;
    
    // Initialize charts after DOM update
    setTimeout(() => {
        initializeAnalysisCharts(analysisType);
    }, 100);
}

function generateTechnicalScoresChart(data) {
    if (!data.criteria || !data.scores) {
        return '<div class="alert alert-warning">No hay datos de evaluación técnica disponibles</div>';
    }
    
    return `
        <div class="row">
            <div class="col-md-8">
                <canvas id="technicalScoresChart" width="400" height="200"></canvas>
            </div>
            <div class="col-md-4">
                <h6>Resumen de Evaluación</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Criterio</th>
                                <th>Peso</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.criteria.map(criterion => `
                                <tr>
                                    <td>${criterion.criterion_name}</td>
                                    <td>${criterion.weight_percentage || 0}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function generateEconomicComparisonChart(data) {
    if (!data || data.length === 0) {
        return '<div class="alert alert-warning">No hay datos de comparativo económico disponibles</div>';
    }
    
    return `
        <div class="row">
            <div class="col-md-8">
                <canvas id="economicComparisonChart" width="400" height="200"></canvas>
            </div>
            <div class="col-md-4">
                <h6>Resumen Económico</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Ítem</th>
                                <th>Mejor Oferta</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.slice(0, 5).map(item => `
                                <tr>
                                    <td>${item.item_description}</td>
                                    <td>$${item.best_offer_price || 0}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function generateSavingsAnalysisChart(data) {
    if (!data || data.length === 0) {
        return '<div class="alert alert-warning">No hay datos de análisis de ahorros disponibles</div>';
    }
    
    return `
        <div class="row">
            <div class="col-md-8">
                <canvas id="savingsAnalysisChart" width="400" height="200"></canvas>
            </div>
            <div class="col-md-4">
                <h6>Resumen de Ahorros</h6>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Concepto</th>
                                <th>% Ahorro</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.map(item => `
                                <tr>
                                    <td>${item.concept}</td>
                                    <td>${item.savings_percentage_budget || 0}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function generateSupplierPerformanceChart(data) {
    return `
        <div class="row">
            <div class="col-md-12">
                <canvas id="supplierPerformanceChart" width="400" height="200"></canvas>
            </div>
        </div>
    `;
}

function generateProcessTimelineChart(data) {
    return `
        <div class="row">
            <div class="col-md-12">
                <canvas id="processTimelineChart" width="400" height="200"></canvas>
            </div>
        </div>
    `;
}

// Initialize analysis charts
function initializeAnalysisCharts(analysisType) {
    switch (analysisType) {
        case 'technical-scores':
            initTechnicalScoresChart();
            break;
        case 'economic-comparison':
            initEconomicComparisonChart();
            break;
        case 'savings-analysis':
            initSavingsAnalysisChart();
            break;
        case 'supplier-performance':
            initSupplierPerformanceChart();
            break;
        case 'process-timeline':
            initProcessTimelineChart();
            break;
    }
}

function initTechnicalScoresChart() {
    const ctx = document.getElementById('technicalScoresChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Experiencia', 'Capacidad Técnica', 'Metodología', 'Calidad', 'Cumplimiento'],
            datasets: [{
                label: 'Proveedor 1',
                data: [4, 3, 5, 4, 3],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
            }, {
                label: 'Proveedor 2',
                data: [3, 4, 3, 5, 4],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

function initEconomicComparisonChart() {
    const ctx = document.getElementById('economicComparisonChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Ítem 1', 'Ítem 2', 'Ítem 3', 'Ítem 4', 'Ítem 5'],
            datasets: [{
                label: 'Proveedor 1',
                data: [1200, 1900, 3000, 5000, 2000],
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
            }, {
                label: 'Proveedor 2',
                data: [1100, 2100, 2800, 4800, 2200],
                backgroundColor: 'rgba(255, 99, 132, 0.8)',
            }, {
                label: 'Proveedor 3',
                data: [1300, 1800, 3200, 5200, 1900],
                backgroundColor: 'rgba(75, 192, 192, 0.8)',
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function initSavingsAnalysisChart() {
    const ctx = document.getElementById('savingsAnalysisChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bienes', 'Servicios', 'Otros'],
            datasets: [{
                data: [15, 25, 10],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Porcentaje de Ahorros por Categoría'
                }
            }
        }
    });
}

function initSupplierPerformanceChart() {
    const ctx = document.getElementById('supplierPerformanceChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Proveedores',
                data: [
                    {x: 85, y: 4.2},
                    {x: 78, y: 3.8},
                    {x: 92, y: 4.5},
                    {x: 70, y: 3.5},
                    {x: 88, y: 4.1}
                ],
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Puntuación Técnica'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Calificación General'
                    }
                }
            }
        }
    });
}

function initProcessTimelineChart() {
    const ctx = document.getElementById('processTimelineChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            datasets: [{
                label: 'Procesos Iniciados',
                data: [12, 19, 15, 25, 22, 18],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.1
            }, {
                label: 'Procesos Completados',
                data: [8, 15, 12, 20, 18, 15],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Load processes for analysis and export dropdowns when Excel section is shown
function loadExcelProcesses() {
    loadProcessesForSelect('exportProcessSelect');
    loadProcessesForSelect('analysisProcessSelect');
}

