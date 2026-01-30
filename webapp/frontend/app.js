/**
 * India Visa Processing Estimator - Frontend JavaScript
 * Author: Harsh
 * Handles form submission, API calls, and results display
 */

// API base URL - will be same origin when deployed
const API_BASE = '';

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function () {
    // Set current month as default
    const currentMonth = new Date().getMonth() + 1;
    const monthSelect = document.getElementById('application_month');
    if (monthSelect) {
        monthSelect.value = currentMonth.toString();
    }

    // Setup form submission
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});


/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    // Get form data
    const formData = getFormData();

    // Validate
    if (!validateForm(formData)) {
        return;
    }

    // Show loading state
    showLoading(true);
    hideResults();

    try {
        // Call prediction API
        const response = await fetch(`${API_BASE}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Prediction failed. Please try again.');
        }

        const result = await response.json();

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Prediction error:', error);
        alert('Error: ' + error.message);
    } finally {
        showLoading(false);
    }
}


/**
 * Get form data as object
 */
function getFormData() {
    return {
        applicant_age: parseInt(document.getElementById('age').value) || 30,
        nationality: document.getElementById('nationality').value,
        visa_type: document.getElementById('visa_type').value,
        occupation: document.getElementById('occupation').value || 'Professional',
        education_level: document.getElementById('education').value || 'Graduate',
        duration_requested_days: parseInt(document.getElementById('duration').value) || 30,
        num_previous_visits: parseInt(document.getElementById('previous_visits').value) || 0,
        financial_proof_usd: parseFloat(document.getElementById('financial_proof').value) || 15000,
        has_sponsor: document.getElementById('has_sponsor').checked,
        documents_complete: document.getElementById('documents_complete').checked,
        express_processing: document.getElementById('express_processing').checked,
        application_month: parseInt(document.getElementById('application_month').value) || 1
    };
}


/**
 * Validate form data
 */
function validateForm(data) {
    if (!data.nationality) {
        alert('Please select your nationality');
        document.getElementById('nationality').focus();
        return false;
    }

    if (!data.visa_type) {
        alert('Please select a visa type');
        document.getElementById('visa_type').focus();
        return false;
    }

    if (data.applicant_age < 18 || data.applicant_age > 100) {
        alert('Please enter a valid age (18-100)');
        document.getElementById('age').focus();
        return false;
    }

    return true;
}


/**
 * Display prediction results
 */
function displayResults(result) {
    // Main prediction
    document.getElementById('result-days').innerHTML =
        `${result.predicted_days} <span>days</span>`;

    document.getElementById('result-range').innerHTML =
        `Estimated range: ${result.min_days} to ${result.max_days} days`;

    // Risk level with color
    const riskEl = document.getElementById('result-risk');
    riskEl.textContent = result.risk_level;
    riskEl.className = 'result-item__value ' + getRiskClass(result.risk_level);

    // Approval likelihood
    const approvalEl = document.getElementById('result-approval');
    approvalEl.textContent = `${result.approval_likelihood} (${result.approval_percentage}%)`;
    approvalEl.className = 'result-item__value ' + getApprovalClass(result.approval_likelihood);

    // Averages
    document.getElementById('result-country-avg').textContent =
        `${result.country_average} days`;
    document.getElementById('result-visa-avg').textContent =
        `${result.visa_type_average} days`;

    // Risk gauge
    updateRiskGauge(result.risk_score);

    // Factors
    displayFactors(result.factors, result.is_peak_season);

    // Show results panel with animation
    showResults();
}


/**
 * Get CSS class for risk level
 */
function getRiskClass(level) {
    switch (level.toLowerCase()) {
        case 'low': return 'success';
        case 'medium': return 'warning';
        case 'high': return 'danger';
        default: return '';
    }
}


/**
 * Get CSS class for approval likelihood
 */
function getApprovalClass(likelihood) {
    switch (likelihood.toLowerCase()) {
        case 'high': return 'success';
        case 'medium': return 'warning';
        case 'low': return 'danger';
        default: return '';
    }
}


/**
 * Update risk gauge visualization
 */
function updateRiskGauge(riskScore) {
    const maxRisk = 6;  // Maximum possible risk score
    const percentage = Math.min((riskScore / maxRisk) * 100, 100);

    const gauge = document.getElementById('risk-gauge-fill');
    gauge.style.width = `${percentage}%`;

    // Set color class
    gauge.className = 'risk-gauge__fill';
    if (riskScore <= 1) {
        gauge.classList.add('low');
    } else if (riskScore <= 3) {
        gauge.classList.add('medium');
    } else {
        gauge.classList.add('high');
    }
}


/**
 * Display factors that affected the prediction
 */
function displayFactors(factors, isPeakSeason) {
    const container = document.getElementById('result-factors');

    const factorItems = [
        {
            label: 'Documents',
            value: factors.documents_complete ? '✅ Complete' : '⚠️ Incomplete',
            positive: factors.documents_complete
        },
        {
            label: 'Sponsor',
            value: factors.has_sponsor ? '✅ Yes' : '➖ No',
            positive: factors.has_sponsor
        },
        {
            label: 'Express',
            value: factors.express_processing ? '⚡ Yes' : '➖ No',
            positive: factors.express_processing
        },
        {
            label: 'Previous Visits',
            value: factors.previous_visits > 0 ? `✅ ${factors.previous_visits}` : '➖ First time',
            positive: factors.previous_visits > 0
        },
        {
            label: 'Season',
            value: isPeakSeason ? '📅 Peak Season' : '📅 Off-Peak',
            positive: !isPeakSeason
        }
    ];

    container.innerHTML = factorItems.map(item => `
        <div style="padding: 8px; background: ${item.positive ? 'var(--success-light)' : 'var(--gray-100)'}; 
                    border-radius: 6px; display: flex; justify-content: space-between;">
            <span style="color: var(--gray-600);">${item.label}</span>
            <span style="font-weight: 500;">${item.value}</span>
        </div>
    `).join('');
}


/**
 * Show loading state
 */
function showLoading(show) {
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');

    if (show) {
        loading.classList.add('visible');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
    } else {
        loading.classList.remove('visible');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Get Processing Estimate →';
    }
}


/**
 * Show results panel
 */
function showResults() {
    const panel = document.getElementById('results-panel');
    panel.classList.add('visible');

    // Scroll to results
    setTimeout(() => {
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}


/**
 * Hide results panel
 */
function hideResults() {
    const panel = document.getElementById('results-panel');
    panel.classList.remove('visible');
}


/**
 * Reset form
 */
function resetForm() {
    const form = document.getElementById('prediction-form');
    if (form) {
        form.reset();
        // Re-set defaults
        document.getElementById('documents_complete').checked = true;
        document.getElementById('education').value = 'Graduate';
        document.getElementById('financial_proof').value = '15000';
        document.getElementById('duration').value = '30';

        // Set current month
        const currentMonth = new Date().getMonth() + 1;
        document.getElementById('application_month').value = currentMonth.toString();
    }
    hideResults();
}


/**
 * Reset form and scroll to top
 */
function resetAndScroll() {
    resetForm();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}
