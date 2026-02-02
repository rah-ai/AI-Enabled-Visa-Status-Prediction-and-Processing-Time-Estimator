/**
 * VisaChronos - AI Visa Processing Time Predictor
 * Frontend JavaScript
 * Author: Rahul Makwana
 * Infosys Springboard Project
 */

// API Configuration
const API_BASE = '';

// ============================================
// THEME TOGGLE
// ============================================
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Check saved preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    themeToggle.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Add smooth transition
        document.body.style.transition = 'background 0.3s ease, color 0.3s ease';
    });
}

// ============================================
// SCROLL REVEAL ANIMATIONS
// ============================================
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');

    if (!revealElements.length) return;

    const revealOnScroll = () => {
        revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementTop < windowHeight - 100) {
                el.classList.add('visible');
            }
        });
    };

    // Initial check
    revealOnScroll();

    // On scroll
    window.addEventListener('scroll', revealOnScroll, { passive: true });
}

// ============================================
// FORM HANDLING
// ============================================
const form = document.getElementById('prediction-form');
const submitBtn = document.getElementById('submit-btn');
const loadingEl = document.getElementById('loading');
const resultsPanel = document.getElementById('results-panel');

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

// ============================================
// DISPLAY RESULTS
// ============================================
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

    // Timeline visualization
    displayTimeline(data.predicted_days, data.min_days, data.max_days);

    // Show results
    showResults();
}

// Update the risk gauge bar
function updateRiskGauge(riskScore) {
    const gauge = document.getElementById('risk-gauge-fill');
    if (!gauge) return;

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
    if (!container) return;

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

// Display timeline visualization
function displayTimeline(predictedDays, minDays, maxDays) {
    const timelineContainer = document.getElementById('timeline-container');
    if (!timelineContainer) return;

    const today = new Date();
    const expectedDate = new Date(today);
    expectedDate.setDate(expectedDate.getDate() + Math.round(predictedDays));

    const maxDate = new Date(today);
    maxDate.setDate(maxDate.getDate() + Math.round(maxDays));

    const formatDate = (date) => {
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    timelineContainer.innerHTML = `
        <div class="timeline">
            <div class="timeline__track">
                <div class="timeline__progress" style="width: 50%"></div>
            </div>
            <div class="timeline__points">
                <div class="timeline__point timeline__point--start">
                    <div class="timeline__marker"></div>
                    <div class="timeline__label">Application</div>
                    <div class="timeline__date">${formatDate(today)}</div>
                </div>
                <div class="timeline__point timeline__point--mid">
                    <div class="timeline__marker timeline__marker--active"></div>
                    <div class="timeline__label">Expected</div>
                    <div class="timeline__date">${formatDate(expectedDate)}</div>
                </div>
                <div class="timeline__point timeline__point--end">
                    <div class="timeline__marker"></div>
                    <div class="timeline__label">Latest</div>
                    <div class="timeline__date">${formatDate(maxDate)}</div>
                </div>
            </div>
        </div>
        <div class="timeline__summary">
            <p>If you apply today, expect your visa by <strong>${formatDate(expectedDate)}</strong></p>
        </div>
    `;
}

// ============================================
// HELPER FUNCTIONS
// ============================================
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
        // Smooth scroll to results
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

// ============================================
// INITIALIZE
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initScrollReveal();
    setDefaultMonth();
});
