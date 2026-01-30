/**
 * India Visa Processing Estimator
 * Frontend JavaScript
 * Author: Rahul Makwana
 * Infosys Springboard Project
 */

// API Configuration
const API_BASE = '';

// DOM Elements
const form = document.getElementById('prediction-form');
const submitBtn = document.getElementById('submit-btn');
const loadingEl = document.getElementById('loading');
const resultsPanel = document.getElementById('results-panel');

// Form submission handler
if (form) {
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Show loading, hide results
        showLoading(true);
        hideResults();

        // Collect form data
        const formData = {
            applicant_age: parseInt(document.getElementById('age').value),
            nationality: document.getElementById('nationality').value,
            visa_type: document.getElementById('visa_type').value,
            occupation: document.getElementById('occupation').value,
            education_level: document.getElementById('education').value,
            duration_requested_days: parseInt(document.getElementById('duration').value) || 30,
            num_previous_visits: parseInt(document.getElementById('previous_visits').value) || 0,
            financial_proof_usd: parseFloat(document.getElementById('financial_proof').value) || 15000,
            has_sponsor: document.getElementById('has_sponsor').checked,
            documents_complete: document.getElementById('documents_complete').checked,
            express_processing: document.getElementById('express_processing').checked,
            application_month: parseInt(document.getElementById('application_month').value) || 1
        };

        try {
            const response = await fetch(API_BASE + '/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Prediction failed');
            }

            const result = await response.json();
            showLoading(false);
            displayResults(result);

        } catch (error) {
            console.error('Error:', error);
            showLoading(false);
            alert('An error occurred. Please try again.');
        }
    });
}

// Display prediction results
function displayResults(data) {
    // Main prediction
    document.getElementById('result-days').innerHTML =
        data.predicted_days + ' <span>days</span>';

    document.getElementById('result-range').textContent =
        'Estimated range: ' + data.min_days + ' to ' + data.max_days + ' days';

    // Risk level
    const riskEl = document.getElementById('result-risk');
    riskEl.textContent = data.risk_level;
    riskEl.className = 'result-item__value ' + getRiskClass(data.risk_level);

    // Approval likelihood
    const approvalEl = document.getElementById('result-approval');
    approvalEl.textContent = data.approval_likelihood + ' (' + data.approval_percentage + '%)';
    approvalEl.className = 'result-item__value ' + getApprovalClass(data.approval_likelihood);

    // Averages
    document.getElementById('result-country-avg').textContent =
        data.country_average + ' days';
    document.getElementById('result-visa-avg').textContent =
        data.visa_type_average + ' days';

    // Risk gauge
    updateRiskGauge(data.risk_score);

    // Key factors
    displayFactors(data.factors);

    // Show results
    showResults();
}

// Update the risk gauge bar
function updateRiskGauge(riskScore) {
    const gauge = document.getElementById('risk-gauge-fill');
    // Risk score is 0-5+, map to percentage
    const percentage = Math.min((riskScore / 5) * 100, 100);
    gauge.style.width = percentage + '%';

    // Set color based on risk
    gauge.classList.remove('low', 'medium', 'high');
    if (riskScore <= 1) {
        gauge.classList.add('low');
    } else if (riskScore <= 3) {
        gauge.classList.add('medium');
    } else {
        gauge.classList.add('high');
    }
}

// Display key factors
function displayFactors(factors) {
    const container = document.getElementById('result-factors');
    container.innerHTML = '';

    if (!factors) return;

    const factorLabels = {
        peak_season: 'Peak Season',
        documents_complete: 'Documents Complete',
        has_sponsor: 'Has Sponsor',
        express_processing: 'Express Processing',
        previous_visits: 'Previous Visits',
        financial_proof: 'Financial Proof'
    };

    for (const [key, value] of Object.entries(factors)) {
        const label = factorLabels[key] || key.replace(/_/g, ' ');
        const displayValue = typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value;

        const factorEl = document.createElement('div');
        factorEl.className = 'factor';
        factorEl.innerHTML =
            '<span class="factor__label">' + label + '</span>' +
            '<span class="factor__value">' + displayValue + '</span>';
        container.appendChild(factorEl);
    }
}

// Helper functions
function getRiskClass(riskLevel) {
    if (riskLevel === 'Low') return 'success';
    if (riskLevel === 'Medium') return 'warning';
    return 'danger';
}

function getApprovalClass(likelihood) {
    if (likelihood === 'High') return 'success';
    if (likelihood === 'Medium') return 'warning';
    return 'danger';
}

function showLoading(show) {
    if (loadingEl) {
        loadingEl.classList.toggle('visible', show);
    }
    if (submitBtn) {
        submitBtn.disabled = show;
        submitBtn.textContent = show ? 'Processing...' : 'Get Processing Estimate';
    }
}

function showResults() {
    if (resultsPanel) {
        resultsPanel.classList.add('visible');
        // Scroll to results
        setTimeout(function () {
            resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }
}

function hideResults() {
    if (resultsPanel) {
        resultsPanel.classList.remove('visible');
    }
}

// Reset form
function resetForm() {
    if (form) {
        form.reset();
    }
    hideResults();
}

// Reset and scroll to top
function resetAndScroll() {
    resetForm();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Set current month as default
function setDefaultMonth() {
    const monthSelect = document.getElementById('application_month');
    if (monthSelect) {
        const currentMonth = new Date().getMonth() + 1;
        monthSelect.value = currentMonth;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    setDefaultMonth();
});
