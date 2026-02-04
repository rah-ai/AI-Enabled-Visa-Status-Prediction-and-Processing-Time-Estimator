# VisaChronos - Complete Features List

## 🎯 Project Overview
**VisaChronos** is an AI-powered visa processing time prediction application for visitors coming to India from 45+ countries.

---

## 🤖 AI/ML/DL Features

### 1. Linear Regression Prediction Model
- Trained on **2,000+ synthetic visa applications**
- **77% accuracy (R² = 0.77)**
- Error margin: **±2.1 days**

### 2. Feature-Based Prediction
Uses **15+ engineered features**:
- Nationality-based processing averages
- Visa type processing patterns
- Seasonal index (peak vs off-peak seasons)
- Application completeness score
- Financial proof assessment
- Previous visit history
- Age group classification
- Risk score calculation
- Express processing adjustment

### 3. Risk Assessment Algorithm
- Custom scoring formula based on multiple factors
- Classifies applications as Low/Medium/High risk
- Visual risk gauge with color coding

### 4. ML Feature Importance Display
- Shows which factors most affect prediction
- Visual bar chart: Visa Type (85%), Nationality (72%), Season (58%), Documents (45%), Financial (32%)

### 5. Model Confidence Metrics
- Animated circular gauge showing 77% accuracy
- Training samples count (2,000+)
- R² Score display
- Error margin indicator

---

## 🌐 Frontend Features

### 1. Premium VisaChronos Branding
- Custom logo (VC monogram with clock element)
- Consistent "VisaChronos - AI Time Predictor" branding
- Professional color scheme (Navy + Saffron accent)

### 2. Dark/Light Theme Toggle
- Automatic system preference detection
- Manual toggle button with smooth transitions
- Persistent theme storage in localStorage

### 3. Responsive Design
- Mobile-friendly layout
- Adapts to all screen sizes
- Touch-friendly form elements

### 4. Interactive Visualizations

#### Bar Charts (Homepage):
- Processing Time by Visa Type
- Seasonal Processing Trends
- Processing Time by Nationality (8 countries)

#### Results Page Visualizations:
- Animated risk gauge
- ML feature importance bars
- Timeline visualization (Application → Expected → Latest dates)
- Comparison chart (Your estimate vs averages)

### 5. Scroll Reveal Animations
- Elements fade in as user scrolls
- Smooth, professional appearance

### 6. Custom Form Styling
- Premium styled select dropdowns
- Custom checkbox designs
- Clear visual feedback on focus

---

## 🆕 NEW FEATURES (February 2026)

### 1. 📄 PDF Export
- "Download PDF" button on results page
- Uses browser print-to-PDF functionality
- Excludes unnecessary elements for clean output
- Custom filename with date

### 2. 📋 Prediction History Dashboard
- Automatically saves each prediction locally
- Shows last 10 predictions
- Displays visa type, nationality, date, and days
- "Clear History" button
- Persists across browser sessions (localStorage)

### 3. 📈 Monthly Processing Trends Chart
- Visual bar chart showing 6-month trends
- Highlights current month
- Shows peak vs off-peak comparison
- Indicates 21% faster processing in off-peak

### 4. 🌍 Multi-Language Support (Foundation)
- Translation infrastructure in place
- Supports English, Hindi, Spanish
- Language preference stored in localStorage
- Foundation for full i18n implementation

### 5. 📖 Visa Documentation Page (`/visa-info.html`)
**Official Portal Links:**
- Indian Visa Online (Official)
- Ministry of External Affairs
- Bureau of Immigration

**Visa Categories Section:**
- Tourist, Business, Student, Medical, Employment, Conference
- Duration and processing time info for each

**Country-Specific Information (45 countries):**
- Flag emoji, country name
- Average processing time
- Direct link to Indian Embassy/High Commission

**Regions Covered:**
- Americas: USA, Canada, Mexico, Brazil, Argentina
- Europe: UK, Germany, France, Italy, Spain, Netherlands, Belgium, Poland, Sweden, Switzerland, Portugal, Ukraine, Russia, Turkey
- Asia Pacific: Australia, New Zealand, Japan, South Korea, China, Singapore, Malaysia, Thailand, Indonesia, Philippines, Vietnam
- South Asia: Bangladesh, Nepal, Sri Lanka, Pakistan, Afghanistan
- Middle East: UAE, Saudi Arabia, Iran, Iraq, Israel, Egypt
- Africa: South Africa, Nigeria, Kenya

**Disclaimer & Updates:**
- Clear disclaimer about estimates
- Last updated timestamp
- Data source information

---

## 📊 Data & Statistics

### Homepage Stats Bar:
- 2,000+ Applications Analyzed
- 77% Prediction Accuracy
- 15+ ML Features Used
- 45+ Countries Supported

### Countries Supported (45):
Afghanistan, Argentina, Australia, Bangladesh, Belgium, Brazil, Canada, China, Egypt, France, Germany, Indonesia, Iran, Iraq, Israel, Italy, Japan, Kenya, Malaysia, Mexico, Nepal, Netherlands, New Zealand, Nigeria, Pakistan, Philippines, Poland, Portugal, Russia, Saudi Arabia, Singapore, South Africa, South Korea, Spain, Sri Lanka, Sweden, Switzerland, Thailand, Turkey, UAE, UK, Ukraine, USA, Vietnam

### Visa Types:
- Tourist
- Business
- Student
- Employment
- Medical
- Conference
- Transit

---

## 🔧 Backend Features

### FastAPI Backend
- RESTful API endpoints
- CORS enabled for cross-origin requests
- Static file serving with cache control

### API Endpoints:
- `POST /api/predict` - Get processing time prediction
- `GET /api/statistics` - Get overall statistics
- `GET /api/options` - Get form dropdown options
- `GET /api/health` - Health check
- `GET /visa-info.html` - Visa documentation page

### Prediction Response Includes:
- Predicted days (main estimate)
- Min/Max day range
- Risk level (Low/Medium/High)
- Risk score (numeric)
- Approval likelihood & percentage
- Country average processing time
- Visa type average processing time
- Key factors breakdown

---

## 🎨 UI/UX Features

### 1. Sample Prediction Card (Homepage)
- Live demo of prediction output
- Shows example Tourist visa from USA

### 2. AI Model Insights Section
- 3 info cards explaining technology
- Linear Regression, 15+ Features, Real-Time processing

### 3. Similar Applications Comparison
- Your estimate vs Visa type average
- Country average comparison
- Overall average (8.2 days)

### 4. Expected Timeline Visualization
- Application date
- Expected completion date
- Latest possible date

### 5. Technology Section
- Explains ML model used
- Shows accuracy metrics
- Feature engineering details

---

## 🚀 Deployment

### Render Deployment Ready
- `render.yaml` configuration
- `Procfile` for Heroku compatibility
- `requirements.txt` with all dependencies

### Cache Busting
- Version query strings on CSS/JS files
- Ensures fresh files on deployment

---

## 📁 Project Structure

```
webapp/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── prediction_service.py
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Homepage
│   ├── predict.html        # Prediction form
│   ├── visa-info.html      # NEW: Visa documentation
│   ├── styles.css          # All styling
│   └── app.js              # JavaScript logic
├── render.yaml             # Deployment config
└── Procfile                # Process file
```

---

## ✅ Summary

| Category | Count |
|----------|-------|
| Countries Supported | 45+ |
| ML Features | 15+ |
| Training Samples | 2,000+ |
| Model Accuracy | 77% |
| Visa Types | 7 |
| API Endpoints | 5 |
| UI Themes | 2 (Light/Dark) |
| Visualizations | 10+ |
| Languages (Foundation) | 3 |
| Pages | 3 |

---

*Created for Infosys Springboard Project by Rahul Makwana*
*Last Updated: February 4, 2026*
