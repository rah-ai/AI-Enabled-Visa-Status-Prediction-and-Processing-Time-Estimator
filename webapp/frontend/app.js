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

    // NEW: Animate model confidence gauge
    animateConfidenceGauge();

    // NEW: Update comparison chart with actual values
    updateComparisonChart(data.predicted_days, data.visa_type_average, data.country_average);

    // Save to history
    saveToHistory(data);

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
// AI VISUALIZATION ANIMATIONS
// ============================================

// Animate the model confidence circular gauge
function animateConfidenceGauge() {
    const circle = document.getElementById('confidence-circle');
    if (!circle) return;

    // 77% accuracy - animate to show this
    const accuracy = 77;
    const circumference = 339.3; // 2 * PI * 54
    const offset = circumference - (accuracy / 100) * circumference;

    // Delay animation slightly for visual effect
    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 300);
}

// Update the comparison chart with actual prediction values
function updateComparisonChart(yourEstimate, visaAvg, countryAvg) {
    const overallAvg = 8.2; // Historical overall average
    const maxValue = Math.max(yourEstimate, visaAvg, countryAvg, overallAvg, 15);

    // Helper to set bar and value
    const setBar = (barId, valueId, value) => {
        const bar = document.getElementById(barId);
        const valueEl = document.getElementById(valueId);
        if (bar && valueEl) {
            const percentage = (value / maxValue) * 100;
            setTimeout(() => {
                bar.style.width = percentage + '%';
            }, 500);
            valueEl.textContent = value.toFixed(1) + ' days';
        }
    };

    setBar('your-estimate-bar', 'your-estimate-value', yourEstimate);
    setBar('visa-avg-bar', 'visa-avg-value', visaAvg);
    setBar('country-avg-bar', 'country-avg-value', countryAvg);
    setBar('overall-avg-bar', 'overall-avg-value', overallAvg);
}

// ============================================
// PDF EXPORT
// ============================================
function downloadPDF() {
    // Use browser's print functionality to save as PDF
    const originalTitle = document.title;
    document.title = 'VisaChronos_Prediction_' + new Date().toISOString().split('T')[0];

    // Hide elements that shouldn't be in PDF
    const elementsToHide = document.querySelectorAll('.pdf-btn, .btn--outline, .history-panel, .trends-section');
    elementsToHide.forEach(el => el.style.display = 'none');

    window.print();

    // Restore elements
    elementsToHide.forEach(el => el.style.display = '');
    document.title = originalTitle;
}

// ============================================
// PREDICTION HISTORY
// ============================================
const HISTORY_KEY = 'visachronos_history';
const MAX_HISTORY = 10;

// Save prediction to history
function saveToHistory(data) {
    const history = getHistory();
    const entry = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        visa_type: document.getElementById('visa_type')?.value || 'Unknown',
        nationality: document.getElementById('nationality')?.value || 'Unknown',
        predicted_days: data.predicted_days,
        risk_level: data.risk_level,
        approval_percentage: data.approval_percentage
    };

    history.unshift(entry);

    // Keep only last MAX_HISTORY entries
    if (history.length > MAX_HISTORY) {
        history.pop();
    }

    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
}

// Get history from localStorage
function getHistory() {
    try {
        const data = localStorage.getItem(HISTORY_KEY);
        return data ? JSON.parse(data) : [];
    } catch (e) {
        return [];
    }
}

// Render history in the UI
function renderHistory() {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    const history = getHistory();

    if (history.length === 0) {
        historyList.innerHTML = `
            <li class="history-item" style="color: var(--text-muted); font-style: italic;">
                No predictions yet. Submit a prediction to see your history.
            </li>
        `;
        return;
    }

    historyList.innerHTML = history.map(entry => `
        <li class="history-item">
            <div class="history-item__info">
                <span class="history-item__visa">${entry.visa_type} - ${entry.nationality}</span>
                <span class="history-item__date">${entry.date}</span>
            </div>
            <div class="history-item__days">${entry.predicted_days} days</div>
        </li>
    `).join('');
}

// Clear all history
function clearHistory() {
    if (confirm('Are you sure you want to clear your prediction history?')) {
        localStorage.removeItem(HISTORY_KEY);
        renderHistory();
    }
}

// ============================================
// MULTI-LANGUAGE SUPPORT (Basic)
// ============================================
const translations = {
    en: {
        title: 'Know Your Visa Processing Time',
        submit: 'Get My Estimate',
        reset: 'Try Another Estimate',
        history: 'Your Prediction History',
        trends: 'Monthly Processing Trends'
    },
    hi: {
        title: 'अपना वीज़ा प्रोसेसिंग समय जानें',
        submit: 'मेरा अनुमान प्राप्त करें',
        reset: 'एक और अनुमान आज़माएं',
        history: 'आपका पूर्वानुमान इतिहास',
        trends: 'मासिक प्रोसेसिंग रुझान'
    },
    es: {
        title: 'Conozca su tiempo de procesamiento de visa',
        submit: 'Obtener mi estimación',
        reset: 'Intentar otra estimación',
        history: 'Tu historial de predicciones',
        trends: 'Tendencias de procesamiento mensual'
    }
};

let currentLang = localStorage.getItem('visachronos_lang') || 'en';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('visachronos_lang', lang);
    // Note: Full implementation would update all text elements
    // This is a foundation for future internationalization
}

// ============================================
// CUSTOM VALIDATION (Premium UI)
// ============================================
function initCustomValidation() {
    const form = document.getElementById('prediction-form');
    if (!form) return;

    // Add custom validation messages
    const selects = form.querySelectorAll('select[required]');
    const inputs = form.querySelectorAll('input[required]');

    // Disable browser default validation UI
    form.setAttribute('novalidate', 'true');

    // Add validation message elements
    [...selects, ...inputs].forEach(field => {
        const group = field.closest('.form-group');
        if (group && !group.querySelector('.validation-message')) {
            const msg = document.createElement('div');
            msg.className = 'validation-message';
            msg.textContent = '⚠ Please fill this field';
            group.appendChild(msg);
        }

        // Listen for changes
        field.addEventListener('blur', function () {
            validateField(this);
        });

        field.addEventListener('change', function () {
            validateField(this);
        });
    });

    // Custom form submit validation
    form.addEventListener('submit', function (e) {
        let isValid = true;

        [...selects, ...inputs].forEach(field => {
            if (!validateField(field)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            // Shake animation on invalid fields
            const errorFields = form.querySelectorAll('.form-group.error');
            errorFields.forEach(field => {
                field.style.animation = 'shake 0.4s ease';
                setTimeout(() => field.style.animation = '', 400);
            });
        }
    });
}

function validateField(field) {
    const group = field.closest('.form-group');
    if (!group) return true;

    const isSelect = field.tagName === 'SELECT';
    const isEmpty = isSelect
        ? (field.value === '' || field.selectedIndex === 0)
        : field.value.trim() === '';

    if (field.required && isEmpty) {
        group.classList.add('error');
        const msg = group.querySelector('.validation-message');
        if (msg) {
            msg.textContent = isSelect
                ? '⚠ Please select an option'
                : '⚠ This field is required';
        }
        return false;
    } else {
        group.classList.remove('error');
        return true;
    }
}

// Add shake animation
const shakeKeyframes = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(4px); }
}
`;
if (!document.getElementById('shake-style')) {
    const style = document.createElement('style');
    style.id = 'shake-style';
    style.textContent = shakeKeyframes;
    document.head.appendChild(style);
}

// ============================================
// CUSTOM STYLED DROPDOWN
// ============================================
const countryFlags = {
    'Afghanistan': '🇦🇫', 'Argentina': '🇦🇷', 'Australia': '🇦🇺', 'Austria': '🇦🇹',
    'Bangladesh': '🇧🇩', 'Belgium': '🇧🇪', 'Brazil': '🇧🇷', 'Canada': '🇨🇦',
    'Chile': '🇨🇱', 'China': '🇨🇳', 'Colombia': '🇨🇴', 'Czech Republic': '🇨🇿',
    'Denmark': '🇩🇰', 'Egypt': '🇪🇬', 'Finland': '🇫🇮', 'France': '🇫🇷',
    'Germany': '🇩🇪', 'Greece': '🇬🇷', 'Hungary': '🇭🇺', 'India': '🇮🇳',
    'Indonesia': '🇮🇩', 'Iran': '🇮🇷', 'Iraq': '🇮🇶', 'Ireland': '🇮🇪',
    'Israel': '🇮🇱', 'Italy': '🇮🇹', 'Japan': '🇯🇵', 'Kenya': '🇰🇪',
    'Malaysia': '🇲🇾', 'Mexico': '🇲🇽', 'Morocco': '🇲🇦', 'Nepal': '🇳🇵',
    'Netherlands': '🇳🇱', 'New Zealand': '🇳🇿', 'Nigeria': '🇳🇬', 'Norway': '🇳🇴',
    'Pakistan': '🇵🇰', 'Peru': '🇵🇪', 'Philippines': '🇵🇭', 'Poland': '🇵🇱',
    'Portugal': '🇵🇹', 'Romania': '🇷🇴', 'Russia': '🇷🇺', 'Saudi Arabia': '🇸🇦',
    'Singapore': '🇸🇬', 'South Africa': '🇿🇦', 'South Korea': '🇰🇷', 'Spain': '🇪🇸',
    'Sri Lanka': '🇱🇰', 'Sweden': '🇸🇪', 'Switzerland': '🇨🇭', 'Thailand': '🇹🇭',
    'Turkey': '🇹🇷', 'UAE': '🇦🇪', 'UK': '🇬🇧', 'USA': '🇺🇸',
    'Ukraine': '🇺🇦', 'Vietnam': '🇻🇳', 'United States': '🇺🇸', 'United Kingdom': '🇬🇧'
};

function initCustomDropdowns() {
    const selects = document.querySelectorAll('select[data-custom-select]');

    selects.forEach(select => {
        createCustomDropdown(select);
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-select')) {
            document.querySelectorAll('.custom-select.open').forEach(el => {
                el.classList.remove('open');
            });
        }
    });
}

function createCustomDropdown(nativeSelect) {
    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select';

    // Get options from native select
    const options = Array.from(nativeSelect.options).slice(1); // Skip placeholder
    const placeholder = nativeSelect.options[0]?.text || 'Select...';

    // Create trigger button
    const trigger = document.createElement('div');
    trigger.className = 'custom-select__trigger';
    trigger.innerHTML = `
        <span class="custom-select__value">
            <span class="custom-select__placeholder">${placeholder}</span>
        </span>
        <svg class="custom-select__arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
        </svg>
    `;

    // Create dropdown panel
    const dropdown = document.createElement('div');
    dropdown.className = 'custom-select__dropdown';

    // Create search box
    const searchBox = document.createElement('div');
    searchBox.className = 'custom-select__search';
    searchBox.innerHTML = `
        <svg class="custom-select__search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
        </svg>
        <input type="text" class="custom-select__search-input" placeholder="Search...">
    `;

    // Create options list
    const optionsList = document.createElement('div');
    optionsList.className = 'custom-select__options';

    options.forEach(opt => {
        const optionEl = document.createElement('div');
        optionEl.className = 'custom-select__option';
        optionEl.dataset.value = opt.value;

        const flag = countryFlags[opt.text] || countryFlags[opt.value] || '🌍';

        optionEl.innerHTML = `
            <span class="custom-select__option-flag">${flag}</span>
            <span class="custom-select__option-text">${opt.text}</span>
        `;

        optionEl.addEventListener('click', () => {
            selectOption(wrapper, nativeSelect, opt.value, opt.text, flag);
        });

        optionsList.appendChild(optionEl);
    });

    // Add no results message
    const noResults = document.createElement('div');
    noResults.className = 'custom-select__no-results';
    noResults.textContent = 'No countries found';
    noResults.style.display = 'none';
    optionsList.appendChild(noResults);

    dropdown.appendChild(searchBox);
    dropdown.appendChild(optionsList);

    wrapper.appendChild(trigger);
    wrapper.appendChild(dropdown);

    // Hide native select but keep for form submission
    nativeSelect.classList.add('native-select');
    nativeSelect.parentNode.insertBefore(wrapper, nativeSelect);
    wrapper.appendChild(nativeSelect);

    // Toggle dropdown on trigger click
    trigger.addEventListener('click', (e) => {
        e.stopPropagation();

        // Close other dropdowns
        document.querySelectorAll('.custom-select.open').forEach(el => {
            if (el !== wrapper) el.classList.remove('open');
        });

        wrapper.classList.toggle('open');

        if (wrapper.classList.contains('open')) {
            const searchInput = searchBox.querySelector('.custom-select__search-input');
            setTimeout(() => searchInput.focus(), 100);
        }
    });

    // Search functionality
    const searchInput = searchBox.querySelector('.custom-select__search-input');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        let hasResults = false;

        optionsList.querySelectorAll('.custom-select__option').forEach(opt => {
            const text = opt.querySelector('.custom-select__option-text').textContent.toLowerCase();
            const matches = text.includes(query);
            opt.classList.toggle('hidden', !matches);
            if (matches) hasResults = true;
        });

        noResults.style.display = hasResults ? 'none' : 'block';
    });

    searchInput.addEventListener('click', (e) => e.stopPropagation());

    // Set initial value if native select has one
    if (nativeSelect.value) {
        const selectedOpt = nativeSelect.options[nativeSelect.selectedIndex];
        if (selectedOpt && selectedOpt.value) {
            const flag = countryFlags[selectedOpt.text] || countryFlags[selectedOpt.value] || '🌍';
            selectOption(wrapper, nativeSelect, selectedOpt.value, selectedOpt.text, flag, false);
        }
    }
}

function selectOption(wrapper, nativeSelect, value, text, flag, closeDropdown = true) {
    // Update native select
    nativeSelect.value = value;
    nativeSelect.dispatchEvent(new Event('change', { bubbles: true }));

    // Update trigger display
    const valueEl = wrapper.querySelector('.custom-select__value');
    valueEl.innerHTML = `
        <span class="custom-select__option-flag">${flag}</span>
        <span>${text}</span>
    `;

    // Mark option as selected
    wrapper.querySelectorAll('.custom-select__option').forEach(opt => {
        opt.classList.toggle('selected', opt.dataset.value === value);
    });

    // Close dropdown
    if (closeDropdown) {
        wrapper.classList.remove('open');
    }

    // Clear search
    const searchInput = wrapper.querySelector('.custom-select__search-input');
    if (searchInput) {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
    }
}

// ============================================
// RESET FORM FUNCTION
// ============================================
function resetForm() {
    // Get the form element
    const form = document.getElementById('prediction-form');
    if (form) {
        form.reset();
    }

    // Reset all custom dropdowns to their initial state
    document.querySelectorAll('.custom-select').forEach(wrapper => {
        const nativeSelect = wrapper.querySelector('select');
        if (nativeSelect) {
            // Reset to first option (usually placeholder)
            nativeSelect.selectedIndex = 0;

            // Update the custom dropdown display
            const valueEl = wrapper.querySelector('.custom-select__value');
            const placeholder = nativeSelect.options[0]?.text || 'Select...';
            valueEl.innerHTML = `<span class="custom-select__placeholder">${placeholder}</span>`;

            // Remove selected state from all options
            wrapper.querySelectorAll('.custom-select__option').forEach(opt => {
                opt.classList.remove('selected');
            });
        }
    });

    // Hide results panel if visible
    const resultsPanel = document.getElementById('results-panel');
    if (resultsPanel) {
        resultsPanel.style.display = 'none';
        resultsPanel.classList.remove('active');
    }

    // Scroll to top of form
    if (form) {
        form.scrollIntoView({ behavior: 'smooth' });
    }
}

// ============================================
// INITIALIZE
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initScrollReveal();
    setDefaultMonth();
    renderHistory(); // Load prediction history
    initCustomValidation(); // Custom validation UI
    initCustomDropdowns(); // Custom styled dropdowns
});
