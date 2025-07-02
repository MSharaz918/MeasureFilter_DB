// MIPS Measure Filter - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload functionality
    initializeFileUpload();
    
    // Measure selection functionality
    initializeMeasureSelection();
    
    // Form submission handling
    initializeFormHandling();
});

function initializeFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const uploadInfo = document.getElementById('uploadInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');

    if (!uploadArea || !fileInput) return;

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidExcelFile(file)) {
                fileInput.files = files;
                displayFileInfo(file);
            } else {
                alert('Please select a valid Excel file (.xlsx or .xls)');
            }
        }
    });

    // File input change
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            if (isValidExcelFile(file)) {
                displayFileInfo(file);
            } else {
                alert('Please select a valid Excel file (.xlsx or .xls)');
                fileInput.value = '';
            }
        } else {
            hideFileInfo();
        }
    });

    function isValidExcelFile(file) {
        const validTypes = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ];
        const validExtensions = ['.xlsx', '.xls'];
        
        return validTypes.includes(file.type) || 
               validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    }

    function displayFileInfo(file) {
        if (fileName && fileSize && uploadPlaceholder && uploadInfo) {
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            uploadPlaceholder.style.display = 'none';
            uploadInfo.style.display = 'block';
        }
    }

    function hideFileInfo() {
        if (uploadPlaceholder && uploadInfo) {
            uploadPlaceholder.style.display = 'block';
            uploadInfo.style.display = 'none';
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

function initializeMeasureSelection() {
    const measureCards = document.querySelectorAll('.measure-card');
    const selectAllBtn = document.getElementById('selectAllBtn');
    
    // Handle measure card clicks
    measureCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.type !== 'checkbox') {
                const checkbox = card.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    updateCardState(card, checkbox.checked);
                }
            } else {
                updateCardState(card, e.target.checked);
            }
        });
        
        // Initialize card state
        const checkbox = card.querySelector('input[type="checkbox"]');
        if (checkbox) {
            updateCardState(card, checkbox.checked);
        }
    });
    
    // Handle select all button
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.measure-card input[type="checkbox"]');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            
            checkboxes.forEach((checkbox, index) => {
                checkbox.checked = !allChecked;
                updateCardState(measureCards[index], checkbox.checked);
            });
            
            selectAllBtn.innerHTML = allChecked 
                ? '<i data-feather="check-square" class="me-2"></i>Select All'
                : '<i data-feather="square" class="me-2"></i>Deselect All';
            
            // Re-initialize feather icons
            feather.replace();
        });
    }
    
    function updateCardState(card, isSelected) {
        if (isSelected) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    }
}

function initializeFormHandling() {
    const uploadForm = document.getElementById('uploadForm');
    const measureForm = document.getElementById('measureForm');
    const processingModal = document.getElementById('processingModal');
    
    // Handle upload form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('fileInput');
            const submitBtn = document.getElementById('submitBtn');
            const progressBar = document.getElementById('uploadProgress');
            
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Please select a file to upload.');
                return;
            }
            
            // Show progress and disable button
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Uploading...';
            }
            
            if (progressBar) {
                progressBar.style.display = 'block';
                // Simulate progress (actual progress would require additional backend support)
                simulateProgress(progressBar.querySelector('.progress-bar'));
            }
        });
    }
    
    // Handle measure selection form submission
    if (measureForm && processingModal) {
        measureForm.addEventListener('submit', function(e) {
            const selectedMeasures = document.querySelectorAll('.measure-card input[type="checkbox"]:checked');
            
            if (selectedMeasures.length === 0) {
                e.preventDefault();
                alert('Please select at least one measure to process.');
                return;
            }
            
            // Show processing modal
            const modal = new bootstrap.Modal(processingModal);
            modal.show();
        });
    }
    
    function simulateProgress(progressBar) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            progressBar.style.width = progress + '%';
        }, 200);
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }
}

// Auto-refresh functionality for job status (if needed)
function initializeStatusRefresh() {
    const statusElements = document.querySelectorAll('[data-status="processing"]');
    
    if (statusElements.length > 0) {
        // Refresh page every 30 seconds if there are processing jobs
        setTimeout(() => {
            window.location.reload();
        }, 30000);
    }
}

// Initialize status refresh on dashboard
if (window.location.pathname.includes('dashboard')) {
    initializeStatusRefresh();
}
